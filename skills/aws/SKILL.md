---
name: aws
description: Expert guidance for AWS CLI operations with SSO authentication. Use when the user asks to "view CloudWatch logs", "invoke Lambda", "send SNS notification", "check SES", "list Lambda functions", or mentions AWS CLI, CloudWatch, SNS, SES, Lambda, or AWS resource management with SSO profiles.
---

# AWS CLI

Comprehensive guide for interacting with AWS services using AWS CLI with SSO authentication. All commands include the required profile and region flags.

## Quick Reference

**SSO Login:**

```bash
aws sso login --profile <AWS_PROFILE> --region <AWS_REGION>
```

**Common Commands:**

```bash
# View recent logs
aws logs tail /aws/lambda/function-name --follow --profile <AWS_PROFILE> --region <AWS_REGION>

# Send SNS notification
aws sns publish --topic-arn arn:aws:sns:<AWS_REGION>:<AWS_ACCOUNT_ID>:topic-name --message "Alert message" --profile <AWS_PROFILE> --region <AWS_REGION>

# Check Lambda function
aws lambda get-function --function-name function-name --profile <AWS_PROFILE> --region <AWS_REGION>
```

## AWS Configuration

### Profile and Region

**All AWS CLI commands must include these flags:**

- `--profile <AWS_PROFILE>`
- `--region <AWS_REGION>`

**Why this matters:**

- The application uses AWS SSO for authentication
- Multiple profiles may exist on the system
- Explicit profile/region prevents accidental operations in the wrong environment

### SSO Authentication

**Login command:**

```bash
aws sso login --profile <AWS_PROFILE> --region <AWS_REGION>
```

**When to login:**

- First time using AWS CLI
- Session expired (usually after 8 hours)
- Error: "The SSO session associated with this profile has expired"

**Verify authentication:**

```bash
aws sts get-caller-identity --profile <AWS_PROFILE> --region <AWS_REGION>
```

**Output should show:**

```json
{
  "UserId": "...",
  "Account": "<AWS_ACCOUNT_ID>",
  "Arn": "arn:aws:sts::<AWS_ACCOUNT_ID>:assumed-role/..."
}
```

## CloudWatch Logs

### View Log Groups

**List all log groups:**

```bash
aws logs describe-log-groups --profile <AWS_PROFILE> --region <AWS_REGION>
```

**Filter log groups by name:**

```bash
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda" --profile <AWS_PROFILE> --region <AWS_REGION>
```

**Count log groups:**

```bash
aws logs describe-log-groups --profile <AWS_PROFILE> --region <AWS_REGION> --query 'length(logGroups)'
```

### View Log Streams

**List log streams in a group:**

```bash
aws logs describe-log-streams \
  --log-group-name /aws/lambda/function-name \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Get most recent log stream:**

```bash
aws logs describe-log-streams \
  --log-group-name /aws/lambda/function-name \
  --order-by LastEventTime \
  --descending \
  --max-items 1 \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

### Read Logs

**Tail logs (real-time):**

```bash
aws logs tail /aws/lambda/function-name \
  --follow \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Tail with filter pattern:**

```bash
aws logs tail /aws/lambda/function-name \
  --follow \
  --filter-pattern "ERROR" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Get logs from specific time range:**

```bash
aws logs filter-log-events \
  --log-group-name /aws/lambda/function-name \
  --start-time $(date -u -v-1H +%s)000 \  # macOS date syntax
  --end-time $(date -u +%s)000 \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Search logs for specific text:**

```bash
aws logs filter-log-events \
  --log-group-name /aws/lambda/function-name \
  --filter-pattern "order_id" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Get logs from specific stream:**

```bash
aws logs get-log-events \
  --log-group-name /aws/lambda/function-name \
  --log-stream-name "2025/10/28/[$LATEST]abc123" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

### Log Insights Queries

**Run CloudWatch Insights query:**

```bash
# Start query
QUERY_ID=$(aws logs start-query \
  --log-group-name /aws/lambda/function-name \
  --start-time $(date -u -v-1H +%s) \  # macOS date syntax
  --end-time $(date -u +%s) \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | limit 20' \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> \
  --query 'queryId' \
  --output text)

# Wait for results
sleep 5

# Get results
aws logs get-query-results \
  --query-id "$QUERY_ID" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Common query patterns:**

```bash
# Find errors in last hour
'fields @timestamp, @message | filter @message like /ERROR/ | limit 100'

# Count errors by type
'stats count() by @message | filter @message like /ERROR/'

# Parse JSON logs
'fields @timestamp, requestId, userId | filter statusCode = 500'

# Response time analysis
'stats avg(duration), max(duration), min(duration) by bin(5m)'
```

## SNS (Notifications)

### List Topics

**List all SNS topics:**

```bash
aws sns list-topics --profile <AWS_PROFILE> --region <AWS_REGION>
```

**Get topic details:**

```bash
aws sns get-topic-attributes \
  --topic-arn arn:aws:sns:<AWS_REGION>:<AWS_ACCOUNT_ID>:topic-name \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

### Send Notifications

**Send simple message:**

```bash
aws sns publish \
  --topic-arn arn:aws:sns:<AWS_REGION>:<AWS_ACCOUNT_ID>:topic-name \
  --message "Alert: System notification" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Send with subject:**

```bash
aws sns publish \
  --topic-arn arn:aws:sns:<AWS_REGION>:<AWS_ACCOUNT_ID>:topic-name \
  --subject "Production Alert" \
  --message "Critical error detected in payment processing" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Send structured message (JSON):**

```bash
aws sns publish \
  --topic-arn arn:aws:sns:<AWS_REGION>:<AWS_ACCOUNT_ID>:topic-name \
  --message '{
    "default": "Fallback message",
    "email": "Email version of message",
    "sms": "SMS version"
  }' \
  --message-structure json \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Send with attributes:**

```bash
aws sns publish \
  --topic-arn arn:aws:sns:<AWS_REGION>:<AWS_ACCOUNT_ID>:topic-name \
  --message "Order processed" \
  --message-attributes '{
    "priority": {"DataType": "String", "StringValue": "high"},
    "orderID": {"DataType": "Number", "StringValue": "12345"}
  }' \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

### Manage Subscriptions

**List subscriptions:**

```bash
aws sns list-subscriptions-by-topic \
  --topic-arn arn:aws:sns:<AWS_REGION>:<AWS_ACCOUNT_ID>:topic-name \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Subscribe email to topic:**

```bash
aws sns subscribe \
  --topic-arn arn:aws:sns:<AWS_REGION>:<AWS_ACCOUNT_ID>:topic-name \
  --protocol email \
  --notification-endpoint your@example.com \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

### Manage Identities

**Verify email address:**

```bash
aws ses verify-email-identity \
  --email-address your@example.com \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Get verification status:**

```bash
aws ses get-identity-verification-attributes \
  --identities your@example.com \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

## Lambda

### List Functions

**List all Lambda functions:**

```bash
aws lambda list-functions --profile <AWS_PROFILE> --region <AWS_REGION>
```

**Filter by name prefix:**

```bash
aws lambda list-functions \
  --query "Functions[?starts_with(FunctionName, 'your-app-')].FunctionName" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

### Get Function Details

**Get function configuration:**

```bash
aws lambda get-function \
  --function-name function-name \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

**Get function environment variables:**

```bash
aws lambda get-function-configuration \
  --function-name function-name \
  --query 'Environment.Variables' \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

### Invoke Functions

**Invoke function synchronously:**

```bash
aws lambda invoke \
  --function-name function-name \
  --payload '{"key": "value"}' \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> \
  response.json

cat response.json
```

**Invoke function asynchronously:**

```bash
aws lambda invoke \
  --function-name function-name \
  --invocation-type Event \
  --payload '{"orderId": "12345"}' \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> \
  response.json
```

**Invoke with CloudWatch logs:**

```bash
aws lambda invoke \
  --function-name function-name \
  --log-type Tail \
  --payload '{"test": true}' \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> \
  response.json \
  --query 'LogResult' \
  --output text | base64 --decode
```

## Common Workflows

### Workflow 1: Troubleshoot Production Error

```bash
# 1. Login to AWS
aws sso login --profile <AWS_PROFILE> --region <AWS_REGION>

# 2. Find relevant log group
aws logs describe-log-groups \
  --log-group-name-prefix "/aws/lambda/order" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>

# 3. Tail logs with error filter
aws logs tail /aws/lambda/your-function \
  --follow \
  --filter-pattern "ERROR" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>

# 4. Run CloudWatch Insights query for analysis
QUERY_ID=$(aws logs start-query \
  --log-group-name /aws/lambda/your-function \
  --start-time $(date -u -v-2H +%s) \  # macOS date syntax
  --end-time $(date -u +%s) \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | stats count() by @message' \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> \
  --query 'queryId' \
  --output text)

sleep 5

aws logs get-query-results \
  --query-id "$QUERY_ID" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

### Workflow 2: Monitor Lambda Function Performance

```bash
# 1. Get function details
aws lambda get-function \
  --function-name your-function \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>

# 2. Check recent invocations
aws logs filter-log-events \
  --log-group-name /aws/lambda/your-function \
  --start-time $(date -u -v-1H +%s)000 \  # macOS date syntax
  --filter-pattern "REPORT" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>

# 3. Run performance query
QUERY_ID=$(aws logs start-query \
  --log-group-name /aws/lambda/your-function \
  --start-time $(date -u -v-24H +%s) \  # macOS date syntax
  --end-time $(date -u +%s) \
  --query-string 'filter @type = "REPORT" | stats avg(@duration), max(@duration), min(@duration), avg(@maxMemoryUsed)' \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> \
  --query 'queryId' \
  --output text)

sleep 5

aws logs get-query-results \
  --query-id "$QUERY_ID" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

### Workflow 3: Send Alert Notification

```bash
# 1. Check SNS topics
aws sns list-topics --profile <AWS_PROFILE> --region <AWS_REGION>

# 2. Get topic details
aws sns get-topic-attributes \
  --topic-arn arn:aws:sns:<AWS_REGION>:<AWS_ACCOUNT_ID>:production-alerts \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>

# 3. Send alert
aws sns publish \
  --topic-arn arn:aws:sns:<AWS_REGION>:<AWS_ACCOUNT_ID>:production-alerts \
  --subject "Production Issue Detected" \
  --message "Error rate increased by 50% in your-function lambda" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

### Workflow 4: Debug Failed Lambda Invocation

```bash
# 1. Get recent errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/your-function \
  --start-time $(date -u -v-30M +%s)000 \  # macOS date syntax
  --filter-pattern "ERROR" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> \
  --max-items 10

# 2. Get specific invocation details
aws logs get-log-events \
  --log-group-name /aws/lambda/your-function \
  --log-stream-name "2025/10/28/[$LATEST]abc123" \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>

# 3. Test with same payload
aws lambda invoke \
  --function-name your-function \
  --log-type Tail \
  --payload '{"orderId": "12345"}' \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> \
  response.json

# 4. Check response and logs
cat response.json
```

## Advanced JQ Queries

AWS CLI outputs JSON by default. Use `jq` for parsing:

**Extract specific fields:**

```bash
aws lambda list-functions \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> | \
  jq '.Functions[] | {name: .FunctionName, runtime: .Runtime, memory: .MemorySize}'
```

**Filter by condition:**

```bash
aws logs describe-log-groups \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> | \
  jq '.logGroups[] | select(.storedBytes > 1000000) | .logGroupName'
```

**Count items:**

```bash
aws lambda list-functions \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> | \
  jq '.Functions | length'
```

**Format output:**

```bash
aws logs describe-log-streams \
  --log-group-name /aws/lambda/your-function \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> | \
  jq -r '.logStreams[] | "\(.logStreamName) - \(.lastEventTime)"'
```

## Useful Aliases

Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# Base AWS command with profile and region
alias awsapp='aws --profile <AWS_PROFILE> --region <AWS_REGION>'

# SSO login
alias awslogin='aws sso login --profile <AWS_PROFILE> --region <AWS_REGION>'

# Quick log tail
alias awslogs='aws logs tail --follow --profile <AWS_PROFILE> --region <AWS_REGION>'

# List Lambda functions
alias awslambdalist='aws lambda list-functions --profile <AWS_PROFILE> --region <AWS_REGION>'

# List log groups
alias awslogslist='aws logs describe-log-groups --profile <AWS_PROFILE> --region <AWS_REGION>'
```

**Usage with aliases:**

```bash
# Login
awslogin

# Tail logs
awslogs /aws/lambda/your-function

# List functions
awslambdalist | jq '.Functions[].FunctionName'
```

## Troubleshooting

### Issue: "The SSO session has expired"

**Solution:**

```bash
aws sso login --profile <AWS_PROFILE> --region <AWS_REGION>
```

### Issue: "Could not connect to the endpoint URL"

**Solution:**
Check that `--region` is set to the correct value for your environment.

### Issue: "An error occurred (AccessDeniedException)"

**Solution:**

```bash
# Check current identity
aws sts get-caller-identity --profile <AWS_PROFILE> --region <AWS_REGION>

# Re-login if needed
aws sso login --profile <AWS_PROFILE> --region <AWS_REGION>
```

### Issue: Command hangs or times out

**Solution:**
Add `--cli-read-timeout` and `--cli-connect-timeout`:

```bash
aws logs tail /aws/lambda/your-function \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION> \
  --cli-read-timeout 30 \
  --cli-connect-timeout 10
```

### Issue: Output too large

**Solution:**
Use pagination and filtering:

```bash
aws logs filter-log-events \
  --log-group-name /aws/lambda/your-function \
  --max-items 100 \
  --profile <AWS_PROFILE> \
  --region <AWS_REGION>
```

## Best Practices

1. **Always include profile and region** - Prevents accidental operations in wrong environment
2. **Use SSO login** - More secure than long-term credentials
3. **Filter logs early** - Use `--filter-pattern` to reduce data transfer
4. **Use CloudWatch Insights** - More powerful than `filter-log-events` for complex queries
5. **Parse with jq** - Makes JSON output readable and scriptable
6. **Create aliases** - Reduces typing and prevents errors
7. **Check quotas** - SES has sending limits, SNS has rate limits
8. **Monitor costs** - CloudWatch Logs Insights queries cost money
9. **Use tail for real-time** - `aws logs tail --follow` is better than polling
10. **Clean up responses** - Delete response.json files after Lambda invocations

## Related Skills

For infrastructure:

- `/kubectl` - AWS EKS cluster operations

## See Also

- AWS CLI Documentation: https://docs.aws.amazon.com/cli/
- CloudWatch Logs Insights Query Syntax: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html
