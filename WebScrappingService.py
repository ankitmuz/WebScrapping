from random import choice

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import ui
from datetime import date, timedelta

from ProductDetailsVO import ProductDetailsVO


def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") is not None


def calculatePostDate(postDateList):
    for dateVal in postDateList:
        dateVal = dateVal.split()
        for val in dateVal:
            if val.isdigit():
                val = int(val)
                dt = date.today() - timedelta(val)
                return str(dt)
                # print('Current Date :', date.today())
                # print('5 days before Current Date :', dt)


class ProductDetails:

    def __init__(self, baseurl):
        # self.total_pages_to_scrap = no_of_pages_to_scrap
        self.driver = object()
        self.baseUrl = baseurl
        # self.driver = webdriver.Firefox()
        self.DRIVER_PATH = './chromedriver'
        self.jdAttributes = ['price', 'title', 'stock', 'maftr']

    def formUrlWithDesignation(self, query_parameters):
        try:
            link = self.baseUrl
            for query_param in query_parameters:
                link += query_param
            return link
        except Exception as e:
            print(e)
            SystemExit

    def getAllJobsForOneDesignation(self, query_parameters, job_profile):
        link = query_parameters
        browse = link
        print(browse)
        listOfData = []
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(executable_path=self.DRIVER_PATH, chrome_options=chrome_options)

            capabilities = DesiredCapabilities.CHROME.copy()
            capabilities['acceptSslCerts'] = True
            capabilities['acceptInsecureCerts'] = True

            proxy = proxy_generator()
            self.driver.get(browse)
            wait = ui.WebDriverWait(self.driver, 10)
            wait.until(page_is_loaded)
            pageVal = self.driver.find_elements_by_xpath("//a[@href]")
            page_links = []
            for val in pageVal:
                href = val.get_attribute("href")
                if href.startswith('https://www.midsouthshooterssupply.com/item'):
                    page_links.append(href)

            for lnk in page_links:
                prodVO = ProductDetailsVO()
                self.driver.get(lnk)
                wait = ui.WebDriverWait(self.driver, 10)
                wait.until(page_is_loaded)

                # Get the Price of the particular Product
                prodVO.set_price(self.get_prod_price())

                prodVO.set_title(self.get_prod_title())

                prodVO.set_stock(self.get_prod_stock())

                prodVO.set_maftr(self.get_prod_manufacturer())

                listOfData.append(prodVO.__dict__)
            self.driver.quit()
            return listOfData
        except Exception as e:
            print(e)
            self.driver.quit()
        self.driver.quit()
        return listOfData

    def get_prod_price(self):
        try:
            price = self.driver.find_elements_by_xpath("//span[@class='price']")

            if price[0] is not None:
                return price[0].text

        except:
            return ''

    def get_prod_title(self):
        try:
            prodNameList = self.driver.find_elements_by_xpath("//h1[@class='product-name']")
            if prodNameList[0] is not None:
                return prodNameList[0].text

        except:
            return []

    def get_prod_manufacturer(self):
        try:
            manftrLst = self.driver.find_elements_by_xpath("//div[@class='catalog-item-brand-item-number']")
            if manftrLst[0] is not None and manftrLst[0].text is not None:
                completeList = manftrLst[0].text
                return completeList.split('#')[0]

            else:
                return ''
        except:
            return ''

    def get_prod_stock(self):
        try:
            qnttyCaart = self.driver.find_elements_by_xpath("//div[@class='quantity-cart']")
            if qnttyCaart[0] is not None and qnttyCaart[0].text is "":
                return False
            else:
                return True
        except:
            return ['NA']


def proxy_generator():
    response = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(response.content, 'html5lib')
    proxy = {'https': choice(list(map(lambda x: x[0] + ':' + x[1], list(
        zip(map(lambda x: x.text, soup.findAll('td')[::8]), map(lambda x: x.text, soup.findAll('td')[1::8]))))))}

    return proxy
