from cc98 import *
from bs4 import *
import re
name = "ph-test"
password = "1qaz"

url_soul = "http://www.cc98.org/list.asp?boardid=182"
cc = cc98(name, password)
cc.login()
response = cc.opener.open(url_soul)

soup = BeautifulSoup(response.read())

title = soup.find_all('td', class_ = "tablebody1")

for i in title:
	tmp = i.find('a')
	try:
		print tmp['title']
		print tmp['href']
	except:
		pass

	NextPages = i.find_all('a')
	try:
		if len(NextPages) == 1:
			print "Only One"
		else:
			PageUrl = NextPages[-1]['href']
			PageLen = int(re.search(r'star=\d+',PageUrl).group()[5:])
			for k in range(1, PageLen+1):
				RepPageNum = 'star=' + str(k)
				VisitUrl = re.sub(r'star=\d+', RepPageNum, PageUrl)
				print VisitUrl


	except:
		pass



