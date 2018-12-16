#! /usr/bin/env python
# Author : Khaled Dallah
# Date : 8-12-2018


import scrapy 
from scrapy.crawler import CrawlerProcess
import re , os
import json
from items import Person,Job
from jsonAnalyser import JA

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
		done=False
		nameOfProfile=response.url.split('/')[4]
		for i in (response.text.split('\n')):
			t=re.findall('\s+{&quot;data&quot;:{&quot;\*profile.*',i)
			if (len(t)>0):
				try:
					t2=t[0].replace('&quot;','\"')
					t2=t2.replace('&#92;','\\')
					self.saveRawFile(nameOfProfile+'_json',t2)
					dataJson=json.loads(t2)
					done=True

				except Exception as e: 
					print("\n!!! ERROR in json loads DATA to dataJson :\n",e)
		if(done):
			print('\n... Profile : ',response.url)
			print('\n... DONE')
			self.saveRawFile(nameOfProfile,response.text)
			self.saveJsonFile(nameOfProfile,dataJson,response)
			self.parseImpData(dataJson,nameOfProfile)


		else:
			self.saveRawFile(nameOfProfile,response.text)
			print('\n... Profile : ',response.url)
			print('\n!!! ERROR in find Data Section in Profile')


	def saveRawFile(self,name,text1):
		directory='cache'
		rawFilePath='/'.join([directory,str(name+'_raw')])
		print('\n... writing file ',rawFilePath)
		with open(rawFilePath,'w+') as f:
			f.write(text1)


	def saveJsonFile(self,name,dataJson,response):
		directory='cache'
		filePath='/'.join([directory,name])
		with open(filePath, "w+") as json_file:
			try:
				json.dump(dataJson, json_file, indent=4)
				json_file.write("\n")
			except:
				print('\n!!! ERROR in Json extractor')


	# def closed( self, reason ):
	# 	self.saveToFile()
	# 	print('numParsedProfile is :',self.numParsedProfile)
	
	def parseImpData(self,dataJson,nameOfProfile):
		sw={
		'fs_profile':['firstName', 'lastName', 'locationName', 'headline'],
		'fs_position':['title', 'companyName', 'locationName' ],
		'fs_education':['degreeName', 'schoolName', 'fieldOfStudy', 'activities'],
		'fs_volunteerExperience':['companyName', 'role', 'cause'],
		'fs_skill':['name'],
		'fs_certification':['authority', 'name', 'licenseNumber'],
		'fs_course':['name'],
		'fs_language':['name','proficiency'],
		'fs_project':['title', 'description', 'url'],
		'fs_honor':['description', 'title', 'issuer']
			}
		ja=JA(dataJson,nameOfProfile,sw)
		ja.run()
		dataExtractor(ja.saveRes(),sw)





	def dataExtractor(self,sw):
		pass


	def chechCacheDir(self):
		directory='cache'
		if not os.path.exists(directory):
			print('\n... LPS Directory created')
			os.makedirs(directory)		




