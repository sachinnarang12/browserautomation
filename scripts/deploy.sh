#!/bin/bash

# Production deployment script for AI Question App
set -e

# Configuration
STACK_NAME="ai-question-app-infrastructure"
REGION="us-east-1"
ENVIRONMENT="production"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting production deployment for AI Question App${NC}"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo -e "${RED}EB CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Prompt for OpenAI API Key if not provided
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}Please enter your OpenAI API Key:${NC}"
    read -s OPENAI_API_KEY
    if [ -z "$OPENAI_API_KEY" ]; then
        echo -e "${RED}OpenAI API Key is required${NC}"
        exit 1
    fi
fi

# Prompt for notification email
echo -e "${YELLOW}Please enter email for cost budget notifications:${NC}"
read NOTIFICATION_EMAIL
if [ -z "$NOTIFICATION_EMAIL" ]; then
    echo -e "${RED}Notification email is required${NC}"
    exit 1
fi

# Update CloudFormation template with notification email
sed -i.bak "s/admin@example.com/$NOTIFICATION_EMAIL/g" cloudformation/infrastructure.yaml

echo -e "${GREEN}Deploying CloudFormation infrastructure...${NC}"

# Deploy CloudFormation stack
aws cloudformation deploy \
    --template-file cloudformation/infrastructure.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides \
        ApplicationName=ai-question-app \
        Environment=$ENVIRONMENT \
        OpenAIApiKey=$OPENAI_API_KEY \
        CostBudgetLimit=50 \
    --capabilities CAPABILITY_NAMED_IAM \
    --region $REGION

if [ $? -eq 0 ]; then
    echo -e "${GREEN}CloudFormation stack deployed successfully${NC}"
else
    echo -e "${RED}CloudFormation deployment failed${NC}"
    exit 1
fi

# Get the Elastic Beanstalk application and environment names
APP_NAME=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`ApplicationName`].OutputValue' \
    --output text)

ENV_NAME=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`EnvironmentName`].OutputValue' \
    --output text)

echo -e "${GREEN}Initializing Elastic Beanstalk...${NC}"

# Initialize EB if not already done
if [ ! -f .elasticbeanstalk/config.yml ]; then
    eb init $APP_NAME --region $REGION --platform python-3.9
fi

echo -e "${GREEN}Deploying application to Elastic Beanstalk...${NC}"

# Deploy to existing environment
eb deploy $ENV_NAME

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Application deployed successfully${NC}"
    
    # Get the application URL
    APP_URL=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs[?OutputKey==`ApplicationURL`].OutputValue' \
        --output text)
    
    echo -e "${GREEN}Application is available at: $APP_URL${NC}"
    echo -e "${GREEN}Health check endpoint: $APP_URL/health${NC}"
else
    echo -e "${RED}Application deployment failed${NC}"
    exit 1
fi

# Restore original CloudFormation template
mv cloudformation/infrastructure.yaml.bak cloudformation/infrastructure.yaml

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${YELLOW}Don't forget to:${NC}"
echo -e "1. Set up SSL certificate for HTTPS"
echo -e "2. Configure custom domain if needed"
echo -e "3. Monitor costs in AWS Budgets"
echo -e "4. Check CloudWatch logs for application monitoring"