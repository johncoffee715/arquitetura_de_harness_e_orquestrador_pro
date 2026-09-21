# Examples for Browser-use Skill
# This demonstrates typical usage of the browser-use skill with different scenarios.

Example 1: Basic web page summary
Input: { "url": "https://example.com/basic-page" }
Output: {
  "status": "SUCCESS",
  "url": "https://example.com/basic-page",
  "context_length": 100,
  "key_points": [
    "Page contains basic content about the topic",
    "Main heading is 'Welcome to Example.com'",
    "Contains 3 main sections with headings"
  ],
  "evidence_id": "browser-use-example-001"
}

Example 2: Long technical document summary
Input: { "url": "https://example.com/technical-guide", "max_context": 8192 }
Output: {
  "status": "SUCCESS",
  "url": "https://example.com/technical-guide",
  "context_length": 8192,
  "key_points": [
    "Comprehensive guide covering installation and configuration",
    "Step-by-step instructions for setup",
    "Troubleshooting section with common issues",
    "API reference with example calls"
  ],
  "evidence_id": "browser-use-example-002"
}

Example 3: API documentation extraction
Input: { "url": "https://api.example.com/docs" }
Output: {
  "status": "SUCCESS",
  "url": "https://api.example.com/docs",
  "context_length": 4096,
  "key_points": [
    "API provides RESTful endpoints for various operations",
    "Includes authentication requirements and rate limits",
    "Provides comprehensive API reference with example requests",
    "Has troubleshooting guide for common errors"
  ],
  "evidence_id": "browser-use-example-003"
}
