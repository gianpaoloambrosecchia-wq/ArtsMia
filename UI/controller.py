import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato", color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi")
        )

        # Abilito i campi solo dopo aver creato il grafo
        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False
        self._view.update_page()


    def handleCompConnessa(self,e):
        txtIdOggetto = self._view._txtIdOggetto.value
        # Devo eseguire tutte le verifiche sul valore inserito dall'utente
        if txtIdOggetto == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione inserire un valore nel campo id", color="red")
            )
            self._view.update_page()
            return

        try:
            # Se la conversione in int non va a buon fine (quindi il valore inserito non è un intero)
            # entra nel except
            idOggetto = int(txtIdOggetto)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione inserire un valore numerico nel campo id", color="red")
            )
            self._view.update_page()
            return

        if not self._model.hasNode(idOggetto):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione l'id inserito non è presente nel grafo", color="red")
            )
            self._view.update_page()
            return

        sizeCompConn = self._model.getInfoCompConnessa(idOggetto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente connessa contenente l'oggetto con id {idOggetto} è composta di {sizeCompConn} nodi" , color="green")
        )

        # Una volta trovata la componenete connessa posso sbloccare questi due elementi
        self._view._ddLun.disabled=False
        self._view._btnCerca.disabled=False

        # Dalla traccia dice di considerare da 2 alla lunghezza della componente connessa
        # quindi riempio in questo modo il dropdown
        lunValues = range(2, sizeCompConn)
        #for v in lunValues:
            #self._view._ddLun.options.append(ft.dropdown.Option(v))

        # Questa funzione a partire da una lista crea un'altra lista da poter direttamente inserire nel dropdown
        lunValuesDD = map(lambda x: ft.dropdown.Option(x), lunValues)
        self._view._ddLun.options = lunValuesDD

        self._view.update_page()


    def handleCerca(self, e):
        source = self._model.getNodeFromId(self._view._txtIdOggetto.value)
        lun = self._view._ddLun.value

        if lun is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione selezionare un valore di lunghezza", color="red")
            )
            self._view.update_page()
            return

        lunInt = int(lun)

        path, cost = self._model.getOptPath(source, lunInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ho trovato un cammino che parte da {source} che ha un peso totale pari a {cost}", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text("Di seguito i nodi che compongono questo cammino:")
        )
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))

        self._view.update_page()



