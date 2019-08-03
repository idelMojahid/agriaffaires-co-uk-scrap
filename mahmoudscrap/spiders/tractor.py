# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class TractorSpider(scrapy.Spider):
    name = 'tractor'
    allowed_domains = ['agriaffaires.co.uk']
    start_urls = ['http://agriaffaires.co.uk/']
    domain_url = 'http://agriaffaires.co.uk'
    #had lklab del headers dima m3etlini
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}


    def cat_paginated(self,page):
        return  'https://www.agriaffaires.co.uk/used/'+str(page)+'/farm-tractor.html'

    def start_requests(self):
        #to be changed by the num of pages
        for i in range(1,2):
            yield scrapy.Request(url=self.cat_paginated(i),callback = self.parse,headers=self.headers)

    def parse(self, response):
        content = response.body
        tractors_page = BeautifulSoup(content,"lxml")
        tractors_links_dom = tractors_page.find_all('div',{'class':'listing--element'})
        tractors_links = [ (l.find('a',{'class':'link'}))['href']for l in tractors_links_dom]
        for l in tractors_links:
            yield scrapy.Request(url=self.domain_url+l, callback=self.parse_tractor,headers=self.headers)

    def parse_tractor(self, response):
        content = response.body
        tractor_page = BeautifulSoup(content,"lxml")
        table_scpecs =(tractor_page.find('table',{'class':'table--specs'})).find_all('tr')
        tractor = {}
        for tr in table_scpecs :
            tds = tr.find_all('td')
            tds_texts = [((td_txt.text).strip()).replace(":", "") for td_txt in tds]
            try:
                tractor[tds_texts[0]] = tds_texts[1]
            except :
                print('wa lharba')
        yield tractor
        # yield
        pass
