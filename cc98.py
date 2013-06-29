import hashlib
import urllib
import urllib2
import cookielib

class cc98():
	def __init__(self, name, pwd):
		self.name = name
		self.pwd = pwd = hashlib.md5(pwd).hexdigest()
		self.cj = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

	def login(self):
		params = {
				'a':'i',
				'u':self.name,
				'p':self.pwd,
				'userhidden':1
		}

		data = urllib.urlencode(params)
		LogUrl = "http://www.cc98.org/sign.asp"
		try:
			req = urllib2.Request(LogUrl, data)
		except:
			print "Request Error!"
			print req

		try:
			response = self.opener.open(req)
		except:
			print "Open Error!"
			print response

def main():
	name = "ph-test"
	password = "1qaz"
	url_soul = "http://www.cc98.org/list.asp?boardid=182"
	cc = cc98(name, password)
	cc.login()
	response = cc.opener.open(url_soul)
	print response.read()

if __name__ == '__main__':
	main()


