#region Import
from flask import Flask, render_template, request
import mysql.connector
import mysql.connector
import re
import math
import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#endregion

#region MySQL Connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql",
  database="uticon"
)
mycursor = mydb.cursor()
#endregion

#region Search Product Function
# Step:
# 1. Lowercasing
# 2. Tokenize
# 3. Remove special character
# 4. Stopword
# 5. Lemmatization

nlp = spacy.load('en_core_web_sm')
def preprocessing(data):
    result = []
    arr_pos = ["ADJ", "NOUN", "PROPN", "VERB", "ADV", "X"]
    
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
    arr_pos = ["ADJ", "NOUN", "PROPN", "VERB", "ADV", "X"]
    
    # Lowercasing and Tokenization
    doc = nlp(data.lower().replace("|", " "))
    for x in doc:
        # Remove Special Character and Stopword Checking
        if x.is_stop is False and x.pos_ in arr_pos and str(x).isalnum() and len(str(x)) > 1:
            # Lemmatization
            le = x.lemma_
            result.append(le)
            if (x.pos_ == "NOUN" or x.pos_ == "X"):
                if re.search('[sxz]$', le):
                    result.append(re.sub('$', 'es', le))
                elif re.search('[^aeioudgkprt]h$', le):
                    result.append(re.sub('$', 'es', le))
                elif re.search('[aeiou]y$', le):
                    result.append(re.sub('y$', 'ies', le))
                else:
                    result.append(le + 's')

    return result

def calculateSimilarity(keyword, mode):
    resultRaw = []
    pluralPreprocessedKeyword = preprocessingPluralKeyword(keyword) 
    preprocessedKeyword = preprocessing(keyword)
    keywordlist = []
    for w in pluralPreprocessedKeyword:
        keywordlist.extend(["[[:<:]]" + w + "[[:>:]]"] * 2)
    
    result = [] 
    if (len(pluralPreprocessedKeyword) > 0):   
        sql = "SELECT * FROM product where name REGEXP %s or description REGEXP %s"
        sql += " or name REGEXP %s or description REGEXP %s" * (len(pluralPreprocessedKeyword) - 1) if (len(pluralPreprocessedKeyword) > 1) else ""
        mycursor.execute(sql, tuple(keywordlist))
        resultRaw = list(mycursor.fetchall())

        data_similarity = []
        for i in range(len(resultRaw)):
            # Example
            # Book 1                               Book 2
            # Title: Harry Potter                  Title: A Great Book
            # Description: A Great Book            Description: Harry Potter
            
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
            if (sim > 0.15):
                data_similarity.append([resultRaw[i],sim])
            
        # Sort the best similarity up top
        data_similarity.sort(key=lambda sim: sim[1], reverse= True)
        
        # If called from search insert to database
        if len(data_similarity) > 0 and mode == 1:
            insertSearchResult(data_similarity, preprocessedKeyword)
        
        result = [x[0] for x in data_similarity]
    
    return result

def insertSearchResult(data_similarity, preprocessedKeyword):
    lemmatizedKeyword = " ".join(preprocessedKeyword)
    sql = "SELECT * FROM search where keyword=%s" 
    mycursor.execute(sql, (lemmatizedKeyword,))
    keywordResult = list(mycursor.fetchall())

    if (len(keywordResult) > 0):
        searchHistory = keywordResult[0]
        sql2 = "UPDATE search SET count=%s, time=NOW() where id=%s"
        mycursor.execute(sql2, (str(int(searchHistory[2]) + 1), searchHistory[0]))
        mydb.commit()
    else:
        sql2 = "INSERT INTO search (`keyword`, `count`, `time`) VALUES (%s, 1, NOW())"
        mycursor.execute(sql2, (lemmatizedKeyword,))
        mydb.commit()
        searchId = mycursor.lastrowid
        
        for i in range(len(data_similarity)):
            sql3 = "INSERT INTO search_result (`search_id`, `product_id`, `priority`) VALUES (%s, %s, %s)"
            mycursor.execute(sql3, (searchId, data_similarity[i][0][0], str(i + 1)))
            mydb.commit()
            if(i == 14):
                break
#endregion

# =========================================================================================================
# FLASK
# =========================================================================================================
app = Flask(__name__)

#region Home Page
@app.route('/')
def index():
    # Delete all search history and result if its last searched date exceeding 4 days (>= 5 days)
    sql = "SELECT * FROM `search` where timestampdiff(DAY, time, now()) >= 5"
    mycursor.execute(sql)
    exceedingSearchResult = list(mycursor.fetchall())
    
    if (len(exceedingSearchResult) > 0):
        for x in exceedingSearchResult:
            sql2 = "DELETE FROM `search_result` where search_id=%s"
            mycursor.execute(sql2, (x[0],))
            mydb.commit()
            
            sql3 = "DELETE FROM `search` where id=%s"
            mycursor.execute(sql3, (x[0],))
            mydb.commit()     
    
    # Select all search
    sql4 = "SELECT s.*, timestampdiff(DAY, time, now()) as diff FROM `search` as s where timestampdiff(DAY, time, now()) < 5"
    mycursor.execute(sql4)
    searchResult = list(mycursor.fetchall())
    
    countInvertDateArr = []
    # [id, count, invert]
    for x in searchResult:
        invert = 5 - int(x[4])
        countInvertDateArr.append([int(x[0]), int(x[2]), invert])
    
    countInvertDateArr.sort(key=lambda x: (x[2], x[1]), reverse= True)
    if(len(countInvertDateArr) > 10):
        countInvertDateArr = countInvertDateArr[:10]
        
    totalCount = 0
    totalInvert = 0
    for x in countInvertDateArr:
        totalCount += int(x[1])
        totalInvert += int(x[2])
    
    recommendation = []
    for x in countInvertDateArr:
        recomAmount = round(((x[1] / totalCount) + (x[2] / totalInvert)) / 2 * 15)
        sql5 = "SELECT p.* FROM search_result sr inner join product p on sr.product_id = p.id where sr.search_id=%s order by sr.priority limit %s"
        mycursor.execute(sql5, (x[0], recomAmount))
        for x in list(mycursor.fetchall()):
            if (x not in recommendation):
                recommendation.append(x)
    
    if (len(recommendation) < 15):
        randomCount = 15 - len(recommendation)
        sql6 = "SELECT * FROM product ORDER BY RAND() LIMIT %s"
        mycursor.execute(sql6, (randomCount,))
        recommendation.extend(list(mycursor.fetchall()))
    
    random = []
    sql7 = "SELECT * FROM product ORDER BY RAND() LIMIT %s"
    mycursor.execute(sql7, (12,))
    random.extend(list(mycursor.fetchall()))
    
    return render_template('index.html', result = recommendation, random = random)
#endregion

#region Product Page
@app.route('/products/', methods=['GET'])
def products():
    keyword = request.args.get('search', type=str, default="")
    page = request.args.get('page', type=int, default=1)
    offset = (page - 1) * 28

    first_page = 1 if math.floor(page/10) == 0 else 10 * math.floor(page/10)
    max_page = (page + 10) if page % 10 == 0 else 10 * math.ceil(page/10)

    if (keyword == ""):
        sql = "SELECT * FROM product LIMIT %s,28"
        mycursor.execute(sql % offset)
        result = list(mycursor.fetchall())

        sql = "SELECT COUNT(*) FROM product"
        mycursor.execute(sql)
        number_page = math.ceil(((mycursor.fetchall())[0][0])/28)

        if max_page > number_page:
            max_page = number_page 
        
        return render_template('product.html', result=result, use_pagination=1, page=page, first_page=first_page, max_page=max_page, number_page=number_page, search=keyword, count=-1)
    else:
        data_similarity = calculateSimilarity(keyword, 1)

        return render_template('product.html', result=data_similarity, use_pagination=0, search=keyword, count=len(data_similarity))
#endregion

#region Product Detail Page
@app.route('/detail/<string:id>')
def detail(id):
    sql = "SELECT * FROM product Where id = %s"
    mycursor.execute(sql, (id,))
    result = list(mycursor.fetchall())
    data_similarity = calculateSimilarity(result[0][2], 0)
    return render_template('product-detail.html', result=result, similar = data_similarity[:15])
#endregion

#region About Page
@app.route('/about')
def about():
    return render_template('about.html')
#endregion