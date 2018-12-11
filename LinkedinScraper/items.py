# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item

class Person(Item):
    name = Field()
    carer = Field()
    summary = Field()
    experience = Field()
    education = Field()
    skills = Field()



class Job(Item):
    carer = Field()
    company = Field()
    requirements = Field()
    email = Field()
    easy_application = Field()
    