from pusher_push_notifications import PushNotifications
from new_dawn_server.settings import (
    BEAMS_INSTANCE_ID,
    BEAMS_SECRET_KEY
)

beams_client = PushNotifications(
    instance_id=BEAMS_INSTANCE_ID,
    secret_key=BEAMS_SECRET_KEY,
)


class NotificationService:

    @staticmethod
    def beams_auth(user_id):
        beams_token = beams_client.generate_token(str(user_id))
        return beams_token

    @staticmethod
    def send_notification(user_ids, message=None):
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
