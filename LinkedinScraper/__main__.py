#! /usr/bin/env python

# Author : Khaled Dallah
# Date : 8-12-2018

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

import scrapy 
from LinkedinScraper import LS
from CookiesLinkedin import CL
from items import Person,Job
import argparse
import os , json ,re

class MainClass :


	def __init__(self):
		self.incookies=dict()
		self.inheaders=dict()
		
		self.email=''
		self.password=''
		
		self.finalUrls=[]
		
		self.outputFile=''

		self.cookiesParserEnable=False
		
		configure_logging()
		self.runner = CrawlerRunner()



	#build spiders
	@defer.inlineCallbacks
	def crawl(self):
		if(self.cookiesParserEnable):
			yield self.runner.crawl(CL,email=self.email
				,password=self.password)
			self.incookies=CL.incookies
		
		yield self.runner.crawl(LS,
			incookies=self.incookies,
			finalUrls=self.finalUrls)
		reactor.stop()



	#Read Cookies from cookies file
	def readCookiesFile (self):
		cookies_file_path='cookie_files/cookies'
		if(os.path.exists(cookies_file_path)):
			print("\n... cookies file exists")
			
			#read cookies file and parse it
			with open(cookies_file_path,'r+') as f:
				cookies_text=f.readline()

			#parse cookies and headers
			self.incookies=json.loads(cookies_text.replace('\'','\"'))
			return (True)

			#if Cookies expired
			###########

		else:
			print("\n... cookies file not exists")
			return (False)



	#Parse user input arguments
	def args_parser(self):
		#Parse arguments
		parser=argparse.ArgumentParser(description='Linkedin Scraper\nAuthor: Khaled Dallah',
									 formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('searchUrl',help="URL of Linkedin search")
		parser.add_argument('-n','--num',dest='num',action='store',default='10',type=str,
							help='''num of profiles
							** the number must be lower or equal of result number
							\'page\' will parse profiles of url page (10 profiles) (Default)''')
		parser.add_argument('-o','--output',dest='output',action='store',default='NULL',type=str,
					help='Output file')
		args=parser.parse_args()

		self.UrlsCreator(args.searchUrl, args.num, args.output)



	#parse args and build final urls
	def UrlsCreator(self,searchUrl,num,output):
		nosp=0 #Num of Search Pages

		#num
		if(num=='first'):
			nosp=1
		else:
			nosp=self.getNosp(self.CCN(num))

		#output 
		if (output=='NULL'):
			#get keyword value
			self.outputFile=re.findall('.*keywords=(.*?)&.*',searchUrl)[0].replace('%20','_')
		else:
			self.outputFile=output

		#build final urls
		if('page' not in searchUrl):
			init_page_num=0
			self.finalUrls.append(searchUrl)
			nosp-=1
		else:
			init_page_num=int(re.findall('.*page=([0-9]*).*',searchUrl)[0])-2
			a=searchUrl.find('page')
			part1=searchUrl[:(a-1)]
			
			temp_part2=searchUrl[a:]
			b=temp_part2.find('&')
			if(b==-1):
				searchUrl=part1
			else:
				part2=temp_part2[(b):]
				searchUrl=part1+part2

		for i in range(nosp):
			temp_url=searchUrl+'&page='+str(init_page_num+i+2)
			print(i,' : ',temp_url)
			self.finalUrls.append(temp_url)






	#Check Correct Num
	def CCN(self,num):
		try:
			return(int(num))
		except:
			print('\n... NUM is wrong\n')
			exit(0)


	#get the nosp(Num of search page):
	def getNosp(self,num):
		nosp=0
		nosp=num//10
		if((num%10)>0):
			nosp+=1
		return (nosp)



	#Read Email and Password from User
	def readAccount(self):
		self.email=input('\n... Enter Linkedin email: ')
		self.password=input('\n... Enter Linkedin password: ')





	def main(self):
		self.args_parser()

		#If Cookies file not exists
		if (not(self.readCookiesFile())):
			self.readAccount()
			self.cookiesParserEnable=True

		#Run Spiders
		self.crawl()
		reactor.run()



if __name__ == '__main__':
	mainClass=MainClass()
	mainClass.main()