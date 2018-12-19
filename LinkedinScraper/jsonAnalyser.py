#! /usr/bin/env python

# Author : Khaled Dallah
# Email : khaled.dallah0@gmail.com
# Date : 8-12-2018


import re 
import html

class JA:
	def __init__(self,jsonData,name,sw):
		self.name=name
		self.jsonData=jsonData
		self.out=[]
		#Level of depth
		self.lvl=0
		#index of current processing item
		self.index=[]
		#search Words
		self.sw=sw
		#result
		self.res=dict()


	#Write clear json Data to File
	# def saver(self):
	# 	directory='cache'
	# 	filePath='/'.join([directory,self.name+'_Data'])
	# 	with open(filePath, "w+") as json_file:
	# 		json_file.writelines(self.out)


	#process elements of list
	def listAn(self,list1):
		self.out.append('[\n')
		self.lvl+=1
		for i in range(len(list1)):
			#put the index of current item in index list
			self.index.append(i)
			self.out.append(str(self.lvl*4*' ')+'('+str(i)+') ')
			#self.search(i)
			self.chkprn(list1[i])
			#delete last index when we move to next
			self.index.pop()
		self.lvl-=1
		self.out.append(str(self.lvl*4*' ')+']\n')


	#process elements of Dict
	def dictAn(self,dict1):
		self.out.append('{\n')
		self.lvl+=1
		for i in dict1:
			#put the index of current item in index list
			self.index.append(i)
			self.out.append(str(self.lvl*4*' ')+i+' : ')
			#self.search(i)
			self.searchEU(i)
			self.chkprn(dict1[i])
			#delete last index when we move to next
			self.index.pop()		
		self.lvl-=1
		self.out.append(str(self.lvl*4*' ')+'}\n')


	#check the element
	#if it Str it will append directly
	#if Dict or List it will go to DictAn to process all its elements
	def chkprn(self,element):
		if(type(element)==str):
			#change some keys
			self.out.append(html.unescape(element)+'\n')
			#self.search(element)
		elif(type(element)==dict):
			self.dictAn(element)
		elif(type(element)==list):
			self.listAn(element)

	#Json file will go to chkprn() and that will send it to DictAn
	def run(self):
		self.chkprn(self.jsonData)
		# self.saver()


	#make searching about 
	def search(self,element):
		if (element in self.sw):
			if element not in self.res:
				self.res[element]=['.'.join(self.index)]
			else:
				self.res[element].append('.'.join(self.index))



	#search for "entityUrn" key (special for linkedin )
	def searchEU(self,element):
		if (element=="entityUrn"):
			valueOfEU=self.gValueOfCI(self.index)
			for i in self.sw:
				if (re.search('^urn:li:'+i+':.*',valueOfEU)):
					#add to all section that contain Important entityUrn 
					#(value of entityUrn exist in )
					if i not in self.res:
						self.res[i]=[self.gValueOfCI(self.index[:-1])]
					else:
						self.res[i].append(self.gValueOfCI(self.index[:-1]))


	#Get value of current Index
	def gValueOfCI(self,index1):
		temp=self.jsonData[index1[0]]
		for i in index1[1:]:
			temp=temp[i]
		return (temp)


	#Save ImpSec Of data and return it
	def saveRes(self):
		#sort dict
		sortedRes=dict()
		l=list(self.res.keys())
		l.sort()
		for i in l:
			sortedRes[i]=self.res[i]

		#save to file
		directory='cache'
		filePath='/'.join([directory,self.name+'_ImpSec'])
		with open(filePath, "w+") as json_file:
			json_file.writelines(str(sortedRes))

		return(self.res)





