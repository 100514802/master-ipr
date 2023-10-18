# master-ipr

- Asignatura: Introducción a la Planificación de Robots (IPR)

## Installation

Installation instructions for installing from source can be found [here](doc/master-ipr-install.md).

## Comms

The following is recommended if working with a Virtual Machine:
- Remove firewall (usually activated in Windows), at least for private networks.
- For the machines to be able to see each other, use VirtualBox `Bridged adapter`, and set the virtual machine's IP within the machine.

## Intructions 
Para sacar los datos en un csv es necesario tener la biblioteca 'pandas'. 
El código implementa dos tipos de algoritmos distintos:
- BFS: realiza una busqueda exhaustiva
- Greedy: trata de realizar el desplazamiento mas directo posible, calculando la distancia desde los nodos hasta la meta y escogiendo la más corta.
    Puede retroceder, evitando asi quedarse atascado/encerrado cuando ya ha visitado todas las celdas que lo rodean.

Cuando lanzamos el programa se pide por terminal especificar las coordenadas iniciales y de la meta, siendo X = filas, Y = columnas. 
En caso de meter unas coordenadas invalidas (ya que son parte del muro o estan fuera del mapa) se pedirá introducir de nuevo estas.
El programa trata de resolver el mapa mediante los dos algoritmos, devolviendo al final el tiempo requerido por cada uno de ellos.
Se pueden consultar los nodos que han sido recorridos en el excel "AlgoritmosBusqueda.xlsx"
