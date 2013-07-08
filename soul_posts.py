# coding = utf-8
from cc98 import *
from bs4 import *
from thread import *
from Queue import *
import json
import cPickle
import re

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

#queue store the url to parse
UrlQueue = Queue()

#queue store the id and the length of the post
PostQueue = Queue()

#store the url of the pages
PageQueue = Queue()

ThreadList = []

#count the user post total
UserHashCount = {}

#user info
#{name:[postTotal,[postId]]}
UserPostInfo = {}

#according to the post, find each user
def get_uid(url):
	response = cc.opener.open(url)
	soup = BeautifulSoup(response.read())
	#one user every table
	for i in soup.find_all('table', class_ = "tableborder1"):
		 try:
		 	user = i.td.td.b.string
		 	if user in UserHashCount:
		 		UserHashCount[user] += 1
		 	else:
		 		UserHashCount[user] = 1
		 except:
		 	pass

#according to the post, find each user post what
def get_user_post(BoardId, id, len):
	url = DispSite + "?boardID=" + BoardId + "&ID=" + id + "&star" + len
	response = cc.opener.open(url)
	soup = BeautifulSoup(response.read())
	#one user every table
	for i in soup.find_all('table', class_ = "tableborder1"):
		 try:
		 	user = i.td.td.b.string
		 	if user in UserPostInfo:
		 		UserPostInfo[user][0] += 1
		 	else:
		 		UserPostInfo[user] = [1,[]]
		 		UserPostInfo[user][0] = 1
		 	UserPostInfo[user][1] = id_set(id,UserPostInfo[user][1])
		 except:
		 	pass

#according to the page, find each post
def get_url(PageUrl):
	response = cc.opener.open(PageUrl)
	soup = BeautifulSoup(response.read())
	#each post
	for i in soup.find_all('td', class_ = "tablebody1"):
		try:
			UrlHref = i.find_all('a')
			if len(UrlHref) == 1:
				UrlQueue.put(UrlSite+UrlHref[0]['href'])
			else:
				PagePattern = re.compile(r'star=\d+')
				#the link to the last page of the post
				LastPage = UrlHref[-1]['href']
				PageLen = int(PagePattern.search(LastPage).group()[5:])
				for i in range(1, PageLen+1):
					RepNum = 'star=' + str(i)
					PageUrl = PagePattern.sub(RepNum,LastPage)
					UrlQueue.put(UrlSite+PageUrl)
		except:
			pass

#post id set for user
def id_set(id, li):
	if id in li:
		return li
	else:
		li.append(id)
		return li


#according to the page, find the post and the length
def get_post(PageUrl):
	response = cc.opener.open(PageUrl)
	soup = BeautifulSoup(response.read())
	#find the ID of the post
	IdPattern = re.compile(r'&ID=\d+')
	BoardIdPattern = re.compile(r'boardID=\d+')
	#each post, find the ID of the post
	for i in soup.find_all('td', class_ = "tablebody1"):
		try:
			UrlHref = i.find_all('a')
			PostId = IdPattern.search(UrlHref[0]['href']).group()[4:]
			BoardId = BoardIdPattern.search(UrlHref[0]['href']).group()[8:]
			if len(UrlHref) == 1:
				PageLen = 1
			else:
				PagePattern = re.compile(r'star=\d+')
				#the link to the last page of the post
				LastPage = UrlHref[-1]['href']
				PageLen = int(PagePattern.search(LastPage).group()[5:])
			PostQueue.put([BoardId,PostId,PageLen])
		except:
			pass

#according to the board, find the pages
def get_page(BoardId, len = 10):
	PageExtend = "?boardid=" + str(BoardId) + "&page="
	for i in range(1,len+1):
		PageSuffix = PageExtend + str(i)
		PageQueue.put(ListSite+PageSuffix)


def main():
	cc.login()
	get_page(BoarIdInfo["love"],10)
	while not PageQueue.empty():
		a = PageQueue.get()
		#print a
		get_post(a)
		while not PostQueue.empty():
			t = PostQueue.get()
			for i in range(1,t[2]+1):
				get_user_post(t[0],t[1],str(i))

	FileName = "user.json"
	FileStore = file(FileName, "w")
	StoreInfo = json.dumps(UserPostInfo)
	cPickle.dump(StoreInfo, FileStore)
	FileStore.close()
	#Sort the Dict
	b = sorted(UserPostInfo.items(), key=lambda d:len(d[1][1]), reverse = True)

	for i in b:
		print i[0],
		print ":",
		info = i[1]
		print "post", info[0], "total, occured in", len(info[1]), "posts."

if __name__ == '__main__':
	main()
