#!/usr/bin/env python


#Using Navigation Timing API
#based on tripadvisor website calculation
#http://engineering.tripadvisor.com/html5-navigation-timing/

#download selenium, textwrap via pip
#download the - selenium chrome webdriver via {apt-get install chromium-chromedriver}



import collections
import textwrap
import json

from selenium import webdriver

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

        #min_time = min((epoch for epoch in timings.values() if epoch != 0))

        ordered_events = ('navigationStart', 'fetchStart', 'domainLookupStart',
                          'domainLookupEnd', 'connectStart', 'connectEnd','secureConnectionStart',
                          'requestStart','responseStart', 'responseEnd', 'domLoading',
                          'domInteractive', 'domContentLoadedEventStart',
                          'domContentLoadedEventEnd', 'domComplete',
                          'loadEventStart', 'loadEventEnd'
                          )
        event_times = ([(event, timings[event]) for event
                       in ordered_events if event in timings])

        return collections.OrderedDict(event_times)


if __name__ == '__main__':

    url = 'http://buzz4pun.com'
	
    options = webdriver.ChromeOptions()
    #uncomment to run headless
    options.add_argument('headless')
    #used igcognito to disable caches
    options.add_argument('incognito')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver",chrome_options=options)
    driver.implicitly_wait(10)
    
    driver.get(url)

    timer = PageLoadTimer(driver)
    events_time = timer.get_event_times()

   
    driver.quit()
	
    results = {}

    print "*** Events Time\n"
    
    for key in events_time.iterkeys():

    	print "%s: %s" % (key, events_time[key])

    results["latency"] = events_time["responseStart"] - events_time["fetchStart"]
    results["transfer"] = events_time["responseEnd"] - events_time["responseStart"]
    results["dom_processing"] = events_time["domInteractive"] - events_time["domLoading"]
    results["dom_interactive"] = events_time["domComplete"] - events_time["domInteractive"]
    results["onload"] = events_time["loadEventEnd"] - events_time["loadEventStart"]

    results["total_page_load"] = results["latency"] + results["transfer"] + results["dom_processing"] + results["dom_interactive"] + results["onload"]


    print "\n"
    print "*** Page Load Time Results\n"
    print json.dumps(results)
	

	
