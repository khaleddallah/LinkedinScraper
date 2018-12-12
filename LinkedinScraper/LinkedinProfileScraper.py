#! /usr/bin/env python
# Author : Khaled Dallah
# Date : 8-12-2018


import scrapy 
from scrapy.crawler import CrawlerProcess
import re , os
import json
from items import Person,Job


class LPS(scrapy.Spider):
	name='LPS'
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
	profileUrls=[]
	temp_output=[]
	outputFile=''



	def start_requests(self):
		self.inheaders['csrf-token']=self.incookies['JSESSIONID']
		print('\n... LPS cookies reached to LS : \n',self.incookies)
		print('\n... LPS Request of LS Spider')
		yield scrapy.Request(url=self.root_url,
				cookies=self.incookies,
				callback =self.reqProfiles)


	def reqProfiles(self,response):
		print('\n... LPS reqProfiles running')
		print('\n... LPS profileUrls is \n',self.profileUrls)
		self.chechCacheDir()
		for req in reversed(self.profileUrls):
			yield scrapy.Request(url=req,headers=self.inheaders,callback=self.parse)

		

	def parse(self,response):
		#search between lines about dataJson line
		self.temp_output.append(response.text)
		nameOfProfile=response.url.split('/')[4]
		for i in (response.text.split('\n')):
			t=re.findall('\s+{&quot;data&quot;:{&quot;\*profile.*',i)
			if (len(t)>0):
				dataJson=json.loads(t[0].replace('&quot;','\"'))
		self.saveToFile(nameOfProfile,dataJson)


	def saveToFile(self,name,dataJson):
		directory='cache'
		filePath='/'.join([directory,name])
		# with open(filePath,'w+') as f:
		# 	temp='\n\n'.join(self.temp_output)
		# 	f.write(temp)
		with open(filePath, "w") as json_file:
			json.dump(dataJson, json_file, indent=4)
			json_file.write("\n")  


	# def closed( self, reason ):
	# 	self.saveToFile()
	# 	print('numParsedProfile is :',self.numParsedProfile)
	

	def chechCacheDir(self):
		directory='cache'
		if not os.path.exists(directory):
			print('\n... LPS Directory created')
			os.makedirs(directory)		