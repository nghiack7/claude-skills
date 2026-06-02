---
name: mongodb
description: Expert guidance for querying MongoDB databases containing ad platform analytics and application data. Use when the user asks to "query MongoDB", "check ad insights", "analyze ad orders", "Facebook ads data", "TikTok ads data", "Google ads data", or mentions MongoDB, ad platform data, attribution data, or advertising performance analysis.
---

## Related Skills

- **starrocks** - OLAP analytics (MongoDB for operational data)

# MongoDB - Ad Platform & Application Databases

Access MongoDB databases containing ad platform analytics and production application data.

## Connection

**Secrets location:** `secret/databases/.env`

| Environment Variable | Database | Purpose |
| ---------------------- | --------------------- | --------------------------------------- |
| `MONGODB_PROD_URI` | db-prod (production) | Main application production data |
| `MONGODB_ADS_PROD_URI` | ad-platform | Facebook/Google/TikTok advertising data |

## Python Query Template

```python
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Auto-load secrets
load_dotenv('secret/databases/.env')

# Connect to Ad Platform (advertising data)
ads_client = MongoClient(os.getenv('MONGODB_ADS_PROD_URI'))
ads_db = ads_client['ad-platform']

# Connect to Production (main application data)
prod_client = MongoClient(os.getenv('MONGODB_PROD_URI'))
prod_db = prod_client['db-prod']

# Example: Query ad insights
collection = ads_db[f'ad-insights_<SHOP_ID>']
results = collection.find({'channel': 'facebook'}).limit(10)
for doc in results:
    print(doc)
```

---

## Database Overview

### 1. ad-platform Database

**Purpose:** Facebook, Google, TikTok advertising data per shop

**Architecture:** Per-shop collections with naming pattern:

- `ad-insights_{shop_id}` - Daily ad performance metrics
- `ad-details_{shop_id}` - Ad/campaign metadata
- `ad-orders_{shop_id}` - Order attribution to ads

**Global Collections:**
| Collection | Description |
|------------|-------------|
| `campaign-filter-rules` | Campaign exclusion rules |
| `connect_state_ids` | OAuth connection states |
| `synccron-jobs` | Sync job scheduling |

### 2. db-prod Database (Production)

**Purpose:** Main application data (shops, orders, products, etc.)

**Architecture:** Per-shop collections for orders:

- `orders_{shop_id}` - Shop orders stored in separate collections by shop_id

---

## Collection Schemas

### ad-insights\_{shop_id}

Daily advertising performance metrics per ad.

| Field | Type | Description |
| ------------------------ | ---------- | ------------------------- |
| `_id` | ObjectId | Document ID |
| `channel` | String | facebook/google/tiktok/x |
| `date` | Date | Metrics date |
| `account_id` | String | Platform account ID |
| `account_name` | String | Account display name |
| `ad_account_id` | String | Ad account ID |
| `ad_account_name` | String | Ad account name |
| `campaign_id` | String | Campaign ID |
| `campaign_name` | String | Campaign name |
| `campaign_status` | String | ACTIVE/INACTIVE/etc. |
| `ad_group_id` | String | Ad group/ad set ID |
| `ad_group_name` | String | Ad group name |
| `ad_group_status` | String | Ad group status |
| `ad_id` | String | Ad ID |
| `ad_name` | String | Ad name |
| `ad_status` | String | Ad status |
| `currency_code` | String | Currency (USD, EUR, etc.) |
| `time_zone` | String | Account timezone |
| **Metrics** | | |
| `impressions` | Long | Total impressions |
| `clicks` | Long | Total clicks |
| `spend` | Decimal128 | Spend in account currency |
| `origin_spend` | Decimal128 | Original spend amount |
| `purchases` | Long | Purchase conversions |
| `purchases_value` | Decimal128 | Purchase value |
| `origin_purchases_value` | Decimal128 | Original purchase value |
| `add_to_cart` | Long | Add to cart events |
| `conversion` | Long | Total conversions |
| **Attribution** | | |
| `product_id` | Long | Product ID |
| `url_tags` | String | UTM/tracking parameters |
| `valid_parameters` | Boolean | Has valid tracking params |
| `is_exclude` | Boolean | Excluded by filter rules |

### ad-details\_{shop_id}

Ad and campaign metadata (no time-series, updated periodically).

| Field | Type | Description |
| ------------------ | -------- | ------------------------ |
| `_id` | ObjectId | Document ID |
| `channel` | String | facebook/google/tiktok/x |
| `account_id` | String | Platform account ID |
| `account_name` | String | Account display name |
| `ad_account_id` | String | Ad account ID |
| `ad_account_name` | String | Ad account name |
| `campaign_id` | String | Campaign ID |
| `campaign_name` | String | Campaign name |
| `campaign_status` | String | Campaign status |
| `ad_group_id` | String | Ad group ID |
| `ad_group_name` | String | Ad group name |
| `ad_group_status` | String | Ad group status |
| `ad_id` | String | Ad ID |
| `ad_name` | String | Ad name |
| `ad_status` | String | Ad status |
| `currency_code` | String | Currency code |
| `product_id` | Long | Linked product ID |
| `url_tags` | String | Tracking parameters |
| `valid_parameters` | Boolean | Has valid tracking |

### ad-orders\_{shop_id}

Order attribution linking orders to ad clicks.

| Field | Type | Description |
| ------------------ | ---------- | ------------------------- |
| `_id` | ObjectId | Document ID |
| `channel` | String | facebook/google/tiktok/x |
| `date` | Date | Order date |
| `order_id` | Long | Order ID |
| `order_name` | String | Order number (#12345) |
| `customer_name` | String | Customer name |
| `country_code` | String | Customer country |
| `processed_at` | Date | Order processed timestamp |
| `attribution_type` | String | direct/indirect |
| `account_id` | String | Platform account ID |
| `ad_account_id` | String | Ad account ID |
| `campaign_id` | String | Attributed campaign |
| `ad_group_id` | String | Attributed ad group |
| `ad_id` | String | Attributed ad |
| **Financial** | | |
| `total_price` | Decimal128 | Order total price |
| `total_cost` | Decimal128 | Order COGS |
| `revenue` | Decimal128 | Net revenue |

### campaign-filter-rules

Rules for excluding campaigns from attribution.

| Field | Type | Description |
| ----------------- | ------------- | ------------------------ |
| `_id` | ObjectId | Document ID |
| `shop_id` | Long | Shop ID |
| `name` | String | Rule name |
| `status` | String | on/off |
| `type` | String | exclude/include |
| `channel` | String | facebook/google/tiktok/x |
| `account_id` | String | Platform account ID |
| `account_name` | String | Account name |
| `ad_account_id` | String | Ad account ID |
| `ad_account_name` | String | Ad account name |
| `keywords` | Array[String] | Filter keywords |
| `create_date` | Date | Created timestamp |
| `update_date` | Date | Updated timestamp |

---

## Common Query Scripts

### List All Shop Collections

```python
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('secret/databases/.env')
client = MongoClient(os.getenv('MONGODB_ADS_PROD_URI'))
db = client['ad-platform']

# Get all collection names
collections = db.list_collection_names()

# Count by type
insights = [c for c in collections if c.startswith('ad-insights_')]
details = [c for c in collections if c.startswith('ad-details_')]
orders = [c for c in collections if c.startswith('ad-orders_')]

print(f"ad-insights collections: {len(insights)}")
print(f"ad-details collections: {len(details)}")
print(f"ad-orders collections: {len(orders)}")
```

### Query Ad Insights for a Shop

```python
import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('secret/databases/.env')
client = MongoClient(os.getenv('MONGODB_ADS_PROD_URI'))
db = client['ad-platform']

shop_id = '<SHOP_ID>'
collection = db[f'ad-insights_{shop_id}']

# Find Facebook ads from last 30 days
results = collection.find({
    'channel': 'facebook',
    'date': {'$gte': datetime(2024, 11, 1)}
}).limit(10)

for doc in results:
    print(f"{doc['campaign_name']}: ${doc['spend']} spend, {doc['purchases']} purchases")
```

### Aggregate Spend by Campaign

```python
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('secret/databases/.env')
client = MongoClient(os.getenv('MONGODB_ADS_PROD_URI'))
db = client['ad-platform']

shop_id = '<SHOP_ID>'
collection = db[f'ad-insights_{shop_id}']

pipeline = [
    {'$match': {'channel': 'facebook'}},
    {'$group': {
        '_id': '$campaign_id',
        'campaign_name': {'$first': '$campaign_name'},
        'total_spend': {'$sum': '$spend'},
        'total_purchases': {'$sum': '$purchases'}
    }},
    {'$sort': {'total_spend': -1}},
    {'$limit': 10}
]

for doc in collection.aggregate(pipeline):
    print(f"{doc['campaign_name']}: ${doc['total_spend']:.2f}, {doc['total_purchases']} purchases")
```

### Find Orders Attributed to Ads

```python
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('secret/databases/.env')
client = MongoClient(os.getenv('MONGODB_ADS_PROD_URI'))
db = client['ad-platform']

shop_id = '<SHOP_ID>'
collection = db[f'ad-orders_{shop_id}']

results = collection.find({
    'channel': 'facebook',
    'attribution_type': 'direct'
}).sort('date', -1).limit(20)

for doc in results:
    print(f"Order {doc['order_name']}: ${doc['total_price']} - {doc['campaign_id']}")
```

### Get Campaign Filter Rules

```python
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('secret/databases/.env')
client = MongoClient(os.getenv('MONGODB_ADS_PROD_URI'))
db = client['ad-platform']

collection = db['campaign-filter-rules']
results = collection.find({'status': 'on'}).limit(50)

for doc in results:
    print(f"Shop {doc['shop_id']}: {doc['name']} ({doc['channel']})")
```

### Get Collection Schema (Sample Document)

```python
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('secret/databases/.env')
client = MongoClient(os.getenv('MONGODB_ADS_PROD_URI'))
db = client['ad-platform']

shop_id = '<SHOP_ID>'
collection = db[f'ad-insights_{shop_id}']

# Get one sample document
sample = collection.find_one()
if sample:
    # Convert ObjectId and Decimal128 for display
    for key, value in sample.items():
        print(f"{key}: {type(value).__name__}")
```

---

## Tips

1. **Collection naming:** Shop data uses `{type}_{shop_id}` pattern
2. **Decimal128:** Financial values use Decimal128 for precision - convert with `float()` for calculations
3. **Dates:** Use Python `datetime` objects in filters
4. **Channels:** facebook, google, tiktok, x (Twitter)
5. **Always use limit:** Large collections can have millions of documents
6. **Read-only:** These scripts are for querying only - do not modify data

---

## Environment Variables

| Variable | Description |
| ---------------------- | -------------------------------- |
| `MONGODB_PROD_URI` | Production db connection string |
| `MONGODB_ADS_PROD_URI` | Ad platform connection string |
| `MONGODB_STAGING_URI` | Staging environment |
| `MONGODB_REVIEW_URI` | Review environment |
