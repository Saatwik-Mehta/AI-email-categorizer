import json
import logging
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
comprehend_client = boto3.client("comprehend")

sentiment_to_category_mapping = {
    "positive": "support",
    "negative": "critical",
    "neutral": "normal",
    "mixed": "normal",
}


def lambda_function(event, context):
    try:
        body = json.loads(event["body"])
        plain_email_content = body.get("body-plain")
        logger.info("Received email content: " + plain_email_content)
        response = comprehend_client.detect_sentiments(
            Text=plain_email_content, LanguageCode="en"
        )
        # 'POSITIVE'|'NEGATIVE'|'NEUTRAL'|'MIXED'
        email_sentiment = response["Sentiment"].lower()

        # We will categorize the email based on the sentiments:
        # - Positive -> will be stored for support (praised by audience)
        # - Neutral -> will be stored normal
        # - Mixed -> will be stored normal
        # - Negative -> will be stored for critical

        # Create Fifo Qs to process emails.
        return {
            "statusCode": 200,
            "body": "Message will be processed",
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "*",
            },
        }
    except Exception as err:
        logger.error(err)
        return {"statusCode": 500, "body": "Internal Server Error"}
