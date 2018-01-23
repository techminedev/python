#!/usr/bin/env python
# -*- coding: utf-8 -*-

# note : pls install opencv-contrib-python via pip
from selenium import webdriver
import cv2 
import numpy as np
from matplotlib import pyplot as plt

CHROME_BROWSER_PATH = "/usr/lib/chromium-browser/chromedriver"


class ImageDetector:
	
	""" 
		OpenCV based image within image detector using keypoints detection
	"""

	def __init__(self):
		pass
		
	def show_detection(self,template,target_image):
		
		status = False
				
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
				if m.distance < 0.75*n.distance:
					good.append([m])

			# cv2.drawMatchesKnn expects list of lists as matches.
			img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)

			plt.imshow(img3),plt.show()
			
			if len(good) > 0:
				status = True
			
		except Exception,e:
			print e
		finally:
			pass
		
		return status
		
	def is_detected(self,template,target_image):
		
		status = False
				
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
				if m.distance < 0.75*n.distance:
					good.append([m])

			if len(good) > 0:
				status = True
			
		except Exception,e:
			print e
		finally:
			pass
		
		return status
		
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
			status = id.show_detection(template,screenshot) 
				
			# status = id.is_detected(template,screenshot) 
			
			print "IS DETECTED: %s" % status
		
	# TEST FOR NON DETECTION
	print "=== TESTING FOR NON DETECTION ==="
	
	status = id.show_detection("bugs_bunny.jpg",screenshot) 
	#status = id.is_detected("bugs_bunny.jpg",screenshot) 
	print "IS DETECTED: %s" % status

	
	
	
	
	
		
		