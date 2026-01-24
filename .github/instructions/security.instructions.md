---
description: 'Security best practices for servidor backend'
applyTo: '**/*.py'
---

# Security Best Practices

## Authentication & Authorization

### JWT Tokens
- Use strong secret keys (minimum 32 characters)
- Set appropriate token expiration times (30 minutes for access tokens)
- Never expose secret keys in logs or error messages
- Validate tokens on every protected endpoint
- Use OAuth2 password flow for authentication

### Password Security
- Hash all passwords using bcrypt (via passlib)
- Never log passwords (plain or hashed)
- Enforce minimum password complexity in validation
- Use password_hash, never store plain passwords
- Salt is automatically handled by bcrypt

### Authorization
- Verify user ownership for all resource operations
- Check `user_id` matches current user for CRUD operations
- Return 404 (not 403) for unauthorized access to hide existence
- Use FastAPI dependencies for auth checks

## Input Validation

### Request Validation
- Use Pydantic models for all request bodies
- Validate all path and query parameters
- Sanitize user inputs to prevent injection attacks
- Set max lengths for string fields
- Use EmailStr for email validation

### Data Sanitization
- Never trust user input
- Validate UUIDs before database queries
- Check for SQL/NoSQL injection patterns
- Escape special characters when necessary
- Use parameterized queries (boto3 handles this)

## Secret Management

### Environment Variables
- Never commit `.env` files to git
- Use `.env.example` for templates
- Rotate secrets regularly in production
- Use different secrets for each environment
- Store production secrets in AWS Secrets Manager

### AWS Credentials
- Use IAM roles in production (not access keys)
- Use temporary credentials where possible
- Follow principle of least privilege
- Never hardcode AWS credentials
- Use LocalStack credentials only for local dev

## API Security

### Rate Limiting
- Implement rate limiting for authentication endpoints
- Use exponential backoff for failed login attempts
- Protect against brute force attacks
- Consider IP-based rate limiting

### CORS Configuration
- Whitelist specific origins (not `*`)
- Configure CORS in settings, not hardcoded
- Restrict allowed methods to those needed
- Be explicit about allowed headers

### Error Handling
- Don't expose internal errors to clients
- Log detailed errors server-side
- Return generic error messages
- Avoid stack traces in production
- Don't reveal system architecture in errors

## DynamoDB Security

### Data Access
- Use least privilege IAM policies
- Enable encryption at rest
- Use encryption in transit (HTTPS)
- Audit access logs regularly
- Implement row-level security via filters

### Query Safety
- Use Key and GSI queries (not scans)
- Implement pagination for large datasets
- Use conditional writes to prevent race conditions
- Validate partition and sort keys

## S3 Security

### Bucket Configuration
- Enable bucket versioning
- Use private buckets by default
- Enable encryption at rest
- Use signed URLs for temporary access
- Set appropriate bucket policies

### File Upload Security
- Validate file types and sizes
- Scan uploads for malware (if handling user files)
- Use random filenames to prevent overwrites
- Implement upload size limits
- Check MIME types, not just extensions

## Dependency Security

### Package Management
- Regularly update dependencies (`uv pip list --outdated`)
- Review security advisories
- Use specific version pins in production
- Audit new packages before adding
- Use tools like `safety` or `pip-audit`

### Known Vulnerabilities
- Subscribe to security mailing lists
- Monitor CVE databases
- Update critical vulnerabilities immediately
- Test updates in staging first

## Logging & Monitoring

### What to Log
- Authentication attempts (success/failure)
- Authorization failures
- Data access patterns
- Configuration changes
- Error conditions

### What NOT to Log
- Passwords (plain or hashed)
- JWT tokens
- API keys or secrets
- Personal identifiable information (PII)
- Credit card data or sensitive user info

### Log Security
- Sanitize logs before writing
- Use structured logging (JSON)
- Implement log retention policies
- Protect log access (IAM policies)
- Monitor logs for security events

## Production Deployment

### Environment Hardening
- Disable debug mode in production
- Use HTTPS only (no HTTP)
- Set secure cookie flags
- Enable security headers (HSTS, CSP)
- Use WAF for additional protection

### AWS Lambda Security
- Use minimal IAM execution roles
- Enable VPC if accessing private resources
- Set memory and timeout limits
- Enable AWS X-Ray for tracing
- Use environment variables for config

## Security Checklist

Before deploying:
- [ ] All secrets are in environment variables
- [ ] Debug mode is disabled
- [ ] CORS is properly configured
- [ ] Authentication is enforced on protected routes
- [ ] Input validation is comprehensive
- [ ] Error messages don't leak sensitive info
- [ ] Dependencies are up to date
- [ ] Logs don't contain sensitive data
- [ ] IAM roles follow least privilege
- [ ] HTTPS is enforced

## Incident Response

If a security issue is discovered:
1. Assess the severity and impact
2. Contain the issue immediately
3. Rotate affected credentials
4. Patch the vulnerability
5. Review logs for exploitation
6. Document the incident
7. Implement preventive measures
