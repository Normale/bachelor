from tortoise import fields, models


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    full_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    is_superuser = fields.BooleanField(default=False)


class Notes(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=225)
    content = fields.TextField()
    author = fields.ForeignKeyField("models.Users", related_name="note")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    def __str__(self):
        return f"{self.title}, {self.author_id} on {self.created_at}"

class Styles(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=225)
    author = fields.ForeignKeyField("models.Users", related_name="style")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    def __str__(self):
        return f"{self.name}, {self.author_id} on {self.created_at}"

class Results(models.Model):
    id = fields.IntField(pk=True)
    content_image = fields.CharField(max_length=255)
    style_image = fields.CharField(max_length=255)
    result_url = fields.CharField(max_length=4096)
    style = fields.ForeignKeyField("models.Styles", related_name="result")
    user = fields.ForeignKeyField("models.Users", related_name="result")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    def __str__(self):
        return f"Result by user {self.user_id} with style {self.style_id} on {self.created_at}"
