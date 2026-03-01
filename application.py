# AWS Elastic Beanstalk expects 'application' variable
from app import app

# For AWS Elastic Beanstalk
application = app

if __name__ == "__main__":
    application.run()