from cc98 import *
from bs4 import *
from thread import *
from Queue import *
import re

name = "ph-test"
password = "1qaz"

UrlSite = "http://www.cc98.org/"

cc = cc98(name,password)

UrlQueue = Queue()

UserHashCount = {}

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

def get_url(BoardUrl):
	response = cc.opener.open(BoardUrl)
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



def main():
	url_soul = "http://www.cc98.org/list.asp?boardid=182"

	cc.login()
	UrlPost = "http://www.cc98.org/dispbbs.asp?boardID=182&ID=4213090&page=1"
	get_url(url_soul)
	while not UrlQueue.empty():
		#
		get_uid(UrlQueue.get())
		#print UrlQueue.get()
	#
	#for i in UserHashCount:
	#	print i,
	#	print ":",
	#	print UserHashCount[i]
	#
	#Sort the Dict
	b = sorted(UserHashCount.items(), key=lambda d:d[1], reverse = True)
	for i in b:
		print i[0],
		print ":",
		print i[1]

if __name__ == '__main__':
	main()
