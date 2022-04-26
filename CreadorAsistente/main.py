from encodings import utf_8
from pydoc import cli
import PySimpleGUI as sg
import os

sg.theme('DarkAmber')

###################################################
###     DISEÑO      DE      LA      INTERFAZ    ###
###################################################

primera_columna = [
    [sg.HSeparator()],
    [sg.T()],
    [sg.Text("Selecciona un tipo de asistente")], 
    [sg.Combo(size=(25,1), values=["Preguntas Frecuentes", "Secuencia de Pasos"], default_value="Preguntas Frecuentes",readonly=True, key="-TIPO-", enable_events=True)],
    [sg.T()],
    [sg.HSeparator()],
    [sg.T()],
    [sg.Text("Selecciona un archivo XML")], 
    [sg.Input(key="-FILE-", enable_events=True), sg.FileBrowse(button_text="Buscar", file_types=(("XML Files", "*.xml"), ("ALL Files", "*.*")))],
    [sg.Button("Mostrar archivo", size=(46,1), key="-SHOW-")],
    [sg.T()],
    [sg.HSeparator()],
    [sg.T()],
    [sg.Text("Selecciona un método para añadir ejemplos")],
    [sg.Combo(size=(25,1), values=["Jaro-Winkler", "LCS", "Coseno", "BM25"], default_value="Jaro-Winkler",readonly=True, key="-ALG-", enable_events=True), sg.Text("Recomendado", key="-RECO-")],
    [sg.T()],
    [sg.HSeparator()],
    [sg.T()],
    [sg.Text("Indica un nombre para el asistente")],
    [sg.Input(key="-NAME-", enable_events=True)],
    [sg.Text("Y una localización")],
    [sg.Input(key="-FOLDER-", enable_events=True), sg.FolderBrowse(button_text="Elegir")],
    [sg.T()],
    [sg.HSeparator()],
    [sg.T()],
    [sg.T()],
    [sg.Submit(size=(40,5),button_text="Crear asistente", key="-OK-")],
    [sg.T()],
    [sg.T()],
    [sg.HSeparator()]
]

segunda_columna = [
    [sg.Text("Contenido del archivo seleccionado")],
    [sg.MLine(size=(400,44), key="-CONTENT-")],
    [sg.Button(button_text="Modificar", key="-MOD-")]

]

layout = [
    [
        sg.VSeparator(),
        sg.Column(primera_columna),
        sg.VSeparator(),
        sg.Column(segunda_columna)
    ]
]

window = sg.Window("Creador de Asistentes con RASA", layout, size=(1400, 800))

###########################################################
###     FUNCIONAMIENTO      DE      LOS      BOTONES    ###
###########################################################

fichero = ""
algoritmo = "Jaro-Winkler"
nombrebot = ""
location = ""
tipo = "Preguntas Frecuentes"

while True:
    event, values = window.read()

    if event == "EXIT" or event == sg.WIN_CLOSED:               # boton salir
        break

    if event == "-FILE-":                                       # primer input, archivo xml
        fichero = values["-FILE-"]       
        n = os.path.basename(fichero)                           # se obtiene el nombre del archivo
        nombrebot = n.replace(".xml", "")                       # se quita la terminacion ".xml"
        window["-NAME-"].update(nombrebot)                      # se actualiza el input del nombre del asistente con esta sugerencia

    if event == "-SHOW-":                                       # boton para mostrar el contenido del archivo xml a la derecha
        try:            
            ff = open(fichero,"r", encoding="utf8")             # se abre el archivo

            lines = ""
            for f in ff:                                        # se guardan las lineas
                lines += f

            window["-CONTENT-"].update(lines)                   # y se muestran
            
        except:
            sg.PopupOK("Debes seleccionar un archivo para mostrarlo", title="Aviso")

    if event == "-ALG-":                                        # combobox donde seleccionas el algoritmo
        algoritmo = values["-ALG-"]
        if algoritmo == "Jaro-Winkler":                         #pongo recomendado si y solo si se selecciona esta algoritmo
            window["-RECO-"].update("Recomendado")
        else:
            window["-RECO-"].update("")

    if event == "-NAME-":                                       # nombre del asistente
        nombrebot = values["-NAME-"]

    if event == "-FOLDER-":                                     # carpeta de destino
        location = values["-FOLDER-"]

    if event == "-MOD-":                                        # boton para modificar el archivo xml mostrado
        output = values["-CONTENT-"]     
        if fichero != "" and output != "":                      # si modificamos el XML --> se va a sobrescribir
            click = sg.PopupOKCancel("Va a sobrescribir el archivo {}\n\n¿Esta seguro?".format(fichero), title="Aviso")
            if click == "OK":
                try:                                        
                    contenido = open(fichero, "w", encoding="utf-8") 
                    for linea in output:
                        contenido.write(linea)
                    contenido.close()
                except:
                    sg.PopupOK("Ocurrio un error", title="Aviso")
        else:
            sg.PopupOK("No hay nada que editar", title="Aviso")

    if event == "-TIPO-":                                       # tipo de asistente (preguntas frecuentes o pasos secuencia)
        tipo = values["-TIPO-"]

    if event == "-OK-":                                         # crear el asistente
        try:
            if fichero == "":
                sg.PopupOK("Falta el fichero XML", title="Aviso")
            elif algoritmo == "":
                sg.PopupOK("Falta el algoritmo", title="Aviso")
            elif nombrebot == "":
                sg.PopupOK("Falta el nombre del asistente", title="Aviso")
            elif location == "":
                sg.PopupOK("Falta el destino del asistente", title="Aviso")
            else:                
                click = sg.PopupOKCancel("Se creará el asistente {}\nEn la carpeta {}\n\nPor favor dirijase a la consola".format(nombrebot, location), title="Aviso")
                #crear bot aqui
                if click == "OK":                           # segun el tipo de asistente
                    if tipo == "Preguntas Frecuentes":      # se llama a un lector u otro
                        os.system("python lectorFAQ_builder.py {} {} {} {}".format(fichero,algoritmo, nombrebot, location))
                        print("")
                    if tipo == "Secuencia de Pasos":
                        os.system("python lectorSEQ_builder.py {} {} {} {}".format(fichero,algoritmo, nombrebot, location))
                        print("")

                    sg.PopupOK("Asistente creado", title="Aviso")       
                                            
        except:
            sg.PopupOK("Se produjo un error", title="Aviso")