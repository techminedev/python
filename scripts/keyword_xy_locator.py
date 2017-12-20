#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver

CHROME_BROWSER_PATH = "/usr/lib/chromium-browser/chromedriver"


class KeywordXYLocator:
	
	def __init__(self):
		pass
		
	def retrieve_coordinates(self,url,keywords):
	
		results =  {}	
		
		driver = None

		try:

			options = webdriver.ChromeOptions()

			options.add_argument('headless')
			options.add_argument('window-size=1920x1080')

			driver = webdriver.Chrome(executable_path=CHROME_BROWSER_PATH ,chrome_options=options)
			driver.implicitly_wait(10)

			driver.get(url)
			
			for keyword in keywords:
				
				temp_results = []

				# note : find_elements_by_partial_link_text() is case sensitive
				matches = driver.find_elements_by_partial_link_text(keyword)

				for match in matches:
					
					loc = match.location
					temp_results.append(loc)
					
				results[keyword] = temp_results

		except Exception,e:
			print e
		finally:
			if driver:
				driver.quit()
		
		return results
		

if __name__ == "__main__":

	scraper =  KeywordXYLocator()
	keywords = ["iPhone","Remax"]
	print scraper.retrieve_coordinates("https://www.lazada.com.ph/catalog/?q=remax",keywords)

		
		