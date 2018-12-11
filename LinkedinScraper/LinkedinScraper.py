#! /usr/bin/env python
# Author : Khaled Dallah
# Date : 8-12-2018


import scrapy 
from scrapy.crawler import CrawlerProcess
import re , os
import json
from items import Person,Job


class LS(scrapy.Spider):
	name='LS'
	allowed_domains=['www.linkedin.com']
	root_url = 'https://www.linkedin.com/'
	custom_settings ={
		'ROBOTSTXT_OBEY' : False,
		'DOWNLOAD_DELAY' : 0.25 ,
 		'COOKIES_ENABLED' : True,
		'COOKIES_DEBUG' : True,
		'USER_AGENT':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
	}

	incookies=dict()
	inheaders=dict()
	urlRequests=[]
	temp_output=[]


	def start_requests(self):
		self.inheaders['csrf-token']=self.incookies['JSESSIONID']
		print('\n... cookies reached to LS : \n',self.incookies)
		print('\n... Request of LS Spider')
		yield scrapy.Request(url=self.root_url,
				cookies=self.incookies,
				callback =self.reqRequests)


	def reqRequests(self,response):
		print('\n... reqRequests running')
		print('\n... urlRequests is \n',self.urlRequests)
		for req in self.urlRequests:
			yield scrapy.Request(url=req,headers=self.inheaders,callback=self.parse)




	def parse(self,response):
		self.temp_output.append('\n')
		self.temp_output.append(str(response.request.headers))
		self.temp_output.append(str(response.text))
		



	def saveToFile(self):
		directory='cache'
		filename='temp2'
		filePath='/'.join([directory,filename])
		if not os.path.exists(directory):
			os.makedirs(directory)
		with open(filePath,'w+') as f:
			f.writelines(temp_output)


