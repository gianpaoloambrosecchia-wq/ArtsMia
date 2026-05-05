from database.DB_connect import DBConnect
from model.arco import Arco
from model.artObject import ArtObject


class DAO():

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        query = "SELECT * FROM objects o"

        cursor.execute(query)

        for row in cursor:
            res.append(ArtObject(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getEdgePeso(v1,v2):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        # Query per considerare coppie di oggetti nella stessa esibizione (2 tabelle exhibition_objects)
        # ed escludo le coppie uguali (sia stesso oggetto sia due coppie speculari). Conto
        # il numero di volte in cui la coppia compare e quello è il peso dell'arco
        query = """SELECT eo.object_id AS o1, eo2.object_id AS o2, COUNT(*) as peso
               FROM exhibition_objects eo, exhibition_objects eo2
               WHERE eo.exhibition_id = eo2.exhibition_id
                 AND eo.object_id < eo2.object_id
                 AND eo.object_id = %s
                 AND eo2.object_id = %s
               GROUP BY eo.object_id, eo2.object_id"""

        cursor.execute(query, (v1.object_id,v2.object_id))

        for row in cursor:
            res.append(row["peso"])



        cursor.close()
        conn.close()

    # Passi l'idMap in modo da salvare l'oggetto artObject a partire dal suo id
    @staticmethod
    def getAllEdges(idMapAO):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        #Uso una query per costruire gli archi con i rispettivi pesi
        query = """select eo.object_id as o1, eo2.object_id as o2, count(*) as peso
                       from exhibition_objects eo, exhibition_objects eo2
                       where eo.exhibition_id = eo2.exhibition_id 
                       and eo.object_id < eo2.object_id 
                       group by eo.object_id , eo2.object_id
                       order by peso desc"""

        cursor.execute(query)

        for row in cursor:
            res.append(Arco(idMapAO[row["o1"]],idMapAO[row["o2"]],row["peso"]))

        cursor.close()
        conn.close()
        return res






