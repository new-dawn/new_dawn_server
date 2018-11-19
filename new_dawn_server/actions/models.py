from django.db import models


class ActionsMetadata(models.Model):
    user_account_from = models.ForeignKey("users.Account", on_delete=models.CASCADE, related_name="from_user")
    user_account_to = models.ForeignKey("users.Account", on_delete=models.SET_NULL, related_name="to_user", null=True)
    update_time = models.DateTimeField(auto_now_add=True)


class Block(models.Model):
    block_id = models.OneToOneField(ActionsMetadata, on_delete=models.CASCADE, primary_key=True)


class Like(models.Model):
    like_id = models.OneToOneField(ActionsMetadata, on_delete=models.CASCADE, primary_key=True)


class Relationship(models.Model):
    relationship_id = models.OneToOneField(ActionsMetadata, on_delete=models.CASCADE,
                                           primary_key=True)


class Match(models.Model):
    match_id = models.OneToOneField(ActionsMetadata, on_delete=models.CASCADE, primary_key=True)
