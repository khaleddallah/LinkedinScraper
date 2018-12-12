
import argparse

parser=argparse.ArgumentParser(description='Linkedin Scraper\nAuthor: Khaled Dallah',
							 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('Search URL or Profiles URL',help="URL of Linkedin search",nargs='+')
parser.add_argument('-n','--num',dest='num',action='store',type=str,default='page',
					help='''num of profiles
					** the number must be lower or equal of result number
					\'page\' will parse profiles of url page (10 profiles) (Default)''')
parser.add_argument('-o','--output',dest='output',action='store',default='NULL',type=str,
			help='Output file')
parser.add_argument('-p','--profile',dest='profiles',action='store_true',default=False,
			help='Enable Parse Profiles')

args=parser.parse_args()

print(args)