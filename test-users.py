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

	print('\n ----------------------------------------------------- \n')
	print('Hay', users_active_n, ' usuarios activos de un total de', users_t, '\nPorcentaje de usuarios activos:', users_active_n*100/users_t, '%')
	print('\n ----------------------------------------------------- \n')
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
		print('El usuario ', fila,  'tiene ', elements_by_user[fila][0], ' documentos, ', elements_by_user[fila][1], ' ejercicios, y ', elements_by_user[fila][2], ' submissions.')
		fila+=1

	return elements_by_user, filas, columnas
	

def calculate_averages(elements_by_user):
	print('\n ----------------------------------------------------- \n')
	#media de documentos (columna 0):
	doc_av=np.average(elements_by_user[:,0])
	print('La media de docuementos por usuario es: ', doc_av)	

	#media de ejercicios (columna 1):
	ex_av=np.average(elements_by_user[:,1])
	print('La media de ejercicios por usuario es: ', ex_av)	

	#media de submissions (columna 2):
	sub_av=np.average(elements_by_user[:,2])
	print('La media de submissions por usuario es: ', sub_av)

	medias=[doc_av, ex_av, sub_av]
	
	print('\n ----------------------------------------------------- \n')
	return medias


def exercise_stadistics(db, elements_by_user, n_usuarios):
	exercises=np.zeros((n_usuarios, 2)) # dos columnas
	fila=0
	columnas=('ejercicios_tot', 'ejercicios_doc')
	filas=[] # usuarios
	max_docs=np.amax(elements_by_user[:,0])
	n_ex_doc=np.zeros((n_usuarios, int(max_docs)))
	medias_ex_doc=np.zeros(int(max_docs))
	# Documentos, ejercicios y entregas por usuario:
	for user in db.usermodels.find({'active': True}):
		exercises[fila][0]=elements_by_user[fila][1]
		documents=db.documentmodels.find({'user': user['_id']})
		doc=0
		for document in documents:
			n_ex_doc[fila][doc]=db.exercisemodels.count_documents({'user':user['_id'], 'document': document['_id']})
			doc+=1
		#exercises[fila][1]=db.exercisemodels.count_documents({'document': user['_id']})
		filas.append('usuario{}'.format(fila))
		fila+=1
	for i in range(int(max_docs)):
		medias_ex_doc[i]=np.average(n_ex_doc[:,i])
	media_ex_t=np.average(medias_ex_doc)
	print('La media de ejercicios por documento y por usuario es: ',media_ex_t)
	print('\n ----------------------------------------------------- \n')
	return exercises, filas, columnas

def submissions_stadistics(db, elements_by_user, n_usuarios):
	submissions=np.zeros((n_usuarios, 2)) # dos columnas
	fila=0
	columnas=('submissions_tot', 'submissions_ex')
	filas=[] # usuarios
	max_ex=np.amax(elements_by_user[:,1])
	n_sub_ex=np.zeros((n_usuarios, int(max_ex)))
	medias_sub_ex=np.zeros(int(max_ex))
	# Documentos, ejercicios y entregas por usuario:
	for user in db.usermodels.find({'active': True}):
		submissions[fila][0]=elements_by_user[fila][2]
		exercises=db.exercisemodels.find({'user': user['_id']})
		ex=0
		for exercise in exercises:
			n_sub_ex[fila][ex]=db.submissionmodels.count_documents({'user':user['_id'], 'exercise': exercise['_id']})
			ex+=1
		#submissions[fila][1]=db.exercisemodels.count_exercises({'exercise': user['_id']})		
		filas.append('usuario{}'.format(fila))
		fila+=1
	for i in range(int(max_ex)):
		medias_sub_ex[i]=np.average(n_sub_ex[:,i])
	media_sub_t=np.average(medias_sub_ex)
	print('La media de entregas por ejercicio y por usuario es: ',media_sub_t)
	print('\n ----------------------------------------------------- \n')
	return submissions, filas, columnas	

def draw_elements(data, rows, columns, medias):
	colores = ('g', 'r', 'b', 'w')
	n_usuarios=len(rows)
	n_docs_type=len(columns)
	ancho=0.35
	index = np.arange(n_usuarios)+0.3
	plt.figure()

	# Initialize the vertical-offset for the stacked bar chart.
	y_offset = np.zeros(n_usuarios)

	med_docs= np.zeros(n_usuarios)+medias[0]

	# Plot bars and create text labels for the table
	cell_text = []
	for n in range(n_docs_type):
		plt.bar(index, data[:,n], ancho, bottom=y_offset, color=colores[n])
		plt.plot(index, np.zeros(n_usuarios)+medias[n], color=colores[n]) # pinta en una línea la media
		y_offset = y_offset + data[:,n]

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

def login_statics(log_data):
	n_logins=0
	plt.figure()
	for fila in range(len(log_data)):
		if(log_data['action'][fila]=='login'):
			n_logins+=1
			plt.plot(log_data['Datetime'][fila], n_logins, 'ro')
	plt.savefig('logins.png')

def main():
	headers=['date', 'info', 'api', 'modelType', 'action', 'docType', 'userID', 'other']
	log_data=pd.read_csv('info.log', parse_dates={"Datetime": [0]}, names=headers)
	login_statics(log_data)

	client = MongoClient('localhost', 27017)
	db= client['back_bitbloq_db']

	users_active_n, users_t=active_users(db)
	models_by_user, filas, columnas = elements_by_user(db, users_active_n, 3) #y es 3 porque hay documentos, ejercicios y enetregas
	medias = calculate_averages(models_by_user)
	draw_elements(models_by_user, filas, columnas, medias)

	exercise_stadistics(db, models_by_user, users_active_n)
	submissions_stadistics(db, models_by_user, users_active_n)
	sub_create, sub_login=submissions_statics(log_data)



main()

