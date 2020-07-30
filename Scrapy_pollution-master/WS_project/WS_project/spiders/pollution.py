import scrapy
from scrapy_splash import SplashRequest
import pandas as pd

#This script scrap two items from the links generated by the spider pages

df = pd.read_csv(
    'WS_project/Data/Links/pages.csv')  # To read the output from the spider pages
a = df.values.tolist()
b = []
for i in range(len(a)): 
    b.append(str(', '.join(a[i])))
b

class WsProjectItem(scrapy.Item):
    pollution = scrapy.Field()
    date = scrapy.Field() 
    text = scrapy.Field() #We will take three items

class MySpider(scrapy.Spider):
    name = "pollution"

    def start_requests(self):
        urls = b
        for url in urls:
            yield SplashRequest(
            url,
            callback=self.parse,
            endpoint='render.html',
            args={"wait": 8}
            )

    def parse(self, response):
        xpath = '/html/body/div[1]/div/main/section/header/div/div/h1[1][1]//text()' #To take text, city and country
        xpath3 = '//dt[text() = "PM2.5"]/following-sibling::dd[1]//text()[1]' #To take pollution
        xpath4 = '//dt[text() = "PM2.5"]/following-sibling::dd[1]//text()[4]' #To take date
        items = {
            'text': response.xpath(xpath).getall() or 'N/A',
            'pollution': response.xpath(xpath3).getall() or 'N/A',
            'date': response.xpath(xpath4).getall() or 'N/A'
        }
        yield items

#In the shell it should be run: scrapy crawl pollution -o Data/pollution.csv

#In this case is not needed to create the class WsProjectItem, becuase in def parse(self, response) a list was created, but it is better
#to create it before, in order to be more organize, because you do not need to go till the end to see the item that are scrapped
