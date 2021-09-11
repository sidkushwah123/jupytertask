import nltk
nltk.download('punkt')
import numpy as np
import pandas as pd
import codecs
from nltk.corpus import stopwords
import string
from datetime import datetime
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import   RegexpTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
# --------------------------------------- #
import pyarabic.araby as araby
import pyarabic.number as number
from pyarabic.araby import strip_tashkeel
from pyarabic.araby import strip_tatweel
from pyarabic.araby import tokenize, is_arabicrange, strip_tashkeel
# --------------------------------------- #
import pyarabic.arabrepr
arepr = pyarabic.arabrepr.ArabicRepr()
repr = arepr.repr
from tashaphyne.stemming import ArabicLightStemmer
import emoji
import seaborn
import matplotlib.pyplot as plt
#special import
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pickle
import re 
# normal import
from django.shortcuts import get_object_or_404
from .models import Alldata_tweet,FILTER_tweet_DATA,FINAL_TWEET_DATA

def get_sentiment_arabic(get_data): 
                datadf = []
                for item in get_data:
                    new_data = []
                    new_data.append(item.tweet.id)
                    new_data.append(item.Tweet_text) 
                    datadf.append(new_data)

                df = pd.DataFrame(datadf,columns=['object_id','text'])
                newdata = df.reset_index()
                newdata["id"] = newdata.object_id 
                newdata.columns= newdata.columns.str.lower()
                new = newdata[['text','id']] 

                arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
                english_punctuations = string.punctuation
                punctuations_list = arabic_punctuations + english_punctuations
                arabic_diacritics = re.compile("""
                                            ّ    | # Tashdid
                                            َ    | # Fatha
                                            ً    | # Tanwin Fath
                                            ُ    | # Damma
                                            ٌ    | # Tanwin Damm
                                            ِ    | # Kasra
                                            ٍ    | # Tanwin Kasr
                                            ْ    | # Sukun
                                            ـ     # Tatwil/Kashida
                                        """, re.VERBOSE)

                def normalize_arabic(text):
                    text = re.sub("[إأآا]", "ا", text)
                    text = re.sub("ى", "ي", text)
                    text = re.sub("ؤ", "ء", text)
                    text = re.sub("ئ", "ء", text)
                    text = re.sub("ة", "ه", text)
                    text = re.sub("گ", "ك", text)
                    return text

                def remove_diacritics(text):
                    text = re.sub(arabic_diacritics, '', text)
                    return text

                def remove_punctuations(text):
                    translator = str.maketrans('', '', punctuations_list)
                    return text.translate(translator)

                def remove_repeating_char(text):
                    return re.sub(r'(.)\1+', r'\1', text)

                def remove_hashtag(text):
                    return text.replace("#\\p{IsAlphabetic}+", "");

                def processPost(tweet):
                    #Replace @username with empty string
                    tweet = re.sub('@[^\s]+', ' ', tweet)
                    #Replace RT with empty string
                    tweet = re.sub('RT', ' ', tweet)
                    #Convert www.* or https?://* to " "
                    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))',' ',tweet)
                    #Replace #word with word
                    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
                    return tweet

                new['text'].replace('[^ء-ي0-9]', ' ', regex=True, inplace=True)
                new['text'].replace('_', ' ', regex=True, inplace=True)
                new['text'] = new['text'].str.replace(r'\d+','')
                new['text']= new['text'].apply(lambda x: remove_diacritics(x))
                new['text']= new['text'].apply(lambda x: remove_repeating_char(x))
                new['text']= new['text'].apply(lambda x: processPost(x))
                new['text']= new['text'].apply(lambda x: remove_hashtag(x))
                new['text']= new['text'].apply(lambda x: remove_punctuations(x))
                new['text']= new['text'].apply(lambda x: remove_repeating_char(x))

                tokens = TweetTokenizer()
                new['text'] = new['text'].apply(tokens.tokenize)

                stop = ['إذ', 'إذا', 'إذما', 'إذن', 'أف', 'أقل', 'أكثر', 'ألا', 'إلا', 'التي', 'الذي', 'الذين', 'اللاتي', 'اللائي', 'اللتان', 'اللتيا', 'اللتين', 'اللذان', 'اللذين', 'اللواتي', 'إلى', 'إليك', 'إليكم', 'إليكما', 'إليكن', 'أم', 'أما', 'أما', 'إما', 'أن', 'إن', 'إنا', 'أنا', 'أنت', 'أنتم', 'أنتما', 'أنتن', 'إنما', 'إنه', 'أنى', 'أنى', 'آه', 'آها', 'أو', 'أولاء', 'أولئك', 'أوه', 'آي', 'أي', 'أيها', 'إي', 'أين', 'أين', 'أينما', 'إيه', 'بخ', 'بس', 'بعد', 'بعض', 'بك', 'بكم', 'بكم', 'بكما', 'بكن', 'بل', 'بلى', 'بما', 'بماذا', 'بمن', 'بنا', 'به', 'بها', 'بهم', 'بهما', 'بهن', 'بي', 'بين','و', 'بيد',
                    'تلك', 'تلكم', 'تلكما', 'ته', 'تي', 'تين', 'تينك',
                    'ثم', 'ثمة', 'حاشا', 'حبذا', 'حتى', 'حيث', 'حيثما',
                    'حين', 'خلا', 'دون', 'ذا', 'ذات', 'ذاك', 'ذان', 'ذانك', 'ذلك',
                    'ذلكم', 'ذلكما', 'ذلكن', 'ذه', 'ذو', 'ذوا', 'ذواتا',
                    'ذواتي', 'ذي', 'ذين', 'ذينك', 'ريث', 'سوف', 'سوى', 'شتان', 'عدا',
                    'عسى', 'عل', 'على', 'عليك', 'عليه', 'عما', 'عن', 'عند', 'غير',
                    'فإذا', 'فإن', 'فلا', 'فمن', 'في', 'فيم', 'فيما', 'فيه', 'فيها',
                    'قد', 'كأن', 'كأنما', 'كأي', 'كأين', 'كذا', 'كذلك', 'كل', 'كلا',
                    'كلاهما', 'كلتا', 'كلما', 'كليكما', 'كليهما', 'كم', 'كم', 'كما',
                    'كي', 'كيت', 'كيف', 'كيفما', 'لا', 'لاسيما', 'لدى', 'لست', 'لستم',
                    'لستما', 'لستن', 'لسن', 'لسنا', 'لعل', 'لك', 'لكم', 'لكما',
                    'لكن', 'لكنما', 'لكي', 'لكيلا', 'لم', 'لما', 'لن', 'لنا',
                    'له', 'لها', 'لهم', 'لهما', 'لهن', 'لو', 'لولا', 'لوما',
                    'لي', 'لئن', 'ليت', 'ليس', 'ليسا', 'ليست', 'ليستا', 'ليسوا', 'ما',
                    'ماذا', 'متى', 'مذ', 'مع', 'مما', 'ممن', 'من', 'منه', 'منها', 'منذ',
                    'مه', 'مهما', 'نحن', 'نحو', 'نعم', 'ها', 'هاتان', 'هاته', 'هاتي',
                    'هاتين', 'هاك', 'هاهنا', 'هذا', 'هذان', 'هذه', 'هذي', 'هذين', 'هكذا',
                    'هل', 'هلا', 'هم', 'هما', 'هن', 'هنا', 'هناك', 'هنالك', 'هو', 'هؤلاء',
                    'هي', 'هيا', 'هيت', 'هيهات', 'والذي', 'والذين', 'وإذ', 'وإذا', 'وإن',
                    'ولا', 'ولكن', 'ولو', 'وما', 'ومن', 'وهو', 'يا' , 'من' , 'على', 'الى','هما', 'مع', 'هذه', 'التي', 'كما ', 'ذلك ', 'لذا', 'عن', 'في','ان','كان','كانت','الى','قبل','أنه','تم'
                    ,'وقال','قال','فى','وقد','قد','ولم','وذلك','ذلك','يكون','او','وهذه','وهي ','وبعد','وهذا','عندها','جدا','بأن','انه','الي']

                new['text'] = [w for w in new['text'] if not w in stop]
                y = new['text'].apply(lambda x: ' '.join(x))
                vectorizer = CountVectorizer(max_features=250, min_df=5, max_df=0.7, stop_words=stop)
                X = vectorizer.fit_transform(y).toarray()

                tfidfconverter = TfidfTransformer()
                X = tfidfconverter.fit_transform(X).toarray()
                # acc = 77 or 79
                with open('RFModel250', 'rb') as training_model:
                    taqa = pickle.load(training_model)
                new['predictions'] = taqa.predict(X)

                Ad = ["دعايه","لداعياتكم","الفكره", "الوقت" , "الاعلان", "اعلانكم","فكره","اعلان", "التوقيت","الاخراج","التصوير", "وقت"]

                religon = ["يوفقك","رسول","حرام","حلال","موسيقى" ,"اغاني", "أغاني", "بنات","متبرجة","متبرجه","كاشفة", "كاشفه","مايجوز","استغفرالله"]

                Others = []

                Actor = ["تمثيل","ممثل","التمثيل","تمثيله","شخصيات", "الاداء", "اداء", "شخصيه", "يمثل","الممثل", "المثل", ""] 

                def setcategory(tweet):
                    label="Others"
                    for word in Ad:
                        if word in tweet:
                            label="Ad"     
                        for word in religon:
                            if word in tweet:
                                label="religon"          
                            for word in Actor:
                                if word in tweet:
                                    label="Actor"                          
                    return label
                new["category"] = new['text'].apply(lambda x: setcategory(x))
                for item in new.index: 
                    status = 0
                    try:

                        object_id = new['id'][item]

                        raw = get_object_or_404(Alldata_tweet, id=object_id)

                        all_data = FINAL_TWEET_DATA(keyword_search=raw.keyword_search,Search_date=raw.Search_date
                        ,tweet_created=raw.tweet_created,tweet_id=raw.tweet_id,tweet_id_str=raw.tweet_id_str
                        ,User_name=raw.User_name,Screen_name=raw.Screen_name,user_location=raw.user_location
                        ,verified=raw.verified,source=raw.source,followers=raw.followers,
                        Tweet_text=raw.Tweet_text,in_reply_to_screen_name=raw.in_reply_to_screen_name,in_reply_to_user_id_str=raw.in_reply_to_user_id_str,
                        reply_count=raw.reply_count,retweet_count=raw.retweet_count,favorite_count=raw.favorite_count,lang=raw.lang,favorited=raw.favorited,
                        retweeted=raw.retweeted,sentiment=new['predictions'][item],category=new['category'][item])

                        all_data.save()

                        status = 1
                    except:
                        get_data = FILTER_tweet_DATA.objects.filter(status=False) 
                        for item in get_data:
                            FILTER_tweet_DATA.objects.filter(id=item.id).update(status=True)
                            Alldata_tweet.objects.filter(id=item.tweet.id).update(status=True)
                        status = 0
                        
                return status


    
