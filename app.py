from chalice import Chalice
import requests
import re
import nltk
from nltk.corpus import wordnet as WN
from nltk.corpus import stopwords
stop_words_en = set(stopwords.words('english'))

app = Chalice(app_name='analyzer')
rating = 0

@app.route('/')
def index():
	return "index"

@app.route('/get_userstories')
def get_userstories():
	url = "https://api.trello.com/1/lists/5a9d0a0536a40a8cd0658e1b/cards?fields=name"
	querystring = {"key":"7877dd27f5b9b34fc38e734dadeeff61","token":"94260ec7eb53519bddd84cef66175f225d83fc2e8ac4d6ee616e28da519a67cd"}
	response = requests.request("GET", url, params=querystring)
	data = response.json()
	return data
	
@app.route('/check_grammar')
def tokens(sent):
        return nltk.word_tokenize(sent)

def SpellChecker(line):
    for i in tokens(line):
        strip = i.rstrip()
        if not WN.synsets(strip):
            if strip in stop_words_en:    # <--- Check whether it's in stopword list
                print("No mistakes :" + i)
            else:
                print("Wrong spellings : " +i)
        else: 
            print("No mistakes :" + i)

def removePunct(str):
        return  " ".join((c for c in str if c not in ('!','.',':',',')))
l = []
userstories = get_userstories()
for v in userstories:
	l.append(v['name'])
noPunct = removePunct(l)
if(SpellChecker(noPunct)):
       	print(l)
       	print(noPunct)

@app.route('/set_rating')
def set_rating():
	#rating = get_rating()
	global rating
	userstories = get_userstories()
	data = []
	for v in userstories:
		rating += 5
		data.append({'Userstory': v['name'], 'Rating': rating})
	return data

@app.route('/check_role')
def check_role():
	global rating
	userstories = get_userstories()
	data = []
	for v in userstories:
		#print v['name']
		rating = 0
		searchrole = re.search(r'As a', v['name'])
		if searchrole:
			#print 'Role was found.'
			rating += 5
			#break
		else:
			return 'Role was not found.'
		data.append({'Userstory': v['name'], 'Rating': rating})
	return data

@app.route('/check_feature')
def check_feature():
	global rating
	userstories = get_userstories()
	#check_role()
	data = []
	for v in userstories:
		#print v['name']
		rating = 0
		searchfeature = re.search(r'I want to', v['name'])
		if searchfeature:
			#print 'Feature was found.'
			rating += 5
			#break
		else:
			print 'Feature was not found.'
		data.append({'Userstory': v['name'], 'Rating': rating})
	return data

@app.route('/check_length')
def check_length():
	userstories = get_userstories()
	data = []
	for v in userstories:
		length_userstory = len(v['name'])
		if length_userstory > 20:
			data.append({'Userstory': v['name'], 'Rating': 'Good Userstory'})
		else:
			return 'Bad Userstory'
	return data

@app.route('/get_all_ratings')
def get_all_ratings():
	ratings_role = []
	ratings_feature = []
	#ratings_total = []
	checkrole = check_role()
	checkfeature = check_feature()
	for r in checkrole:
		ratings_role.append(r['Rating'])
	for r in checkfeature:
		ratings_feature.append(r['Rating'])
	ratings_total = [x + y for x, y in zip(ratings_role, ratings_feature)]
	return ratings_total
'''
@app.route('/test')
def test():
	test = "asdasd"
	return test
	
@app.route('/test2')
def test2():
	get_test = test()
	return get_test
'''