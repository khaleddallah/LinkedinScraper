#! /usr/bin/env python

# Author : Khaled Dallah
# Email : khaled.dallah0@gmail.com
# Date : 8-12-2018


import scrapy 
from scrapy.crawler import CrawlerProcess
import re, os, sys
import json
import html

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
			print('\n... req: ',req)
			yield scrapy.Request(url=req,
				headers=self.inheaders,
				callback=self.parse)


		

	#Get profiles URLs
	def parse(self,response):
		#search between lines about dataJson line
		for i in (response.text.split('\n')):
			t=re.findall('\s+{&quot;data&quot;:{&quot;metadata.*',i)
			if (len(t)>0):
				temp1=html.unescape(t[0])
				try:
					dataJson=json.loads(temp1)
				except:
					print(sys.exc_info())
					print('\n!!! ERROR in make json from data of ',response.url)
					logFileName=self.outputFile+'.log'
					print('log file of tha data in ',logFileName)
					with open('cache/'+logFileName,'w+') as l:
						l.write(temp1)
					return(-1)


				# with open('cache/test.html','w+') as f:
				# 	json.dump(dataJson, f, indent=4, ensure_ascii = False)
				#Get Puplic ID
				AllElementsList=[]
				for e in range(len(dataJson["data"]["elements"])):
					elements=dataJson["data"]["elements"][e]["elements"]
					if(len(elements)>0):
						AllElementsList.append(elements)

				for elements1 in AllElementsList:	
					for j in elements1:
						try:
							tempUrl='https://www.linkedin.com/in/'+str(j["publicIdentifier"])
							print(tempUrl)
							self.profileUrls.append(tempUrl)
							self.numParsedProfile+=1
						except:
							print('\nNum '+str(self.numParsedProfile+1)+' profile is out of your network and you have limited visibility.')
					else:
						print('\n!!! ERROR : No Data Section found in :\n',response.url)


	#Save profiles URLs
	def saveToFile(self):
		#Check Cache Dir
		directory='cache'
		if not os.path.exists(directory):
			print('\n... Directory created')
			os.makedirs(directory)

		filePath='/'.join([directory,str(self.outputFile+'_searchPageUrl')])

		#Save profiles Urls
		with open(filePath,'w+') as f:
			temp='\n'.join(self.profileUrls)
			f.write(temp)
 


	def closed( self, reason ):
		self.saveToFile()
