"""Configurações e clientes AWS (SQS, CloudWatch, etc)."""

import os
import boto3

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "sa-east-1")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

# Cliente SQS
sqs_client = boto3.client("sqs", region_name=AWS_REGION)
