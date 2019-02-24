import pusher

from new_dawn_server.settings import (
	PUSHER_APP_ID,
	PUSHER_APP_KEY,
	PUSHER_APP_SECRET,
	PUSHER_CLUSTER,
)

CHAT_EVENT = "chat_event"
TEST_CHANNEL = "test_channel"
MESSAGE = "message"
USER_FROM_ID = "user_from_id"
USER_TO_ID = "user_to_id"

class ChatService:

	def __init__(self, user_me_id=None, user_you_id=None):
		self.user_me_id = user_me_id
		self.user_you_id = user_you_id

	def _build_channel_id(self):
		if self.user_me_id < self.user_you_id:
			return TEST_CHANNEL + "_" + self.user_me_id + "_" + self.user_you_id
		return TEST_CHANNEL + "_" + self.user_me_id + "_" + self.user_you_id

	def send(self, message):
		pusher_client = pusher.Pusher(
			app_id=PUSHER_APP_ID,
			key=PUSHER_APP_KEY,
			secret=PUSHER_APP_SECRET,
			cluster=PUSHER_CLUSTER,
			ssl=True
		)
		if self.user_me_id and self.user_you_id:
			pusher_client.trigger(
				self._build_channel_id(), 
				CHAT_EVENT, 
				{
					MESSAGE: message,
					USER_FROM_ID: str(self.user_me_id),
					USER_TO_ID: str(self.user_you_id)
				})
		else:
			pusher_client.trigger(
				TEST_CHANNEL, CHAT_EVENT, {MESSAGE: message})


