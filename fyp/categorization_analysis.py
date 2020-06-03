import re

# import inline as inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string
import nltk
from nltk.stem.porter import *
import warnings
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

warnings.filterwarnings("ignore", category=DeprecationWarning)

# %matplotlib inline

train = pd.read_csv('C:/Users/apex/PycharmProjects/tca/trained_data.csv', sep=',', engine='python')
test = pd.read_csv('C:/Users/apex/PycharmProjects/tca/testing_data.csv', sep=',', engine='python')
print('Train Data')
print(train.head())

combi = train.append(test, ignore_index=True)
print('After Append Data')
print(combi.head())


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt


def trained_data():
    # remove twitter handles (@user)
    # combi['user Id'] = combi['user_id']
    combi['tidy_tweet'] = np.vectorize(remove_pattern)(combi['text'], "@[\w]*")
    # remove special characters, numbers, punctuations
    combi['tidy_tweet'] = combi['tidy_tweet'].str.replace("[^a-zA-Z#]", " ")
    # removing short words
    combi['tidy_tweet'] = combi['tidy_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w) > 3]))
    return combi

# # tokenizing
# tokenized_tweet = combi['tidy_tweet'].apply(lambda x: x.split())
# print('Tokenized Tweets')
# print(tokenized_tweet.head())
# # stemming
# stemmer = PorterStemmer()
# tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x])  # stemming
# print('Stemmed tweets')
# print(tokenized_tweet.head())
#
# for i in range(len(tokenized_tweet)):
#     tokenized_tweet[i] = ' '.join(tokenized_tweet[i])
# combi['tidy_tweet'] = tokenized_tweet
# # combi.to_csv('cleaned_tweets.csv', index=False)
# print('Stitched back tokens together')
# print(combi.head())
#
# # all_words = ' '.join([text for text in combi['tidy_tweet']])
# # wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)
# # plt.figure(figsize=(10, 7))
# # plt.imshow(wordcloud, interpolation="bilinear")
# # plt.axis('off')
# # plt.show()
#
# Rape_words = ' '.join([text for text in combi['tidy_tweet'][combi['label'] == 1]])
#
# wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(Rape_words)
# plt.figure(figsize=(10, 7))
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis('off')
# plt.show()
#
# killing_words = ' '.join([text for text in combi['tidy_tweet'][combi['label'] == 2]])
# wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(killing_words)
# plt.figure(figsize=(10, 7))
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis('off')
# plt.show()
#
# abusive_words = ' '.join([text for text in combi['tidy_tweet'][combi['label'] == 3]])
# wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(abusive_words)
# plt.figure(figsize=(10, 7))
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis('off')
# plt.show()
#
#
# # function to collect hashtags
# def hashtag_extract(x):
#     hashtags = []
#     # Loop over the words in the tweet
#     for i in x:
#         ht = re.findall(r"#(\w+)", i)
#         hashtags.append(ht)
#
#     return hashtags
#
#
# def crime_wise(x):
#     crime = []
#     for i in x:
#         cr = re.findall(r"#(rape|killing|abuse+\w*)", i)
#         crime.append(cr)
#     return crime
#
#
# # extracting hashtags from non racist/sexist tweets
# # crime_rape = hashtag_extract(combi['tidy_tweet'][combi['label'] == 1])
# # print(crime_rape)
# HT_rape = hashtag_extract(combi['tidy_tweet'][combi['label'] == 1])
#
# # extracting hashtags from racist/sexist tweets
# HT_killing = hashtag_extract(combi['tidy_tweet'][combi['label'] == 2])
#
# # extracting hashtags from racist/sexist tweets
# HT_abusive = hashtag_extract(combi['tidy_tweet'][combi['label'] == 3])
#
# # unnesting list
# HT_rape = sum(HT_rape, [])
# HT_killing = sum(HT_killing, [])
# HT_abusive = sum(HT_abusive, [])
# # crime_rape_total = sum(crime_rape, [])
# a = nltk.FreqDist(HT_rape)
# d = pd.DataFrame({'Rape': list(a.keys()),
#                   'Count': list(a.values())})
# # selecting top 10 most frequent hashtags
# d = d.nlargest(columns="Count", n=10)
# plt.figure(figsize=(16, 5))
# ax = sns.barplot(data=d, x="Rape", y="Count")
# ax.set(ylabel='Count')
# plt.show()
#
# b = nltk.FreqDist(HT_killing)
# e = pd.DataFrame({'Killing/Murder': list(b.keys()), 'Count': list(b.values())})
# # selecting top 10 most frequent hashtags
# e = e.nlargest(columns="Count", n=10)
# plt.figure(figsize=(16, 5))
# ax = sns.barplot(data=e, x="Killing/Murder", y="Count")
# ax.set(ylabel='Count')
# plt.show()
#
# c = nltk.FreqDist(HT_abusive)
# e = pd.DataFrame({'Abusing': list(c.keys()), 'Count': list(c.values())})
# # selecting top 10 most frequent hashtags
# e = e.nlargest(columns="Count", n=10)
# plt.figure(figsize=(16, 5))
# ax = sns.barplot(data=e, x="Abusing", y="Count")
# ax.set(ylabel='Count')
# plt.show()
#
# bow_vectorizer = CountVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
# # bag-of-words feature matrix
# bow = bow_vectorizer.fit_transform(combi['tidy_tweet'])
#
# tfidf_vectorizer = TfidfVectorizer(max_df=0.90, min_df=2, max_features=1000, stop_words='english')
# # TF-IDF feature matrix
# tfidf = tfidf_vectorizer.fit_transform(combi['tidy_tweet'])
#
# train_bow = bow[:600, :]
# test_bow = bow[600:, :]
#
# # splitting data into training and validation set
# xtrain_bow, xvalid_bow, ytrain, yvalid = train_test_split(train_bow, train['label'], random_state=42, test_size=0.3)
#
# lreg = LogisticRegression()
# lreg.fit(xtrain_bow, ytrain)  # training the model
#
# prediction = lreg.predict_proba(xvalid_bow)  # predicting on the validation set
# prediction_int = prediction[:, 1] >= 0.3  # if prediction is greater than or equal to 0.3 than 1 else 0
# prediction_int = prediction_int.astype(np.int)
#
# print(f1_score(yvalid, prediction_int))  # calculating f1 score
#
# test_pred = lreg.predict_proba(test_bow)
# test_pred_int = test_pred[:, 1] >= 0.3
# test_pred_int = test_pred_int.astype(np.int)
# test['label'] = test_pred_int
# submission = test[['id', 'label']]
# submission.to_csv('sub_lreg_bow.csv', index=False)  # writing data to a CSV file
#
# train_tfidf = tfidf[:31962, :]
# test_tfidf = tfidf[31962:, :]
#
# xtrain_tfidf = train_tfidf[ytrain.index]
# xvalid_tfidf = train_tfidf[yvalid.index]
#
# lreg.fit(xtrain_tfidf, ytrain)
#
# prediction = lreg.predict_proba(xvalid_tfidf)
# prediction_int = prediction[:, 1] >= 0.3
# prediction_int = prediction_int.astype(np.int)
#
# print(f1_score(yvalid, prediction_int))
