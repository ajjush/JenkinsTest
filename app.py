import json
import logging
import os

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

HOOK_URL = os.environ['HookUrl']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message = event['message']
    try:
        stage = " on stage - " + message['detail']['stage']
        logger.info(stage)
    except:
        stage=""
    if message['detail']['pipeline'] != "SC-019725351547-pp-wnmj5clcy4qgq-BackendPipeline-3E189YXAX76N":
        return {
            "statusCode":200,
            "body": "No msg sent to MS Teams"
        }

    message = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "themeColor": "0076D7",
    "summary": message['source'],
    "title": message['detail-type'],
    "sections": [
        {
            "activityTitle": message['detail']['pipeline'] + " has " + message['detail']['state'] +stage,
            "activitySubtitle": "On "+ message['time'],
            "activityImage": "https://img.stackshare.io/service/3297/aws-codepipeline.png",
        }
    ]
}

    req = Request(HOOK_URL, json.dumps(message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info(message)
        logger.info("Message posted")
        return {
            "statusCode":200,
            "body": "Success"
        }
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
