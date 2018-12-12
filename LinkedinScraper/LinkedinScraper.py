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
	searchPageUrls=[]
	outputFile=''
	profileUrls=[]
	numParsedProfile=0



	def start_requests(self):
		self.inheaders['csrf-token']=self.incookies['JSESSIONID']
		print('\n... cookies reached to LS : \n',self.incookies)
		print('\n... Request of LS Spider')
		yield scrapy.Request(url=self.root_url,
				cookies=self.incookies,
				callback =self.reqRequests)


	def reqRequests(self,response):
		print('\n... reqRequests running')
		print('\n... searchPageUrls is \n',self.searchPageUrls)
		for req in reversed(self.searchPageUrls):
			yield scrapy.Request(url=req,headers=self.inheaders,callback=self.parse)

		


	def parse(self,response):
		#search between lines about dataJson line
		for i in (response.text.split('\n')):
			t=re.findall('\s+{&quot;data&quot;:{&quot;metadata.*',i)
			if (len(t)>0):
				dataJson=json.loads(t[0].replace('&quot;','\"'))
				#Get Puplic ID
				for j in (dataJson["data"]["elements"][0]["elements"]):
					try:
						self.profileUrls.append('https://www.linkedin.com/in/'+str(j["publicIdentifier"]))
						self.numParsedProfile+=1
					except:
						print('\nNum '+str(self.numParsedProfile+1)+' profile is out of your network and you have limited visibility.')


	def saveToFile(self):
		directory='cache'
		filePath='/'.join([directory,str(self.outputFile+'_searchPageUrl')])
		if not os.path.exists(directory):
			print('\n... Directory created')
			os.makedirs(directory)
		with open(filePath,'w+') as f:
			temp='\n'.join(self.profileUrls)
			f.write(temp)
		# with open("foobar.json", "w") as json_file:
		# 	json.dump(self.temp_output[0], json_file, indent=4)
		# 	json_file.write("\n")  


	def closed( self, reason ):
		self.saveToFile()
		print('numParsedProfile is :',self.numParsedProfile)
