# coding= utf-8
from cc98 import *
from bs4 import *
from thread import *
from Queue import *
import json
import re

from pymongo import MongoClient
DBClient = MongoClient('10.110.91.236')
DBSave = DBClient["test"]
Collection = DBSave["test"]


name = "ph-test"
password = "1qaz"

UrlSite = "http://www.cc98.org/"

#display site
DispSite = "http://www.cc98.org/dispbbs.asp" 

#list post site
ListSite = "http://www.cc98.org/list.asp"


#the boardID of the each board
BoarIdInfo = {
	"soul":182,
	"love":152
}

#each floor in contain information
FloorInfo = {
	"user":"",
	"floor":"",
	"time":"",
	"date":"",
	"message":"",
	"location":[],
}

cc = cc98(name,password)

def print_post_info(BoardId, PostId, PageNum):
	url = DispSite + "?boardID=" + BoardId + "&ID=" + PostId + "&star=" + PageNum
	response = cc.opener.open(url)
	soup = BeautifulSoup(response.read())
	#each floor
	for i in soup.find_all('table', class_ = "tableborder1"):
		 try:
		 	info_tr1 = i.tr
		 	info_tr2 = info_tr1.next_sibling.next_sibling
		 	info_tr1_td1 = info_tr1.td
		 	info_tr1_td2 = info_tr1_td1.next_sibling.next_sibling
		 	FloorInfo["user"] = info_tr1_td1.td.b.string
		 	FloorInfo["floor"] = ''.join(info_tr1_td2.tr.get_text().split())
		 	TimeData = info_tr2.td.contents[2].string
		 	FloorInfo["date"] = re.search(r'\d+/\d+/\d+', TimeData).group()
		 	FloorInfo["time"] = re.search(r'\d+:\d+:\d+\s\w+', TimeData).group()
		 	FloorInfo["message"] = info_tr1_td2.blockquote.span.get_text()
		 	FloorInfo["location"] = [BoardId, PostId, PageNum]
		 	for i in FloorInfo:
		 		print i,
		 		print ":", FloorInfo[i]
		 	print "---------"
		 except:
		 	pass

def main():
	cc.login()
	print_post_info("147","4219781","2")
	#Collection.insert(FloorInfo)

if __name__ == '__main__':
	main()