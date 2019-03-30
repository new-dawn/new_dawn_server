from pusher_push_notifications import PushNotifications

beams_client = PushNotifications(
    instance_id='466cb5de-0fd2-40c7-ad45-802b6c79550e',
    secret_key='26C789164E94F87D4125293F36DE3C988A36998FBEF78FE8BFE86B274E998BFD',
)


class NotificationService:

    @staticmethod
    def beams_auth(user_id):
        beams_token = beams_client.generate_token(str(user_id))
        return beams_token

    @staticmethod
    def send_notification(user_ids, message=None, title=None):
        response = beams_client.publish_to_users(
            user_ids=user_ids,
            publish_body={
                'apns': {
                    'aps': {
                        'alert': message,
                    },
                },
                'fcm': {
                    'notification': {
                        'title': 'Hello',
                        'body': 'Hello, world!',
                    },
                },
            },
        )
