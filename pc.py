#%%
from pymongo import MongoClient
import datetime
import pprint
cliente = MongoClient('localhost')
db = cliente['blog']
noticia = db['noticia']
usuario = db['usuario']
comentario = db['comentario']
noticia.delete_many({})
usuario.delete_many({})
comentario.delete_many({})
def mostrar(coleccion):
    print(f'{coleccion.name:*^64s}')
    for documento in coleccion.find():
        pprint.pprint(documento)
def crear_usuario(id_, nombre, twitter, descripcion, calle=None, 
                  numero=None, puerta=None, ciudad=None, telefonos=None):
    try:
        usuario.insert_one({'_id':id_})
        usuario.delete_one({'_id':id_})
    except(Exception):
        print('ID repetido')
        return
    user = {'_id':id_, 'nombre':nombre, 'twitter':twitter, 'descripcion':descripcion,
            'calle':calle, 'numero':numero, 'puerta':puerta, 'ciudad':ciudad, 'telefonos':telefonos,
            'articulos':None
           }
    usuario.insert_one(user)
def crear_noticia(id_, titulo, cuerpo, id_autor, tags=None):
    try:
        noticia.insert_one({'_id':id_})
        noticia.delete_one({'_id':id_})
    except(Exception):
        print('ID repetido')
        return
    user = usuario.find_one({'_id':id_autor})
    if user is None:
        print('No existe Autor')
        return
    articulos = user['articulos']
    if articulos is None:
        articulos = []
    articulo = {'_id':id_, 'titulo':titulo, 'cuerpo':cuerpo, 'fecha_pub':datetime.datetime.now(),
               'id_autor':id_autor, 'tags':tags,'comentarios':None}
    noticia.insert_one(articulo)
    articulos.append(id_)
    usuario.update_one({'_id':id_autor},{'$set':{'articulos':articulos}})
def crear_comentario(id_, id_noticia, id_usuario, texto):
    try:
        comentario.insert_one({'_id':id_})
        comentario.delete_one({'_id':id_})
    except(Exception):
        print('ID repetido')
        return
    notice = noticia.find_one({'_id':id_noticia})
    user = usuario.find_one({'_id':id_usuario})
    if notice is None or user is None:
        print('No existe Usuario o Noticia')
        return
    comentarios = notice['comentarios']
    if comentarios is None:
        comentarios = []
    coment = {'_id':id_, 'id_usuario':id_usuario, 'id_noticia':id_noticia, 'texto':texto,
              'fecha_pub':datetime.datetime.now()}
    comentario.insert_one(coment)
    comentarios.append(id_)
    noticia.update_one({'_id':id_noticia},{'$set':{'comentarios':comentarios}})

crear_usuario(id_=94,nombre='jainy', twitter='jainy.com',descripcion='green smile',
telefonos=[999888777,111222333,555666777],ciudad='Lima')
crear_usuario(id_=41,nombre='silvia', twitter='silvia.com',descripcion='faz divina')
crear_usuario(id_=1,nombre='user1', twitter='user1.com',descripcion='solamente user1')
crear_usuario(id_=2,nombre='user2', twitter='user2.com',descripcion='solamente user2')
crear_usuario(id_=3,nombre='user3', twitter='user3.com',descripcion='solamente user3')

crear_noticia(id_=55,titulo='Bondad', cuerpo='Los niños nacidos en "Un mundo feliz"',
              id_autor=94, tags=['psicologia','etica'])
crear_noticia(id_=66, titulo='Mujeres', cuerpo='Reseña de la novela "Mujeres"',
              id_autor=41,tags=['sexo','literatura'])

crear_comentario(id_=15,id_noticia=55, id_usuario=41, texto='Padres e hijos')
crear_comentario(id_=16,id_noticia=55, id_usuario=41, texto='Los Gammas, los Epsilones, los Deltas')
crear_comentario(id_=17,id_noticia=55, id_usuario=41, texto='Los criterios de producción aplicados a la biología')
crear_comentario(id_=14,id_noticia=66, id_usuario=1, texto='spam')
crear_comentario(id_=13,id_noticia=66, id_usuario=2, texto='spam')
crear_comentario(id_=12,id_noticia=66, id_usuario=3, texto='spam')

mostrar(usuario)
mostrar(noticia)
mostrar(comentario)
#%%
import numpy as np
import matplotlib.pyplot as plt
def maxmin(x,y):
    m,n,p = x.shape[0],y.shape[1],x.shape[1]
    z = np.zeros((m,n),dtype=np.float64)
    w = np.zeros(p)
    for i in range(0,m):
        for j in range(0,n):
            for k in range(0,p):
                w[k] = min(x[i][k],y[k][j])
            z[i][j] = max(w)
    return z
p = np.array([[0.8,0.2],[1,0],[0.2,0.8],[0,1]])
q = np.array([[0.8,0.2,0],[0,0.2,0.8]])
print(p)
print(q)
print(maxmin(p,q))
plt.axis((2,4,3,4))
plt.plot([2,4],[3,4],'--r')