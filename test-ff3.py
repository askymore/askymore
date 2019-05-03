# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import os
import csv
import sys


profile = webdriver.FirefoxProfile()

profile.set_preference("browser.download.folderList",2)
profile.set_preference("browser.helperApps.alwaysAsk.force", False)
profile.set_preference("browser.download.manager.showWhenStarting",False)
profile.set_preference("browser.download.dir", os.path.join(os.getcwd(), 'pdfs/'))
profile.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
profile.set_preference("pdfjs.disabled", True)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

driver=webdriver.Firefox(firefox_profile=profile)
driver.maximize_window()
driver.implicitly_wait(1)
fileaddr = []
filename = []
companies=[]

out = open('Stu_csv.csv','w')
csv_write = csv.writer(out,dialect='excel')

def downPDF(url):
	time.sleep(1)#等待一秒
	driver.get(url)
	driver.execute_script("document.getElementById('download').style.display = 'block';")
	down_button = driver.find_element_by_id("download")
	down_button.click()

def companyloop(company):
	driver.get("http://icid.iachina.cn/front/getCompanyInfos.do?columnid=2015120115460095&comCode="+company+"&attr=01")
	soup = BeautifulSoup(driver.page_source, 'lxml')
	arr = []
	for p in soup.find_all('p'):
	    for a in p.find_all('a'):
	       at=a.attrs
	       arr.append(at['id'])

	time.sleep(5)
	for ar in arr:
		driver.get("http://icid.iachina.cn/front/infoDetail.do?informationno="+ar)
		soup = BeautifulSoup(driver.page_source, 'lxml')	
		for p in soup.find_all('li'):
		    for a in p.find_all('a'):
		       at=a.attrs 
		       filename.append(a.string)              
		       fileaddr.append(at['id'])
		       csv_write.writerow([company,a.string.decode("utf-8"),at['id']])
		       downPDF("http://icid.iachina.cn/files/piluxinxi/pdf/viewer.html?file="+at['id'])            



driver.get("http://icid.iachina.cn/front/leafColComType.do?columnid=2015120115460095")
soup = BeautifulSoup(driver.page_source, 'lxml')
com_div = soup.find(attrs={"class":"jie_nei"})
for c in com_div.findAll('li',attrs={"op_id":"type_me"}):
     for a in c.findAll('a',attrs={"href":"javascript:void(0);"}):
       at=a.attrs 
       companies.append(at['id'])

for com in companies:
        companyloop(com)
#driver.get("http://icid.iachina.cn/?columnid_url=2015120115460095")
#driver.find_element_by_xpath("//*[@id='03']").click()#然后点击“百度一下”

#driver.find_element_by_xpath("//*[@id='ZGRS']").click()

#driver.find_element_by_id(arr[0]).click()

#driver.find_element_by_xpath('//a[contains(@id,"PDF")]')

#http://icid.iachina.cn/?columnid_url=2015120115460095
#driver.find_element_by_xpath("//*[@id='03']").click()#然后点击“百度一下”

#driver.find_element_by_xpath("//*[@id='ZGRS']").click()
 
#time.sleep(20)#等待两秒

driver.quit()#关闭浏览器
