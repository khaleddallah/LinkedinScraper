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

	def saver(self):
		directory='cache'
		filePath='/'.join([directory,self.name+'_JA'])
		with open(filePath, "w+") as json_file:
			json_file.writelines(self.out)


	#process elements of list
	def listAn(self,list1):
		self.out.append('[\n')
		self.lvl+=1
		for i in range(len(list1)):
			#put the index of current item in index list
			self.index.append(str(i))
			self.out.append(str(self.lvl*4*' ')+'('+str(i)+') ')
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
			self.out.append(element+'\n')
			self.search(element)
		elif(type(element)==dict):
			self.dictAn(element)
		elif(type(element)==list):
			self.listAn(element)

	#Json file will go to chkprn() and that will send it to DictAn
	def run(self):
		self.chkprn(self.jsonData)
		self.saver()


	#make searching about 
	def search(self,element):
		if (element in self.sw):
			print('\n... index of ('+element+') is : '+'.'.join(self.index))





