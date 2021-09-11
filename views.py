from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
import tweepy
import time
from django.template.loader import render_to_string
import requests
import json
from .models import insta_data,twitter_data

from django.contrib import messages
from role.views import check_permition_validation
from django.urls import reverse
from dashboard.models import Sync_accounts




@method_decorator(login_required, name="dispatch")
class SearchEngineView(generic.TemplateView):
    template_name = 'search_engine/search_engine.html'

    def get(self, request, *args, **kwargs):
    
        user_id = request.user.id
        file_name = "search-engine"

        status = check_permition_validation(file_name,user_id)
    
        if status == 1: 
            return render(request, self.template_name)
        else:
            messages.error(request, "You have not authority to access Search Engine ")
            return HttpResponseRedirect(reverse('dashboard:dashboard'))

    def post(self,request):
        keyword = request.POST.get("keyword")
        # facebook = facebook_search(request,keyword)
        instagram = instagram_search(request,keyword)
        twitter = twitter_search(request,keyword)

        
        return render(request,self.template_name,{'instagram':instagram,'twitter':twitter})
        

def twitter_search(request,keyword):

    result = twitter_data.objects.filter(Tweet_text__contains=keyword)

    fiter_data = []
    for item in result:
        data_dist = {}
        data_dist['Date'] = item.Date
        data_dist['Tweet_id'] = item.Tweet_id
        data_dist['Tweet_text'] = item.Tweet_text
        data_dist['screan_name'] = item.screan_name
        data_dist['user_name'] = item.user_name

        fiter_data.append(data_dist) 

    return fiter_data




    # Twitter_account = Sync_accounts.objects.filter(current_sync=True,account_type="Twitter")

    # for item in Twitter_account:
    #     access_token = item.access_token
    #     access_token_secret = item.access_token_secret

    

    

    # if len(Twitter_account) > 0:

    #     # token = request.session["access_token_twitter"]

    #     mycreds = {
    #         'consumer_key': "eNrUeXaXL5eHWTI6V8SC29ZUH",
    #         'consumer_secret': "YrU89LE4yLkL6bJK1u8Up2z5Oj9PafSZKoxPrAFDpbvpjgYg8A",
    #         'access_token': access_token,
    #         'access_token_secret': access_token_secret
    #         }

    #     t_auth = tweepy.OAuthHandler(
    #                 consumer_key = mycreds['consumer_key'],
    #                 consumer_secret = mycreds['consumer_secret']
    #     )
    #     t_auth.set_access_token(
    #         mycreds['access_token'],
    #         mycreds['access_token_secret']
    #     )

    #     api = tweepy.API(t_auth)

    #     me_obj = api.me()
    #     # print(me_obj)
    #     user_id = me_obj.id
    #     # print(me_obj)

    #     fetched_tweets =  tweepy.Cursor(api.user_timeline, user_id=user_id, tweet_mode="extended").items()

    #     fiter_data = []
    #     for tweet in fetched_tweets: 
    #         # if tweet.truncated:
    #         #     tweet_text = tweet.extended_tweet['full_text']     
    #         # else:
    #         #     tweet_text = tweet.text  
    #         data_dist = {}
    #         if keyword in tweet.full_text:
    #             if hasattr(tweet, "retweeted_status"):
    #                 data_dist['created_at'] = tweet.retweeted_status.created_at
    #                 data_dist['user_name'] = tweet.retweeted_status.user.name
    #                 data_dist['screan_name'] = tweet.retweeted_status.user.screen_name
    #                 data_dist['profile_image_background'] = tweet.retweeted_status.user.profile_background_image_url_https
    #                 data_dist['profile_image'] = tweet.retweeted_status.user.profile_image_url_https
    #                 data_dist['id'] = tweet.retweeted_status.id
    #                 data_dist['text'] = tweet.retweeted_status.full_text
    #                 data_dist['hastags'] = tweet.retweeted_status.entities['hashtags']
    #                 data_dist['symbol'] = tweet.retweeted_status.entities['symbols']
    #                 data_dist['user_mantion'] = tweet.retweeted_status.entities['user_mentions']
    #                 data_dist['url_attach'] = tweet.retweeted_status.entities['urls']
    #                 data_dist['main_url'] = "https://twitter.com/"+tweet.retweeted_status.user.screen_name+"/status/"+str(tweet.retweeted_status.id)
                    
    #                 if 'media' in tweet.retweeted_status.entities: 
    #                     data_dist['media'] = tweet.retweeted_status.entities['media']  
    #                 else:
    #                     data_dist['media'] = "None"

    #                 # if 'reply_count' in tweet.retweeted_status: 
    #                 if hasattr(tweet.retweeted_status, "reply_count"): 
    #                     data_dist['reply_count'] = tweet.retweeted_status.reply_count
    #                 else:
    #                     data_dist['reply_count'] = "None"
                    
    #                 data_dist['retweet_count'] = tweet.retweeted_status.retweet_count
    #                 data_dist['favorite_count'] = tweet.retweeted_status.favorite_count
    #                 print(tweet.retweeted_status)


                        
    #                 # print(tweet.retweeted_status.created_at,tweet.retweeted_status.user.name,tweet.retweeted_status.user.screen_name,tweet.retweeted_status.profile_background_image_url_https,tweet.retweeted_status.profile_image_url_https,tweet.retweeted_status.id,)
    #                 # url = https://twitter.com/tweet.retweeted_status.user.screen_name/status/tweet.retweeted_status.id
    #             else:
    #                 data_dist['created_at'] = tweet.created_at
    #                 data_dist['user_name'] = tweet.user.name
    #                 data_dist['screan_name'] = tweet.user.screen_name
    #                 data_dist['profile_image_background'] = tweet.user.profile_background_image_url_https
    #                 data_dist['profile_image'] = tweet.user.profile_image_url_https
    #                 data_dist['id'] = tweet.id
    #                 data_dist['text'] = tweet.full_text
    #                 data_dist['hastags'] = tweet.entities['hashtags']
    #                 data_dist['symbol'] = tweet.entities['symbols']
    #                 data_dist['user_mantion'] = tweet.entities['user_mentions']
    #                 data_dist['url_attach'] = tweet.entities['urls']
    #                 data_dist['main_url'] = "https://twitter.com/"+tweet.user.screen_name+"/status/"+str(tweet.id)
                   
    #                 if 'media' in tweet.entities: 
    #                     data_dist['media'] = tweet.entities['media']
    #                 else:
    #                     data_dist['media'] = "None"

    #                 if hasattr(tweet, "reply_count"): 
    #                     data_dist['reply_count'] = tweet.reply_count
    #                 else:
    #                     data_dist['reply_count'] = "None"
                    
    #                 data_dist['retweet_count'] = tweet.retweet_count
    #                 data_dist['favorite_count'] = tweet.favorite_count

    #             fiter_data.append(data_dist) 

    #     return fiter_data
    # else:
    #     return HttpResponse("first authorize your system")
              


# def facebook_search(request,keyword):
    if 'access_token_facebook' in request.session:
    
        accessToken = request.session["access_token_facebook"]

        page_token_url = "https://graph.facebook.com/me/accounts?fields=name,access_token&access_token="+accessToken
        page_token_response = requests.get(page_token_url)
        page_token_responseObj = json.loads(page_token_response.content)

        page_list = []

        for item in page_token_responseObj['data']:

            page_list.append(item)
        
        # print(page_list)
        # return page_list
        fiter_data = []
        for item in page_list:

            page_id = item['id']
            page_access_token = item['access_token']

            page_data_get = "https://graph.facebook.com/v9.0/"+page_id+"/feed?access_token="+page_access_token
            page_data_get_response = requests.get(page_data_get)
            page_data_get_responseObj = json.loads(page_data_get_response.content)
            # return page_data_get_responseObj
            print(page_data_get_responseObj)

            # fiter_data.append(page_data_get_responseObj)

            if 'data' in page_data_get_responseObj:
                
                for item in page_data_get_responseObj['data']:

                    if 'message' in item:
                        data_dist = {}
                        if keyword in item['message']:
                            page_info = "https://graph.facebook.com/v9.0/"+page_id+"?fields=name,picture&access_token="+page_access_token
                            page_info_response = requests.get(page_info)
                            page_info_responseObj = json.loads(page_info_response.content)
                            
                            data_dist["page_data"] = page_info_responseObj
                            # print(page_info_responseObj['picture']['data']['url'])
                            data_dist["page_name"] = page_info_responseObj['name']
                            data_dist["page_profile"] = page_info_responseObj['picture']['data']['url']
                            data_dist["post_created_time"] = item['created_time']
                            data_dist["message"] = item['message']
                            # data_dist[]
                            
                            # data_dist["main_data"] = item
                            post_who_match_url = "https://graph.facebook.com/v9.0/"+item['id']+"?fields=permalink_url&access_token="+page_access_token
                            post_who_match_url_response = requests.get(post_who_match_url)
                            post_who_match_url_responseObj = json.loads(post_who_match_url_response.content)
    
                            data_dist["post_url"] = post_who_match_url_responseObj['permalink_url']

                            post_who_match_attach = "https://graph.facebook.com/v9.0/"+item['id']+"/attachments?access_token="+page_access_token
                            post_who_match_attach_response = requests.get(post_who_match_attach)
                            post_who_match_attach_responseObj = json.loads(post_who_match_attach_response.content)

                            data_dist["attachments"] = post_who_match_attach_responseObj['data']
                            post_who_match_data = "https://graph.facebook.com/v9.0/"+item['id']+"?fields=shares,reactions.summary(true),comments.summary(true)&access_token="+page_access_token
                            post_who_match_data_response = requests.get(post_who_match_data)
                            post_who_match_data_responseObj = json.loads(post_who_match_data_response.content)

                            data_dist["engagement"] = post_who_match_data_responseObj
                            fiter_data.append(data_dist)
                            
                        
                        
            # data[item['name']] = page_token_responseObj

        # print(data)  
        print(fiter_data)
        return fiter_data
        # return render(request,"taqa/facebook/page_list.html",{'page_list':page_list})
    else:
        print("out")
        return HttpResponse("first authorize your system")


def instagram_search(request,keyword):

    result = insta_data.objects.filter(caption__contains=keyword)

    fiter_data = []
    for item in result:
        data_dist = {}
        data_dist['ig_id'] = item.ig_id
        data_dist['caption'] = item.caption
        data_dist['username'] = item.username
        data_dist['name'] = item.name
        
        fiter_data.append(data_dist) 

    return fiter_data
    # if 'access_token_instagram' in request.session:
    
    #     accessToken = request.session["access_token_instagram"]

    #     page_token_url = "https://graph.facebook.com/v9.0/me/accounts?access_token="+accessToken
    #     page_token_response = requests.get(page_token_url)
    #     page_token_responseObj = json.loads(page_token_response.content)

    #     page_list = []

    #     for item in page_token_responseObj['data']:

    #         page_list.append(item)

    #     fiter_data = []
    #     for item in page_list:
    
    #         page_id = item['id']
    #         page_access_token = item['access_token']

    #         page_token_url = "https://graph.facebook.com/v9.0/"+page_id +"?fields=instagram_business_account&access_token="+accessToken
    #         page_token_response = requests.get(page_token_url)
    #         page_token_responseObj = json.loads(page_token_response.content)

    #         if "instagram_business_account" in page_token_responseObj:

    #             instagram_accounts_id = page_token_responseObj['instagram_business_account']["id"]

    #             instagram_account_data_url = "https://graph.facebook.com/v9.0/"+instagram_accounts_id+"/media?fields=ig_id,caption,like_count,media_type,media_url,comments_count,thumbnail_url,owner,comments,permalink&access_token="+accessToken
    #             instagram_account_data_response = requests.get(instagram_account_data_url)
    #             instagram_account_data_responseObj = json.loads(instagram_account_data_response.content)

    #             for item in instagram_account_data_responseObj['data']:
    #                 if 'caption' in  item:
    #                     data_dist = {}
    #                     if keyword in item['caption']:
    #                         user_id = item['owner']['id']

    #                         user_info_url = "https://graph.facebook.com/v9.0/"+user_id +"?fields=biography,name,username,profile_picture_url&access_token="+accessToken
    #                         user_info_response = requests.get(user_info_url)
    #                         user_info_responseObj = json.loads(user_info_response.content)

    #                         data_dist['user_data'] = user_info_responseObj
    #                         data_dist['media'] = item
    #                         fiter_data.append(data_dist)

    #             # print(instagram_account_data_responseObj)
    #         else:
    #             print(page_id)
    #             print("no dat is there ")

    #     return fiter_data
    #     # return HttpResponse("done done ")  
    # else:
    #     return HttpResponse("first authorize your system")

