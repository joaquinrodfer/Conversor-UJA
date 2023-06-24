from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilenames
from tkinter import StringVar

class RecursosPantallas:
    def __init__(self) -> None:
        self.directorio = StringVar()
        self.directorio.set('')

    def __pedirDirectorio(self):
        self.directorio.set(askdirectory())

    def __pedirArchivo(self):
        self.archivo = StringVar()
        self.archivo.set(askopenfilenames())