from flask import Flask, render_template, request
import mysql.connector
import mysql.connector
import re
from nltk.corpus import stopwords
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# MySQL Connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql",
  database="uticon"
)
mycursor = mydb.cursor()

# Define Keyword
keyword = "cat food"

# =========================================================================================================
# Preprocessing Function
# =========================================================================================================
# Step:
# lowercasing
# tokenize
# remove special character
# stopword
# expansion of abbreviations and slang words (ga wajib, kalo ada waktu) > buat querynya aja
# lemmatization atau stemming

nlp = spacy.load('en_core_web_sm')
def preprocessing(data):
    result = []
    arr_pos = ["ADJ", "NOUN", "PROPN", "VERB", "ADV"]
    
    # Lowercasing and Tokenization
    doc = nlp(data.lower().replace("|", " "))
    for x in doc:
        # Remove Special Character and Stopword Checking
        if x.is_stop is False and x.pos_ in arr_pos and str(x).isalnum() and len(str(x)) > 1:
            # Lemmatization
            result.append(x.lemma_)

    return result

def preprocessingPluralKeyword(data):
    result = []
    arr_pos = ["ADJ", "NOUN", "PROPN", "VERB", "ADV"]
    
    # Lowercasing and Tokenization
    doc = nlp(data.lower().replace("|", " "))
    for x in doc:
        # Remove Special Character and Stopword Checking
        if x.is_stop is False and x.pos_ in arr_pos and str(x).isalnum() and len(str(x)) > 1:
            # Lemmatization
            le = x.lemma_
            result.append(le)
            if (x.pos_ == "NOUN"):
                if re.search('[sxz]$', le):
                    result.append(re.sub('$', 'es', le))
                elif re.search('[^aeioudgkprt]h$', le):
                    result.append(re.sub('$', 'es', le))
                elif re.search('[aeiou]y$', le):
                    result.append(re.sub('y$', 'ies', le))
                else:
                    result.append(le + 's')

    return result

# =========================================================================================================
# FLASK
# =========================================================================================================
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    keyword = "cat food"

    if (keyword == ""):
        sql = "SELECT * FROM product"
        mycursor.execute(sql)
        result = list(mycursor.fetchall())
        return render_template('product.html', result=result)
    else:
        resultRaw = []
        pluralPreprocessedKeyword = preprocessingPluralKeyword(keyword)
        preprocessedKeyword = preprocessing(keyword)
        keywordlist = []
        for w in pluralPreprocessedKeyword:
            keywordlist.extend(["[[:<:]]" + w + "[[:>:]]"] * 2)
            
        sql = "SELECT * FROM product where name REGEXP %s or description REGEXP %s"
        sql += " or name REGEXP %s or description REGEXP %s" * (len(pluralPreprocessedKeyword) - 1) if (len(pluralPreprocessedKeyword) > 1) else ""
        sql += " limit 10"
        mycursor.execute(sql, tuple(keywordlist))
        resultRaw = list(mycursor.fetchall())

        data_similarity = []
        for i in range(len(resultRaw)):
            # Title Similarity
            tfidf = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False)
            vectorTitle = tfidf.fit_transform([preprocessing(resultRaw[i][2]), preprocessedKeyword])
            # print(tfidf.vocabulary_)
            cosTitle = cosine_similarity(vectorTitle)
            
            # Description Similarity
            tfidf = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False)
            vectorDescription = tfidf.fit_transform([preprocessing(resultRaw[i][3]), preprocessedKeyword])
            cosDescription = cosine_similarity(vectorDescription)
            
            # Calculate Similarity (80% Title & 20% Description)    
            sim = 0.8 * cosTitle[0][1] + 0.2 * cosDescription[0][1]
            data_similarity.append([resultRaw[i], sim])
            
        # Sort the best similarity up top
        data_similarity.sort(key=lambda sim: sim[1], reverse= True)

        return render_template('product.html', result=data_similarity)

@app.route('/products', methods=['POST'])
def products2():
    resultRaw = []
    #keyword=""
    #keyword = request.form['inputSearch']
    keyword = ""
    if 'inputSearch' in request.form:
        keyword = request.form['inputSearch']

    if (keyword == ""):
        sql = "SELECT * FROM product"
        mycursor.execute(sql)
        result = list(mycursor.fetchall())
        return render_template('product.html', result=result)
    else:
        pluralPreprocessedKeyword = preprocessingPluralKeyword(keyword)
        preprocessedKeyword = preprocessing(keyword)
        keywordlist = []
        for w in pluralPreprocessedKeyword:
            keywordlist.extend(["[[:<:]]" + w + "[[:>:]]"] * 2)
            
        sql = "SELECT * FROM product where name REGEXP %s or description REGEXP %s"
        sql += " or name REGEXP %s or description REGEXP %s" * (len(pluralPreprocessedKeyword) - 1) if (len(pluralPreprocessedKeyword) > 1) else ""
        sql += " limit 5"
        mycursor.execute(sql, tuple(keywordlist))
        resultRaw = list(mycursor.fetchall())

        data_similarity = []
        for i in range(len(resultRaw)):
            # Title Similarity
            tfidf = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False)
            vectorTitle = tfidf.fit_transform([preprocessing(resultRaw[i][2]), preprocessedKeyword])
            # print(tfidf.vocabulary_)
            cosTitle = cosine_similarity(vectorTitle)
            
            # Description Similarity
            tfidf = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False)
            vectorDescription = tfidf.fit_transform([preprocessing(resultRaw[i][3]), preprocessedKeyword])
            cosDescription = cosine_similarity(vectorDescription)
            
            # Calculate Similarity (80% Title & 20% Description)    
            sim = 0.8 * cosTitle[0][1] + 0.2 * cosDescription[0][1]
            data_similarity.append([resultRaw[i], sim])
            
        # Sort the best similarity up top
        data_similarity.sort(key=lambda sim: sim[1], reverse= True)
        
        return render_template('product.html', result=data_similarity)

@app.route('/carts')
def carts():
    return render_template('shoping-cart.html')

def search(keyword):
    result = []
    return result



