from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, send, emit
import time
import os
#################################################
import json
from time import time as t
import numpy as np
import math

app = Flask(__name__,static_url_path="/video_index/static")
socketio = SocketIO(app)

@app.route('/video_index/uploader', methods = ['GET', 'POST'])
def upload():
	global filename
	global datos
	if request.method == 'GET':
		filename = request.args.get('file')
		if filename == 'CCTV.mp4':
			datos = np.load('./cctv_values.npy')
		elif filename == 'Fast_Food.mp4':
			datos = np.load('./fast_values.npy')
		elif filename == 'Robo.mp4':
			datos = np.load('./robo_values.npy')
		elif filename == 'Crimes.mp4':
			datos = np.load('./crimes_values.npy')
		elif filename == 'Supermercado.mp4':
			datos = np.load('./super_values.npy')
		elif filename == 'Asalto.mp4':
			datos = np.load('./asalto_values.npy')
		print ("datos: ", datos.shape)
		print ("nombre del video en get: ", filename)
		return render_template('./index.html',nameVideo=filename)

@socketio.on('my event')
def handle_my_custome_event( json_data ):
	print('Received something: ' + str(json_data))
	n = json_data.get('i')
	s = json_data.get('state')
	print('state: ', s)
	t_state = math.floor(int(s))
	print (" index ", t_state)
	clase = datos[t_state][0]
	accuracy = datos[t_state][1]
	time.sleep(0.4)
	respond = {"results" : {"class_name": clase, "score": accuracy, "limit": 1000, "status": 1} }
	result = json.dumps(respond)
	print ('Enviando.............')
	socketio.emit('my response', result)


@app.route('/video_index/')
def index():
    return render_template('./base.html', nameVideo=None)    

if __name__ == '__main__':
	socketio.run(app, debug = True, port=5007)
