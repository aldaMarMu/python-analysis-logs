import matplotlib.pyplot as plt
import numpy as np
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db= client['back_bitbloq_db']

# Contar documentos, ejercicios y submissions de cada tipo
docs=db.documentmodels.count_documents({});
docs_rob=db.documentmodels.count_documents({'type': 'robotica'},)
docs_3D=db.documentmodels.count_documents({'type': '3D'},)
docs_jr=db.documentmodels.count_documents({'type': 'robotica_jr'},)
docs_resto=docs-(docs_rob+docs_3D+docs_jr)
documentos=[docs_rob, docs_3D, docs_jr, docs_resto]

exs=db.exercisemodels.count_documents({})
exs_rob=db.exercisemodels.count_documents({'type': 'robotica'},)
exs_3D=db.exercisemodels.count_documents({'type': '3D'},)
exs_jr=db.exercisemodels.count_documents({'type': 'robotica_jr'},)
exs_resto=exs-(exs_rob+exs_3D+exs_jr)
ejercicios=[exs_rob, exs_3D, exs_jr, exs_resto]

subs=db.submissionmodels.count_documents({})
subs_rob=db.submissionmodels.count_documents({'type': 'robotica'},)
subs_3D=db.submissionmodels.count_documents({'type': '3D'},)
subs_jr=db.submissionmodels.count_documents({'type': 'robotica_jr'},)
subs_resto=subs-(subs_rob+subs_3D+subs_jr)
submissions=[subs_rob, subs_3D, subs_jr, subs_resto]

# crear la matriz con todos os datos
datos=np.array([documentos, ejercicios, submissions])
columnas=('robotica', '3D', 'JR', 'otros')
filas=('documentos', 'ejercicios', 'submissions')
print(datos)

#colores y datos para pintar la gráfica
colores = ('g', 'r', 'b', 'w')
n_filas=len(filas)
ancho=0.35
index = np.arange(len(columnas)) + 0.3

# Initialize the vertical-offset for the stacked bar chart.
y_offset = np.zeros(len(columnas))

# Plot bars and create text labels for the table
cell_text = []
for fila in range(n_filas):
    plt.bar(index, datos[fila], ancho, bottom=y_offset, color=colores[fila])
    y_offset = y_offset + datos[fila]

# Adjust layout to make room for the table:
plt.subplots_adjust(left=0.2, bottom=0.2)
print('y_offset: ',(np.max(y_offset)+5))

plt.ylabel('Numero de documentos')
plt.title('Documentos, ejercicios y entregas por tipos')
plt.xticks(index, ('robotica', '3D', 'robotica JR', 'otros'))
plt.yticks(np.arange(0, (np.max(y_offset)+5), 2))
plt.legend(filas)
plt.savefig('docs_ejs_by_type.png')