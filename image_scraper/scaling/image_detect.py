#!/usr/bin/env python
# -*- coding: utf-8 -*-

# note : pls install opencv-contrib-python via pip

import cv2 
import numpy as np
import requests
from selenium import webdriver
from matplotlib import pyplot as plt
from config import *

CHROME_BROWSER_PATH = "/usr/lib/chromium-browser/chromedriver"


class ImageDetector:
	
	""" 
		OpenCV based image within image detector using keypoints detection
	"""

	def __init__(self):
		pass
		
	def process(self, id, target_url, image_url, screen_width, screen_height):
		
		print "===================================="
		print "=> PROCESS : %s" % id
		
		status = False
		image_match = ""
		
		print target_url
		print image_url
		print screen_width
		print screen_height
		
		screenshot_status, image_screenshot = self.__get_screenshot(id, target_url, screen_width, screen_height)
		image_status, image_overlay = self.__get_image(id, image_url)
		
		if screenshot_status and image_status:
			#status = True			
			matches_status, image_match = self.__get_matches(id,image_screenshot,image_overlay)
			status = matches_status			
		
		return status, image_match
	
	def __get_screenshot(self, id, target_url, screen_width, screen_height):
		
		print "=> GET SCREENSHOT"
	
		status = True
		
		driver = None
		
		image_screenshot = DIR_RESOURCES + "%s_screenshot.png" % id
		
		try:
			options = webdriver.ChromeOptions()

			options.add_argument('headless')
			options.add_argument('window-size=%sx%s' % (screen_width, screen_height))

			driver = webdriver.Chrome(executable_path=CHROME_BROWSER_PATH ,chrome_options=options)
			driver.implicitly_wait(10)

			driver.get(target_url)
			
			driver.save_screenshot(image_screenshot)
		except:
			status = False
		finally:
			if driver:
				driver.quit()	
			
		return status, image_screenshot
		
	def __get_image(self, id, image_url):
		
		print "=> GET IMAGE"
		
		status = False
		
		is_downloadable, ext = self.__is_downloadable(image_url)
		image_overlay = None
		
		if is_downloadable:
			
			image_overlay = DIR_RESOURCES + "%s_image.%s" % (id,ext)
			
			# download image	
				
			r = requests.get(image_url,stream=True)
			if r.status_code == 200:
				with open(image_overlay, 'wb') as f:
					f.write(r.content)
				status = True

		print "--- GET IMAGE FINISHED"
				
		return status, image_overlay
		
	def __is_downloadable(self, image_url):
		
		status = False
		extension = None
		
		h = requests.head(image_url, allow_redirects=True)
		header = h.headers
		content_type = header.get('content-type').lower().strip()
		
		print content_type
		
		if content_type.find("image") == 0:
			status = True
			extension = content_type.split("/")[1]
		
		return status, extension	
		
		
	def __get_matches(self,id,template,target_image):
		
		status = False
		
		image_match = DIR_RESOURCES + "%s_result.png" % id
				
		try:

			img1 = cv2.imread(template,0)
			img2 = cv2.imread(target_image,0)
			
			# Initiate SIFT detector
			sift = cv2.xfeatures2d.SIFT_create()

			# find the keypoints and descriptors with SIFT
			kp1, des1 = sift.detectAndCompute(img1,None)
			kp2, des2 = sift.detectAndCompute(img2,None)

			# BFMatcher with default params
			bf = cv2.BFMatcher()
			matches = bf.knnMatch(des1,des2, k=2)

			# Apply ratio test
			good = []
			for m,n in matches:
				if m.distance < 0.25*n.distance:
					good.append([m])

			# cv2.drawMatchesKnn expects list of lists as matches.
			img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)

			cv2.imwrite(image_match, img3)
			
			if len(good) > 0:
				status = True
			
		except Exception,e:
			print e
		finally:
			pass
		
		return status, image_match	
	

if __name__ == "__main__":

	detector = ImageDetector()
	
	id = "watoom"
	target_url = "http://opencv-python-tutroals.readthedocs.io/en/latest/index.html"
	image_url = "http://opencv-python-tutroals.readthedocs.io/en/latest/_static/opencv-logo-white.png"
	detector.process(id,target_url,image_url,1920,1080)
	
	
	
	
	
		
		
