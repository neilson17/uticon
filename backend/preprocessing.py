from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy
nlp = spacy.load('en_core_web_sm')

# nltk.download('stopwords')

ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

dump = [
    'Allegiance Economy Dual-scale Digital Thermometer Part #5516811EDS - Allegiance Economy Dual-Scale Digital Thermometer Allegiance Dual-scale Digital Thermometer, 4 15/16" L x 3/4" W x 3/8" H, Mercury-free, Water-resistant [ Sold by the Each, Quantity per Each : 1 EA, Category : Thermometers, Product Class : Self Care ]',
    'Kenneth Cole Reaction Eau De Parfum Spray For Women 3.40 Oz Kenneth Cole Reaction perfume for her captures the freshness, confidence, and energy of the Reaction Woman - one that blends a youthful, playful spirit with a touch of seductive femininity. A fragrance designed to get a Reaction!  Intriguing and chic, this fragrance begins with a juicy and uplifting burst of sparkling pink grapefruit , lush kiwi with a hint of watermelon blended with the zesty freshness of mandarin. A vibrant and fresh floral body brings sunshine, romance and a sweetness that is tempered by a warm and sleek woody background. Notes:  Sparkling Pink Grapefruit, Fresh Mandarin, Lush Kiwi with hint of Watermelon, Lily of the Valley, White Orchid, Poppy Flowers, Sweet Pea, Violet Leaves, Cottonwood, Sleek Vetiver, White Amber, Musk.',
    'Kid Tough Fitness Inflatable Free-Standing Punching Bag + Machine Washable Fabric Cover South Carolina Gamecocks Kids Workout Buddy by Bonk Fit Bonk Fit is the inflatable punching bag you remember from childhood and so much more! Kids enjoy a high-performance fitness inflatable, made from super-durable polyurethane, PLUS form-fitting fabric cover featuring a colorful character to make exercise fun, easy, and accessible. Great for indoors and outdoors, kids are motivated to exercise in the living room, driveway, backyard, anywhere and anytime. Its so much fun, kids dont realize theyre working out! A sturdy fabric cover is the coolest part; its removable and machine-washable so its super-easy to keep clean and fresh. Beautifully-designed characters make the perfect workout partners while looking great in your house. Bonk Fit comes with one-year warranty so if the inflatable breaks, you get a new one! Parents and grandparents alike feel good about giving kids a durable PVC-free product, made by a mother inspired to create a fun workout experience at home. Watch your kids step away from the TV and get physical. Kid Tough Fitness Inflatable Free-Standing Punching Bag + Machine Washable Fabric Cover Officially Licensed South Carolina Gamecocks Kids Workout Buddy by Bonk Fit: Stands 36" tall For ages 2+ One-year manufacturer warranty Includes strong polyurethane inflatable (same material used in air mattresses) PVC-free, super-durable construction for rough-and-tumble activities Includes form-fitting cover made from recycled poly jersey knit (feels like a workout shirt) Removable and machine-washable (additional covers sold separately) Officially Licensed South Carolina Gamecocks design Cocky is the perfect workout partner Show your school spirit and get kids in the game Easy to assemble, consumer required to add weight and inflate Fill base with five (5) pounds of play-sand, uncooked rice, or kitty litter — no water Inflate until firm, basic air pump or by mouth Weighted substance and pump not included Made by a certified woman-owned business |Stands 36" tall|For ages 2+|One-year manufacturer warranty|Includes strong polyurethane inflatable (same material used in air mattresses)|PVC-free, super-durable construction for rough-and-tumble activities|Includes form-fitting cover made from recycled poly jersey knit (feels like a workout shirt)|Removable and machine-washable (additional covers sold separately)|Officially Licensed South Carolina Gamecocks design|Cocky is the perfect workout partner|Show your school spirit and get kids in the game|Easy to assemble, consumer required to add weight and inflate|Fill base with five (5) pounds of play-sand, uncooked rice, or kitty litter — no water|Inflate until firm, basic air pump or by mouth|Weighted substance and pump not included|Made by a certified woman-owned business'
]

def lower_case_str(data):
    return list(map(lambda text: text.lower(), data))

def remove_special_character(data):
    output = []
    for i in range(len(data)):
        new_words = []
        for word in data[i].split(' '):
            w = ''
            for c in word:
                if c.isalnum():
                    w += c
            
            if w != '':
                new_words.append(w)
        
        output.append(' '.join(word for word in new_words))

    return output

lower_cased = lower_case_str(dump)
data_cleansed = remove_special_character(lower_cased)

# tokenizing
word_tokenized = []
for d in data_cleansed:
    word_tokenized.append(word_tokenize(d))
print(word_tokenized)

# lematization
lemma = []
for word in word_tokenized:
    temp = []
    for w in word:
        if w not in stop_words:
            #print(w, ":", lemmatizer.lemmatize(w))
            temp.append(nlp(w)[0].lemma_)
    lemma.append(temp)

# print(lemma)
# print(lemma)
    # print(w, " : ", ps.stem(w))

# stopwords
stopped_words = []
for word in word_tokenized:
    temp = []
    for w in word:
        if w not in stop_words:
            temp.append(w)

    stopped_words.append(temp)

# print(stem("adding"))
# print(lemmatize("adding"))
# print(stopped_words)