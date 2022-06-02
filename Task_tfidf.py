from nltk.tokenize import word_tokenize
import pandas as pd
import math
import re
import numpy as np

corpus = pd.read_csv('/Users/abhishektiwari/Documents/GitHub/HeadOfData_Group7/tf_idf_dataset.csv')

def clean_data(text):
  #text = text.lower()
  text = re.sub("_"," ",text)
  text = re.sub("@[A-Za-z0-9_]+","", text) #mentions
  text = re.sub("#[A-Za-z0-9_]+","", text) #hashtags
  text = re.sub(r"https?:\/\/\S+", "", text) #links
  text = re.sub(r"www.\S+", "", text) #links
  text = re.sub(r"RT[\s]+","",text) #Retweets
  text = re.sub('[()!?]', ' ', text) #punctuations
  text = re.sub('\[.*?\]',' ', text)
  text = re.sub("[0-9_]+","",text) #numbers
  text = re.sub("\n","",text) #spacing
  text = re.sub(r'\b\w{1,3}\b', '', text);
  text = re.sub(r'^\s+", "', "a\n b\n c", text)
  punctuations = '@#!?+&*,[]-%.:/();$=><|{}^»«""'
  for p in punctuations:
      text = text.replace(p, '')
  text = text.replace("\\"," ")
  text = text.replace("'"," ") #apostrophe
  text = text.replace("’"," ") #apostrophe
  return text

corpus["product_name"] = corpus["product_name"].apply(lambda x: clean_data(x.strip()))

sentences = []
word_set = []

sentences = corpus.apply(lambda x: word_tokenize(x))
for sent in sentences:
    for word in sent:
        if word not in word_set:
            word_set.append(word)

# Set of vocab
word_set = set(word_set)
# Total documents in our corpus
total_documents = len(sentences)

# Creating an index for each word in our vocab.
index_dict = {}  # Dictionary to store index for each word
i = 0
for word in word_set:
    index_dict[word] = i
    i += 1


# Create a count dictionary

def count_dict(sentences):
    word_count = {}
    for word in word_set:
        word_count[word] = 0
        for sent in sentences:
            if word in sent:
                word_count[word] += 1
    return word_count


word_count = count_dict(sentences)

#Term Frequency
def termfreq(document, word):
    N = len(document)
    occurance = len([token for token in document if token == word])
    return occurance/N


# Inverse Document Frequency
def inverse_doc_freq(word):
    try:
        word_occurance = word_count[word] + 1
    except:
        word_occurance = 1
    return np.log(total_documents / word_occurance)


def tf_idf(sentence):
    tf_idf_vec = np.zeros((len(word_set),))
    for word in sentence:
        tf = termfreq(sentence, word)
        idf = inverse_doc_freq(word)

        value = tf * idf
        tf_idf_vec[index_dict[word]] = value
    return tf_idf_vec


# TF-IDF Encoded text corpus
vectors = []
for sent in sentences:
    vec = tf_idf(sent)
    vectors.append(vec)

for i in vectors:
    print(i)