#! /usr/bin/env python

# Author : Khaled Dallah
# Email : khaled.dallah0@gmail.com
# Date : 8-12-2018


import scrapy 
from scrapy.crawler import CrawlerProcess
import re , os
import json
from jsonAnalyser import JA
import html

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
	FinalRess=[]
	numOfp=0
	format1=''

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
		for req in reversed(self.profileUrls[:self.numOfp]):
			yield scrapy.Request(url=req,headers=self.inheaders,callback=self.parse)

		
	#get Data Section from response
	def parse(self,response):
		#search between lines about dataJson line
		done=False
		nameOfProfile=response.url.split('/')[4]
		for i in (response.text.split('\n')):
			t=re.findall('\s+{&quot;data&quot;:{&quot;\*profile.*',i)
			if (len(t)>0):
				try:
					t2=html.unescape(t[0])
					dataJson=json.loads(t2)
					done=True
				except Exception as e: 
					print("\n!!! ERROR in json loads DATA to dataJson :\n",e)
		if(done):
			print('\n... Profile : ',response.url)
			print('\n... DONE')
			self.parseImpData(dataJson,nameOfProfile)
		else:
			print('\n... Profile : ',response.url)
			print('\n!!! ERROR in find Data Section in Profile')



	#Save Json file of jsonData
	def saveJsonFile(self,name,dataJson):
		directory='cache'
		filePath='/'.join([directory,name])
		with open(filePath, "w+") as json_file:
			try:
				json.dump(dataJson, json_file, indent=4, ensure_ascii = False)
				#json_file.write("\n")
			except:
				print('\n!!! ERROR in Json extractor')


	#Get ImpData Of ImpSection Of Data
	def parseImpData(self,dataJson,nameOfProfile):
		sw={
		'fs_profile':[{'firstName':'', 'lastName':'','summary':'', 'locationName':'', 'headline':''}],
		'fs_position':[{'title':'', 'companyName':'', 'locationName':'' }],
		'fs_education':[{'degreeName':'', 'schoolName':'', 'fieldOfStudy':'', 'activities':''}],
		'fs_volunteerExperience':[{'companyName':'', 'role':'', 'cause':''}],
		'fs_skill':[{'name':''}],
		'fs_certification':[{'authority':'', 'name':'', 'licenseNumber':''}],
		'fs_course':[{'name':''}],
		'fs_language':[{'name':'','proficiency':''}],
		'fs_project':[{'title':'', 'description':'', 'url':''}],
		'fs_honor':[{'description':'', 'title':'', 'issuer':''}],
		'fs_miniProfile':[{'picture':{},'firstName':''}]
			}
		ja=JA(dataJson,nameOfProfile,sw)
		ja.run()
		FinalData=self.dataExtractor(ja.saveRes(),sw)
		print('\n............................................\n')
		FinalData['fs_miniProfile']=[self.diu(FinalData['fs_miniProfile'],FinalData['fs_profile'][0]['firstName'])]
		self.saveJsonFile(nameOfProfile+'_finalRes',FinalData)
		self.FinalRess.append(FinalData)



	#Filter Important Section from plus Data
	def dataExtractor(self,impData,sw):
		#Final Data
		fData=impData
		#loop for all data
		for i in impData:
			#loop for saved list in single essential key
			for j in range(len(impData[i])):
				#loop for single item in list
				for k in list(impData[i][j]):
					if k not in sw[i][0]:
						del fData[i][j][k]

		return(fData)




	#Get Img Url
	def diu(self,imgSection,name):
		tempUrl=''
		for i in imgSection:
			if (i['firstName']==name):
				try:
					firstSec=i['picture']['rootUrl']
					secondSec=html.unescape(i['picture']['artifacts'][-1]['fileIdentifyingUrlPathSegment'])
					tempUrl=firstSec+secondSec
				except:
					print('\n!!! ERROR in parse picture')
		return(tempUrl)




	def chechCacheDir(self):
		directory='cache'
		if not os.path.exists(directory):
			print('\n... LPS Directory created')
			os.makedirs(directory)		



	def closed( self, reason ):
		#save output.json in Output Dir
		if(self.format1=='all' or self.format1=='json'):
			self.saveJsonFile('../Output/'+self.outputFile+'.json',self.FinalRess)
