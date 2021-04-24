from pyfcm import FCMNotification

push_service = FCMNotification(
    api_key="API_KEY")

topic = "Stream"

# To get Api Key:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

message_title = "We're live!"
message_body = "Please open the app"
result = push_service.notify_topic_subscribers(
    topic_name=topic, message_body=message_body, message_title=message_title)


print(result)
