# po-demos
# GCP Process
```mermaid
---
config:
  theme: 'neutral'
---
flowchart TB
    bq_raw@{ shape: cyl, label: "BigQuery (Raw)"}
        style bq_raw fill: #CD7F32, stroke-width:5px
    bq_prod@{ shape: cyl, label: "BigQuery (Prod)"}
        style bq_prod fill: #FFD700, stroke-width:5px
    sf@{ shape: cyl, label: "Salesforce Object" }
    gcp_store@{ shape: cyl, label: "GCP Storage Bucket" }
    trx@{ shape: cyl, label: "JSON from API"}
    data_transfer@{ shape: process, label: "Data Transfer Service"}
    dataform@{ shape: processes, label: "Dataform"}
    cloud_scheduler@{ shape: process, label: "Cloud Scheduler"}
    pubsub@{ shape: process, label: "Pub/Sub Message"}
    cloud_run@{ shape: process, label: "Cloud Run"}
    python@{ shape: lean-r, label: "Python Script \n (GitHub Hosted)"}
    bi@{ shape: docs, label: "Data Studio Reporting" }
    spacer[ ]
        style spacer opacity:0,height:5px

    subgraph ingestion["Data Ingestion"]
        direction TB
        data_transfer
        cloud_scheduler --> |_cron schedule creates_| pubsub
        pubsub --> |_initiates_| cloud_run
        cloud_run --> |_packages and runs_| python
        python --- |_fetches and parses_| trx --> |_outputs parsed json to_| gcp_store
        sf --> |_on a schedule_| data_transfer
        data_transfer --> |_direct copy_| bq_raw
        bq_raw --- |_directly queries via external table_| gcp_store
    end

    subgraph transformation["Data Transformation"]
        spacer ~~~ dataform
        dataform --> |_scheduled sql scripts_| bq_prod
    end

    bq_raw --> dataform
    bq_prod --> bi
```