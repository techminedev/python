import requests
import ujson
import time

URL_MATCH = "http://0.0.0.0:5000/api/search/match"
URL_RESULT_BY_TASK_ID = "http://0.0.0.0:5000/api/search/task_id"
URL_RESULT_BY_DATE = "http://0.0.0.0:5000/api/search/date"
URL_RESULT_BY_DATE_RANGE = "http://0.0.0.0:5000/api/search/daterange"
URL_RESULT_BY_MONTH = "http://0.0.0.0:5000/api/search/month"
headers = {"Content-Type" : "application/json"}

print "==========================================="
print "MATCH SINGLE IMAGE"
payload={}
payload["target_url"] = "https://www.gunsamerica.com/934027991/GLOCK-G43-9MM-6-1-NO-CREDIT-CARD-FE.htm"
payload["images"] = []
image1 = {}
image1["image_url"] = "https://www.gunsamerica.com/userimages/135830/934027991/wm_12387848.jpg"
image1["screen_width"] = 1920
image1["screen_height"] = 1080
payload["images"].append(image1)

r = requests.post(URL_MATCH,data=ujson.dumps(payload),headers=headers)
print r.status_code
print r.text
task_id = ujson.loads(r.text)["task_id"]

print "==========================================="
print "FETCH RESULT BY TASK ID wait 120 sec : %s" % task_id
time.sleep(120)
params= {}
params["task_ids"] = ujson.dumps([task_id])
r = requests.get(URL_RESULT_BY_TASK_ID,params=params)
print r.status_code
print r.text

print "==========================================="
print "MATCH MULTIPLE IMAGES"
payload={}
payload["target_url"] = "https://www.gunsamerica.com/934027991/GLOCK-G43-9MM-6-1-NO-CREDIT-CARD-FE.htm"
payload["images"] = []
image1 = {}
image1["image_url"] = "https://news.nationalgeographic.com/content/dam/news/2017/04/27/frog-gallery/01-frog-day-gallery.jpg"
image1["screen_width"] = 1920
image1["screen_height"] = 1080
image2 = {}
image2["image_url"] = "https://upload.wikimedia.org/wikipedia/en/5/59/Hulk_%28comics_character%29.png"
image2["screen_width"] = 1920
image2["screen_height"] = 1080
image3 = {}
image3["image_url"] = "https://www.gunsamerica.com/userimages/135830/934027991/wm_12387848.jpg"
image3["screen_width"] = 1920
image3["screen_height"] = 1080
image4 = {}
image4["image_url"] = "https://vignette.wikia.nocookie.net/swfanon/images/7/78/Padme.jpg/revision/latest?cb=20110710054422"
image4["screen_width"] = 1920
image4["screen_height"] = 1080
payload["images"].append(image1)
payload["images"].append(image2)
payload["images"].append(image3)
payload["images"].append(image4)

r = requests.post(URL_MATCH,data=ujson.dumps(payload),headers=headers)
print r.status_code
print r.text
task_id = ujson.loads(r.text)["task_id"]

print "==========================================="
print "FETCH RESULT BY TASK ID wait 120 sec: %s" % task_id
time.sleep(120)
params= {}
params["task_ids"] = ujson.dumps([task_id])
r = requests.get(URL_RESULT_BY_TASK_ID,params=params)
print r.status_code
print r.text

print "==========================================="
print "FETCH RESULT BY DATE"
params = {}
params["date"] = "2018-05-19"
r = requests.get(URL_RESULT_BY_DATE,params=params)
print r.status_code
print r.text

print "==========================================="
print "FETCH RESULT BY DATE RANGE"
params = {}
params["date_start"] = "2018-05-19"
params["date_end"] = "2018-05-20"
r = requests.get(URL_RESULT_BY_DATE_RANGE,params=params)
print r.status_code
print r.text

print "==========================================="
print "FETCH RESULT BY MONTH"
params = {}
params["month"] = "May"
r = requests.get(URL_RESULT_BY_MONTH,params=params)
print r.status_code
print r.text










