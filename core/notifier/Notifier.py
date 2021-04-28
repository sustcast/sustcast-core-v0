from pyfcm import FCMNotification
from decouple import config


def CreatePush(message_title, message_body):

    key = config('SECRET_KEY')
    push_service = FCMNotification(
        api_key=key)

    result = push_service.notify_topic_subscribers(
        topic_name="Stream", message_body=message_body, message_title=message_title)

    print(result)