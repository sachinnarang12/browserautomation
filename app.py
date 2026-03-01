from flask import Flask, render_template, request, jsonify
import openai
import os
import boto3
import logging
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv

# Load environment variables (for local development only)
if os.path.exists('.env'):
    load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_openai_api_key():
    """Get OpenAI API key from AWS Systems Manager Parameter Store or environment variable"""
    try:
        # Try to get from AWS Systems Manager Parameter Store first (production)
        ssm = boto3.client('ssm')
        parameter = ssm.get_parameter(
            Name='/ai-question-app/openai-api-key',
            WithDecryption=True
        )
        logger.info("Retrieved OpenAI API key from AWS Systems Manager")
        return parameter['Parameter']['Value']
    except (ClientError, NoCredentialsError) as e:
        # Fallback to environment variable (local development)
        logger.warning(f"Could not retrieve from AWS SSM: {e}. Falling back to environment variable.")
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("No OpenAI API key found in AWS SSM or environment variables")
            raise ValueError("OpenAI API key not configured")
        return api_key

# Configure OpenAI API key
try:
    openai.api_key = get_openai_api_key()
except Exception as e:
    logger.error(f"Failed to configure OpenAI API key: {e}")
    openai.api_key = None

@app.route('/')
def index():
    """Render the main page with the question form"""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle question submission and get LLM response"""
    try:
        # Get question from form
        question = request.json.get('question', '').strip()
        
        if not question:
            logger.warning("Empty question submitted")
            return jsonify({'error': 'Please enter a question'}), 400
        
        if not openai.api_key:
            logger.error("OpenAI API key not configured")
            return jsonify({'error': 'Service temporarily unavailable'}), 503
        
        logger.info(f"Processing question with {len(question)} characters")
        
        # Send question to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Extract the response text
        answer = response.choices[0].message.content.strip()
        
        logger.info("Successfully generated AI response")
        return jsonify({'answer': answer})
        
    except openai.error.AuthenticationError as e:
        logger.error(f"OpenAI authentication error: {e}")
        return jsonify({'error': 'Service authentication failed'}), 401
    except openai.error.RateLimitError as e:
        logger.warning(f"OpenAI rate limit exceeded: {e}")
        return jsonify({'error': 'Service temporarily busy. Please try again later.'}), 429
    except openai.error.APIError as e:
        logger.error(f"OpenAI API error: {e}")
        return jsonify({'error': 'Service temporarily unavailable'}), 503
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for load balancer"""
    try:
        # Basic health check - verify OpenAI API key is configured
        if openai.api_key:
            return jsonify({'status': 'healthy', 'service': 'ai-question-app'}), 200
        else:
            return jsonify({'status': 'unhealthy', 'error': 'API key not configured'}), 503
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503

if __name__ == '__main__':
    # Use environment variables for production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)