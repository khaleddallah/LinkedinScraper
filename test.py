
searchUrl='https://www.linkedin.com/search/results/all/?keywords=Robotic&origin=GLOBAL_SEARCH_HEADER&page=2'
#build final urls
if('page' not in searchUrl):
	finalUrls.append(searchUrl)
	nosp-=1
else:
	a=searchUrl.find('page')
	part1=searchUrl[:(a-1)]
	
	temp_part2=searchUrl[a:]
	b=temp_part2.find('&')
	if(b=-1):
		searchUrl=part1
	else:
		searchUrl=part1+searchUrl[]


for i in range(nosp):
	finalUrls.append(searchUrl+'$page='+str(i+2))