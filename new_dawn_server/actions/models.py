from django.db import models


class UserToUserActionMetadata(models.Model):
    user_account_from = models.ForeignKey("users.Account", on_delete=models.CASCADE, related_name="from_user",
                                          null=True, blank=True)
    user_account_to = models.ForeignKey("users.Account", on_delete=models.SET_NULL, related_name="to_user", null=True,
                                        blank=True)
    update_time = models.DateTimeField(auto_now_add=True)


class Block(models.Model):
    block_metadata = models.OneToOneField(UserToUserActionMetadata, on_delete=models.CASCADE, blank=True, null=True)


class Like(models.Model):
    like_metadata = models.OneToOneField(UserToUserActionMetadata, on_delete=models.CASCADE, blank=True, null=True)


class Relationship(models.Model):
    relationship_metadata = models.OneToOneField(UserToUserActionMetadata, on_delete=models.CASCADE, blank=True,
                                                 null=True)


class Match(models.Model):
    match_metadata = models.OneToOneField(UserToUserActionMetadata, on_delete=models.CASCADE, blank=True, null=True)
