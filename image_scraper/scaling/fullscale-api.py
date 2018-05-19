#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import *

from flask import Flask, abort, render_template, request, send_file,jsonify

# from pymemcache.client.base import Client as MemcacheClient

from orator import DatabaseManager
from mysql_config import DATABASES
from orator import Model
from models.task import *

import json
import ujson
import uuid
import hashlib

from datetime import datetime
import arrow

db = DatabaseManager(DATABASES)
Model.set_connection_resolver(db)

app = Flask(__name__)

app.config['STATIC_PATH'] = MATCHES_IMAGE_DIRECTORY



@app.route('/')
def main():
    return "home"

#full scale search

@app.route('/api/search/match', methods=['POST'])
def search_match():
    try:

        data = request.get_json()

        if 'images' in data.keys() and 'target_url' in data.keys():

            is_ok_continue = True

            for image in data['images']:
                data_keys = ['image_url', 'screen_height', 'screen_width']
                is_not_found = False

                for key in data_keys:
                    if key not in image.keys():
                        print 'something missing'
                        is_not_found = True
                        break

                if is_not_found:
                    is_ok_continue = False
                    break

            if is_ok_continue:

                m = hashlib.md5()
                m.update(str(uuid.uuid4()))
                id = m.hexdigest()

                with db.transaction():
                    for image in data['images']:

                        print 'target_url %s' % data['target_url']
                        print 'image_url %s' % image['image_url']

                        t_data = []
                        t_data.append(id)
                        t_data.append(data['target_url'])
                        t_data.append(image['image_url'])
                        t_data.append(image['screen_width'])
                        t_data.append(image['screen_height'])
                        t_data.append(datetime.now().strftime("%y-%m-%d-%H-%M"))
                        db.insert('insert into tasks (task_id, target_url, image_url, screen_width, screen_height,created_at) values (%s,%s,%s,%s,%s,%s)', t_data)

            response = \
                app.response_class(response=ujson.dumps({'status': 'OK'}),
                                   status=200, mimetype='application/json',
                                   headers={'Access-Control-Allow-Origin': '*'
                                   })
            return response
        else:
            abort(403)
    except:
        abort(403)


@app.route("/api/search/task_id", methods=["GET"])
def get_search_task_id():
    try:
        data = request.get_json()
        transaction = []

        if "task_id" in data.keys():
            task_id = data["task_id"]
            transaction = db.table("tasks").where_in("task_id", task_id).get().serialize()

            return jsonify(transaction)

        return jsonify(transaction)

    except:
        abort(403)

@app.route("/api/search/daterange", methods=["GET"])
def get_search_daterange():
    try:
        data = request.get_json()
        transaction = []

        if "date_start" in data.keys() and "date_end" in data.keys():
            date_start = data["date_start"]
            date_end = data["date_end"]
            transaction = Task.where_between("created_at",[date_start,date_end]).get().serialize()

            return jsonify(transaction)

        return jsonify(transaction)

    except:
        abort(403)

@app.route("/api/search/date", methods=["GET"])
def get_search_date():
    try:
        data = request.get_json()
        transaction = []

        if "date" in data.keys():
            date = data["date"]
            transaction = Task.where("created_at",">",str(arrow.get(date, 'YYYY-MM-DD').format('YYYY-MM-DD'))).where("created_at","<",str(arrow.get(date, 'YYYY-MM-DD').shift(days=1).format('YYYY-MM-DD'))).get().serialize()
            #transaction = db.select("select * from tasks where DATE(created_at) = %s",[date])
            return jsonify(transaction)

        return jsonify(transaction)

    except:
        abort(403)

@app.route("/api/search/month", methods=["GET"])
def get_search_month():
    try:
        data = request.get_json()
        transaction = []

        if "month" in data.keys():
            month = data["month"]
            transaction = db.select("select * from tasks where MONTH(created_at) = MONTH(str_to_date(%s,'%%b')) and YEAR(now()) = YEAR( CURDATE())",[month]) 
            return jsonify(transaction)

        return jsonify(transaction)

    except:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)