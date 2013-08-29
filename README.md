CC98
====

#爬虫
设定板块的ID号，然后爬虫开始去追踪版面信息，把该板块的每个帖子里，每层楼的发帖者，发帖时间，楼层，发帖内容，改帖子信息存储到MongoDB数据库。  
#依赖库
1.	Beautifusoup4  
	用来解析HTML页面，定位和提取HTML页面里面所需存储的信息。  
	```
	pip install beautifulsoup4
	```
2.	lxml  
	Beautifulsoup使用的第三方解析器  
	```
	pip install lxml
	```
3.	pymongo  
	MongoDB的python接口  
	```
	pip install pymongo	
	```
4.	jieba  
	用于分词  
	`` pip install jieba ``
	
