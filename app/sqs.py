"""Serviço para integração com Amazon SQS."""

import os
import boto3
import logging

logger = logging.getLogger(__name__)

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "sa-east-1")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", "")

# Cliente SQS
try:
    sqs_client = boto3.client("sqs", region_name=AWS_REGION)
    logger.info("✅ Cliente SQS inicializado com sucesso.")
except Exception as e:
    logger.warning(f"⚠️ Falha ao inicializar cliente SQS: {e}")
    sqs_client = None
