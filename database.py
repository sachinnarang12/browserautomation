#!/usr/bin/env python3
"""
Database Models
SQLAlchemy models for Portal Automation Agent V2.0
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

Base = declarative_base()

class TaskStatus(enum.Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class User(Base):
    """User model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    credentials = relationship("Credential", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")

class Credential(Base):
    """Stored credentials"""
    __tablename__ = 'credentials'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    credential_id = Column(String(100), unique=True, nullable=False)  # For keyring lookup
    name = Column(String(100), nullable=False)
    description = Column(Text)
    url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="credentials")
    tasks = relationship("Task", back_populates="credential")

class Task(Base):
    """Automation task"""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    credential_id = Column(Integer, ForeignKey('credentials.id'))
    
    name = Column(String(200), nullable=False)
    description = Column(Text)
    url = Column(String(500), nullable=False)
    instructions = Column(Text, nullable=False)
    
    scheduled_time = Column(String(5), nullable=False)  # HH:MM format
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    enabled = Column(Boolean, default=True)
    
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_run = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="tasks")
    credential = relationship("Credential", back_populates="tasks")
    executions = relationship("Execution", back_populates="task", cascade="all, delete-orphan")

class Execution(Base):
    """Task execution record"""
    __tablename__ = 'executions'
    
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(Enum(TaskStatus), nullable=False)
    
    result = Column(Text)
    error_message = Column(Text)
    
    steps_executed = Column(Integer, default=0)
    duration_seconds = Column(Integer)
    
    # Relationships
    task = relationship("Task", back_populates="executions")

class AuditLog(Base):
    """Audit log for security and compliance"""
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    action = Column(String(100), nullable=False)  # login, create_task, delete_task, etc.
    resource_type = Column(String(50))  # task, credential, user
    resource_id = Column(String(100))
    
    details = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")

class SystemConfig(Base):
    """System configuration"""
    __tablename__ = 'system_config'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Database:
    """Database manager"""
    
    def __init__(self, db_url='sqlite:///portal_agent.db'):
        self.engine = create_engine(db_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(self.engine)
    
    def drop_tables(self):
        """Drop all tables (use with caution!)"""
        Base.metadata.drop_all(self.engine)
    
    def get_session(self):
        """Get a new database session"""
        return self.Session()
    
    def init_default_data(self):
        """Initialize database with default data"""
        session = self.get_session()
        
        try:
            # Check if admin user exists
            admin = session.query(User).filter_by(username='admin').first()
            
            if not admin:
                from werkzeug.security import generate_password_hash
                
                admin = User(
                    username='admin',
                    password_hash=generate_password_hash('admin123'),
                    email='admin@localhost',
                    is_admin=True
                )
                session.add(admin)
                session.commit()
                
                print("✅ Default admin user created")
                print("   Username: admin")
                print("   Password: admin123")
                print("   ⚠️  Please change the password immediately!")
            
            # Add default system config (API keys loaded from environment)
            import os
            configs = [
                ('nova_act_api_key', os.environ.get('NOVA_ACT_API_KEY', ''), 'Nova Act API Key (set NOVA_ACT_API_KEY env var)'),
                ('scheduler_enabled', 'true', 'Enable automatic task scheduling'),
                ('max_concurrent_tasks', '5', 'Maximum concurrent task executions'),
                ('log_retention_days', '30', 'Days to retain execution logs'),
            ]
            
            for key, value, description in configs:
                existing = session.query(SystemConfig).filter_by(key=key).first()
                if not existing:
                    config = SystemConfig(key=key, value=value, description=description)
                    session.add(config)
            
            session.commit()
            print("✅ Default configuration created")
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error initializing database: {e}")
        finally:
            session.close()

def init_database():
    """Initialize database with tables and default data"""
    print("🗄️  Initializing database...")
    
    db = Database()
    db.create_tables()
    print("✅ Tables created")
    
    db.init_default_data()
    print("✅ Database initialized successfully")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            init_database()
        elif sys.argv[1] == "reset":
            confirm = input("⚠️  This will delete all data. Are you sure? (yes/no): ")
            if confirm.lower() == 'yes':
                db = Database()
                db.drop_tables()
                print("✅ Tables dropped")
                db.create_tables()
                db.init_default_data()
                print("✅ Database reset complete")
            else:
                print("❌ Cancelled")
        else:
            print("Usage: python database.py [init|reset]")
    else:
        print("🗄️  Database Manager")
        print("Usage:")
        print("  python database.py init   - Initialize database")
        print("  python database.py reset  - Reset database (deletes all data)")