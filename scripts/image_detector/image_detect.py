#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
import cv2
import numpy as np
from matplotlib import pyplot as plt

CHROME_BROWSER_PATH = "/usr/lib/chromium-browser/chromedriver"


class ImageDetector:
	
	""" 
		OpenCV based image within image detector using matchTemplate() 
	"""

	def __init__(self):
		pass
		
	def show_detection(self,image_pattern,target_image):
		
		status = False
				
		driver = None

		try:

			template = cv2.imread(image_pattern,0)
			img = cv2.imread(target_image,0)
			w, h = template.shape[::-1]
			
			methods = ['cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
			
			for meth in methods:
				method = eval(meth)
				
				res = cv2.matchTemplate(img,template,method)
				min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

				# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
				if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
					top_left = min_loc
				else:
					top_left = max_loc
				bottom_right = (top_left[0] + w, top_left[1] + h)

				cv2.rectangle(img,top_left, bottom_right, 255, 2)

				plt.subplot(121),plt.imshow(res,cmap = 'gray')
				plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
				plt.subplot(122),plt.imshow(img,cmap = 'gray')
				plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
				plt.suptitle(meth)

				plt.show()			

		except Exception,e:
			print e
		finally:
			pass
		
		return status
		
	def is_detected(self,image_pattern,target_image):
		
		status = False
		detected_methods = []
		
		driver = None

		try:

			template = cv2.imread(image_pattern,0)
			img = cv2.imread(target_image,0)
			w, h = template.shape[::-1]
			
			methods = ['cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
			
			for meth in methods:
				method = eval(meth)
				
				res = cv2.matchTemplate(img,template,method)
				
				min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
				
				if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
					if min_val == 0.0: # min threshold
						detected_methods.append(meth)					
				else:
					if max_val == 1.0: # max threshold 
						detected_methods.append(meth)			

		except Exception,e:
			print e
		finally:
			pass
			
		if len(detected_methods) > 0:
			status = True
		
		return status,detected_methods
		
	def get_image_from_image(self, source_file,target_file,beginX,beginY,length,width):
	
		status = True
		
		try:
			src_image = cv2.imread(source_file)
			
			cropped_image = src_image[beginY:beginY+length,beginX:beginX+width]
			
			cv2.imwrite(target_file, cropped_image)
		except:
			status = False
			
		return status
		
	def get_screenshot_hd(self,url,target_image):
		
		status = True
		
		driver = None
		
		try:
			options = webdriver.ChromeOptions()

			options.add_argument('headless')
			options.add_argument('window-size=1280x720')

			driver = webdriver.Chrome(executable_path=CHROME_BROWSER_PATH ,chrome_options=options)
			driver.implicitly_wait(10)

			driver.get(url)
			
			driver.save_screenshot(target_image)
		except:
			status = False
		finally:
			if driver:
				driver.quit()	
				
		return status
		
	def get_screenshot_fhd(self,url,target_image):
		
		status = True
		
		driver = None
		
		try:
			options = webdriver.ChromeOptions()

			options.add_argument('headless')
			options.add_argument('window-size=1920x1080')

			driver = webdriver.Chrome(executable_path=CHROME_BROWSER_PATH ,chrome_options=options)
			driver.implicitly_wait(10)

			driver.get(url)
			
			driver.save_screenshot(target_image)
		except:
			status = False
		finally:
			if driver:
				driver.quit()	
			
		return status

if __name__ == "__main__":

	id = ImageDetector()
	
	# TEST FOR DETECTION
		
	print "=== TESTING FOR DETECTION ==="
	
	target_url = "http://opencv-python-tutroals.readthedocs.io/en/latest/index.html"
	screenshot = "screenshot.png"
	template = "template.png"
	
	screenshot_status = id.get_screenshot_fhd(target_url,screenshot)
	if screenshot_status:
		cropped_status = id.get_image_from_image(screenshot,template,0,0,200,200)
		if cropped_status:
			
			# show visual detection per matching algorithm
			#id.show_detection(template,screenshot) 
				
			status, match_methods = id.is_detected(template,screenshot) 
			
			print "IS DETECTED: %s" % status
			print "MATCHING METHODS: %s" % match_methods
	

		
	# TEST FOR NON DETECTION
	print "=== TESTING FOR NON DETECTION ==="
	
	#id.show_detection("bugs_bunny.jpg",screenshot) 
	status, match_methods = id.is_detected("bugs_bunny.jpg",screenshot) 
	print "IS DETECTED: %s" % status
	print "MATCHING METHODS: %s" % match_methods
	
	
	
	
	
		
		