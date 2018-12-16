from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
import json
import numpy as np


class Ete :
	#Set the Input & Output 	
	def __init__(self,name,data):
		self.filePath='../Output/'+name
		self.data=data


	#Open Excel file and first sheet 
	def open_file_sheet(self):
		self.wb = Workbook()
		self.ws1 = self.wb.create_sheet(title="first")

	#Save Excel file
	def save_file(self):
		self.wb.save(filename = self.filePath)



	#Write header data to Exel file
	def write_header(self):
		al = Alignment(horizontal="center", vertical="center")


		#additon for merge cell
		amc=1
		for i in self.data:
			temp=self.ws1.cell(column=amc , row=1 , value=i )
			temp.alignment=al
			shift=len(self.data[i][0])
			#print ('merge from ',i,'to',i+shift)
			self.ws1.merge_cells(start_row=1, start_column=amc, end_row=1, end_column=amc+shift-1)
			print("\n... Printing ",i,"in col ",amc,' and make marge from ',amc,' to ',amc+shift-1)
			subind=0
			for j in self.data[i][0]:
				temp=self.ws1.cell(column=amc+subind , row=2 , value=j )
				temp.alignment=al
				subind+=1

			amc+=shift




	def run(self):
		self.open_file_sheet()
		self.write_header()
		self.save_file()



def main():
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
	pathh='../cache/jawad-mash_finalRes'
	with open(pathh,'r+') as f:
		jsonData=json.load(f)


	ete1=Ete('aa.xlsx',sw)
	ete1.run()



if __name__=='__main__':
	main()