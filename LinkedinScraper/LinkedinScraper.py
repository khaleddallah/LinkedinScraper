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
	finalUrls=[]
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
		print('\n... finalUrls is \n',self.finalUrls)
		for req in self.finalUrls:
			yield scrapy.Request(url=req,headers=self.inheaders,callback=self.parse)

		


	def parse(self,response):
		for i in (response.text.split('\n')):
			t=re.findall('\s+{&quot;data&quot;:{&quot;metadata.*',i)
			if (len(t)>0):
				dataJson=json.loads(t[0].replace('&quot;','\"'))
				for j in (dataJson["data"]["elements"][0]["elements"]):
					self.temp_output.append(j["publicIdentifier"])
					self.temp_output.append('\n\n')
				
	


	def saveToFile(self):
		directory='cache'
		filename='temp5'
		filePath='/'.join([directory,filename])
		if not os.path.exists(directory):
			print('\n... Directory created')
			os.makedirs(directory)
		with open(filePath,'w+') as f:
			f.writelines(self.temp_output)
		# with open("foobar.json", "w") as json_file:
		# 	json.dump(self.temp_output[0], json_file, indent=4)
		# 	json_file.write("\n")  


	def closed( self, reason ):
		self.saveToFile()
