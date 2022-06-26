# # importing modules
# from nltk.stem import PorterStemmer
# from nltk.tokenize import word_tokenize
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
 
# ps = PorterStemmer()
# factory = StemmerFactory()
# stemmer = factory.create_stemmer()
 
# sentence = "Programmers program with programming languages"
# words = word_tokenize(sentence)
 
# for w in words:
#     print(w, " : ", ps.stem(w))

# import csv
 
# # opening the CSV file
# # with open('marketing_sample_for_walmart_com-product_details__20200101_20200331__30k_data.csv', mode ='r')as file:
# with open('data.csv', mode ='r')as file:
   
#   # reading the CSV file
#   csvFile = csv.reader(file)
 
#   # displaying the contents of the CSV file
#   for lines in csvFile:
#         print(lines)
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

import pandas as pd
# import numpy as np

# csvFile = pd.read_csv('data2.csv')
csvFile = pd.read_csv('./data/data.csv')
# c = pd.DataFrame(csvFile)
# csvFile = csvFile.replace('', np.nan, inplace=True)
# csvFile.shape
# csvFile.isnull()
# csvFile.isnull().sum()
# csvFile.dropna(inplace=True)
csvFile.drop('Crawl Timestamp', inplace=True, axis=1)
csvFile.drop('Item Number', inplace=True, axis=1)
csvFile.drop('Gtin', inplace=True, axis=1)
csvFile.drop('Package Size', inplace=True, axis=1)
csvFile.drop('Postal Code', inplace=True, axis=1)

mod = csvFile.dropna()
# mod.isnull().sum()
# mod.to_csv('')
# print(mod)

# mod['product'] = mod['Product Name'].map(str) + ' ' + mod['Description'].map(str)

# mod2 = [i['Product Name'] + i['Description'] for i in mod]
# print(mod['product'].str.lower())
# mod.loc[:,'product'] = mod['Product Name']+ mod['Description']
# print(mod['product'][2])
# print(mod['product'][2])
# print(type(mod['product']))
dump = [
    'Allegiance Economy Dual-scale Digital Thermometer Part #5516811EDS - Allegiance Economy Dual-Scale Digital Thermometer Allegiance Dual-scale Digital Thermometer, 4 15/16" L x 3/4" W x 3/8" H, Mercury-free, Water-resistant [ Sold by the Each, Quantity per Each : 1 EA, Category : Thermometers, Product Class : Self Care ]',
    'Kenneth Cole Reaction Eau De Parfum Spray For Women 3.40 Oz Kenneth Cole Reaction perfume for her captures the freshness, confidence, and energy of the Reaction Woman - one that blends a youthful, playful spirit with a touch of seductive femininity. A fragrance designed to get a Reaction!  Intriguing and chic, this fragrance begins with a juicy and uplifting burst of sparkling pink grapefruit , lush kiwi with a hint of watermelon blended with the zesty freshness of mandarin. A vibrant and fresh floral body brings sunshine, romance and a sweetness that is tempered by a warm and sleek woody background. Notes:  Sparkling Pink Grapefruit, Fresh Mandarin, Lush Kiwi with hint of Watermelon, Lily of the Valley, White Orchid, Poppy Flowers, Sweet Pea, Violet Leaves, Cottonwood, Sleek Vetiver, White Amber, Musk.'
    'Kid Tough Fitness Inflatable Free-Standing Punching Bag + Machine Washable Fabric Cover South Carolina Gamecocks Kids Workout Buddy by Bonk Fit Bonk Fit is the inflatable punching bag you remember from childhood and so much more! Kids enjoy a high-performance fitness inflatable, made from super-durable polyurethane, PLUS form-fitting fabric cover featuring a colorful character to make exercise fun, easy, and accessible. Great for indoors and outdoors, kids are motivated to exercise in the living room, driveway, backyard, anywhere and anytime. Its so much fun, kids dont realize theyre working out! A sturdy fabric cover is the coolest part; its removable and machine-washable so its super-easy to keep clean and fresh. Beautifully-designed characters make the perfect workout partners while looking great in your house. Bonk Fit comes with one-year warranty so if the inflatable breaks, you get a new one! Parents and grandparents alike feel good about giving kids a durable PVC-free product, made by a mother inspired to create a fun workout experience at home. Watch your kids step away from the TV and get physical. Kid Tough Fitness Inflatable Free-Standing Punching Bag + Machine Washable Fabric Cover Officially Licensed South Carolina Gamecocks Kids Workout Buddy by Bonk Fit: Stands 36" tall For ages 2+ One-year manufacturer warranty Includes strong polyurethane inflatable (same material used in air mattresses) PVC-free, super-durable construction for rough-and-tumble activities Includes form-fitting cover made from recycled poly jersey knit (feels like a workout shirt) Removable and machine-washable (additional covers sold separately) Officially Licensed South Carolina Gamecocks design Cocky is the perfect workout partner Show your school spirit and get kids in the game Easy to assemble, consumer required to add weight and inflate Fill base with five (5) pounds of play-sand, uncooked rice, or kitty litter — no water Inflate until firm, basic air pump or by mouth Weighted substance and pump not included Made by a certified woman-owned business |Stands 36" tall|For ages 2+|One-year manufacturer warranty|Includes strong polyurethane inflatable (same material used in air mattresses)|PVC-free, super-durable construction for rough-and-tumble activities|Includes form-fitting cover made from recycled poly jersey knit (feels like a workout shirt)|Removable and machine-washable (additional covers sold separately)|Officially Licensed South Carolina Gamecocks design|Cocky is the perfect workout partner|Show your school spirit and get kids in the game|Easy to assemble, consumer required to add weight and inflate|Fill base with five (5) pounds of play-sand, uncooked rice, or kitty litter — no water|Inflate until firm, basic air pump or by mouth|Weighted substance and pump not included|Made by a certified woman-owned business'
]

def remove_special_character(data):
    output = []
    for i in range(len(data)):
        temp = str(data[i]).lower()
        # a = [word for word in temp.split(' ')]
        # print(a)
        # break
        # output.append(' '.join(''.join(l for l in [c for c in word if c.isalnum()] if l != '') for word in temp.split(' ')))
        new_words = []
        for word in temp.split(' '):
            w = ''
            for c in word:
                if c.isalnum():
                    w += c
            
            if w != '':
                new_words.append(w)
        
        output.append(' '.join(word for word in new_words))

    return output

# remove_special_character(dump)
print(remove_special_character(dump)[0])

# print(type(mod.loc[:,'product'].to_numpy()))
# for i in mod.loc:
#   print(i)
# print(mod.columns.values.tolist())