import numpy
import os
from pymongo import MongoClient
#DBNAME = 'vistorRatings'
DBNAME = 'heroku_app16046823'
SIMDBNAME = ''
def get_collection():
    return MongoClient(host = os.environ['MONGOLAB_URI'])[DBNAME].ratings

def random_movies():
	curs = MongoClient(host = os.environ['MONGOLAB_URI'])[DBNAME].simTable
	movies =  list(curs.find({},{'title':1,'_id':0}))
	i = numpy.unique(numpy.random.randint(0,len(movies),size=200))
	print i
	
	movs = [movies[k] for k in i]
	print movs
	return movs


def random_movie():
	curs = MongoClient(host = os.environ['MONGOLAB_URI'])[DBNAME].simTable
	movies =  list(curs.find({},{'title':1,'_id':0}))
	i = numpy.random.randint(0,len(movies))
	print "in random", movies[i]

	return movies[i]



def insert_rating(rating):
	coll = get_collection()
	#coll
	coll.insert(rating)
	#Get this uid's count 
	return len(list(coll.find({'uid':rating['uid']})))

def get_recommendation(uid):
	coll = get_collection()
	cursor = MongoClient(host = os.environ['MONGOLAB_URI'])[DBNAME].simTable
	a = coll.find({'uid':uid},{'title':1, '_id':0, 'score':1})
	userRatings = list(a)
	scores = {} 
	totalSim = {}
	hits = {}
	for ur in userRatings:
		print ur['title'], ur['score']
		title = ur['title']
		rating = ur['score']
		matches = list(cursor.find({'title':title}))[0]
		similar = simt = matches['similarTitles']

		for (similarity, title2) in similar: 
			#print similarity, title2
			if title2 == title: continue 
			scores.setdefault(title2,0) 
			scores[title2] += similarity*rating 
			totalSim.setdefault(title2,0) 
			totalSim[title2] += similarity
			hits.setdefault(title2,0) 
			hits[title2] += 1
	#print totalSim
	for tit, hit in hits.items():
		if hit < 5:
			scores.pop(tit)
			hits.pop(tit)
			totalSim.pop(tit)
	rankings = [(score/totalSim[item], item) for item, score in scores.items()]
	rankings.sort()
	rankings.reverse()
	#print rankings
	return rankings[:50]
	
