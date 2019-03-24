from pusher_push_notifications import PushNotifications

# from new_dawn_server.settings import (
#     PUSHER_BEAM_INSTANCEID,
#     PUSHER_APP_SECRET
# )

PUSHER_BEAM_INSTANCEID = "d03e2f58-b24e-4343-a01d-3122b609b9b9"
PUSHER_APP_SECRET = "2EAD4A8184D4A7F3DEC7CB60C4D3DDDBB2F623A657F319AA8D7A28D3B05818B9"

beams_client = PushNotifications(
    instance_id=PUSHER_BEAM_INSTANCEID,
    secret_key=PUSHER_APP_SECRET,
)

class BeamsNotification:
    def __init__(self, user_id):
        self.user_id = user_id

    def auth(self):
        beams_token = beams_client.generate_token(self.user_id)
        return beams_token

    def notify(self, title, message):
        response = beams_client.publish_to_users(
            user_ids=[self.user_id],
            publish_body={
                'apns': {
                    'aps': {
                        'alert': 'hello',
                    },
                },
                'fcm': {
                    'notification': {
                        'title': title,
                        'body': message,
                    },
                },
            },
        )
        return response['publishId']