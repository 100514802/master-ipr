#! /usr/bin/env python

"""
# Notactión

## Mapa

En mapa original:

* 0: libre
* 1: ocupado (muro/obstáculo)

Vía código incorporamos:

* 2: visitado
* 3: start
* 4: goal

## Nodo

Nós
* -2: parentId del nodo start
* -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

# Específico de implementación Python

* Índices empiezan en 0
* charMap
"""

# # Initial values are hard-coded (A nivel mapa)

#FILE_NAME = "/usr/local/share/master-ipr/map1/map1.csv" # Linux-style absolute path
#FILE_NAME = "C:\\Users\\USER_NAME\\Downloads\\master-ipr\\map1\\map1.csv" # Windows-style absolute path, note the `\\` and edit `USER_NAME`
#FILE_NAME = "../../../../map1/map1.csv" # Linux-style relative path
FILE_NAME = "C:\\Users\\quiqu\\Desktop\\Master\\Introducción a la planificación de robots\\Practica\\master-ipr\\map1\\map1.csv" # Windows-style relative path, note the `\\`

# # Define Node class (A nivel grafo/nodo)

class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId))

# # Mapa

# ## Creamos estructura de datos para mapa

charMap = []

# ## Creamos función para volcar estructura de datos para mapa

def dumpMap():
    for line in charMap:
        print(line)

# ## De fichero, llenar estructura de datos de fichero (`to parse`/`parsing``) para mapa

with open(FILE_NAME) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

# ## Ahora vamos a ver cual es la dimension del mapa cargado

num_filas = len(charMap)

if num_filas > 0:
    num_columnas = len(charMap[0])  # Tenemos todas las filas con igual longitud
else:
    num_columnas = 0

# ## Pido por terminal los puntos de partida y de meta:
datos_partida = 0 # pongo la variable a uno cuando los datos son validos

while not datos_partida:
    START_X = int(input("Ingrese la coordenada X de partida: ")) - 1
    START_Y = int(input("Ingrese la coordenada Y de partida: ")) - 1
    if (START_X < 0 or START_X > num_filas ):
        print("La coordenada X de partida esta fuera del rango del mapa")
    elif (START_Y < 0 or START_Y > num_columnas ):
        print("La coordenada Y de partida esta fuera del rango del mapa")
    elif (charMap[START_X][START_Y] == '1'): # celda ocupada
        print("El punto de partida coincide con un muro")
    else:
        datos_partida = 1

datos_meta = 0 # pongo la variable a uno cuando los datos son validos

while not datos_meta:
    END_X = int(input("Ingrese la coordenada X de la meta: "))
    END_Y = int(input("Ingrese la coordenada Y de la meta: "))
    if (END_X < 0 or END_X > num_filas ):
        print("La coordenada X de la meta esta fuera del rango del mapa")
    elif (END_Y < 0 or END_Y > num_columnas ):
        print("La coordenada Y de la meta esta fuera del rango del mapa")
    elif (charMap[END_X][END_Y] == '1'): # celda ocupada
        print("El punto de meta coincide con un muro")
    elif ([END_X, END_Y] == [START_X, START_Y]): # celda de partida = celda de meta
        print("El punto de meta no puede coincidir con el de partida")
    else:
        datos_meta = 1



# ## A nivel mapa, integramos la info que teníamos de start & end

charMap[START_X][START_Y] = '3' # 3: start
charMap[END_X][END_Y] = '4' # 4: goal

# ## Volcamos mapa por consola

dumpMap()

# # Grafo búsqueda

# ## Creamos el primer nodo
init = Node(START_X, START_Y, 0, -2)
# init.dump() # comprobar que primer nodo bien

# ## `nodes` contendrá los nodos del grafo

nodes = []

# ## Añadimos el primer nodo a `nodes`

nodes.append(init)

# ##Creo una variable nodo en la que vamos guardando el nodo visitado
newNode = init


# ## Empieza algoritmo

done = False  # clásica condición de parada del bucle `while`
goalParentId = -1  # -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

# BORRAR mode = 1 #Tenemos cuatro modos de desplazamiento (uno por cada dirección)

while not done:
    print("--------------------- number of nodes: "+str(len(nodes)))
    
    #Actualizamos el nodo
    node = newNode
    
    #Creamos un array con los tipos de movimientos que pueden realizarse
    movimientos_disponibles = [
    (node.x - 1, node.y), # Arriba
    (node.x , node.y - 1), # Izquierda
    (node.x + 1, node.y), # Abajo
    (node.x, node.y + 1), # Derecha
    (node.x - 1, node.y - 1), # Diagonal sup izq
    (node.x - 1, node.y + 1), # Diagonal sup dcha
    (node.x + 1, node.y - 1), # Diagonal inf izq
    (node.x + 1, node.y + 1) # Diagonal inf dcha
    ]
    
    #Creo una función que pueda calcular la distancia hasta la meta
    def distancia(movimiento):
        return abs(movimiento[0] - END_X) + abs(movimiento[1] - END_Y)
    
    #A partir de la distancia a la meta ordenamos los movimientos
    movimientos_disponibles.sort(key=distancia)

    
    #Creo una variable en la que almaceno un contaje de las direcciones en las que no debe/puede moverse,
    #cuando esta variable llega a ocho me indica que debemos retroceder
    direccion_bloqueada = 0
    
    #El siguiente bucle va probando los movimientos según el orden de la lista
    for movimiento in movimientos_disponibles:
        tmpX, tmpY = movimiento
        if( charMap[tmpX][tmpY] == '4' ):
            print("GOALLLL!!!")
            goalParentId = node.myId  # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)
            break
        elif ( charMap[tmpX][tmpY] == '2'): # cuando ya hemos pasado por la celda debemos aumentar el contador
            print("Casilla visitada")
            direccion_bloqueada += 1
            if (direccion_bloqueada == 8): # si ya hemos pasado por todas las celdas de alrededor debemos volver al punto anterior
                for a in nodes:
                    if ( a.myId == node.parentId ): # cuando el ID del nodo coincide con el parentID, hemos encontrado el anterior
                        newNode = a
                        break             
    dumpMap()    

    """
    if mode == 1:
        node = newNode #actualizo el valor del nodo con el que vamos a trabajar
        node.dump()

        # up
        tmpX = node.x - 1
        tmpY = node.y
        if( charMap[tmpX][tmpY] == '4' ):
            print("up: GOALLLL!!!")
            goalParentId = node.myId  # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("up: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)
        elif ( charMap[tmpX][tmpY] == '1' or  charMap[tmpX][tmpY] == '2'): # avanzo en la misma direccion hasta chocar con un muro
            print("up: wall found")
            mode = 2
        
        dumpMap()
            
    if mode == 2:
        node = newNode
        node.dump()
        # right
        tmpX = node.x
        tmpY = node.y + 1
        if( charMap[tmpX][tmpY] == '4' ):
            print("right: GOALLLL!!!")
            goalParentId = node.myId # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("right    : mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)
        elif ( charMap[tmpX][tmpY] == '1' or  charMap[tmpX][tmpY] == '2'):
            print("right: wall found")
            mode = 3

        dumpMap()

    if mode == 3:
        node = newNode
        node.dump()
        # down
        tmpX = node.x + 1
        tmpY = node.y
        if( charMap[tmpX][tmpY] == '4' ):
            print("down: GOALLLL!!!")
            goalParentId = node.myId # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("down: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)
        elif ( charMap[tmpX][tmpY] == '1' or  charMap[tmpX][tmpY] == '2'):
            print("down: wall found")
            mode = 4
        dumpMap()
        
        
    if mode == 4:
        node = newNode
        node.dump()
        # left
        tmpX = node.x
        tmpY = node.y - 1
        if( charMap[tmpX][tmpY] == '4' ):
            print("left: GOALLLL!!!")
            goalParentId = node.myId # aquí sustituye por real
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("left: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)
        elif ( charMap[tmpX][tmpY] == '1' or  charMap[tmpX][tmpY] == '2'):
            print("left: wall found")
            mode = 1
        dumpMap()
"""

# ## Display solución hallada

import pandas as pd

# Convierte charMap en un DataFrame de pandas
mapa = pd.DataFrame(charMap)
output_csv = "mapa_resultado.csv"  # Nombre del archivo CSV de salida
mapa[mapa==1] = 5

print("%%%%%%%%%%%%%%%%%%%")
ok = False
while not ok:
    for node in nodes:
        if( node.myId == goalParentId ):
            node.dump()
            mapa.at[node.x, node.y] = node.myId
            goalParentId = node.parentId
            if( goalParentId == -2):
                print("%%%%%%%%%%%%%%%%%2")
                ok = True



# Guarda el DataFrame en un archivo CSV
mapa.to_csv(output_csv, index=False, header=False)
print("Mapa final guardado en", output_csv)
