#!/usr/bin/env python


#Using Navigation Timing API
#based on tripadvisor website calculation
#http://engineering.tripadvisor.com/html5-navigation-timing/

#download selenium, textwrap via pip
#download the - selenium chrome webdriver via {apt-get install chromium-chromedriver}



import collections
import textwrap

from selenium import webdriver

CHROME_BROWSER_PATH = "/usr/lib/chromium-browser/chromedriver"

class PageLoadTimer:

	def __init__(self, driver):
		self.driver = driver
		self.jscript = textwrap.dedent("""
			var performance = window.performance || {};
			var timings = performance.timing || {};
			return timings;
		""")

	def inject_timing_js(self):

		timings = self.driver.execute_script(self.jscript)

		return timings

	def get_event_times(self):

		timings = self.inject_timing_js()

		min_time = min([epoch for epoch in timings.values() if epoch != 0])

		ordered_events = ('navigationStart', 'fetchStart', 'domainLookupStart',
			'domainLookupEnd', 'connectStart', 'connectEnd','secureConnectionStart',
			'requestStart','responseStart', 'responseEnd', 'domLoading',
			'domInteractive', 'domContentLoadedEventStart',
			'domContentLoadedEventEnd', 'domComplete',
			'loadEventStart', 'loadEventEnd'
			)


		results = []

		for event in ordered_events:
			if event in timings:
				if timings[event] == 0:
					results.append((event, timings[event]))
				if timings[event] > 0:
					results.append((event, (timings[event] - min_time)))
		
		return collections.OrderedDict(results)


def calculate_page_time(url):

	results =  {}		
	
	driver = None

	try:

		options = webdriver.ChromeOptions()
	
		options.add_argument('headless')
		options.add_argument('igcognito')
		options.add_argument('window-size=1920x1080')

		driver = webdriver.Chrome(executable_path=CHROME_BROWSER_PATH,chrome_options=options)
		driver.implicitly_wait(10)

		driver.get(url)
		
		timing = PageLoadTimer(driver)
		events_time = timing.get_event_times()
		
		results["latency"] = events_time["responseStart"] - events_time["fetchStart"]
		results["transfer"] = events_time["responseEnd"] - events_time["responseStart"]
		results["dom_processing"] = events_time["domInteractive"] - events_time["domLoading"]
		results["dom_interactive"] = events_time["domComplete"] - events_time["domInteractive"]
		results["onload"] = events_time["loadEventEnd"] - events_time["loadEventStart"]

		results["total_page_load"] = results["latency"] + results["transfer"] + results["dom_processing"] + results["dom_interactive"] + results["onload"]				
			
	except Exception,e:
		print e
	finally:
		if driver:
			driver.quit()
	
	return results
	

if __name__ == '__main__':

	url = 'http://facebook.com'
	
	print calculate_page_time(url)
