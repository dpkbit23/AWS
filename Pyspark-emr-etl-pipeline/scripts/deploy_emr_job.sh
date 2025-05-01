#!/bin/bash

REGION="us-east-1"
CLUSTER_NAME="pyspark-daily-pipeline"
S3_SCRIPT_URI="s3://your-code-bucket/path/to/scripts/etl_pipeline.py"
INPUT_S3_PATH="s3://your-raw-data-bucket/path/"
OUTPUT_S3_PATH="s3://your-processed-data-bucket/path/"
CONFIG_S3_PATH="s3://your-config-bucket/path/config.yaml"

aws emr create-cluster \
    --name "$CLUSTER_NAME" \
    --release-label emr-6.15.0 \
    --applications Name=Spark \
    --ec2-attributes KeyName=your-ec2-keypair-name \
    --instance-type m5.xlarge \
    --instance-count 3 \
    --use-default-roles \
    --log-uri s3://your-log-bucket/emr-logs/ \
    --region $REGION \
    --steps Type=Spark,Name="PySparkETLJob",ActionOnFailure=CONTINUE,Args=["--deploy-mode","cluster","--master","yarn","$S3_SCRIPT_URI","$CONFIG_S3_PATH"] \
    --auto-terminate
