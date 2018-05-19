import time
import ujson
import psutil
import multiprocessing
from multiprocessing import Process, Semaphore
from image_detect import *
from config import *
from orator import DatabaseManager
from mysql_config import DATABASES
from orator import Model
from models.task import *

db = DatabaseManager(DATABASES)
Model.set_connection_resolver(db)


class SimpleWorker(Process):

	def __init__(self,task_id,worker_control):
		super(SimpleWorker, self).__init__()
		self.task_id = task_id
		self.worker_control = worker_control

	def run(self):

		print "-- SIMPLE WORKER ONLINE : %s" % self.task_id

		t = Task.where("task_id","=",self.task_id).first()

		if t is not None:

			try:
				target_url = t.target_url
				image_url = t.image_url
				screen_width = t.screen_width
				screen_height = t.screen_height

				image_detector = ImageDetector()

				status, image_match = image_detector.process(self.task_id,target_url,image_url,screen_width,screen_height)

				print status
				print image_match

				t.image_path = image_match
				t.status = status
				t.processing_status = 2 # DONE
				t.save()

			except:
				t.processing_status = 3 # ERROR
				t.save()

		self.worker_control.release()


class BatchWorker(Process):

	def __init__(self,task_id,worker_control):
		super(BatchWorker, self).__init__()
		self.task_id = task_id
		self.worker_control = worker_control

	def run(self):

		print "-- BATCH WORKER ONLINE : %s" % self.task_id

		image_detector = ImageDetector()

		tasks = Task.where("task_id","=",self.task_id).order_by("id","asc").get()

		counter = 0
		is_ok_to_continue = True

		for t in tasks:

			counter = counter + 1

			try:
				if is_ok_to_continue:

					target_url = t.target_url
					image_url = t.image_url
					screen_width = t.screen_width
					screen_height = t.screen_height

					task_id = "%s_%s" % (self.task_id,counter)

					status, image_match = image_detector.process(task_id,target_url,image_url,screen_width,screen_height)

					print status
					print image_match

					t.image_path = image_match
					t.status = status
					t.processing_status = 2 # DONE
					t.save()

					if status:
						is_ok_to_continue = False

				else:
					# at least one of the previous task has succeeded
					# the rest of the task will be set to DONE
					t.processing_status = 2 # DONE
					t.image_path = ""
					t.save()

			except:
				t.processing_status = 3 # ERROR
				t.image_path = ""
				t.save()

		self.worker_control.release()


if __name__ == '__main__':

	print "PROCESSER RUNNING"
	print "#CPU COUNT : %s" % psutil.cpu_count()

	worker_control = Semaphore(psutil.cpu_count())

	while True:

		if worker_control.acquire(False):

			t = Task.where("processing_status","=",0).first()

			if t is not None:

				task_id = t.task_id

				Task.where("task_id","=",task_id).update({'processing_status': 1})

				num_tasks = Task.where("task_id","=",task_id).count()

				if num_tasks > 1:
					w = BatchWorker(task_id,worker_control)
					w.start()
				else:
					w = SimpleWorker(task_id,worker_control)
					w.start()
			else:
				worker_control.release()

			time.sleep(0.1) #sleep for 100 milliseconds
