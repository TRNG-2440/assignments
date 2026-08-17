# Assignment Architecture

┌─────────────────────────────────────────────────────────────────┐
│  GCP Project: revature-assignments                                │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │  Bucket: freshmart_bucket                                   │   │
│  │    └── inventory/                                           │   │
│  │          ├── inventory_001.csv                               │   │
│  │          ├── inventory_002.csv                               │   │
│  │          └── inventory_003.csv                               │   │
│  └───────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                            │  IAM grant: Storage Object Viewer
                            │  (principal = Snowflake service account)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Snowflake Storage Integration: gcs_freshmart_int                  │
│  (secure, credential-less trust between Snowflake & GCS)          │
└──────────────────────────┬──────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Schema: RAW                                                       │
│                                                                     │
│   External Stage (raw.inventory_stage)                            │
│           │  COPY INTO (repeatable, file-tracking load)           │
│           ▼                                                        │
│   Table: raw.raw_inventory_events  ──────────────┐                │
│           │  (append-only, full history)         │                │
│           ▼                                       │                │
│   Stream: raw.raw_inventory_stream                │ (offset marker,│
│   (exposes only unconsumed rows;                  │  no data copy) │
│    METADATA$ACTION / ISUPDATE / ROW_ID)  ◄────────┘                │
└──────────────────────────┬──────────────────────────────────────┘
                            │  read (auto-advances stream offset
                            │  only on successful DML)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Schema: CURATED                                                    │
│                                                                     │
│   Task: process_inventory_stream                                   │
│     - WHEN SYSTEM$STREAM_HAS_DATA(...)  → skip if no new data     │
│     - MERGE INTO current_inventory                                 │
│         WHEN MATCHED     → UPDATE qty/price/ts                    │
│         WHEN NOT MATCHED → INSERT new product+warehouse row       │
│           │                                                        │
│           ▼                                                        │
│   Table: curated.current_inventory                                 │
│   (business key: product_id + warehouse_id)                        │
│   → latest stock position per product/warehouse                   │
└─────────────────────────────────────────────────────────────────┘
