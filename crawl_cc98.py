# coding= utf-8
from cc98 import *
from bs4 import *
from threading import *
from Queue import *
from time import *
import json
import re

from pymongo import MongoClient
#DBClient = MongoClient()
DBClient = MongoClient('112.124.9.75')
DBSave = DBClient["test"]
Collection = DBSave["love"]
DBLog = DBClient["log"]
LogColl = DBLog["Error"]

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


cc = cc98(name,password)

#Page to be parsed Queue
PageToParseQueue = Queue()

<<<<<<< HEAD
=======
def queue_info():
	while True:
		print "PageToParseQueue:",PageToParseQueue.qsize()
		print "BoadrPageQueue:", BoadrPageQueue.qsize()
		sleep(30)

>>>>>>> add error log
def save_post_info():
	while True:
		PageInfo = PageToParseQueue.get()
		BoardId = PageInfo[0]
		PostId = PageInfo[1]
		PageNum = PageInfo[2]
		url = DispSite + "?boardID=" + BoardId + "&ID=" + PostId + "&star=" + PageNum
		try:
			response = cc.opener.open(url)
			soup = BeautifulSoup(response.read(), "lxml")
		except:
			print "Http Request Error"
			ErrInfo = {}
			ErrInfo["PageInfo"] = PageInfo
			ErrInfo["BoardId"] = BoardId
			ErrInfo["PostId"] = PostId
			ErrInfo["PageNum"] = PageNum
			LogColl.insert(ErrInfo)
			pass
		#each floor
		for i in soup.find_all('table', class_ = "tableborder1"):
			 try:
			 	info_tr1 = i.tr
			 	info_tr2 = info_tr1.next_sibling.next_sibling
			 	info_tr1_td1 = info_tr1.td
			 	info_tr1_td2 = info_tr1_td1.next_sibling.next_sibling
			 	FloorInfo = {}
			 	FloorInfo["user"] = info_tr1_td1.td.b.string
			 	FloorInfo["floor"] = ''.join(info_tr1_td2.tr.get_text().split())
			 	TimeData = info_tr2.td.contents[2].string
			 	FloorInfo["date"] = re.search(r'\d+/\d+/\d+', TimeData).group()
			 	FloorInfo["time"] = re.search(r'\d+:\d+:\d+\s\w+', TimeData).group()
			 	FloorInfo["message"] = info_tr1_td2.blockquote.span.get_text()
			 	FloorInfo["location"] = [BoardId, PostId, PageNum]
			 	try:
			 		Collection.insert(FloorInfo)			 		
			 	except:
			 		print "MongoDB insert Error!"
			 except:
			 	pass
	return

#according to the board, calculate the pages
BoardQueue = Queue()
BoadrPageQueue = Queue()
def parse_board():
	while True:
		BoardId = BoardQueue.get()
		BoardUrl = ListSite + "?boardid=" + BoardId
		try:
			response = cc.opener.open(BoardUrl)
			soup = BeautifulSoup(response.read(), "lxml")
		except:
			print "Board Parse Request Error!"
		Info = soup.body.form.next_sibling.next_sibling.td.get_text()
		BoardLen = re.search(r'1/\d+', Info).group()[2:]
		for i in range(1,int(BoardLen)+1):
			BoadrPageQueue.put([BoardId, str(i)])
	return

#parse each page to find the length of each post in this page
def parse_page():
	while True:
		BoardId, BoardPage = BoadrPageQueue.get()
		PageUrl = ListSite + "?boardid=" + BoardId + "&page=" + BoardPage
		try:
			response = cc.opener.open(PageUrl)
			soup = BeautifulSoup(response.read(), "lxml")
		except:
			print "Page Parse Request Error!"
		#find the ID of the post
		IdPattern = re.compile(r'&ID=\d+')
		for i in soup.find_all('td', class_ = "tablebody1"):
			try:
				UrlHref = i.find_all('a')
				PostId = IdPattern.search(UrlHref[0]['href']).group()[4:]
				if len(UrlHref) == 1:
					PostLen = 1
				else:
					PagePattern = re.compile(r'star=\d+')
					#the link to the last page of the post
					LastPage = UrlHref[-1]['href']
					PostLen = int(PagePattern.search(LastPage).group()[5:])
				for i in range(1, PostLen+1):
					PageToParseQueue.put([BoardId, PostId, str(i)])
			except:
				pass
	return
		
def queue_info():
	while True:
		print "PageToParseQueue:", PageToParseQueue.qsize()
		print "BoardQueue:", BoardQueue.qsize()
		print "BoadrPageQueue", BoadrPageQueue.qsize()
		sleep(30)


BoardList = ["182"]
def get_board():
	for i in BoardList:
		BoardQueue.put(i)
	return

ThreadList = []
def main():
	cc.login()

	queue_info_thread = Thread(target=queue_info)
	ThreadList.append(queue_info_thread)

	get_board_thread = Thread(target=get_board)
	ThreadList.append(get_board_thread)
	
	parse_board_thread = Thread(target=parse_board)
	ThreadList.append(parse_board_thread)

	for i in range(0,2):
		i = Thread(target=parse_page)
		ThreadList.append(i)

	for i in range(0,10):
		i = Thread(target=save_post_info)
		ThreadList.append(i)

	for thread_each in ThreadList:
		thread_each.start()

	for thread_each in ThreadList:
		thread_each.join()

if __name__ == '__main__':
	main()
