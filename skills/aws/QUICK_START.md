# AWS CLI Quick Start

Most common AWS operations for daily work.

## First Time Setup

**1. Login to AWS:**
```bash
aws sso login --profile <AWS_PROFILE> --region <AWS_REGION>
```

**2. Verify access:**
```bash
aws sts get-caller-identity --profile <AWS_PROFILE> --region <AWS_REGION>
```

## Daily Operations

### View Application Logs

**Tail logs in real-time:**
```bash
aws logs tail /aws/lambda/your-function --follow --profile <AWS_PROFILE> --region <AWS_REGION>
```

**Tail with error filter:**
```bash
aws logs tail /aws/lambda/your-function --follow --filter-pattern "ERROR" --profile <AWS_PROFILE> --region <AWS_REGION>
```

**Search last hour of logs:**
```bash
aws logs filter-log-events \
  --log-group-name /aws/lambda/your-function \
  --start-time $(date -u -d '1 hour ago' +%s)000 \
  --filter-pattern "order_id" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

### Quick Monitoring

**List all Lambda functions:**
```bash
aws lambda list-functions --profile <AWS_PROFILE> --region <AWS_REGION>
```

**Check Lambda function config:**
```bash
aws lambda get-function --function-name your-function --profile <AWS_PROFILE> --region <AWS_REGION>
```

**List all log groups:**
```bash
aws logs describe-log-groups --profile <AWS_PROFILE> --region <AWS_REGION>
```

### Send Alerts

**Send SNS notification:**
```bash
aws sns publish \
  --topic-arn arn:aws:sns:<AWS_REGION>:<AWS_ACCOUNT_ID>:production-alerts \
  --subject "Alert" \
  --message "Issue detected" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Send email via SES:**
```bash
aws ses send-email \
  --from "sender@example.com" \
  --to "recipient@example.com" \
  --subject "Test" \
  --text "Test message" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

## Useful Aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Base command
alias awsapp='aws --profile <AWS_PROFILE> --region <AWS_REGION>'

# SSO login
alias awslogin='aws sso login --profile <AWS_PROFILE> --region <AWS_REGION>'

# Log tailing
alias awslogs='aws logs tail --follow --profile <AWS_PROFILE> --region <AWS_REGION>'
```

Then use:
```bash
awslogin                              # Login
awslogs /aws/lambda/your-function     # Tail logs
awsapp lambda list-functions          # List functions
```

## Common Issues

**Session expired:**
```bash
aws sso login --profile <AWS_PROFILE> --region <AWS_REGION>
```

**Need to find log group name:**
```bash
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda" --profile <AWS_PROFILE> --region <AWS_REGION>
```

**Parse JSON output:**
```bash
aws lambda list-functions --profile <AWS_PROFILE> --region <AWS_REGION> | jq '.Functions[].FunctionName'
```

## Next Steps

See [SKILL.md](SKILL.md) for:
- CloudWatch Insights queries
- Advanced log filtering
- Lambda invocation
- Complete workflows
- Troubleshooting guide
