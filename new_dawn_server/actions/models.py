from django.db import models


class UserToUserActionMetadata(models.Model):
    entity_id = models.IntegerField(blank=True, null=True)
    entity_type = models.IntegerField(blank=True, null=True)
    user_account_from = models.ForeignKey("users.Account",
                                          on_delete=models.CASCADE, related_name="from_user")
    user_account_to = models.ForeignKey("users.Account", on_delete=models.CASCADE,
                                        related_name="to_user")
    update_time = models.DateTimeField(auto_now_add=True)


class Block(models.Model):
    block_metadata = models.OneToOneField(UserToUserActionMetadata, on_delete=models.CASCADE)


class Like(models.Model):
    like_metadata = models.OneToOneField(UserToUserActionMetadata, on_delete=models.CASCADE)


class Relationship(models.Model):
    relationship_metadata = models.OneToOneField(UserToUserActionMetadata, on_delete=models.CASCADE)


class Match(models.Model):
    match_metadata = models.OneToOneField(UserToUserActionMetadata, on_delete=models.CASCADE)
