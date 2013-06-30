from cc98 import *
from bs4 import *
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


