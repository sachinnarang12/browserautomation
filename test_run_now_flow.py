#!/usr/bin/env python3
"""
Comprehensive tests for the "Run Now" flow.
Mocks NovaAct so the full pipeline can be verified without a real browser.

Run with: python -m pytest test_run_now_flow.py -v
"""

import json
import os
import shutil
import tempfile
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock
import pytest


# ---------------------------------------------------------------------------
# Helpers – isolated working directory per test
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def isolated_workdir(tmp_path, monkeypatch):
    """Run every test inside its own temp directory so nothing is shared."""
    monkeypatch.chdir(tmp_path)
    # Copy templates so Flask can render them
    src_templates = Path(__file__).resolve().parent / "templates"
    if src_templates.exists():
        shutil.copytree(src_templates, tmp_path / "templates")
    yield tmp_path


def write_config(tmp_path, tasks=None, nova_config=None):
    """Write a minimal agent_config.json and return the path."""
    if tasks is None:
        tasks = [
            {
                "id": "task_test_1",
                "name": "Test Task",
                "url": "https://example.com",
                "instructions": "Click login",
                "scheduled_time": "15:00",
                "status": "pending",
                "created_at": "2025-01-01T00:00:00",
                "last_run": None,
                "result": None,
                "error_message": None,
                "retry_count": 0,
                "max_retries": 3,
                "enabled": True,
            }
        ]
    if nova_config is None:
        nova_config = {
            "headless": False,
            "tty": False,
            "ignore_https_errors": True,
            "nova_act_api_key": "test-key",
        }
    config_path = tmp_path / "agent_config.json"
    config_path.write_text(json.dumps({
        "tasks": tasks,
        "nova_config": nova_config,
    }, indent=2))
    return config_path


def write_users(tmp_path):
    """Write a users.json with a known admin so login works."""
    from werkzeug.security import generate_password_hash
    users_path = tmp_path / "users.json"
    users_path.write_text(json.dumps({
        "users": [{
            "id": "test_admin_id",
            "username": "admin",
            "password_hash": generate_password_hash("admin123"),
            "email": "admin@test.com",
            "created_at": "2025-01-01T00:00:00",
            "is_admin": True,
        }]
    }, indent=2))
    return users_path


def write_credentials_index(tmp_path):
    """Write an empty credentials index."""
    ci = tmp_path / "credentials_index.json"
    ci.write_text(json.dumps({"credentials": {}}, indent=2))
    return ci


# ---------------------------------------------------------------------------
# Flask test-client fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def app_client(tmp_path):
    """Create a Flask test client wired to the temp working directory."""
    write_config(tmp_path)
    write_users(tmp_path)
    write_credentials_index(tmp_path)

    # Import after chdir so file-based managers find the right files
    import agent_dashboard_v2 as dash
    dash.app.config["TESTING"] = True
    dash.app.config["WTF_CSRF_ENABLED"] = False
    dash.app.config["LOGIN_DISABLED"] = False

    # Re-init auth_manager so it reads from tmp dir
    from auth_manager import AuthManager
    dash.auth_manager = AuthManager(users_file=str(tmp_path / "users.json"))

    # Re-init credential manager
    from credential_manager import CredentialManager
    dash.credential_manager = CredentialManager()

    client = dash.app.test_client()
    yield client, dash.app, tmp_path


def login(client):
    """Log in as admin and return the response."""
    return client.post("/login", data={
        "username": "admin",
        "password": "admin123",
    }, follow_redirects=True)


# ===========================================================================
# 1. FLASK ROUTE TESTS – does the web app serve pages and APIs correctly?
# ===========================================================================

class TestDashboardRoutes:
    """Verify that routes respond correctly."""

    def test_login_page_loads(self, app_client):
        client, app, _ = app_client
        resp = client.get("/login")
        assert resp.status_code == 200

    def test_login_with_valid_credentials(self, app_client):
        client, app, _ = app_client
        resp = login(client)
        assert resp.status_code == 200
        # Should redirect to dashboard which contains the word "Dashboard"
        assert b"Dashboard" in resp.data or b"dashboard" in resp.data

    def test_login_with_invalid_credentials(self, app_client):
        client, app, _ = app_client
        resp = client.post("/login", data={
            "username": "admin",
            "password": "wrong",
        }, follow_redirects=True)
        assert b"Invalid" in resp.data or resp.status_code == 200

    def test_dashboard_requires_login(self, app_client):
        client, app, _ = app_client
        resp = client.get("/", follow_redirects=False)
        assert resp.status_code == 302  # redirect to login

    def test_task_details_page_loads(self, app_client):
        client, app, _ = app_client
        login(client)
        resp = client.get("/task/task_test_1")
        assert resp.status_code == 200
        assert b"Test Task" in resp.data

    def test_task_details_page_has_run_button(self, app_client):
        client, app, _ = app_client
        login(client)
        resp = client.get("/task/task_test_1")
        assert b"run-now-btn" in resp.data
        assert b"runTaskNow" in resp.data

    def test_task_not_found(self, app_client):
        client, app, _ = app_client
        login(client)
        resp = client.get("/task/nonexistent_task", follow_redirects=True)
        # Should redirect to tasks list or show error
        assert resp.status_code == 200


# ===========================================================================
# 2. API ENDPOINT TESTS – does /api/task/<id>/run actually start a task?
# ===========================================================================

class TestRunTaskAPI:
    """Test the /api/task/<id>/run endpoint."""

    def test_run_returns_success(self, app_client):
        """POST /api/task/task_test_1/run should return success=True."""
        client, app, tmp_path = app_client
        login(client)

        # Mock at the source module since the import is inside run_task()
        mock_nova_cls = MagicMock()
        mock_nova_instance = MagicMock()
        mock_nova_instance.act.return_value = {"status": "ok"}
        mock_nova_cls.return_value = mock_nova_instance

        with patch("portal_automation_agent.NovaAct", mock_nova_cls):
            resp = client.post("/api/task/task_test_1/run")
            data = resp.get_json()

            assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {data}"
            assert data["success"] is True

    def test_run_nonexistent_task_returns_404(self, app_client):
        client, app, _ = app_client
        login(client)

        resp = client.post("/api/task/nonexistent/run")
        data = resp.get_json()
        assert resp.status_code == 404
        assert data["success"] is False

    def test_run_already_running_returns_409(self, app_client):
        client, app, tmp_path = app_client
        login(client)

        # Set the task status to running in config
        config_path = tmp_path / "agent_config.json"
        config = json.loads(config_path.read_text())
        config["tasks"][0]["status"] = "running"
        config_path.write_text(json.dumps(config))

        resp = client.post("/api/task/task_test_1/run")
        data = resp.get_json()
        assert resp.status_code == 409
        assert "already running" in data["message"]

    def test_run_without_config_file_returns_404(self, app_client):
        client, app, tmp_path = app_client
        login(client)

        # Delete the config
        (tmp_path / "agent_config.json").unlink()

        resp = client.post("/api/task/task_test_1/run")
        data = resp.get_json()
        assert resp.status_code == 404

    def test_run_requires_login(self, app_client):
        client, app, _ = app_client
        # Don't log in
        resp = client.post("/api/task/task_test_1/run", follow_redirects=False)
        assert resp.status_code in (302, 401)


# ===========================================================================
# 3. STATUS POLLING TESTS – does /api/task/<id>/status return correct data?
# ===========================================================================

class TestTaskStatusAPI:
    """Test the /api/task/<id>/status endpoint."""

    def test_status_pending(self, app_client):
        client, app, _ = app_client
        login(client)

        resp = client.get("/api/task/task_test_1/status")
        data = resp.get_json()
        assert data["success"] is True
        assert data["status"] == "pending"

    def test_status_after_failure(self, app_client):
        client, app, tmp_path = app_client
        login(client)

        # Simulate a failed task
        config = json.loads((tmp_path / "agent_config.json").read_text())
        config["tasks"][0]["status"] = "failed"
        config["tasks"][0]["error_message"] = "Connection refused"
        (tmp_path / "agent_config.json").write_text(json.dumps(config))

        resp = client.get("/api/task/task_test_1/status")
        data = resp.get_json()
        assert data["status"] == "failed"
        assert data["error_message"] == "Connection refused"

    def test_status_after_completion(self, app_client):
        client, app, tmp_path = app_client
        login(client)

        config = json.loads((tmp_path / "agent_config.json").read_text())
        config["tasks"][0]["status"] = "completed"
        config["tasks"][0]["result"] = "PDF downloaded"
        (tmp_path / "agent_config.json").write_text(json.dumps(config))

        resp = client.get("/api/task/task_test_1/status")
        data = resp.get_json()
        assert data["status"] == "completed"
        assert data["result"] == "PDF downloaded"

    def test_status_nonexistent_task(self, app_client):
        client, app, _ = app_client
        login(client)

        resp = client.get("/api/task/nonexistent/status")
        data = resp.get_json()
        assert resp.status_code == 404


# ===========================================================================
# 4. PORTAL AUTOMATION AGENT TESTS – does the core agent logic work?
# ===========================================================================

class TestPortalAutomationAgent:
    """Test the PortalAutomationAgent class with mocked NovaAct."""

    def _make_agent(self, tmp_path):
        """Create an agent pointed at the temp config file."""
        write_config(tmp_path)
        write_credentials_index(tmp_path)

        with patch("portal_automation_agent.NovaAct"):
            from portal_automation_agent import PortalAutomationAgent
            agent = PortalAutomationAgent(config_file=str(tmp_path / "agent_config.json"))
        return agent

    def test_load_config(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        write_credentials_index(tmp_path)
        agent = self._make_agent(tmp_path)
        assert "task_test_1" in agent.tasks
        assert agent.tasks["task_test_1"].name == "Test Task"

    def test_save_and_reload_config(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        write_credentials_index(tmp_path)
        agent = self._make_agent(tmp_path)

        # Modify a task and save
        from portal_automation_agent import TaskStatus
        agent.tasks["task_test_1"].status = TaskStatus.COMPLETED
        agent.tasks["task_test_1"].result = "All done"
        agent.save_config()

        # Reload from disk
        config = json.loads((tmp_path / "agent_config.json").read_text())
        task_data = config["tasks"][0]
        assert task_data["status"] == "completed"
        assert task_data["result"] == "All done"

    def test_execute_task_success(self, tmp_path, monkeypatch):
        """When NovaAct succeeds, task status should become 'completed'."""
        monkeypatch.chdir(tmp_path)
        write_credentials_index(tmp_path)
        write_config(tmp_path)

        mock_nova_cls = MagicMock()
        mock_nova_instance = MagicMock()
        mock_nova_instance.act.return_value = {"status": "ok", "data": "exported"}
        mock_nova_cls.return_value = mock_nova_instance

        with patch("portal_automation_agent.NovaAct", mock_nova_cls):
            from portal_automation_agent import PortalAutomationAgent, TaskStatus
            agent = PortalAutomationAgent(config_file=str(tmp_path / "agent_config.json"))
            agent._execute_task("task_test_1")

        assert agent.tasks["task_test_1"].status == TaskStatus.COMPLETED
        assert agent.tasks["task_test_1"].result is not None

        # Also verify config file was persisted
        config = json.loads((tmp_path / "agent_config.json").read_text())
        assert config["tasks"][0]["status"] == "completed"

    def test_execute_task_failure(self, tmp_path, monkeypatch):
        """When NovaAct raises, task status should become 'failed'."""
        monkeypatch.chdir(tmp_path)
        write_credentials_index(tmp_path)
        write_config(tmp_path)

        mock_nova_cls = MagicMock()
        mock_nova_instance = MagicMock()
        mock_nova_instance.start.side_effect = ConnectionError("SSL Certificate verification failed")
        mock_nova_cls.return_value = mock_nova_instance

        with patch("portal_automation_agent.NovaAct", mock_nova_cls):
            from portal_automation_agent import PortalAutomationAgent, TaskStatus
            agent = PortalAutomationAgent(config_file=str(tmp_path / "agent_config.json"))
            agent._execute_task("task_test_1")

        assert agent.tasks["task_test_1"].status == TaskStatus.FAILED
        assert "SSL" in agent.tasks["task_test_1"].error_message

        # Verify config was persisted with failure
        config = json.loads((tmp_path / "agent_config.json").read_text())
        assert config["tasks"][0]["status"] == "failed"
        assert config["tasks"][0]["error_message"] is not None

    def test_execute_task_increments_retry(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        write_credentials_index(tmp_path)
        write_config(tmp_path)

        mock_nova_cls = MagicMock()
        mock_nova_instance = MagicMock()
        mock_nova_instance.start.side_effect = RuntimeError("API down")
        mock_nova_cls.return_value = mock_nova_instance

        with patch("portal_automation_agent.NovaAct", mock_nova_cls):
            from portal_automation_agent import PortalAutomationAgent
            agent = PortalAutomationAgent(config_file=str(tmp_path / "agent_config.json"))
            agent._execute_task("task_test_1")

        assert agent.tasks["task_test_1"].retry_count == 1

    def test_execute_disabled_task_skips(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        write_credentials_index(tmp_path)

        tasks = [{
            "id": "task_disabled",
            "name": "Disabled Task",
            "url": "https://example.com",
            "instructions": "Do nothing",
            "scheduled_time": "12:00",
            "status": "pending",
            "created_at": "2025-01-01T00:00:00",
            "last_run": None,
            "result": None,
            "error_message": None,
            "retry_count": 0,
            "max_retries": 3,
            "enabled": False,
        }]
        write_config(tmp_path, tasks=tasks)

        with patch("portal_automation_agent.NovaAct") as mock_nova:
            from portal_automation_agent import PortalAutomationAgent, TaskStatus
            agent = PortalAutomationAgent(config_file=str(tmp_path / "agent_config.json"))
            agent._execute_task("task_disabled")

        # NovaAct should never have been instantiated
        mock_nova.assert_not_called()
        assert agent.tasks["task_disabled"].status == TaskStatus.PENDING

    def test_execute_nonexistent_task(self, tmp_path, monkeypatch):
        """Executing a task that doesn't exist should not crash."""
        monkeypatch.chdir(tmp_path)
        write_credentials_index(tmp_path)
        write_config(tmp_path)

        with patch("portal_automation_agent.NovaAct"):
            from portal_automation_agent import PortalAutomationAgent
            agent = PortalAutomationAgent(config_file=str(tmp_path / "agent_config.json"))
            # Should not raise
            agent._execute_task("nonexistent_id")


# ===========================================================================
# 5. CREDENTIAL RESOLUTION TESTS
# ===========================================================================

class TestCredentialResolution:
    """Test that credential placeholders get resolved correctly."""

    def test_resolve_credentials_with_match(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        write_credentials_index(tmp_path)
        write_config(tmp_path)

        mock_cm = MagicMock()
        mock_cm.get_credential.return_value = {
            "username": "myuser",
            "password": "mypass",
        }

        with patch("portal_automation_agent.NovaAct"):
            from portal_automation_agent import PortalAutomationAgent
            agent = PortalAutomationAgent(config_file=str(tmp_path / "agent_config.json"))

        with patch("portal_automation_agent.CredentialManager", return_value=mock_cm):
            result = agent._resolve_credentials(
                "Login with {{credential:utility_portal:username}} and {{credential:utility_portal:password}}"
            )

        assert "myuser" in result
        assert "mypass" in result
        assert "{{credential:" not in result

    def test_resolve_credentials_no_placeholders(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        write_credentials_index(tmp_path)
        write_config(tmp_path)

        with patch("portal_automation_agent.NovaAct"):
            from portal_automation_agent import PortalAutomationAgent
            agent = PortalAutomationAgent(config_file=str(tmp_path / "agent_config.json"))

        result = agent._resolve_credentials("Just click the button")
        assert result == "Just click the button"

    def test_resolve_credentials_missing_cred(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        write_credentials_index(tmp_path)
        write_config(tmp_path)

        mock_cm = MagicMock()
        mock_cm.get_credential.return_value = None

        with patch("portal_automation_agent.NovaAct"):
            from portal_automation_agent import PortalAutomationAgent
            agent = PortalAutomationAgent(config_file=str(tmp_path / "agent_config.json"))

        with patch("portal_automation_agent.CredentialManager", return_value=mock_cm):
            result = agent._resolve_credentials(
                "Login as {{credential:missing:username}}"
            )

        # Placeholder should remain if credential is not found
        assert "{{credential:missing:username}}" in result


# ===========================================================================
# 6. END-TO-END: Run Now → background thread → status update
# ===========================================================================

class TestEndToEndRunNow:
    """
    Simulate the full 'Run Now' flow:
    1. POST /api/task/<id>/run
    2. Background thread creates PortalAutomationAgent and runs _execute_task
    3. Config file gets updated with new status
    4. GET /api/task/<id>/status reflects the final state
    """

    def test_full_success_flow(self, app_client):
        """Click Run Now → NovaAct succeeds → status shows completed."""
        client, app, tmp_path = app_client
        login(client)

        mock_nova_cls = MagicMock()
        mock_nova_instance = MagicMock()
        mock_nova_instance.act.return_value = {"status": "ok"}
        mock_nova_cls.return_value = mock_nova_instance

        with patch("portal_automation_agent.NovaAct", mock_nova_cls):
            resp = client.post("/api/task/task_test_1/run")
            data = resp.get_json()
            assert data["success"] is True

            # Wait for background thread to complete
            time.sleep(2)

        # Poll status
        resp = client.get("/api/task/task_test_1/status")
        data = resp.get_json()
        assert data["status"] == "completed", f"Expected completed, got {data}"

    def test_full_failure_flow(self, app_client):
        """Click Run Now → NovaAct fails → status shows failed with error."""
        client, app, tmp_path = app_client
        login(client)

        mock_nova_cls = MagicMock()
        mock_nova_instance = MagicMock()
        mock_nova_instance.start.side_effect = ConnectionError("Proxy 403 Forbidden")
        mock_nova_cls.return_value = mock_nova_instance

        with patch("portal_automation_agent.NovaAct", mock_nova_cls):
            resp = client.post("/api/task/task_test_1/run")
            data = resp.get_json()
            assert data["success"] is True

            time.sleep(2)

        resp = client.get("/api/task/task_test_1/status")
        data = resp.get_json()
        assert data["status"] == "failed", f"Expected failed, got {data}"
        assert "Proxy" in (data.get("error_message") or ""), f"Expected proxy error, got {data}"

    def test_background_thread_crash_is_caught(self, app_client):
        """If NovaAct import/init throws, the server should not die."""
        client, app, tmp_path = app_client
        login(client)

        # Mock NovaAct constructor to raise, simulating nova_act not installed
        with patch("portal_automation_agent.NovaAct", side_effect=ImportError("nova_act not installed")):
            resp = client.post("/api/task/task_test_1/run")
            data = resp.get_json()
            assert data["success"] is True  # Endpoint returns before thread runs

            time.sleep(2)

        # The server should still be alive
        resp = client.get("/api/task/task_test_1/status")
        assert resp.status_code == 200
        # Task should be failed, not stuck in running
        data = resp.get_json()
        assert data["status"] == "failed", f"Expected failed after crash, got {data}"


# ===========================================================================
# 7. CONFIG FILE INTEGRITY TESTS
# ===========================================================================

class TestConfigIntegrity:
    """Verify that config file updates are correct after operations."""

    def test_headless_always_false(self, tmp_path, monkeypatch):
        """Config should always override headless to False."""
        monkeypatch.chdir(tmp_path)
        write_credentials_index(tmp_path)
        write_config(tmp_path, nova_config={
            "headless": True,  # User set this to true
            "tty": False,
            "ignore_https_errors": True,
            "nova_act_api_key": "test-key",
        })

        with patch("portal_automation_agent.NovaAct"):
            from portal_automation_agent import PortalAutomationAgent
            agent = PortalAutomationAgent(config_file=str(tmp_path / "agent_config.json"))

        assert agent.nova_config["headless"] is False

    def test_status_enum_round_trip(self, tmp_path, monkeypatch):
        """Status should survive save→load round trip."""
        monkeypatch.chdir(tmp_path)
        write_credentials_index(tmp_path)
        write_config(tmp_path)

        with patch("portal_automation_agent.NovaAct"):
            from portal_automation_agent import PortalAutomationAgent, TaskStatus
            agent = PortalAutomationAgent(config_file=str(tmp_path / "agent_config.json"))
            agent.tasks["task_test_1"].status = TaskStatus.FAILED
            agent.save_config()

        # Raw JSON should have string "failed"
        raw = json.loads((tmp_path / "agent_config.json").read_text())
        assert raw["tasks"][0]["status"] == "failed"

        # Reloading should convert back to enum
        with patch("portal_automation_agent.NovaAct"):
            agent2 = PortalAutomationAgent(config_file=str(tmp_path / "agent_config.json"))
        assert agent2.tasks["task_test_1"].status == TaskStatus.FAILED


# ===========================================================================
# 8. AUTH MANAGER TESTS
# ===========================================================================

class TestAuthManager:

    def test_default_admin_created(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from auth_manager import AuthManager
        am = AuthManager(users_file=str(tmp_path / "users.json"))
        users = am.list_users()
        assert len(users) >= 1
        assert any(u["username"] == "admin" for u in users)

    def test_authenticate_success(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from auth_manager import AuthManager
        am = AuthManager(users_file=str(tmp_path / "users.json"))
        user = am.authenticate("admin", "admin123")
        assert user is not None
        assert user.username == "admin"

    def test_authenticate_failure(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        from auth_manager import AuthManager
        am = AuthManager(users_file=str(tmp_path / "users.json"))
        user = am.authenticate("admin", "wrongpassword")
        assert user is None


# ===========================================================================
# Run standalone
# ===========================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
