from django.db import models

# Create your models here.
class UserTable(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return "<UserTable: %s>" % self.username

class Comment(models.Model):
    userme = models.CharField(max_length=20)
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_time']

