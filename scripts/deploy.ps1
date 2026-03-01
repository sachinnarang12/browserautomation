# Production deployment script for AI Question App (PowerShell version)
param(
    [string]$OpenAIApiKey,
    [string]$NotificationEmail,
    [string]$Region = "us-east-1",
    [string]$Environment = "production"
)

# Configuration
$STACK_NAME = "ai-question-app-infrastructure"

Write-Host "Starting production deployment for AI Question App" -ForegroundColor Green

# Check if AWS CLI is installed
try {
    aws --version | Out-Null
} catch {
    Write-Host "AWS CLI is not installed. Please install it first." -ForegroundColor Red
    exit 1
}

# Check if EB CLI is installed
try {
    eb --version | Out-Null
} catch {
    Write-Host "EB CLI is not installed. Please install it first: pip install awsebcli" -ForegroundColor Red
    exit 1
}

# Prompt for OpenAI API Key if not provided
if (-not $OpenAIApiKey) {
    $OpenAIApiKey = Read-Host "Please enter your OpenAI API Key" -AsSecureString
    $OpenAIApiKey = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($OpenAIApiKey))
    if (-not $OpenAIApiKey) {
        Write-Host "OpenAI API Key is required" -ForegroundColor Red
        exit 1
    }
}

# Prompt for notification email
if (-not $NotificationEmail) {
    $NotificationEmail = Read-Host "Please enter email for cost budget notifications"
    if (-not $NotificationEmail) {
        Write-Host "Notification email is required" -ForegroundColor Red
        exit 1
    }
}

# Update CloudFormation template with notification email
$templateContent = Get-Content "cloudformation/infrastructure.yaml" -Raw
$templateContent = $templateContent -replace "admin@example.com", $NotificationEmail
$templateContent | Set-Content "cloudformation/infrastructure.yaml"

Write-Host "Deploying CloudFormation infrastructure..." -ForegroundColor Green

# Deploy CloudFormation stack
$deployResult = aws cloudformation deploy `
    --template-file cloudformation/infrastructure.yaml `
    --stack-name $STACK_NAME `
    --parameter-overrides `
        ApplicationName=ai-question-app `
        Environment=$Environment `
        OpenAIApiKey=$OpenAIApiKey `
        CostBudgetLimit=50 `
    --capabilities CAPABILITY_NAMED_IAM `
    --region $Region

if ($LASTEXITCODE -eq 0) {
    Write-Host "CloudFormation stack deployed successfully" -ForegroundColor Green
} else {
    Write-Host "CloudFormation deployment failed" -ForegroundColor Red
    exit 1
}

# Get the Elastic Beanstalk application and environment names
$APP_NAME = aws cloudformation describe-stacks `
    --stack-name $STACK_NAME `
    --region $Region `
    --query 'Stacks[0].Outputs[?OutputKey==`ApplicationName`].OutputValue' `
    --output text

$ENV_NAME = aws cloudformation describe-stacks `
    --stack-name $STACK_NAME `
    --region $Region `
    --query 'Stacks[0].Outputs[?OutputKey==`EnvironmentName`].OutputValue' `
    --output text

Write-Host "Initializing Elastic Beanstalk..." -ForegroundColor Green

# Initialize EB if not already done
if (-not (Test-Path ".elasticbeanstalk/config.yml")) {
    eb init $APP_NAME --region $Region --platform python-3.9
}

Write-Host "Deploying application to Elastic Beanstalk..." -ForegroundColor Green

# Deploy to existing environment
eb deploy $ENV_NAME

if ($LASTEXITCODE -eq 0) {
    Write-Host "Application deployed successfully" -ForegroundColor Green
    
    # Get the application URL
    $APP_URL = aws cloudformation describe-stacks `
        --stack-name $STACK_NAME `
        --region $Region `
        --query 'Stacks[0].Outputs[?OutputKey==`ApplicationURL`].OutputValue' `
        --output text
    
    Write-Host "Application is available at: $APP_URL" -ForegroundColor Green
    Write-Host "Health check endpoint: $APP_URL/health" -ForegroundColor Green
} else {
    Write-Host "Application deployment failed" -ForegroundColor Red
    exit 1
}

Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "Don't forget to:" -ForegroundColor Yellow
Write-Host "1. Set up SSL certificate for HTTPS"
Write-Host "2. Configure custom domain if needed"
Write-Host "3. Monitor costs in AWS Budgets"
Write-Host "4. Check CloudWatch logs for application monitoring"