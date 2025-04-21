"""
Webhook used by other mail-client to initiate the process of email categorization.
"""
import json
import logging
import boto3

from Utils.common_responses import ok_response

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
        logger.info("Received email content: %s",  plain_email_content)
        response = comprehend_client.detect_sentiment(
            Text=plain_email_content, LanguageCode="en"
        )
        # Sentiments: 'POSITIVE'|'NEGATIVE'|'NEUTRAL'|'MIXED'
        email_sentiment = response["Sentiment"].lower()
        logger.info("Email Sentiment: %s", email_sentiment)
        # We will categorize the email based on the sentiments:
        # - Positive -> will be stored for support (praised by audience)
        # - Neutral -> will be stored normal
        # - Mixed -> will be stored normal
        # - Negative -> will be stored for critical

        # TODO: Create Fifo Qs to process emails.
        return ok_response("Message will be processed!")
    except Exception as err:
        logger.error(err)
        return ok_response("Something went wrong!")
