from bson.objectid import ObjectId
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pymongo import MongoClient
import pprint

def active_users(db):
	users_t=db.usermodels.count_documents({});
	users_active_n=db.usermodels.count_documents({'active': True},)
	users_resto=users_t-(users_active_n)
	users=[users_active_n, users_resto]

	print('Hay', users_active_n, ' usuarios activos de un total de', users_t, '\nPorcentaje de usuarios activos:', users_active_n*100/users_t, '%')
	return users_active_n, users_t

def elements_by_user(db, x, y):
	elements_by_user=np.zeros((x,y)) #cada fila es un usuario, cada columna un tipo de documento
	fila=0
	columnas=('documentos', 'ejercicios', 'entregas')
	filas=[]
	# Documentos, ejercicios y entregas por usuario:
	for user in db.usermodels.find({'active': True}):
		elements_by_user[fila][0]=db.documentmodels.count_documents({'user': user['_id']})
		elements_by_user[fila][1]=db.exercisemodels.count_documents({'user': user['_id']})
		elements_by_user[fila][2]=db.submissionmodels.count_documents({'user': user['_id']})
		filas.append('usuario{}'.format(fila))
		fila+=1

	return elements_by_user, filas, columnas

def draw_elements(elements, rows, columns):
	colores = ('g', 'r', 'b', 'w')
	n_filas=len(rows)
	ancho=0.35
	index = np.arange(len(columns)) + 0.3

	# Initialize the vertical-offset for the stacked bar chart.
	y_offset = np.zeros(len(columns))

	# Plot bars and create text labels for the table
	cell_text = []
	for fila in range(n_filas):
	    plt.bar(index, elements.T[fila], ancho, bottom=y_offset, color=colores[fila])
	    #plt.legend(filas[fila])
	    y_offset = y_offset + elements.T[fila]

	plt.ylabel('Numero de documentos por usuario')
	plt.title('Documentos, ejercicios y entregas por usuario')
	plt.xticks(index, rows)
	plt.yticks(np.arange(0, (np.max(y_offset)+5), 2))
	plt.legend(columns)
	plt.savefig('docs_ejs_by_user.png')

def submissions_statics(log_data):
	sub_create=0
	sub_login=0
	for fila in range(len(log_data)):
		if(log_data['modelType'][fila]=='submission'):
			if(log_data['action'][fila]=='create'):
				sub_create+=1
			elif(log_data['action'][fila]=='login'):
				sub_login+=1
	
	return sub_create, sub_login


def main():
	headers=['date', 'api', 'info', 'modelType', 'action', 'docType', 'userID', 'other']
	log_data=pd.read_csv('info.log', parse_dates={"Datetime": [0]}, names=headers)

	client = MongoClient('localhost', 27017)
	db= client['back_bitbloq_db']

	users_active_n, users_t=active_users(db)
	elementos, filas, columnas = elements_by_user(db, users_active_n, 3)
	draw_elements(elementos, filas, columnas)
	sub_create, sub_login=submissions_statics(log_data)


main()

