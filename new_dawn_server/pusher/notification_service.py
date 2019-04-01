from pusher_push_notifications import PushNotifications
from django.conf import settings


beams_client = PushNotifications(
            instance_id=settings.BEAMS_INSTANCE_ID,
            secret_key=settings.BEAMS_SECRET_KEY,
        )


class NotificationService():

    def beams_auth(self, user_id):
        beams_token = beams_client.generate_token(str(user_id))
        return beams_token

    def send_notification(self, user_ids, message=None):
        response = beams_client.publish_to_users(
            user_ids=user_ids,
            publish_body={
                'apns': {
                    'aps': {
                        'alert': message,
                    },
                },
            },
        )
