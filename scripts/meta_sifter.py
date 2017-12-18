#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver

CHROME_BROWSER_PATH = "/usr/lib/chromium-browser/chromedriver"


class MetaSifter:
	
	def __init__(self):
		pass
		
	def retrieve_meta_data(self,url):
	
		results =  []		
		
		driver = None

		try:

			options = webdriver.ChromeOptions()

			options.add_argument('headless')
			options.add_argument('window-size=1920x1080')

			driver = webdriver.Chrome(executable_path=CHROME_BROWSER_PATH,chrome_options=options)
			driver.implicitly_wait(10)

			driver.get(url)

			matches = driver.find_elements_by_css_selector("meta")

			for match in matches:
				
				meta_data = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', match)
				results.append(meta_data)

		except Exception,e:
			print e
		finally:
			if driver:
				driver.quit()
		
		return results
		

if __name__ == "__main__":

	scraper = MetaSifter()
	print scraper.retrieve_meta_data("https://www.lazada.com.ph/catalog/?q=remax")

		
		