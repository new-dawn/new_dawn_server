import pusher

from new_dawn_server.settings import (
	PUSHER_APP_ID,
	PUSHER_APP_KEY,
	PUSHER_APP_SECRET,
	PUSHER_CLUSTER,
)

CHAT_EVENT = "chat"
TEST_CHANNEL = "test_channel"
MESSAGE = "message"

class ChatService:

	def __init__(self, user_me_id=None, user_you_id=None):
		self.user_me_id = user_me_id
		self.user_you_id = user_you_id

	def trigger(self):
		pusher_client = pusher.Pusher(
			app_id=PUSHER_APP_ID,
			key=PUSHER_APP_KEY,
			secret=PUSHER_APP_SECRET,
			cluster=PUSHER_CLUSTER,
			ssl=True
		)
		if user_me_id and user_you_id:
			pusher_client.trigger(
				"my-channel", CHAT_EVENT, {MESSAGE: "hello world"})
		else:
			pusher_client.trigger(
				TEST_CHANNEL, CHAT_EVENT, {MESSAGE: "hello world"})


