# Integrating Umami Analytics with Express.js API

## Prerequisites
- Node.js and npm installed
- Express.js application set up
- Access to Umami analytics (self-hosted or cloud)

## Step 1: Set Up Analytics Middleware

First, create the analytics middleware file:

```javascript
// middlewares/umamiTracker.js
const umamiTracker = (req, res, next) => {
  res.setHeader('X-Analytics', 'enabled');

  const trackData = {
    url: req.originalUrl,
    method: req.method,
    timestamp: new Date().toISOString()
  };

  console.log('Analytics:', trackData);
  next();
};

module.exports = umamiTracker;
```

## Step 2: Create Analytics Routes

```javascript
// routes/analytics.js
const express = require('express');
const router = express.Router();

router.post('/track', async (req, res) => {
  const { website_id, url, referrer, event_type, event_value } = req.body;

  try {
    const response = await fetch('YOUR_UMAMI_SERVER/api/collect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ website_id, url, referrer, event_type, event_value })
    });

    res.status(200).json({ success: true });
  } catch (error) {
    res.status(500).json({ success: false, error: 'Analytics tracking failed' });
  }
});

module.exports = router;
```

## Step 3: Configure Environment Variables

Create `.env` file:
```env
UMAMI_SERVER_URL=https://your-umami-server
UMAMI_WEBSITE_ID=your-website-id
UMAMI_API_KEY=your-api-key
```

## Step 4: Create Analytics Utility

```javascript
// utils/analytics.js
const trackEvent = async (eventName, eventData) => {
  try {
    const response = await fetch(`${process.env.UMAMI_SERVER_URL}/api/collect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.UMAMI_API_KEY}`
      },
      body: JSON.stringify({
        website_id: process.env.UMAMI_WEBSITE_ID,
        event_name: eventName,
        event_data: eventData,
        timestamp: new Date().toISOString()
      })
    });
    return response.ok;
  } catch (error) {
    console.error('Analytics Tracking Error:', error);
    return false;
  }
};

module.exports = { trackEvent };
```

## Step 5: Implement in Routes

```javascript
// routes/index.js
const { trackEvent } = require('../utils/analytics');

router.post('/api/:version/:type/calculation', validateParams, validateRequestBody, async (req, res) => {
  try {
    const result = handleCalculation(req);
    await trackEvent('calculation_success', {
      version: req.params.version,
      type: req.params.type
    });
    res.json(result);
  } catch (error) {
    await trackEvent('calculation_error', {
      version: req.params.version,
      type: req.params.type,
      error: error.message
    });
    next(error);
  }
});
```

## Step 6: Docker Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  api-tb40:
    environment:
      - UMAMI_SERVER_URL=http://umami:3000
      - UMAMI_WEBSITE_ID=${UMAMI_WEBSITE_ID}
      - UMAMI_API_KEY=${UMAMI_API_KEY}

  umami:
    image: ghcr.io/umami-software/umami:postgresql-latest
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://umami:umami@db:5432/umami
      DATABASE_TYPE: postgresql
      HASH_SALT: your-hash-salt
    depends_on:
      - db

  db:
    image: postgres:12-alpine
    environment:
      POSTGRES_DB: umami
      POSTGRES_USER: umami
      POSTGRES_PASSWORD: umami
    volumes:
      - umami-db-data:/var/lib/postgresql/data

volumes:
  umami-db-data:
```

## Tracking Metrics

- API endpoint usage
- Calculation success/failure rates
- Response times
- Error rates
- User locations
- API version usage
- Calculation type distribution

## Best Practices

1. ✅ Handle analytics errors gracefully
2. ⚡ Don't block API responses
3. 🔒 Consider privacy implications
4. 📊 Monitor performance impact
5. 🛡️ Secure Umami instance

## Important Notes

- Keep analytics separate from core functionality
- Use async operations for tracking
- Implement proper error handling
- Regular monitoring of collected data
- Validate tracking data before sending
