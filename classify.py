# coding= utf-8
from threading import *
from time import *
from Queue import *
from sets import Set
import datetime
import json
import jieba
import jieba.analyse

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

from pymongo import MongoClient
#DBClient = MongoClient()
DBClient = MongoClient('10.110.91.236')
DBSave = DBClient["cc98"]
Collection = DBSave["soul"]

name = "ph-test"
password = "1qaz"

PostSet = Set()

UrlSite = "http://www.cc98.org/"

#display site
DispSite = "http://www.cc98.org/dispbbs.asp" 

#list post site
ListSite = "http://www.cc98.org/list.asp"



PostQueue = Queue()

def post_analyse():
	while True:
		item = PostQueue.get()
		tmp = {}
		tmp["BoardId"] = item[0];
		tmp["PostId"] = item[1];
		MessFind = Collection.find({"PostId":item[1],"BoardId":i},{"_id":False,"message":True},)



def main():
	ThreadList = []
	PostDict = {}
	for thread_each in ThreadList:
		thread_each.start()

	for thread_each in ThreadList:
		thread_each.join()

	res = Collection.find({"PageNum":{"$gt":30}},{"PostId":True,"BoardId":True,"_id":False},limit=300)
	for i in res:
		if i["BoardId"] in PostDict:
			PostDict[i["BoardId"]].add(i["PostId"])
		else:
			PostDict[i["BoardId"]] = Set([i["PostId"]])

	for i in PostDict:
		for j in PostDict[i]:
			PostQueue.put([i,j])
			MessTotal = ''
			print "Query pre", datetime.datetime.now()
			MessFind = Collection.find({"PostId":j,"BoardId":i},{"_id":False,"message":True},)
			print "Query post", datetime.datetime.now()
			for k in MessFind:
				MessTotal += k['message']
			print "Fenci pre", datetime.datetime.now()
			tags = jieba.analyse.extract_tags(MessTotal, topK=20)
			print ",".join(tags)
			print "Fenci done", datetime.datetime.now()
	

if __name__ == '__main__':
	main()
