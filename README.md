# AWS serverless BI pipeline

Proof-of-concept for building serverless BI pipelines, with benchmarks of various approaches.

Uses serverless AWS services:
- S3 as data lake
- Glue for schema discovery
- Athena for querying files with SQL
- QuickSight for visualization

We use [Yelp dataset](https://www.yelp.com/dataset). Specifically, we select 
a subset of data to work with, which as the most interesting for us in terms 
of BI analysis.
