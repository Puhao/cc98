# coding= utf-8
import re


import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

def tags_filter(tag):
	ReFilter = []
	ReFilter.append(re.compile(r'^\d+$'))
	ReFilter.append(re.compile(r'^\w+$'))
	for i in ReFilter:
		if i.match(tag):
			return False
	ChiFilter = ["楼主", "匿名", "引用", "发言", "以下"]
	if tag in ChiFilter:
		return False
	else:
		return True

tags = ["2324","em23","我知道", "发疯", "lz", "以下"]

a = filter(tags_filter,tags)

print a