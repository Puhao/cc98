# coding= utf-8
from threading import *
from time import *
from Queue import *
from sets import Set
import datetime
import re
import json
import jieba
import jieba.analyse

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

from pymongo import MongoClient
DBClient = MongoClient()
#DBClient = MongoClient('10.110.91.236')
DBSave = DBClient["cc98"]
Collection = DBSave["soul"]
AnalyColl = DBSave["analyse"]

name = "ph-test"
password = "1qaz"

PostSet = Set()

UrlSite = "http://www.cc98.org/"

#display site
DispSite = "http://www.cc98.org/dispbbs.asp" 

#list post site
ListSite = "http://www.cc98.org/list.asp"



PostQueue = Queue()

def tags_filter(tag):
	ReFilter = []
	ReFilter.append(re.compile(r'^\.+$'))
	ReFilter.append(re.compile(r'^\w+$'))
	for i in ReFilter:
		if i.match(tag):
			return False
	ChiFilter = ["楼主", "匿名", "引用", "发言", "以下"]
	if tag in ChiFilter:
		return False
	else:
		return True

def post_analyse():
	while True:
		item = PostQueue.get()
		tmp = {}
		tmp["BoardId"] = item[0];
		tmp["PostId"] = item[1];
		MessTotal = ''
		MessFind = Collection.find({"PostId":item[1],"BoardId":item[0]},{"_id":False,"message":True},)
		for i in MessFind:
			MessTotal += i['message']
		tags = jieba.analyse.extract_tags(MessTotal, topK=40)
		tags = filter(tags_filter,tags)
		tmp["tags"] = tags
		print ",".join(tags)
		AnalyColl.insert(tmp)


def queue_info():
	while True:
		print "Queue size:", PostQueue.qsize()
		sleep(30)
	return


def main():
	ThreadList = []
	PostDict = {}
	
	res = Collection.find({"PageNum":{"$gt":30}},{"PostId":True,"BoardId":True,"_id":False},)
	for i in res:
		if i["BoardId"] in PostDict:
			PostDict[i["BoardId"]].add(i["PostId"])
		else:
			PostDict[i["BoardId"]] = Set([i["PostId"]])

	for i in PostDict:
		for j in PostDict[i]:
			print j
			PostQueue.put([i,j])

	print "Find Post Done"

	for i in range(10):
		i = Thread(target=post_analyse)
		ThreadList.append(i)

	queue_info_thread = Thread(target=queue_info)
	ThreadList.append(queue_info_thread)

	for thread_each in ThreadList:
		thread_each.start()

	for thread_each in ThreadList:
		thread_each.join()
	

if __name__ == '__main__':
	main()
