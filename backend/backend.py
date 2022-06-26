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
keyword = "diaper"

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

# 10 product yang ditampilkan
# Range rekomendasi 1 days <= a <= 4 days (>= 5 days dibuang dari rekomendasi)

# Keyword    Count   Timestamp   Invert (5 - x)
# a          2       2 day ago   3 
# b          4       1 day ago   4
# c          1       4 day ago   1
# d          5       3 day ago   2
# ----------------------------------------------
# total      12                  10    

# (2/12 + 3/10) * 10 / 2 = 2     
# (4/12 + 4/10) * 10 / 2 = 4
# (1/12 + 1/10) * 10 / 2 = 1
# (5/12 + 2/10) * 10 / 2 = 3

# =========================================================================================================
# Search Keyword in Database
# =========================================================================================================
resultRaw = []
pluralPreprocessedKeyword = preprocessingPluralKeyword(keyword)
preprocessedKeyword = preprocessing(keyword)
keywordlist = []
for w in pluralPreprocessedKeyword:
    keywordlist.extend(["[[:<:]]" + w + "[[:>:]]"] * 2)
    
sql = "SELECT * FROM product where name REGEXP %s or description REGEXP %s"
sql += " or name REGEXP %s or description REGEXP %s" * (len(pluralPreprocessedKeyword) - 1) if (len(pluralPreprocessedKeyword) > 1) else ""
mycursor.execute(sql, tuple(keywordlist))
resultRaw = list(mycursor.fetchall())

# =========================================================================================================
# TF-IDF and Similarity
# =========================================================================================================
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

# =============================== Note ===============================
# [[(id, url, nama, desc, dkk), 0,4], [(id, url, nama, desc, dkk), 0.3]]
# def onBackPressed(x):
#     logiccc(x)
#     return hasil

# Andi makan bakso
# ["andi", "makan", "bakso"]
# def token(x):
#     return x 
# ["andi", "makan", "bakso"]
# ["andi", "makan", "bakso"]
# ["andi", "makan", "bakso"]
# ["andi", "makan", "bakso"]

# =========================================================================================================
# Print Result
# =========================================================================================================
# Delete targeted txt file
target = "searchresult.txt"
f = open(target, "r+")
f.truncate(0)
f.close()

# Write targeted txt file
for x in data_similarity:
    with open(target, 'a', encoding='utf-8') as f:
        f.write(str(x[0][2]))
        f.write('\n')
        f.write(str(x[0][3]))
        f.write('\n')
        f.write(str(x[1]))
        f.write('\n')
        f.write('\n')
        
# =========================================================================================================
# Insert Search and Result to database
# =========================================================================================================
if (len(data_similarity) > 0):
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