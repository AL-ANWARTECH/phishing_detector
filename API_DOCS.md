````
# Phishing Detection System - API Documentation

## Base URL
`http://localhost:5000` (default)

## Authentication
No authentication required for basic usage (add authentication in production)

## Endpoints

### Analyze Email
**POST** `/analyze`

Analyze an email for phishing indicators.

#### Request
```json
{
  "email_content": "From: fake-bank@example.com\nTo: victim@gmail.com\nSubject: URGENT: Account Security Alert\n\nDear Customer, Your account has been suspended..."
}
````

#### Response

```json
{
  "is_phishing": true,
  "confidence_score": 75.5,
  "rule_score": 60,
  "ml_prediction": 1,
  "ml_confidence": 0.9,
  "url_score": 70,
  "rule_reasons": ["suspicious domain", "urgent language"],
  "url_reasons": ["IP address in URL"],
  "features": {
    "subject": "URGENT: Account Security Alert",
    "from_address": "fake-bank@example.com",
    "body": "Dear Customer, Your account has been suspended...",
    "links": ["http://fake-bank.com/verify"],
    "attachments": 0,
    "sender_domain": "example.com",
    "reply_domain": "fake-bank.com"
  }
}
```

#### Response Codes

- `200`: Success
- `400`: Bad request (no email content provided)
- `500`: Server error

### Get Analysis History

**GET** `/history`

Retrieve recent analysis results.

#### Response

```json
[
  {
    "id": 1,
    "email_content": "Sample email content...",
    "is_phishing": true,
    "confidence_score": 75.5,
    "rule_score": 60,
    "ml_prediction": 1,
    "ml_confidence": 0.9,
    "url_score": 70,
    "rule_reasons": "suspicious domain, urgent language",
    "url_reasons": "IP address in URL",
    "analyzed_at": "2023-12-01 10:30:45"
  }
]
```

### Health Check

**GET** `/health`

Check system health status.

#### Response

```json
{
  "status": "healthy",
  "ml_model_trained": true,
  "system": "phishing_detector",
  "database": "connected",
  "config": {
    "phishing_threshold": 50,
    "ml_weight": 0.7,
    "rule_weight": 0.3
  }
}
```

### Get Statistics

**GET** `/stats`

Get system usage statistics.

#### Response

```json
{
  "total_analyses": 150,
  "phishing_detected": 25,
  "safe_emails": 125,
  "phishing_percentage": 16.67
}
```

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message description"
}
```

## Example Usage

### Python Example

```python
import requests

# Analyze an email
response = requests.post('http://localhost:5000/analyze', json={
    'email_content': 'From: fake-bank@example.com\nSubject: URGENT: Verify Account\n\nClick here: http://fake.com'
})

result = response.json()
print(f"Phishing detected: {result['is_phishing']}")
print(f"Confidence: {result['confidence_score']}%")
```

### JavaScript Example

```javascript
// Analyze an email
fetch("http://localhost:5000/analyze", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    email_content:
      "From: fake-bank@example.com\nSubject: URGENT: Verify Account\n\nClick here: http://fake.com",
  }),
})
  .then((response) => response.json())
  .then((result) => {
    console.log(`Phishing detected: ${result.is_phishing}`);
    console.log(`Confidence: ${result.confidence_score}%`);
  });
```

### cURL Example

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"email_content": "From: fake-bank@example.com\nSubject: URGENT: Verify Account\n\nClick here: http://fake.com"}'
```

## Rate Limiting

- No rate limiting implemented (add in production)
- Consider implementing for production use

## Security Considerations

- Validate and sanitize all input
- Implement proper authentication
- Use HTTPS in production
- Monitor API usage

```

```
