#include <vector>
#include <fstream>
#include <sstream>

/*
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

# Específico de implementación C++

* Índices empiezan en 0
* intMap
*/

// # Initial values are hard-coded (A nivel mapa)

// #define FILE_NAME "/usr/local/share/master-ipr/map1/map1.csv" // Linux-style absolute path
// #define FILE_NAME "C:\\Users\\USER_NAME\\Downloads\\master-ipr\\map1\\map1.csv" // Windows-style absolute path, note the `\\` and edit `USER_NAME`
//-- For relative paths, adding extra `..` to account for out-of-source builds
// #define FILE_NAME "../../../../../map1/map1.csv" // Linux-style relative path
#define FILE_NAME "..\\..\\..\\..\\..\\map1\\map1.csv" // Windows-style relative path, note the `\\`
#define START_X 2
#define START_Y 2
#define END_X 7
#define END_Y 2

// # Define Node class (A nivel grafo/nodo)

class Node
{
public:
    Node(int x, int y, int id, int parentId) : x(x), y(y), id(id), parentId(parentId) {}
    void dump() { printf("---------- x %d, y %d, id %d, pid %d\n", x, y, id, parentId); }
    int getX() { return x; }
    int getY() { return y; }
    int getId() { return id; }
    int getParentId() { return parentId; }

private:
    int x, y, id, parentId;
};

// # Solo C++: Función auxiliar para llenar estructura de datos de fichero (`to parse`/`parsing``) para mapa

bool parseFileLine(std::ifstream &file, std::vector<int> &intsOnFileLine)
{
    intsOnFileLine.clear();

    if (file.eof())
        return false;

    std::string csv;
    getline(file, csv);
    std::istringstream buffer(csv);
    std::string token;
    int d;

    while (std::getline(buffer, token, ','))
    {
        std::istringstream ss(token);
        ss >> d;
        intsOnFileLine.push_back(d);
    }

    return true;
}

// # Sólo C++: Clase principal

class Program
{
public:
    // # Sólo C++: Función principal de clase principal (sólo en C++)

    bool run()
    {
        // # Mapa

        // ## De fichero, llenar estructura de datos de fichero (`to parse`/`parsing``) para mapa

        std::ifstream file;
        std::string fileName = FILE_NAME;
        file.open(fileName.c_str());
        if (!file.is_open())
        {
            printf("Not able to open file: %s\n", fileName.c_str());
            return false;
        }
        printf("Opened file: %s\n", fileName.c_str());

        std::vector<int> intsOnFileLine;

        while (parseFileLine(file, intsOnFileLine))
        {
            if (intsOnFileLine.size() == 0)
                continue;

            intMap.push_back(intsOnFileLine);
        }

        file.close();

        // ## A nivel mapa, integramos la info que teníamos de start & end

        intMap[START_X][START_Y] = 3;
        intMap[END_X][END_Y] = 4;

        // ## Volcamos mapa por consola

        dumpMap();

        // # Grafo búsqueda

        // ## Creamos el primer nodo

        Node *init = new Node(START_X, START_Y, 0, -2);
        // init->dump(); // comprobar que primer nodo bien

        // ## Añadimos el primer nodo a `nodes`

        nodes.push_back(init);

        // ## Empieza el algoritmo

        bool done = false;

        int goalParentId;

        while (!done)
        {
            int keepNodeSize = nodes.size();
            printf("-------------------------nodes: %d\n", keepNodeSize);

            for (int nodeIdx = 0; nodeIdx < keepNodeSize; nodeIdx++)
            {
                nodes[nodeIdx]->dump();

                int tmpX, tmpY;

                // printf("up\n");
                tmpX = nodes[nodeIdx]->getX() - 1;
                tmpY = nodes[nodeIdx]->getY();
                if (intMap[tmpX][tmpY] == 4)
                {
                    printf("GOOOOL!!!\n");
                    goalParentId = nodes[nodeIdx]->getId();
                    done = true;
                    break;
                }
                else if (intMap[tmpX][tmpY] == 0)
                {
                    // printf("Create node\n");
                    Node *node = new Node(tmpX, tmpY, nodes.size(), nodes[nodeIdx]->getId());
                    intMap[tmpX][tmpY] = 2;
                    nodes.push_back(node);
                }

                // printf("down\n");
                tmpX = nodes[nodeIdx]->getX() + 1;
                tmpY = nodes[nodeIdx]->getY();
                if (intMap[tmpX][tmpY] == 4)
                {
                    printf("GOOOOL!!!\n");
                    goalParentId = nodes[nodeIdx]->getId();
                    done = true;
                    break;
                }
                else if (intMap[tmpX][tmpY] == 0)
                {
                    // printf("Create node\n");
                    Node *node = new Node(tmpX, tmpY, nodes.size(), nodes[nodeIdx]->getId());
                    intMap[tmpX][tmpY] = 2;
                    nodes.push_back(node);
                }

                // printf("right\n");
                tmpX = nodes[nodeIdx]->getX();
                tmpY = nodes[nodeIdx]->getY() + 1;
                if (intMap[tmpX][tmpY] == 4)
                {
                    printf("GOOOOL!!!\n");
                    goalParentId = nodes[nodeIdx]->getId();
                    done = true;
                    break;
                }
                else if (intMap[tmpX][tmpY] == 0)
                {
                    // printf("Create node\n");
                    Node *node = new Node(tmpX, tmpY, nodes.size(), nodes[nodeIdx]->getId());
                    intMap[tmpX][tmpY] = 2;
                    nodes.push_back(node);
                }

                // printf("left\n");
                tmpX = nodes[nodeIdx]->getX();
                tmpY = nodes[nodeIdx]->getY() - 1;
                if (intMap[tmpX][tmpY] == 4)
                {
                    printf("GOOOOL!!!\n");
                    goalParentId = nodes[nodeIdx]->getId();
                    done = true;
                    break;
                }
                else if (intMap[tmpX][tmpY] == 0)
                {
                    // printf("Create node\n");
                    Node *node = new Node(tmpX, tmpY, nodes.size(), nodes[nodeIdx]->getId());
                    intMap[tmpX][tmpY] = 2;
                    nodes.push_back(node);
                }
            }
            dumpMap();
        }

        // ## Display solución hallada

        printf("%%%%%%%%%%%%%%%%%%%%\n");
        bool ok = false;
        while (!ok)
        {
            for (int nodeIdx = 0; nodeIdx < nodes.size(); nodeIdx++)
            {
                if (nodes[nodeIdx]->getId() == goalParentId)
                {
                    nodes[nodeIdx]->dump();
                    goalParentId = nodes[nodeIdx]->getParentId();
                    if (goalParentId == 0)
                    {

                        ok = true;
                        printf("%%%%%%%%%%%%%%%%%%%%2\n");
                    }
                }
            }
        }

        // # Sólo C++: Clean up
        for (int nodeIdx = 0; nodeIdx < nodes.size(); nodeIdx++)
            delete nodes[nodeIdx];

        return true;
    }

private:
    std::vector<std::vector<int>> intMap; // Creamos estructura de datos para mapa
    std::vector<Node *> nodes;            // `nodes` contendrá los nodos del grafo

    // # Creamos función para volcar estructura de datos para mapa

    void dumpMap()
    {
        for (int i = 0; i < intMap.size(); i++)
        {
            for (int j = 0; j < intMap[0].size(); j++)
            {
                printf("%d ", intMap[i][j]);
            }
            printf("\n");
        }
    }
};

int main()
{
    Program program;
    if (!program.run())
        return 1;
    return 0;
}
