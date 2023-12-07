import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from selenium import webdriver
from lxml import html

#1. 웹페이지의 HTML 가져오기
url = "https://www.myasset.com/myasset/research/rs_list/rs_list.cmd?cd006=&cd007=RE01&cd008="
response = requests.get(url)
tree = html.fromstring(response.content)
elements = tree.xpath('//*[@id="RS_0201001_P1_FORM"]/div[4]/table/tbody/tr')


for i, element in enumerate(elements, start=1):
    title = element.xpath('td[4]/a/text()')[0].strip()
    pdf_url = element.xpath('td[5]/a/@href')[0]


    if pdf_url and pdf_url != '#':
        # Construct the full URL if it's a relative URL
        pdf_url = urljoin(url, pdf_url)
        
        # Download the PDF file
        pdf_response = requests.get(pdf_url, stream=True)
        
        # Specify the filename for saving
        filename = f"{i}_{title}.pdf"
        
        # Save the PDF file
        with open(filename, 'wb') as pdf_file:
            for chunk in pdf_response.iter_content(chunk_size=1024):
                if chunk:
                    pdf_file.write(chunk)
        
        print(f"Downloaded {filename}")
    else:
        print(f"Skipped download for element {i} due to an invalid PDF URL")




