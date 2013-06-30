from cc98 import *
from bs4 import *
name = "ph-test"
password = "1qaz"

cc = cc98(name,password)

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

def main():
	url_soul = "http://www.cc98.org/list.asp?boardid=182"
	cc.login()
	UrlPost = "http://www.cc98.org/dispbbs.asp?boardID=182&ID=4213090&page=1"
	get_uid(UrlPost)

if __name__ == '__main__':
	main()
	for i in UserHashCount:
		print i,
		print ":",
		print UserHashCount[i]