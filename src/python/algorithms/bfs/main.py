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
FILE_NAME = "C:\\Users\\quiqu\\Desktop\\Master\\Introducción a la planificación de robots\\Practica\\master-ipr\\map5\\map5.csv" # Windows-style relative path, note the `\\`

# # Empleo la libreria time para medir tiempo de ejecucion, pandas para sacar datos en un archivo csv
import time
import pandas as pd

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

# ## Creo una función que me permita limpiar el mapa antes de buscar la meta con un algoritmo de busqueda
def resetCharMap(charMap):
    for i in range(len(charMap)): # Genero un bucle que me compruebe todas las celdas
        for j in range(len(charMap[i])):
            if charMap[i][j] == '2': # Debo cambiar aquellas celdas que han sido visitadas
                charMap[i][j] = '0'  # Restaura celdas visitadas a su estado original
    return charMap

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

while not datos_partida: #Mediante este bucle me aseguro de que el punto de partida sea válido
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

while not datos_meta: #Mediante este bucle me aseguro de que el punto de partida sea válido
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

# ## Voy a tener dos funciones distintas, una greedy y una exhaustiva, de modo que pueda comparar los tiempos de ejecución de cada una
def greedy(charMap, init):
    inicio = time.time() #inicializo el contador de tiempo
    charMap = resetCharMap(charMap)
    # ## `nodes` contendrá los nodos del grafo

    nodes = []
    node_stack = [] #es una pila que me permitirá volver hacia atrás
    # ## Añadimos el primer nodo a `nodes`

    nodes.append(init)

    # ##Creo una variable nodo en la que vamos guardando el nodo visitado
    newNode = init

    done = False  # clásica condición de parada del bucle `while`
    goalParentId = -1  # -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

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
            if( charMap[tmpX][tmpY] == '4' ): # Encuentro la meta
                print("GOALLLL!!!")
                goalParentId = node.myId  # aquí sustituye por real
                fin = time.time() # finalizo el contador
                duracion = fin - inicio # calculo el tiempo transcurrido en la ejecucion 
                done = True
                break
            elif ( charMap[tmpX][tmpY] == '0' ): # Encuentro nodo sin visitar
                print("mark visited")
                oldNode = newNode #almaceno el nodo anterior
                newNode = Node(tmpX, tmpY, len(nodes), node.myId)
                charMap[tmpX][tmpY] = '2'
                nodes.append(newNode)
                if (oldNode.parentId != -2):
                    node_stack.append(oldNode.parentId) #Actualizo el valor de la pila con el nodo que visito (guardo parentId)
                break
            elif ( charMap[tmpX][tmpY] == '2' or  charMap[tmpX][tmpY] == '1'): # cuando ya hemos pasado por la celda debemos aumentar el contador
                print("Casilla visitada")
                direccion_bloqueada += 1 #Aumento el contador de direcciones no posibles
                if (direccion_bloqueada == 8): #En el momento que el contador llega a 8, tenemos que volver atras dado que no hay moviemiento posible
                    if node_stack :
                        prev_node_id = node_stack.pop() #Extraigo el parentId del último nodo visitado
                        prev_node = nodes[prev_node_id] #busco ese nodo en la lista nodes que contiene todos
                        newNode = prev_node #asigno a mi nuevo nodo el nodo anterior, de modo que me muevo hacia atrás
                    else:
                        print("No hay path posible") #En eo caso que no queden nodos disponibles, se indicará que no hay camino posible
                        done = True
                        break
        dumpMap()  

    # ## Display solución hallada
    # Convierte charMap en un DataFrame de pandas
    mapa = pd.DataFrame(charMap)
    mapa = mapa.replace('1', 'X') # Sustituyo los muros por una X, asi no hay confusión entre un muro y el primer nodo visitado
    mapa = mapa.replace('4', 'G') # La meta la señalizo con G (goal)
    output_csv = "mapa_resultado_greedy.csv"  # Nombre del archivo CSV de salida
    
    nodos_visitados = [] # creo una lista con los nodos que voy a recorrer para enviarlo al excel

    print("%%%%%%%%%%%%%%%%%%%")
    ok = False
    while not ok:
        for node in nodes:
            if( node.myId == goalParentId ):
                node.dump()
                nodos_visitados.append([node.x, node.y, node.myId, node.parentId])  # Relleno la lista con x, y, ID, parentId                 
                mapa.at[node.x, node.y] = node.myId # Relleno el mapa con los nodos que voy a recorrer, de modo que tengo un csv con las celdas visitadas numeradas
                goalParentId = node.parentId
                if( goalParentId == -2):
                    print("%%%%%%%%%%%%%%%%%")
                    ok = True

    # Crear un DataFrame con los datos
    nodos_visitados.reverse() #Invierto el orden de la lista con los nodos que voy a recorrer
    data_nodos = {
        "X": [var[0] for var in nodos_visitados], # Guardo en data_nodos los valores separados en cuatro columnas
        "Y": [var[1] for var in nodos_visitados],
        "ID": [var[2] for var in nodos_visitados],
        "ParentID": [var[3] for var in nodos_visitados]
    }

    df_nodos = pd.DataFrame(data_nodos) # Genero el data frame que se envía al archivo excel
    # Especifica la ruta del archivo Excel de salida
    excel_file = "AlgoritmosBusqueda.xlsx"

    # Guarda el DataFrame en un archivo Excel
    df_nodos.to_excel(excel_file, index=False) # Envío el dataframe al archivo excel especificado

    # Guarda el DataFrame en un archivo CSV
    mapa.to_csv(output_csv, index=False, header=False) # Guardo el mapa en csv
    print("Mapa final guardado en", output_csv)  

    # ## Devuelvo el valor del tiempo transcurrido
    return duracion

def bfs(charMap, init):
    # ## Empieza algoritmo
    inicio = time.time() #inicializo el contador

    charMap = resetCharMap(charMap)
    # ## `nodes` contendrá los nodos del grafo

    nodes = []
    
    # ## Añadimos el primer nodo a `nodes`
    
    nodes.append(init)
    
    # ##Creo una variable nodo en la que vamos guardando el nodo visitado
    newNode = init

    done = False  # clásica condición de parada del bucle `while`
    goalParentId = -1  # -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

    while not done:
        print("--------------------- number of nodes: "+str(len(nodes)))
        for node in nodes:
            node.dump()

            # up
            tmpX = node.x - 1
            tmpY = node.y
            if( charMap[tmpX][tmpY] == '4' ):
                print("up: GOALLLL!!!")
                goalParentId = node.myId  # aquí sustituye por real
                fin = time.time() # finalizo el contador
                duracion = fin - inicio # calculo el tiempo transcurrido en la ejecucion
                done = True
                break
            elif ( charMap[tmpX][tmpY] == '0' ):
                print("up: mark visited")
                newNode = Node(tmpX, tmpY, len(nodes), node.myId)
                charMap[tmpX][tmpY] = '2'
                nodes.append(newNode)

            # down
            tmpX = node.x + 1
            tmpY = node.y
            if( charMap[tmpX][tmpY] == '4' ):
                print("down: GOALLLL!!!")
                goalParentId = node.myId # aquí sustituye por real
                fin = time.time() # finalizo el contador
                duracion = fin - inicio # calculo el tiempo transcurrido en la ejecucion
                done = True
                break
            elif ( charMap[tmpX][tmpY] == '0' ):
                print("down: mark visited")
                newNode = Node(tmpX, tmpY, len(nodes), node.myId)
                charMap[tmpX][tmpY] = '2'
                nodes.append(newNode)

            # right
            tmpX = node.x
            tmpY = node.y + 1
            if( charMap[tmpX][tmpY] == '4' ):
                print("right: GOALLLL!!!")
                goalParentId = node.myId # aquí sustituye por real
                fin = time.time() # finalizo el contador
                duracion = fin - inicio # calculo el tiempo transcurrido en la ejecucion
                done = True
                break
            elif ( charMap[tmpX][tmpY] == '0' ):
                print("right    : mark visited")
                newNode = Node(tmpX, tmpY, len(nodes), node.myId)
                charMap[tmpX][tmpY] = '2'
                nodes.append(newNode)

            # left
            tmpX = node.x
            tmpY = node.y - 1
            if( charMap[tmpX][tmpY] == '4' ):
                print("left: GOALLLL!!!")
                goalParentId = node.myId # aquí sustituye por real
                fin = time.time() # finalizo el contador
                duracion = fin - inicio # calculo el tiempo transcurrido en la ejecucion
                done = True
                break
            elif ( charMap[tmpX][tmpY] == '0' ):
                print("left: mark visited")
                newNode = Node(tmpX, tmpY, len(nodes), node.myId)
                charMap[tmpX][tmpY] = '2'
                nodes.append(newNode)

            dumpMap()

    # ## Display solución hallada 
    print("%%%%%%%%%%%%%%%%%%%")
    ok = False
    while not ok:
        for node in nodes:
            if( node.myId == goalParentId ):
                node.dump()
                goalParentId = node.parentId
                if( goalParentId == -2):
                    print("%%%%%%%%%%%%%%%%%")
                    ok = True

    # ## Devuelvo el valor del tiempo transcurrido
    return duracion

duracion_bfs = bfs(charMap, init)
duracion_greedy = greedy(charMap, init)
print(f"El tiempo con funcion bfs es de: {duracion_bfs:.3f} segundos\n")
print(f"El tiempo con funcion greedy es de: {duracion_greedy:.3f} segundos\n")
