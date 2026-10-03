import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

load_dotenv()

def get_client():

    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")

    if not endpoint:
        raise ValueError(
            "AZURE_LANGUAGE_ENDPOINT is missing from .env" )

    if not key:
        raise ValueError(
            "AZURE_LANGUAGE_KEY is missing from .env"
        )

    return TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

def analyze_sentiment(text):

    client = get_client()
    response = client.analyze_sentiment([text])
    result = response[0]

    if result.is_error:
        raise RuntimeError(result.error.message)

    return {
        "sentiment": result.sentiment,
        "positive": result.confidence_scores.positive,
        "neutral": result.confidence_scores.neutral,
        "negative": result.confidence_scores.negative
    }

def extract_key_phrases(text):
    
    client = get_client()
    response = client.extract_key_phrases([text])
    result = response[0]

    if result.is_error:
        raise RuntimeError(result.error.message)

    return list(result.key_phrases)


def recognize_entities(text):

    client = get_client()
    response = client.recognize_entities([text])
    result = response[0]

    if result.is_error:
        raise RuntimeError(result.error.message)

    entities = []
    
    for entity in result.entities:
        entities.append({
            "text": entity.text,
            "category": entity.category,
            "confidence": entity.confidence_score
        })

    return entities