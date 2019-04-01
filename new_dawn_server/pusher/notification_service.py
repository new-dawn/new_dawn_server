from pusher_push_notifications import PushNotifications
from django.conf import settings


class NotificationService:

    def __init__(self):
        instance_key = self._get_instance_id_and_secret_key()
        self.beams_client = PushNotifications(
            instance_id=instance_key[0],
            secret_key=instance_key[1],
        )

    @staticmethod
    def _get_instance_id_and_secret_key():
        return [settings.BEAMS_INSTANCE_ID, settings.BEAMS_SECRET_KEY]

    def beams_auth(self, user_id):
        beams_token = self.beams_client.generate_token(str(user_id))
        return beams_token

    def send_notification(self, user_ids, message=None):
        response = self.beams_client.publish_to_users(
            user_ids=user_ids,
            publish_body={
                'apns': {
                    'aps': {
                        'alert': message,
                    },
                },
            },
        )
