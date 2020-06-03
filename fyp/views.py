import random
import math
import re
import string
import csv
from fyp import categorization_analysis
from joblib.numpy_pickle_utils import xrange

from fyp import models

# from xxlimited import Null
# import amp as amp
from django.db.models import Count
import tweepy
from django.core.serializers import serialize, deserialize, json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from nltk import TweetTokenizer
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

stemmer = PorterStemmer()
words = stopwords.words("english")
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction import DictVectorizer
from fyp.forms import MessageForm, LoginForm, AddRoleForm, AddUsers, APIForm, SystemSettingForm
from fyp.models import tbl_messages, tbl_user_role, \
    tbl_users, tbl_crime_categories, tbl_reply_msg, \
    tbl_headquarter, tbl_designation, tbl_api_setting, tbl_system_setting, raw_tweets, tbl_tweeter_users, \
    tbl_train_dataset, \
    tbl_tweets, tbl_analysis, tbl_raw_analysis
from django.db import connection
import os
import numpy as np
import tweepy as tw
import pandas as pd
from django.core.files.storage import FileSystemStorage

import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
from textblob import TextBlob
from wordcloud import WordCloud

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.datasets import fetch_20newsgroups

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline


# from sklearn.ensemble import AdaBoostClassifier
# from sklearn.svm import SVC
# import numpy as np
# import graphviz
# from sklearn import preprocessing
# from sklearn.externals import joblib
# from threading import Thread


# from sklearn import datasets
# from sklearn import metrics
# from sklearn.naive_bayes import GaussianNB

# &amp;amp;
# Create your views here.


def index(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        sys_setting_form = SystemSettingForm()
        if form.is_valid():
            try:
                m = tbl_users.objects.get(email=request.POST['email'])
                s = tbl_system_setting.objects.get(system_setting_id=1)
                if m.password == request.POST['password']:
                    request.session['uid'] = m.uid
                    request.session['first_name'] = m.first_name
                    request.session['last_name'] = m.last_name
                    request.session['email'] = m.email
                    request.session['phone_no'] = m.phone_no
                    # request.session['photo'] = m.photo
                    request.session['role_id'] = m.role_id
                    request.session['HQ_id'] = m.HQ_id
                    request.session['designation_id'] = m.designation_id
                    request.session['system_name'] = s.system_name
                    # request.session['system_logo'] = json.Serializer.serialize(s.system_logo, s)
                    request.session['system_lang'] = s.system_lang
                    return redirect(dashboard)
                else:
                    login_error = "Login Credentials are not correct"
                    return render(request, "login/login.html", {'form': form, 'login_error': login_error})
            except tbl_users.DoesNotExist as e:
                pass
                print(type(e))
    else:
        form = LoginForm()
    if 'first_name' in request.session:
        return redirect(dashboard)
    else:
        return render(request, "login/login.html", {'form': form})


def logout(request):
    try:
        del request.session['first_name']
        del request.session['last_name']
        del request.session['email']
        del request.session['phone_no']
        del request.session['photo']
        del request.session['role_id']
        del request.session['HQ_id']
        del request.session['designation_id']
        return redirect(index)
    except Exception as e:
        print(type(e))
        return redirect(dashboard)


def dashboard(request):
    if 'first_name' in request.session:
        total_users = tbl_users.objects.all().count()
        total_cat = tbl_crime_categories.objects.all().count()
        total_msg = tbl_messages.objects.all().count()
        total_reply = tbl_reply_msg.objects.all().count()
        total_neg = tbl_analysis.objects.filter(analysis_status='Negative').count()
        total_pos = tbl_analysis.objects.filter(analysis_status='Positive').count()
        sentiment_wise = tbl_analysis.objects.values('analysis_status').annotate(scount=Count('analysis_status'))
        return render(request, "dashboard/index.html", {
            'total_users': total_users,
            'total_cat': total_cat,
            'total_msg': total_msg,
            'total_reply': total_reply,
            'total_pos': total_pos,
            'total_neg': total_neg,
            'sentiment_analysis': sentiment_wise
        })
    else:
        return redirect(index)


def conversation(request):
    cursor = connection.cursor()
    cursor.execute(
        "select tbl_messages.*, tbl_messages.created_at as 'msg_send_date', tbl_users.* from tbl_messages left join tbl_users on tbl_messages.uid = tbl_users.uid")
    # print(cursor)
    roles = cursor.fetchall()
    x = cursor.description
    resultList = []
    for r in roles:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i + 1
        resultList.append(d)
    # users = tbl_users.objects.all()
    return render(request, "communication/index.html", {'mails': resultList})


def creat_mail(request):
    cursor = connection.cursor()
    cursor.execute(
        "select * from tbl_users where uid not in (" + str(request.session['uid']) + ")")
    # print(cursor)
    roles = cursor.fetchall()
    x = cursor.description
    resultList = []
    for r in roles:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i + 1
        resultList.append(d)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            print("Valid")
            try:
                print("everything Okay")
                obj = form.save(commit=False)
                obj.created_by = request.session['uid']
                obj.sender_id = request.session['uid']
                obj.modified_by = request.session['uid']
                obj.uid = request.POST.get('uid')
                obj.created_at = timezone.now()
                obj.modified_at = timezone.now()
                form.save()
                return redirect(conversation)
            except Exception as e:
                print(type(e))
                pass
        else:
            print(form.errors)
    else:
        form = MessageForm()
    return render(request, "communication/create_new.html", {'form': form,
                                                             'users': resultList})


def drafts(request):
    return render(request, "communication/drafts.html")


def sent(request):
    return render(request, "communication/sent.html")


def trash(request):
    return render(request, "communication/trash.html")


def user_roles(request):
    cursor = connection.cursor()
    cursor.execute(
        "select tbl_user_role.role_id as 'user_role_id', tbl_user_role.role,  tbl_users.* from tbl_user_role "
        "left join tbl_users on tbl_user_role.created_by=tbl_users.uid")
    # print(cursor)
    roles = cursor.fetchall()
    x = cursor.description
    resultList = []
    for r in roles:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i + 1
        resultList.append(d)
    # print(resultList)
    return render(request, "user_roles/index.html", {'roles': resultList})


def add_role(request):
    if request.method == "POST":
        form = AddRoleForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            try:
                print("everything Okay")
                obj = form.save(commit=False)
                obj.created_by = request.session['uid']
                obj.modified_by = request.session['uid']
                form.save()
                return redirect(user_roles)
            except Exception as e:
                print(type(e))
                pass
        else:
            print("Form is not Valid")
    else:
        form = AddRoleForm()
    return render(request, "user_roles/add.html", {'form': form})


def delete_role(request, id):
    role = tbl_user_role.objects.get(role_id=id)
    role.delete()
    return redirect(user_roles)


def edit_role(request, id):
    # instance = get_object_or_404(tbl_user_role, role_id=id)
    role = tbl_user_role.objects.get(role_id=id)
    # if request.method == 'POST':
    #     form = AddRoleForm(request.POST, instance=instance)
    #     if form.is_valid():
    #         print('okay')
    #         try:
    #             print('no exception')
    #             obj = form.save(commit=False)
    #             obj.modified_by = request.session['uid']
    #             obj.modified_at = timezone.now()
    #             form.save()
    #             return redirect(user_roles)
    #         except Exception as e:
    #             print(type(e))
    #     else:
    #         print("Form is not valid")
    # else:
    #     role = tbl_user_role.objects.get(role_id=id)
    return render(request, "user_roles/edit.html", {'role': role})


def update_role(request, id):
    if request.method == "POST":
        form = AddRoleForm(request.POST)
        if form.is_valid():
            try:
                # result = tbl_user_role.objects.update(roles=)
                cursor = connection.cursor()
                result = cursor.execute(
                    "insert into tbl_user_role set role=" + request.POST.get('role') + " role_id=" + str(id))
                print(result.query())
                if result == True:
                    return redirect(user_roles)
                else:
                    print("Not Updated")
            except Exception as e:
                print(type(e))


def users(request):
    print("okay")
    uid = request.session['uid']
    cursor = connection.cursor()
    cursor.execute("select * from tbl_users "
                   "left join tbl_designation on tbl_users.designation_id=tbl_designation.designation_id "
                   "left join tbl_user_role on tbl_users.role_id=tbl_user_role.role_id "
                   "left join tbl_headquarter on tbl_users.HQ_id=tbl_headquarter.HQ_id "
                   "where uid!=" + str(uid))
    users_details = cursor.fetchall()
    x = cursor.description
    resultsList = []
    for r in users_details:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i + 1
        resultsList.append(d)
    return render(request, "users/index.html", {'users': resultsList})


def delete_user(request, id):
    users_details = tbl_users.objects.get(uid=id)
    if users_details.delete():
        return redirect(users_details)
    else:
        msg = "Cannot deleted"
        return redirect(users({'delete_error': msg}))


def view_user(request, id):
    return render(request, "users/view.html")


def edit_user(request, id):
    return render(request, "users/edit.html")


def add_user(request):
    global list_hq, list_roles, list_designation
    if request.method == "POST":
        # profil_photo = request.FILES['photo']
        # fs = FileSystemStorage()
        form = AddUsers(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            try:
                print("everything Okay")
                # print(request.POST.get('photo'))
                obj = form.save(commit=False)
                obj.created_by = request.session['uid']
                obj.modified_by = request.session['uid']
                obj.photo = request.POST.get('photo')
                # print(obj.photo)
                form.save()
                # messages.success(request, 'You uploaded it')
                return redirect(users)
            except Exception as e:
                print(type(e))
                pass
        else:
            print("Form is not Valid")
            print(form.errors)
    else:
        form = AddUsers()
        list_hq = tbl_headquarter.objects.all()
        list_designation = tbl_designation.objects.all()
        list_roles = tbl_user_role.objects.all()
    return render(request, "users/add.html", {'form': form,
                                              'list_hq': list_hq,
                                              'list_roles': list_roles,
                                              'list_designation': list_designation})


def list_of_headquarters(request):
    list_of_hq = tbl_headquarter.objects.all()
    return list_of_hq


def list_of_user_roles(request):
    list_of_roles = tbl_user_role.objects.all()
    return list_of_roles


def list_of_designation(request):
    list_of_designations = tbl_designation.objects.all()
    return list_of_designations


def api_settings(request):
    cursor = connection.cursor()
    cursor.execute("select * from tbl_api_setting")
    api_setting = cursor.fetchall()
    x = cursor.description
    resultsList = []
    for r in api_setting:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i + 1
        resultsList.append(d)
    # api_setting = tbl_api_setting.objects.all()
    return render(request, "apiSettings/index.html", {'setting': resultsList})


def add_api(request):
    if request.method == 'POST':
        form = APIForm(request.POST)
        if form.is_valid():
            try:
                api_setting = tbl_api_setting.objects.all()
                for api in api_setting:
                    if request.POST.get('api_key') == api.api_key:
                        msg = 'API setting already exits'
                        return render(request, "apiSettings/add.html", {'form': form,
                                                                        'msg': msg})
                obj = form.save(commit=False)
                obj.created_by = request.session['uid']
                obj.modified_by = request.session['uid']
                form.save()
                return redirect(api_settings)
            except Exception as e:
                print(type(e))
        else:
            print("form is not valid")
    else:
        form = APIForm()
    return render(request, "apiSettings/add.html", {'form': form})


def delete_api(request, id):
    api_setting = tbl_api_setting.objects.get(api_id=id)
    if api_setting.delete():
        return redirect(api_settings)
    else:
        msg = "Cannot deleted"
        return redirect(api_settings({'delete_error': msg}))


def edit_api(request, id):
    instance = get_object_or_404(tbl_api_setting, api_id=id)
    api_setting = tbl_api_setting.objects.get(api_id=id)
    if request.method == 'POST':
        form = APIForm(request.POST, instance=instance)
        if form.is_valid():
            print('okay')
            try:
                print('no exception')
                # api_setting.objects.get(api_id=id).save()
                obj = form.save(commit=False)
                obj.modified_by = request.session['uid']
                obj.modified_at = timezone.now()
                # obj.setting_status = 'default'
                form.save()
                return redirect(api_settings)
            except Exception as e:
                print(type(e))
        else:
            print("Form is not valid")
    else:
        form = APIForm(instance=instance)
    return render(request, "apiSettings/edit.html", {'setting': api_setting})


def system_setting(request):
    sys_setting = tbl_system_setting.objects.get(system_setting_id=1)
    return render(request, "systemSettings/index.html", {'setting': sys_setting})


def system_setting_edit(request, id):
    instance = get_object_or_404(tbl_system_setting, system_setting_id=id)
    setting = tbl_system_setting.objects.get(system_setting_id=id)
    form = SystemSettingForm(request, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.modified_by = request.session['uid']
                obj.modified_at = timezone.now()
                form.save()
                return redirect(system_setting)
            except Exception as e:
                print(type(e))
        else:
            print("form is not valid")
    else:
        form = SystemSettingForm(instance=instance)
    return render(request, "systemSettings/edit.html", {'form': form,
                                                        'setting': setting})


# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
])

# all emoticons (happy + sad)
emoticons = emoticons_happy.union(emoticons_sad)

stopwords_english = stopwords.words('english')
stemmer = PorterStemmer()


def clean_tweets(tweet):

    tweet = re.sub(r'\$\w*', '', tweet)

    tweet = re.sub(r'^RT[\s]+', '', tweet)

    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)

    tweet = re.sub(r'#', '', tweet)

    # tokenize tweets
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)

    tweets_clean = []
    for word in tweet_tokens:
        if (word not in stopwords_english and  # remove stopwords
                word not in emoticons and  # remove emoticons
                word not in string.punctuation):  # remove punctuation
            # tweets_clean.append(word)
            stem_word = stemmer.stem(word)  # stemming word
            tweets_clean.append(stem_word)
    return tweets_clean


def remove_single_quotation(tweet_text):
    tweet = re.sub("'", ',', tweet_text)
    return tweet


def description_cleaning(description_text):
    # remove stock market tickers like $GE
    description_text = re.sub(r'\$\w*', '', description_text)

    # remove old style retweet text "RT"
    description_text = re.sub(r'^RT[\s]+', '', description_text)

    # remove hyperlinks
    description_text = re.sub(r'https?:\/\/.*[\r\n]*', '', description_text)

    # remove hashtags
    # only removing the hash # sign from the word
    description_text = re.sub(r'#', '', description_text)

    description_text = re.sub("'", ',', description_text)

    return description_text


def split_into_lemmas(tweet):
    bigram_vectorizer = CountVectorizer(ngram_range=(1, 3), stop_words='english', strip_accents='ascii',
                                        token_pattern=r'\b\w+\b', min_df=2)

    analyze = bigram_vectorizer.build_analyzer()

    return analyze(tweet)


# Create a function to clean the tweets
def cleanTxt(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
    text = re.sub('#', '', text)  # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text)  # Removing RT
    text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink
    # text = re.sub(emoticon, '', text)
    return text


def tweets_gathering(request):
    # obj = TwitterAnalysis()
    # obj
    api_setting = tbl_api_setting.objects.get(setting_status='default')
    consumer_key = api_setting.api_key
    consumer_secret = api_setting.api_key_secret
    access_token = api_setting.access_token
    access_token_secret = api_setting.access_token_secret

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    search_words = "killing OR murder OR rape OR abuse OR harass OR assault OR harassment OR abusing OR rapping"
    date_since = "2019-11-16"

    new_search = search_words + " -filter:retweets"
    tweets = tw.Cursor(api.search,
                       q=new_search,
                       lang="ur",
                       since=date_since).items(500)

    cursor = connection.cursor()

    for tweet in tweets:
        print(tweet)
        username = str(tweet.user.screen_name)
        name = str(tweet.user.name)
        location = str(tweet.user.location)
        profile_url = str("https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str)
        protected = str(tweet.user.protected)
        description = description_cleaning(tweet.user.description)
        is_verified = str(tweet.user.verified)
        follower_count = str(tweet.user.followers_count)
        friends_count = str(tweet.user.friends_count)
        list_count = str(tweet.user.listed_count)
        favourites_count = str(tweet.user.favourites_count)
        statuses_count = str(tweet.user.statuses_count)
        profile_created_at = str(tweet.user.created_at)
        profile_image_url_https = str(tweet.user.profile_image_url_https)
        default_profile = str(tweet.user.default_profile_image)
        default_profile_image = str(tweet.user.default_profile_image)
        tweet = cleanTxt(tweet.text)
        tweet_posted_date = ''
        language_code = ''
        source = ''
        search_type = ''
        sql = 'INSERT INTO `tbl_raw_tweets`(`username`, `name`, `location`, `profile_url`, `protected`, `description`, ' \
              '`is_verified`, `follower_count`, `friends_count`, `listed_count`, `favourites_count`, `statuses_count`, ' \
              '`profile_created_at`, `profile_image_url_https`, `default_profile`, ' \
              '`default_profile_image`, `tweet_text`, `tweet_posted_date`, `lang_code`, `tweet_source`, ' \
              '`search_type`) ' \
              'values("' + username + '", "' + name + '", "' + location + '", "' + profile_url + '", "' + protected + '", "' + description \
              + '", "' + is_verified + '", "' + follower_count + '", "' + friends_count + '", "' + list_count + '", "' + \
              favourites_count + '", "' + statuses_count + '", "' + profile_created_at + '", "' + profile_image_url_https \
              + '", "' + default_profile + '", "' + default_profile_image + '", "' + tweet + '", "' + tweet_posted_date \
              + '", "' + language_code + '", "' + source + '", "' + search_type + '")'
        # print(sql)

        try:
            result = cursor.execute(sql)
        except Exception as e:
            print(str(e))

    sql2 = 'INSERT INTO `tbl_tweeter_users`( `name`, `username`, `location`, `profile_url`, `protection_status`, ' \
           '`description`, `verification`, `followers_count`, `friends_count`, `listed_count`, `favourites_count`,' \
           ' `statuses_count`, `profile_created_on`, `profile_banner_url`, `profile_image_url_https`, ' \
           '`default_profile`, `default_profile_image`) ' \
           ' SELECT a.`name`, a.`username`, a.`location`, a.`profile_url`, a.`protected`, a.`description`, a.`is_verified`, ' \
           'a.`follower_count`, a.`friends_count`, a.`listed_count`, a.`favourites_count`, a.`statuses_count`, ' \
           'a.`profile_created_at`, a.`profile_banner_url`, a.`profile_image_url_https`, ' \
           'a.`default_profile`, a.`default_profile_image` ' \
           'from `tbl_raw_tweets` a ' \
           'left join `tbl_tweeter_users` on a.username = tbl_tweeter_users.username ' \
           'group by a.`username`'
    sql3 = 'INSERT INTO `tbl_tweets`(`user_id`, `tweets`, `tweet_posted_date`, `lang_code`, `search_type`) ' \
           'SELECT b.user_id, a.`tweet_text`, a.`tweet_posted_date`, a.`lang_code`, `search_type`  ' \
           'FROM `tbl_raw_tweets` a ' \
           'JOIN tbl_tweeter_users b on a.username = b.username' \
           ' GROUP BY a.`raw_tweet_id`'
    try:
        result = cursor.execute(sql2)
        result = cursor.execute(sql3)
        return redirect(dashboard)
    except Exception as e:
        print(str(e))
        return redirect(dashboard)


def twitter_users(request):
    cursor = connection.cursor()
    cursor.execute("select * from tbl_tweeter_users")
    twitter_users = cursor.fetchall()
    x = cursor.description
    resultsList = []
    for r in twitter_users:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i + 1
        resultsList.append(d)
    # api_setting = tbl_api_setting.objects.all()
    return render(request, "twitter_users/index.html", {'twitter_users': resultsList})


# Create a function to get the subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


# Create a function to get the polarity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity


def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


def preprocess(TWEETS):
    wordlist = []
    tokenizer = RegexpTokenizer(r'#?\w+')
    # normalize text -- TOKENIZE USING REGEX TOKENIZER
    cnt = 0
    for item in TWEETS:
        text = TWEETS[cnt]
        tweet = ''.join(text)
        tweet = tweet.lower().strip('\n')

        tweet = re.sub(r'[0-9]+', "", tweet)
        tweet = re.sub(r'@[^\s]+', "", tweet)
        tweet = re.sub(r'#\w+primary', "", tweet)
        wordlist.extend(tokenizer.tokenize(tweet))
        cnt += 1

    # remove stopwords
    stop = stopwords.words('english') + ['rt', 'via', 'u', 'r', 'b', '2', 'http',
                                         'https', 'co', 'live', 'hall', 'town', 'watch',
                                         'tune', 'time', 'tonight', 'today', 'campaign',
                                         'debate', 'wants', 'without', 'dont',
                                         '#hillaryclinton', '#berniesanders', '#donaldtrump',
                                         '#tedcruz', "#johnkasich", '#politics']
    filtered = [term for term in wordlist if term not in stop]
    filtered_final = [term for term in filtered if len(term) > 3]
    return filtered_final


def get_public_tweets(MAX, queryStr):
    data = tweepy.Cursor(tweepy.api.search, q=queryStr, lang='en').items(MAX)
    # save tweets: text, location
    tweets = []
    for tweet in data:
        decoded = json.loads(json.dumps(tweet._json))
        tweets.append(decoded['text'].encode('ascii', 'ignore'))
    return tweets


def top_words(TWEETS, num):
    words = [word for word in TWEETS if not word.startswith('#')]
    top_words = Counter(words).most_common(num)
    # for word, n in top_words:
    #    print("%s : %d" %(word, n))
    return top_words


def top_hashtags(TWEETS, num):
    hastags = [word for word in TWEETS if word.startswith('#')]
    top_hashtags = Counter(hastags).most_common(num)
    # for word,n in top_hashtags:
    #     print("%s : %d" %(word, n))
    return top_hashtags


def view_profile(request):
    # resultsList = tbl_tweeter_users.objects.get(user_id=id)
    # cursor = connection.cursor()
    # cursor.execute("select * from tbl_tweeter_users where user_id =" + str(id))
    # twitter_users = cursor.fetchall()
    # x = cursor.description
    # resultsList = []
    # for r in twitter_users:
    #     i = 0
    #     d = {}
    #     while i < len(x):
    #         d[x[i][0]] = r[i]
    #         i = i + 1
    #     resultsList.append(d)
    return render(request, 'twitter_users/view2.html')


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
        print(input_txt)
    return input_txt


def analysis(request):
    all_analysis = tbl_analysis.objects.all()
    return render(request, "analysis/index.html", {"all_analysis": all_analysis})


# def analysis(request):
#     train_set_dic = {}
#     test_set_dic = {}
#     train_set = pd.read_csv('C:/Users/apex/PycharmProjects/tca/fyp/train_data.csv')
#     test_set = pd.read_csv('C:/Users/apex/PycharmProjects/tca/fyp/test_data.csv')
#
#     # for train_data in train_set:
#     #     train_set_dic = {
#     #         'labels': train_data.label,
#     #         'tweet': train_data.text
#     #     }
#     # for test_data in test_set:
#     #     test_set_dic = {
#     #         'user_id': test_data.user_id,
#     #         'tweet': str(test_data.tweets)
#     #     }
#
#     # combi = train_set_dic.update(test_set_dic)
#     # combi = np.array(combi)
#     combi = train_set.append(test_set, ignore_index=True)
#     # remove twitter handles (@user)
#     combi['tidy_tweet'] = np.vectorize(remove_pattern)(combi['tweet'], "@[\w]*")
#     # remove special characters, numbers, punctuations
#     combi['tidy_tweet'] = combi['tidy_tweet'].str.replace("[^a-zA-Z#]", " ")
#     # removing short words
#     combi['tidy_tweet'] = combi['tidy_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w) > 3]))
#
#     # tokenizing
#     tokenized_tweet = combi['tidy_tweet'].apply(lambda x: x.split())
#     stemmer = PorterStemmer()
#     tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x])  # stemming
#     for i in range(len(tokenized_tweet)):
#         tokenized_tweet[i] = ' '.join(tokenized_tweet[i])
#     combi['tidy_tweet'] = tokenized_tweet
#     all_words = ' '.join([text for text in combi['tidy_tweet']])
#     wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)
#     plt.figure(figsize=(10, 7))
#     plt.imshow(wordcloud, interpolation="bilinear")
#     plt.axis('off')
#     plt.show()
#
#     normal_words = ' '.join([text for text in combi['tidy_tweet'][combi['label'] == 0]])
#
#     wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(normal_words)
#     plt.figure(figsize=(10, 7))
#     plt.imshow(wordcloud, interpolation="bilinear")
#     plt.axis('off')
#     plt.show()
#     return render(request, "twitter_users/view.html")


def analysis_view(request):
    cursor = connection.cursor()
    # tweets_data = tbl_tweets.objects.all()
    cursor.execute("SELECT a.tweets_id, a.tweets, b.profile_url, b.username FROM tbl_tweets a LEFT join tbl_tweeter_users b on a.user_id = b.user_id LEFT JOIN tbl_raw_analysis c on a.tweets_id = c.tweet_id WHERE c.analysis_id is null GROUP by a.tweets_id")
    twitter_users = cursor.fetchall()
    x = cursor.description
    tweets_data = []
    for r in twitter_users:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i + 1
        tweets_data.append(d)
    # print(tweets_data)
    try:
        for tweet in tweets_data:
            analysis_status = getAnalysis(getPolarity(cleanTxt(tweet['tweets'])))
            polarity = str(getPolarity(cleanTxt(tweet['tweets'])))
            subjectivity = str(getSubjectivity(cleanTxt(tweet['tweets'])))
            tweet_link = tweet['profile_url']
            tweet_text = cleanTxt(tweet['tweets'])
            username = tweet['username']
            profile_url = str("https://twitter.com/" + str(tweet['username']))
            tweet_id = str(tweet['tweets_id'])
            sql = 'INSERT INTO `tbl_raw_analysis`(`analysis_status`, `polarity`, `subjectivity`, `tweet_link`, `tweet_text`, `username`, `profile_url`, `tweet_id`) VALUES("' + \
                  analysis_status + '",' + polarity + ',' + subjectivity + ',"' + tweet_link + '","' + tweet_text + '","' + username + '","' + profile_url + '","' + tweet_id + '"' \
                                                                                                                                                                                ')'
            sql2 = 'INSERT into tbl_analysis (`analysis_status`,`polarity`,`subjectivity`,`tweet_link`,`tweet_text`,`username`,`profile_url`, `tweet_id`)' \
                   'SELECT a.`analysis_status`, a.`polarity`, a.`subjectivity`, a.`tweet_link`, a.`tweet_text`, a.`username`, a.`profile_url`, a.`tweet_id` FROM tbl_raw_analysis a ' \
                   'LEFT JOIN tbl_analysis b ON CONCAT(a.username, a.tweet_text) = CONCAT(b.username, b.tweet_text)' \
                   'WHERE b.username is null Group by a.analysis_id'
            # print(sql)
            try:
                cursor.execute(sql)
                cursor.execute(sql2)
            except:
                all_analysis = tbl_analysis.objects.all()
                return render(request, "analysis/index.html", {"all_analysis": all_analysis})
        all_analysis = tbl_analysis.objects.all()
        return render(request, "analysis/index.html", {"all_analysis": all_analysis})
    except Exception as e:

        print('Error: ' + str(e))
        return redirect(index)


def categorization(request):
    cursor = connection.cursor()
    cursor.execute("SELECT label, text from tbl_train_dataset")
    train_data_set = cursor.fetchall()
    x = cursor.description
    train_set = []
    for r in train_data_set:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i + 1
        train_set.append(d)
    csv_columns_training = ['label', 'text']
    csv_file_training = "trained_data.csv"
    try:
        f = open("trained_data.csv", "w", newline='')
        writer = csv.DictWriter(
            f, fieldnames=["label", "text"])
        writer.writeheader()
        writer.writerows(train_set)
        f.close()
    except IOError:
        print("I/O error")
    cursor.execute("SELECT tweet_id, tweet_text as 'text' from tbl_analysis where analysis_status='Negative'")
    test_data_set = cursor.fetchall()
    x = cursor.description
    test_set = []
    for r in test_data_set:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i + 1
        test_set.append(d)
    csv_columns_testing = ['tweet_id', 'text']
    csv_file_testing = "testing_data.csv"
    try:
        with open(csv_file_testing, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns_testing)
            writer.writeheader()
            for data in test_set:
                writer.writerow(data)
    except IOError:
        print("I/O error")

    final_result = categorization_analysis.trained_data()
    print(final_result)
    return redirect(index)


def faked_account(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM `tbl_tweeter_users` WHERE `followers_count`=0 and friends_count<=20 and favourites_count<10 and description = ''")
    fake_users = cursor.fetchall()
    x = cursor.description
    resultsList = []
    for r in fake_users:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i + 1
        resultsList.append(d)
    # api_setting = tbl_api_setting.objects.all()
    return render(request, "facked_account/index.html", {'fake_users': resultsList})


def category_analysis(request):
    return render(request, "category_analysis/index.html")

# class TwitterAnalysis:
#     api_setting = tbl_api_setting.objects.get(setting_status='default')
#     consumer_key = api_setting.api_key
#     consumer_secret = api_setting.api_key_secret
#     access_token = api_setting.access_token
#     access_token_secret = api_setting.access_token_secret
#
#     auth = tw.OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#     api = tw.API(auth, wait_on_rate_limit=True)
#
#     # Extract 100 tweets from the twitter user
#     # tweets = api.user_timeline(screen_name="BillGates", count=1000, lang="en", tweet_mode="extended")
#
#     search_words = "killing OR murder OR rape OR kidnap OR harassing OR assault OR stealing"
#     date_since = "2019-11-16"
#
#     new_search = search_words + " -filter:retweets"
#     tweets = tw.Cursor(api.search,
#                        q=new_search,
#                        lang="en",
#                        result_type='recent',
#                        include_entities=True,
#                        monitor_rate_limit=True,
#                        wait_on_rate_limit=True,
#                        since=date_since).items(500)
#     result = False
#     cursor = connection.cursor()
#     #  Print the last 5 tweets
#     # print("Show the 5 recent tweets:\n")
#     # i = 1
#     # for tweet in tweets[:5]:
#     #     print(str(i) + ') ' + tweet.full_text + '\n')
#     #     i = i + 1
#
#     # Create a dataframe with a column called Tweets
#     df = pd.DataFrame([tweet.text for tweet in tweets], columns=['Tweets'])
#     # Show the first 5 rows of data
#     df.head()
#
#     # Create a function to clean the tweets
#     def cleanTxt(text):
#         text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
#         text = re.sub('#', '', text)  # Removing '#' hash tag
#         text = re.sub('RT[\s]+', '', text)  # Removing RT
#         text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink
#
#         return text
#
#     # Clean the tweets
#     df['Tweets'] = df['Tweets'].apply(cleanTxt)
#
#     # Show the cleaned tweets
#     df
#
#     # Create a function to get the subjectivity
#     def getSubjectivity(text):
#         return TextBlob(text).sentiment.subjectivity
#
#     # Create a function to get the polarity
#     def getPolarity(text):
#         return TextBlob(text).sentiment.polarity
#
#     # Create two new columns 'Subjectivity' & 'Polarity'
#     df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
#     df['Polarity'] = df['Tweets'].apply(getPolarity)
#
#     # Show the new dataframe with columns 'Subjectivity' & 'Polarity'
#     df
#
#     allWords = ' '.join([twts for twts in df['Tweets']])
#     wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
#
#     plt.imshow(wordCloud, interpolation="bilinear")
#     plt.axis('off')
#     plt.show()
#
#     # Create a function to compute negative (-1), neutral (0) and positive (+1) analysis
#     def getAnalysis(score):
#         if score < 0:
#             return 'Negative'
#         elif score == 0:
#             return 'Neutral'
#         else:
#             return 'Positive'
#
#     df['Analysis'] = df['Polarity'].apply(getAnalysis)
#
#     # Show the dataframe
#     df
#
#     # Printing positive tweets
#     print('Printing positive tweets:\n')
#     j = 1
#     sortedDF = df.sort_values(by=['Polarity'])  # Sort the tweets
#     for i in range(0, sortedDF.shape[0]):
#         if (sortedDF['Analysis'][i] == 'Positive'):
#             print(str(j) + ') ' + sortedDF['Tweets'][i])
#             print()
#             j = j + 1
#
#     # Printing negative tweets
#     print('Printing negative tweets:\n')
#     j = 1
#     sortedDF = df.sort_values(by=['Polarity'], ascending=False)  # Sort the tweets
#     for i in range(0, sortedDF.shape[0]):
#         if (sortedDF['Analysis'][i] == 'Negative'):
#             print(str(j) + ') ' + sortedDF['Tweets'][i])
#             print()
#             j = j + 1
#
#     # Plotting
#     plt.figure(figsize=(8, 6))
#     for i in range(0, df.shape[0]):
#         plt.scatter(df["Polarity"][i], df["Subjectivity"][i], color='Blue')  # plt.scatter(x,y,color)
#
#     plt.title('Criminal Sentiment Analysis')
#     plt.xlabel('Polarity')
#     plt.ylabel('Subjectivity')
#     plt.show()
#
#     # Print the percentage of positive tweets
#     ptweets = df[df.Analysis == 'Positive']
#     ptweets = ptweets['Tweets']
#     ptweets
#
#     round((ptweets.shape[0] / df.shape[0]) * 100, 1)
#
#     # Print the percentage of negative tweets
#     ntweets = df[df.Analysis == 'Negative']
#     ntweets = ntweets['Tweets']
#     ntweets
#
#     round((ntweets.shape[0] / df.shape[0]) * 100, 1)
#
#     # Show the value counts
#     df['Analysis'].value_counts()
#
#     # Plotting and visualizing the counts
#     plt.title('Sentiment Analysis')
#     plt.xlabel('Sentiment')
#     plt.ylabel('Counts')
#     df['Analysis'].value_counts().plot(kind='bar')
#     plt.show()
