#! /usr/bin/env python

# Author : Khaled Dallah
# Email : khaled.dallah0@gmail.com
# Date : 8-12-2018



import scrapy 
import os

class CL(scrapy.Spider):
	name='CL'
	allowed_domains=['www.linkedin.com']
	root_url = 'https://www.linkedin.com/'
	start_urls=[root_url]
	custom_settings ={
		'ROBOTSTXT_OBEY' : False,
		'DOWNLOAD_DELAY' : 0.25,
 		'COOKIES_ENABLED' : True,
		'COOKIES_DEBUG' : True,
		'USER_AGENT':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
	}

	incookies=dict()
	inheaders=dict()

	email=''
	password=''

	#FormData 
	def parse(self,response):
		print('\n... parse root_url')
		print('\n... Email: ',self.email)
		print('\n... Pass: ',self.password)
		

		#parse csrf param
		csrf_value=response.css('input[name="loginCsrfParam"]::attr(value)').extract()[0]
		data={
			'session_key' : self.email ,
			'session_password' : self.password ,
			'isJsEnabled' : 'false',
            'loginCsrfParam': csrf_value
		}
		print("\n... FormRequest")
		yield scrapy.FormRequest.from_response(response,
			formdata=data,
			callback=self.parse_cookies_headers)



	def parse_cookies_headers(self,response):
		print('\n... Parse Cookies and Headers')
		
		#Correct Cookies
		raw_cookies = response.request.headers.getlist('Cookie')[0].decode("utf-8").split('; ')
		for rcookie in raw_cookies:
			self.incookies[rcookie[:str.find(rcookie,'=')]]=rcookie[str.find(rcookie,'=')+1:].replace('"','')
		
		#Headers
		self.inheaders['csrf-token']=self.incookies['JSESSIONID']
		

		#Save Cookies in file 
		directory='cookie_files'
		if not os.path.exists(directory):
			os.makedirs(directory)
			
		filename='cookies'
		filePath='/'.join([directory,filename])

		with open(filePath ,'w+') as f:
			f.write(str(self.incookies))

		print('\n... Cookies file saved')