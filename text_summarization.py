# Author: Endri Dibra

# importing the required libraries
import bs4 as bs
import urllib.request
import re
import heapq
import nltk
from nltk.corpus import stopwords
from gtts import gTTS
from playsound import playsound

# downloading stop words for preprocessing stage (text cleaning)
nltk.download("stopwords")


# gathering data from the link and transforming them into paragraphs
data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Tony_Stark_(Marvel_Cinematic_Universe)')

article = data.read()

parsed_article = bs.BeautifulSoup(article, "lxml")

paragraphs = parsed_article.find_all("p")

# getting text from yhe paragraphs
article_text = ""

for p in paragraphs:

    article_text += p.text


# cleaning text from the symbols
article_text = re.sub(r"\[[0-9]*\]", " ", article_text)
article_text = re.sub(r"\s+", " ", article_text)

processed_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
processed_article_text = re.sub(r'\s+', ' ', processed_article_text)

sentences = nltk.sent_tokenize(article_text)

stop_words = stopwords.words("english")

# getting word's frequency
word_freq = {}

for word in nltk.word_tokenize(processed_article_text):

    if word not in stop_words:

        if word not in word_freq.keys():

            word_freq[word] = 1

        else:

            word_freq[word] += 1

# finding the weighted frequency
max_freq = max(word_freq.values())

for word in word_freq.keys():
    word_freq[word] = (word_freq[word]/max_freq)


# calculating the score for each sentence
sentence_scores = {}

for s in sentences:

    for word in nltk.word_tokenize(s.lower()):

        if word in word_freq.keys():

            if len(s.split(' ')) < 30:

                if s not in sentence_scores.keys():

                    sentence_scores[s] = word_freq[word]

                else:

                    sentence_scores[s] += word_freq[word]


# getting the summary and printing it
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

# separating words with spaces
summary = ' '.join(summary_sentences)

print("Below you can see the summary:\n")

print(summary)

print("\nPlease wait for computer voice to start")


# Initializing the type of audio and language
audio = 'speech.mp3'
language = "en"

# Initializing input, language
sp = gTTS(text=summary, lang=language, slow=False)

# The input from the user will be saved
# and played by the computer using machine-voice
sp.save(audio)
playsound(audio)