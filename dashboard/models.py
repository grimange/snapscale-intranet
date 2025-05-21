import pytz
from django.db import models
from django.contrib.auth import get_user_model

class PostManager(models.Manager):
    def get_all_json(self):
        results = self.all()

        data = []
        for result in results:
            post_date = result.created_at.astimezone(pytz.timezone('Asia/Manila')).strftime('%b %d, %Y %I:%M %p')
            data.append({'id': result.id, 'content': result.content, 'username': result.created_by.username,
                         'post_date': post_date})
        return data

class Post(models.Model):
    content = models.TextField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReplyToComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
