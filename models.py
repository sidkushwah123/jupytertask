from django.db import models
import django

#models
class Alldata_tweet(models.Model):
    keyword_search = models.CharField(max_length=50, null=True, blank=True)
    Search_date = models.DateField(default=django.utils.timezone.now)
    tweet_created = models.DateTimeField(default=django.utils.timezone.now)
    tweet_id = models.BigIntegerField(null=True, blank=True)
    tweet_id_str = models.CharField(max_length=30, null=True, blank=True)
    User_name = models.CharField(max_length=30, null=True, blank=True)
    Screen_name = models.CharField(max_length=50, null=True, blank=True)
    user_location = models.CharField(max_length=100, null=True, blank=True)
    verified = models.BooleanField(default=False)
    source = models.CharField(max_length=30, null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    Tweet_text = models.TextField(max_length=500, null=True, blank=True)
    in_reply_to_screen_name = models.CharField(max_length=50, null=True, blank=True)
    in_reply_to_user_id_str = models.CharField(max_length=30, null=True, blank=True)
    reply_count = models.IntegerField(null=True, blank=True)
    retweet_count = models.IntegerField(null=True, blank=True)
    favorite_count = models.IntegerField(null=True, blank=True)
    lang = models.CharField(max_length=50, null=True, blank=True)
    favorited = models.CharField(max_length=30, null=True, blank=True)
    retweeted = models.CharField(max_length=30, null=True, blank=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.tweet_id)

  
class FILTER_tweet_DATA(models.Model):
    keyword_search = models.CharField(max_length=50, null=True, blank=True)
    Search_date = models.DateField(default=django.utils.timezone.now)
    tweet = models.ForeignKey(Alldata_tweet, related_name='tweet', on_delete=models.CASCADE)
    Tweet_text = models.TextField(max_length=500, null=True, blank=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.tweet)

class FINAL_TWEET_DATA(models.Model):
    keyword_search = models.CharField(max_length=50, null=True, blank=True)
    Search_date = models.DateField(default=django.utils.timezone.now)
    tweet_created = models.DateTimeField(default=django.utils.timezone.now)
    tweet_id = models.BigIntegerField(null=True, blank=True)
    tweet_id_str = models.CharField(max_length=30, null=True, blank=True)
    User_name = models.CharField(max_length=30, null=True, blank=True)
    Screen_name = models.CharField(max_length=50, null=True, blank=True)
    user_location = models.CharField(max_length=100, null=True, blank=True)
    verified = models.BooleanField(default=False)
    source = models.CharField(max_length=30, null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    Tweet_text = models.TextField(max_length=500, null=True, blank=True)
    in_reply_to_screen_name = models.CharField(max_length=50, null=True, blank=True)
    in_reply_to_user_id_str = models.CharField(max_length=30, null=True, blank=True)
    reply_count = models.IntegerField(null=True, blank=True)
    retweet_count = models.IntegerField(null=True, blank=True)
    favorite_count = models.IntegerField(null=True, blank=True)
    lang = models.CharField(max_length=50, null=True, blank=True)
    favorited = models.CharField(max_length=30, null=True, blank=True)
    retweeted = models.CharField(max_length=30, null=True, blank=True)
    sentiment = models.CharField(max_length=30, null=True, blank=True)
    category = models.CharField(max_length=30, null=True, blank=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.tweet_id)
