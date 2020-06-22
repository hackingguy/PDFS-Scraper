import scrapy
import re
import requests
from scrapy.http import Request
import os

class AllSpider(scrapy.Spider):
    name = 'pdfs'
    #Set Max Depth
    custom_settings = { 'DEPTH_LIMIT': '3' }
    path = ""
    company = ""
    visited = []
    #Ignoring Going Further Inside These Content Types
    #You Can Add More If You Want
    content_types = ['mp4','pdf','csv','usdz','wav']
    #Starting Point
    start_urls = ['https://www.apple.com/']
    allowed_domains = ['www.apple.com']
    
    try:
        os.mkdir("Companies")
    except:
        print("Directory Exists Companies")
        
        
    
    for url in start_urls:
        company_array = url.split(".")
        company = company_array[len(company_array)-2]
        try:
            os.system("cd Companies && mkdir {}".format(company))
        except:
            print("Directory Exists {}".format(company))
        try:
            os.system("cd Companies && cd {} && mkdir pdfs && mkdir html".format(company))
        except:
            print("Directories Already Exists")
    
    
    
    def __init__(self):
        self.links=[]
        
        
    def save_html(self, response,href,domain):
        path= "Companies/"+ self.company+"/html/"+ " ".join(response.url.split("/")).strip().split(' ')[-1] + ".html"
        print('Saving HTML {} '.format(path))
        url = ""
        if domain in href:
            url = href;
        else:
            url = "https://"+domain+href;
        r = requests.get(url,stream=True)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(2000):
                f.write(chunk)
       
    def save_pdf(self, response,href,domain):
        path= "Companies/"+ self.company+"/pdfs/"+ href.split('/')[-1]
        print('Saving PDF: {} '.format(path))
        url = ""
        if domain in href:
            url = href;
        else:
            url = "https://"+domain+href;
        r = requests.get(url,stream=True)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(2000):
                f.write(chunk)

    def parse(self, response):
        try:
            #Downloading Specific Pages
            keywords = ['environment','esg']
            self.links.append(response.url)
            print("Link Tried: {}".format(response.url))
            for allowed_domain in self.allowed_domains:
                if allowed_domain in response.url:
                    for href in response.xpath("//a/@href").extract():
                        for keyword in keywords:
                            if re.search(keyword,href) and href not in self.visited:
                                self.visited.append(href)
                                print("Link: {}".format(href))
                                self.save_html(response,href,allowed_domain)
                                if ".pdf" in href:
                                    print("PDF Found: {}".format(href))
                                    self.save_pdf(response,href,allowed_domain)
                        try:
                            if href.split(".")[-1] not in self.content_types:
                                yield response.follow(href, self.parse)
                        except Exception as e:
                            print("Error: {}\n\t{}".format(response.url,e))
        except Exception as es:
            print("Error: {}\n\t{}".format(response.url,es))
