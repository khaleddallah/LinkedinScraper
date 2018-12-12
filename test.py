import os,re

cookies_file_path='cache/temp5'
with open(cookies_file_path,'r+') as f:
	text=f.readlines()


# 	print(text,'\n\n\n')
print('=====================================')
res=[]
for t in text:
	a=re.findall('^\s+{&quot;data&quot;:{&quot;metadata.*',t)
	if(len(a)>0):
		res.append(a)

print('################')
print('res=\n\n')
print(res[:100])
print('=============')
print(res[-100:])
print('\n\nlen of res is :',len(res))