#! /usr/bin/env python

# Author : Khaled Dallah
# Email : khaled.dallah0@gmail.com
# Date : 8-12-2018


from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import scrapy 

from LinkedinScraper import LS
from LinkedinProfileScraper import LPS
from CookiesLinkedin import CL
from ExportToExcel import Ete


import argparse
import os , json ,re

class MainClass :


	def __init__(self):
		self.incookies=dict()
		self.inheaders=dict()
		
		self.email=''
		self.password=''
		
		self.searchPageUrls=[]
		
		self.outputFile=''

		self.CLenable=False
		self.LSenable=False
		self.LPSenable=False
		
		self.profileUrls=[]

		self.finalData=[]


		self.format=''
		self.mode=''
		configure_logging()
		self.runner = CrawlerRunner()


	#build spiders
	@defer.inlineCallbacks
	def crawl(self):
		print('\n... CLenable : ',self.CLenable)
		print('\n... LSenable : ',self.LSenable)
		print('\n... LPSenable : ',self.LPSenable)
		if(self.CLenable):
			print('\n... CL')
			yield self.runner.crawl(CL,email=self.email,
				password=self.password)
			self.incookies=CL.incookies
		if(self.LSenable):
			print('\n... LS')
			yield self.runner.crawl(LS,
				incookies=self.incookies,
				searchPageUrls=self.searchPageUrls,
				outputFile=self.outputFile)
			self.profileUrls=LS.profileUrls
		if(self.LPSenable):
			print('\n... LPS')
			yield self.runner.crawl(LPS,
					incookies=self.incookies,
					profileUrls=self.profileUrls,
					outputFile=self.outputFile,
					numOfp=self.numOfp,
					format1=self.format)
			self.finalData=LPS.FinalRess
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
		example_text='''


Examples:
 $ python LinkedinScraper -p -o 'khaled-dallah' 'https://www.linkedin.com/in/khaled-dallah/'
 $ python LinkedinScraper -n 23 'https://www.linkedin.com/search/results/all/?keywords=Robotic&origin=GLOBAL_SEARCH_HEADER'

		'''

		#Parse arguments
		parser=argparse.ArgumentParser(description='Linkedin Scraper\nAuthor: Khaled Dallah',
									 formatter_class=argparse.RawTextHelpFormatter,
									 epilog=example_text,
									 usage='python LinkedinScraper [-h] [-n NUM] [-o OUTPUT] [-p] [-f format] [-m excelMode] (searchUrl or profilesUrl)')
		parser.add_argument('searchUrl',help="URL of Linkedin search URL or Profiles URL",nargs='+')
		parser.add_argument('-n',dest='num',action='store',type=str,default='page',
							help='''num of profiles
** the number must be lower or equal of result number
\'page\' will parse profiles of url page (10 profiles) (Default)''')
		parser.add_argument('-o',dest='output',action='store',default='NULL',type=str,
					help='Output file')
		parser.add_argument('-p',dest='profiles',action='store_true',default=False,
					help='Enable Parse Profiles')
		parser.add_argument('-f',dest='format',action='store',default='all',
					help='json    Json output file\nexcel    Excel file output\nall    Json and Excel output files')
		parser.add_argument('-m',dest='excelMode',action='store',default='m',
					help='1    to make each profile in Excel file appear in one row\nm    to make each profile in Excel file appear in multi row')
		args=parser.parse_args()
		self.UrlsCreator(args.searchUrl, args.num, args.output, args.profiles, args.format, args.excelMode)



	#parse args and build searchPage urls
	def UrlsCreator(self, searchUrl, num, output, profiles, format1, mode):
		#Profile mode
		if(profiles):
			#print('\n...Output!@# ',output)
			self.LSenable=False
			self.LPSenable=True
			self.profileUrls=searchUrl
			self.numOfp=len(self.profileUrls)
			#must make error to put output if not set
			if (output=='NULL'):
				print('\n!!!ERROR : No name for output file\n')
				print('\n!!!Please set name for output file by -o option')
				exit()
			else:
				self.outputFile=output

		
		#Multi mode
		else:
			self.LSenable=True
			self.LPSenable=True

			#Num of Search Pages
			nosp=0 

			if(num=='page'):
				nosp=1
			else:
				nosp=self.getNosp(self.CCN(num))
				self.numOfp=int(num)



			#output 
			print('\n... Parsing Output name File')
			if (output=='NULL'):
				#get keyword value
				self.outputFile=re.findall('.*keywords=(.*?)&.*',searchUrl[0])[0].replace('%20','_')
			else:
				self.outputFile=output
			print('\n... ArgParser (fileName):',self.outputFile)


			#build searchPage urls
			if('page' not in searchUrl[0]):
				init_page_num=0
				self.searchPageUrls.append(searchUrl[0])
				nosp-=1
			else:
				init_page_num=int(re.findall('.*page=([0-9]*).*',searchUrl[0])[0])-2
				a=searchUrl[0].find('page')
				part1=searchUrl[0][:(a-1)]
				
				temp_part2=searchUrl[0][a:]
				b=temp_part2.find('&')
				if(b==-1):
					searchUrl[0]=part1
				else:
					part2=temp_part2[(b):]
					searchUrl[0]=part1+part2

			for i in range(nosp):
				temp_url=searchUrl[0]+'&page='+str(init_page_num+i+2)
				print(i,' : ',temp_url)
				self.searchPageUrls.append(temp_url)


		#Output File
		self.format=format1

		#Mode of Excel
		self.mode=mode









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
			self.CLenable=True

		#Run Spiders
		print('\n... CRAWL')
		self.crawl()
		reactor.run()


		#Export to Excel
		if(self.format=='all' or self.format=='excel'):
			print('\n...Making Excel File')
			ete1=Ete(self.outputFile,self.finalData,self.mode)
			ete1.run()



if __name__ == '__main__':
	mainClass=MainClass()
	mainClass.main()