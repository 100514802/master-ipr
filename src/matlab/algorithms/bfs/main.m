%{
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

# Específico de implementación MATLAB

* Índices empiezan en 1
* intMap
%}

% # Initial values are hard-coded (A nivel mapa)

%FILE_NAME = "/usr/local/share/master-ipr/map1/map1.csv"; % Linux-style absolute path
%FILE_NAME = "C:\\Users\\USER_NAME\\Downloads\\master-ipr\\map1\\map1.csv"; % Windows-style absolute path, note the `\\` and edit `USER_NAME`
%FILE_NAME = "../../../../map1/map1.csv"; % Linux-style relative path
FILE_NAME = "..\\..\\..\\..\\map1\\map1.csv"; % Windows-style relative path, note the `\\`
START_X = 2+1;
START_Y = 2+1;
END_X = 7+1;
END_Y = 2+1;

% # Mapa

% ## Creamos estructura de datos para mapa
% ## De fichero, llenar estructura de datos de fichero (`to parse`/`parsing``) para mapa

intMap = csvread(FILE_NAME);

% ## A nivel mapa, integramos la info que teníamos de start & end

intMap(START_X, START_Y) = 3;
intMap(END_X, END_Y) = 4;

% ## Volcamos mapa por consola

disp(intMap);

% # Grafo búsqueda

% ## Creamos primer nodo
init = Node(START_X, START_Y, 0, -2);
% init.dump(); % comprobar que primer nodo bien

% ## `nodes` contendrá los nodos del grafo
% ## Añadimos el primer nodo a `nodes`
nodes = init;

% ## Empieza el algoritmo

done = false;
goalParentId = -1;

while(~done)
    fprintf("--------------------- number of nodes: %d\n",length(nodes));
    for node = nodes
        node.dump;

        % up
        tmpX = node.x - 1;
        tmpY = node.y;
        if( intMap(tmpX, tmpY) == 4 )
            disp("up: GOALLLL!!!");
            goalParentId = node.myId;
            done = true;
            break
        elseif ( intMap(tmpX, tmpY) == 0 )
            disp("up: mark visited");
            newNode = Node(tmpX, tmpY, length(nodes), node.myId);
            intMap(tmpX, tmpY) = 2;
            nodes = [nodes newNode];
        end

        % down
        tmpX = node.x + 1;
        tmpY = node.y;
        if( intMap(tmpX, tmpY) == 4 )
            disp("down: GOALLLL!!!");
            goalParentId = node.myId;
            done = true;
            break
        elseif ( intMap(tmpX, tmpY) == 0 )
            disp("down: mark visited");
            newNode = Node(tmpX, tmpY, length(nodes), node.myId);
            intMap(tmpX, tmpY) = 2;
            nodes = [nodes newNode];
        end

        % right
        tmpX = node.x;
        tmpY = node.y + 1;
        if( intMap(tmpX, tmpY) == 4 )
            disp("right: GOALLLL!!!");
            goalParentId = node.myId;
            done = true;
            break
        elseif ( intMap(tmpX, tmpY) == 0 )
            disp("right: mark visited");
            newNode = Node(tmpX, tmpY, length(nodes), node.myId);
            intMap(tmpX, tmpY) = 2;
            nodes = [nodes newNode];
        end

        % left
        tmpX = node.x;
        tmpY = node.y - 1;
        if( intMap(tmpX, tmpY) == 4 )
            disp("left: GOALLLL!!!");
            goalParentId = node.myId;
            done = true;
            break
        elseif ( intMap(tmpX, tmpY) == 0 )
            disp("left: mark visited");
            newNode = Node(tmpX, tmpY, length(nodes), node.myId);
            intMap(tmpX, tmpY) = 2;
            nodes = [nodes newNode];
        end

        disp(intMap);
    end
end

% ## Display solución hallada

disp("%%%%%%%%%%%%%%%%%%%");
ok = false;
while(~ok)
    for node = nodes
        if( node.myId == goalParentId )
            node.dump();
            goalParentId = node.parentId;
            if( goalParentId == -2)
                disp("%%%%%%%%%%%%%%%%%2");
                ok = true;
            end
        end
    end
end
