#! /usr/bin/env python

# Author : Khaled Dallah
# Date : 8-12-2018

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

import scrapy 
from scrapy.crawler import CrawlerProcess
from LinkedinScraper import LS
from CookiesLinkedin import CL
from items import Person,Job
import argparse
import os , json

class MainClass :


	def __init__(self):
		self.incookies=dict()
		self.inheaders=dict()
		self.email=''
		self.password=''
		self.searchUrl=''
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
			incookies=self.incookies)
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
		parser.add_argument('keywords',help="Set search words")
		#parser.add_argument('-e','--email',dest='email',action='store',default='',type=str,
		#					help='Linkedin Email')

		args=parser.parse_args()

		#Create the search Url
		self.urlCreater(args)


	#Create Url using 
	def urlCreater(self,args):
		self.searchUrl='https://www.linkedin.com/in/raneem-khallouf-517892169'



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