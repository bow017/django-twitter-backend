from django.contrib.auth.models import User
from django.db import models
from tweets.models import Tweet


class Comment(models.Model):
    """
    So far we cannot comment on other comments,
    we can only comment on a tweet.
    """
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tweet = models.ForeignKey(Tweet, null=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = (('tweet', 'created_at'),)

    def __str__(self):
        return '{} - {} said {} in tweet {}'.format(
            self.created_at,
            self.user,
            self.content,
            self.tweet_id,
        )
