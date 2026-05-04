import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapAO = {}

        # Aggiungo i nodi al grafo nel costruttore cosi da poter
        # costruire l'idMapAO
        self._nodes = DAO.getAllNodes()
        for n in self._nodes:
            self._idMapAO[n.object_id] = n

    def getInfoCompConnessa(self, id_oggetto):
        # Cercare la componente connessa che contiene l'oggetto con id_oggetto
        if not self.hasNode(id_oggetto):
            return None

        source = self._idMapAO[id_oggetto]

        # 1) Strategia 1
        dfsTree = nx.dfs_tree(self._graph, source)
        print("Size connessa con dfs_tree", len(dfsTree.nodes()))

        # 2) Strategia 2, uso i predecessori
        dfsPred = nx.dfs_predecessors(self._graph, source)
        # dfsPred è un dizionario con chiave nodo e valore il nodo da cui sono arrivato nel nodo chiave
        # quindi la dimensione sara minore di 1 elemento perche scartiamo l'ultimo nodo essendo predecessori
        print("Size connessa con dfs_predecessors", len(dfsPred.values()))

        # 3) Strategia 3, utilizziamo i metodi della libreria (MIGLIORE!!)
        conn = nx.node_connected_component(self._graph, source)
        print("Size connessa con node_connected_component", len(conn))

        return len(conn)




    def buildGraph(self):
        # Aggiunge i nodi al grafo
        self._graph.add_nodes_from(self._nodes)

        # Aggiunge gli archi al grafo
        self.addEdges2()


    def addEdges(self):
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getEdgePeso(u,v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight = None)


    def addEdges2(self):
        allEdges = DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight = e.peso)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def hasNode(self, id_oggetto):
        # Se l'id_oggetto esiste ritorna True senno False
        return id_oggetto in self._idMapAO