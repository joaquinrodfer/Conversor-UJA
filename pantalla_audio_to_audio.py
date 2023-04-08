from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilenames
from tkinter import ttk
from tkinter import messagebox
from time import sleep
from audio_to_audio_converter import AudioToAudioConverter
from recursos_pantallas_conversiones import RecursosPantallas

class PantallaAudioToAudio (ttk.Frame, RecursosPantallas):
    def __init__(self, parent):
        super(PantallaAudioToAudio, self).__init__()
        self.directorio = StringVar()
        self.directorio.set('')

        self.botonDirectorio = ttk.Button(
            parent,
            text = 'Seleccionar Carpeta',
            command = self.__pedirDirectorio
        )
        self.botonDirectorio.place(x = 20, y = 20, width = 200)

        self.etiquetaDirectorio = ttk.Label(
            parent,
            textvariable = self.directorio
        )
        self.etiquetaDirectorio.place(x = 250, y = 22
        , width = 200)

        self.etiquetaFormato = ttk.Label(
            parent,
            text='Formato del archivo:'
        )
        self.etiquetaFormato.place(x=20, y=50, width=120)

        self.desplegableFormato = ttk.Combobox(
            parent,
            state = "readonly",
            values = ['mp3', 'wav']
        )
        self.desplegableFormato.place(x = 170, y = 50, width = 100)

        self.etiquetaNombreCarpeta = ttk.Label(
            parent,
            text='Nombre carpeta:'
        )
        self.etiquetaNombreCarpeta.place(x=20, y=80, width=100)

        self.cajaCarpeta = ttk.Entry(parent)
        self.cajaCarpeta.place(x=170, y=80, width = 100)

        self.boton = ttk.Button(
            parent,
            text = 'Enviar',
            command = self.audioToAudioMultiple
        )
        self.boton.place(x = 20, y = 110)

    def audioToAudioMultiple(self):
        correct = True
        audioToAudio = AudioToAudioConverter(super().directorio.get(), self.desplegableFormato.get(), self.cajaCarpeta.get())
        if not audioToAudio.comprobarDirectorio():
            messagebox.showerror(
                title='Directorio no encontrado', 
                message='El directorio no ha sido encontrado, por favor vuelva a intentarlo'
            )
            correct = False
        else:
            if not audioToAudio.comprobarExtension():
                messagebox.showerror(
                    title='Formato no válido', 
                    message='El formato de archivo no es válido, por favor vuelva a intentarlo'
                )
                correct = False

        if correct:
            audioToAudio.conversionMultiple()
            sleep(1)
            messagebox.showinfo(
                title = 'Conversión finalizada',
                message = 'Conversión realizada correctamente'
            )

    def __pedirDirectorio(self):
        self.directorio.set(askdirectory())