"""Serviço para integração com Amazon SQS."""

import os
import boto3
import logging

logger = logging.getLogger(__name__)

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "sa-east-1")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", "")

sqs_client = None
if SQS_QUEUE_URL:
    try:
        sqs_client = boto3.client("sqs", region_name=AWS_REGION)
        logger.info("✅ Cliente SQS inicializado com sucesso.")
    except Exception as e:
        logger.warning(f"⚠️ Falha ao inicializar cliente SQS: {e}")


def enviar_mensagem(mensagem: dict) -> bool:
    """Envia uma mensagem para a fila SQS."""
    if not sqs_client or not SQS_QUEUE_URL:
        logger.warning("SQS não configurado, mensagem não enviada.")
        return False
    try:
        sqs_client.send_message(QueueUrl=SQS_QUEUE_URL, MessageBody=str(mensagem))
        logger.info("Mensagem enviada para SQS com sucesso.")
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem para SQS: {e}")
        return False


def ler_mensagens(max_messages: int = 5) -> list:
    """Lê mensagens da fila SQS (sem deletar)."""
    if not sqs_client or not SQS_QUEUE_URL:
        return []

    try:
        response = sqs_client.receive_message(
            QueueUrl=SQS_QUEUE_URL, MaxNumberOfMessages=max_messages, WaitTimeSeconds=2
        )
        return response.get("Messages", [])
    except Exception as e:
        logger.error(f"⚠️ Erro ao ler mensagens da SQS: {e}")
        return []
