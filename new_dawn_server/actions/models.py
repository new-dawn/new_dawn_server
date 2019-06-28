from django.db import models
from django.contrib.auth.models import User


class UserAction(models.Model):
    action_type = models.IntegerField(blank=True, null=True)
    entity_id = models.IntegerField(blank=True, null=True)
    entity_type = models.IntegerField(blank=True, null=True)
    message = models.CharField(blank=True, max_length=200, null=True)
    user_from = models.ForeignKey(User,
                                  on_delete=models.CASCADE, related_name="from_user", blank=True, null=True)
    user_to = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="to_user", blank=True, null=True)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return str(self.user_from.id) + "_to_" + str(self.user_from.id) + "_action_" + str(self.action_type)
