# Linkedin Scraper Project    

* Scrape number of profiles that exist in result of Linkedin searchUrl.    
* Export the content of profiles to Excel and Json files.    
    
    
## Installation

* Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Scrapy.  
(Anaconda Recomended)
```    
cd LinkedinScraperProject     
pip install -r requirements.txt    
```
* clone the project
```
git clone https://github.com/khaleddallah/GoogleImageScrapyDownloader.git
```



## Usage
* get into the directory of the project:
```
cd LinkedinScraperProject   
```   
* to get help :
```
python LinkedinScraper -h
```
<pre>
usage: python LinkedinScraper [-h] [-n NUM] [-o OUTPUT] [-p] (searchUrl or profilesUrl)

<b>positional arguments:</b>
  searchUrl      URL of Linkedin search URL or Profiles URL

<b>optional arguments:</b>
  -h, --help     show this help message and exit
  -n NUM         num of profiles
                 ** the number must be lower or equal of result number
                 'page' will parse profiles of url page (10 profiles) (Default)
  -o OUTPUT      Output file
  -p, --profile  Enable Parse Profiles

</pre>

## Examples

* Parse <b>(</b> https://www.linkedin.com/in/khaled-dallah/ and https://www.linkedin.com/in/linustorvalds/ <b>) profiles</b> and export the result content to <b>ABC.xlsx</b> and <b>ABC.json</b>
<br>(<b>-p</b>) because of parsing single profiles
```
python LinkedinScraper -p -o 'ABC' 'https://www.linkedin.com/in/khaled-dallah/' 'https://www.linkedin.com/in/linustorvalds/'
```


* Parse <b>23</b> profiles of searchUrl [https://www.linkedin.com/.../?keywords=Robotic&...&](https://www.linkedin.com/search/results/all/?keywords=Robotic&origin=GLOBAL_SEARCH_HEADER)
<br>if you don't set output name by (-o), Name of result files will be value of keywords (<b>Robotic</b>)
```
python LinkedinScraper -n 23 'https://www.linkedin.com/search/results/all/?keywords=Robotic&origin=GLOBAL_SEARCH_HEADER'
```
## Built with
* Python 3.7
* Scrapy
* openpyxl


## Author

* **Khaled Dallah** - *Software Engineer*


## Issues:   
Report bugs and feature requests
[here](https://github.com/khaleddallah/LinkedinScraperProject/issues).

## License

This project is licensed under the LGPL-V3.0 License - see the [LICENSE.md](https://github.com/khaleddallah/LinkedinScraperProject/blob/master/LICENSE) file for details
