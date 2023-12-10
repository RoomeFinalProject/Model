from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By  # Corrected import
from selenium.webdriver.common.keys import Keys  # Corrected import
import time
from bs4 import BeautifulSoup  # Corrected import

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#driver = webdriver.Chrome(ChromeDriverManager().install())
time.sleep(10)

url = 'https://www.naver.com/'
driver.get(url)

