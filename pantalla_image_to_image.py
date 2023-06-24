import glob
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilenames
from tkinter import ttk
from tkinter import messagebox
from recursos_pantallas_conversiones import RecursosPantallas
import os
from PIL import Image
from converter import Converter

class PantallaImagenToImagen (ttk.Frame, Converter):
    def __init__(self, parent):
        super(PantallaImagenToImagen, self).__init__()
        self.directorio = StringVar()
        self.directorio.set('')
        self.valores = ['png', 'jpg', 'jpeg']
        self.extensiones = ('*.png', '*.jpg', '*.jpeg')

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
        , width = 400)

        self.etiquetaFormato = ttk.Label(
            parent,
            text='Formato del archivo:'
        )
        self.etiquetaFormato.place(x=20, y=50, width=120)

        self.desplegableFormato = ttk.Combobox(
            parent,
            state = "readonly",
            values = self.valores
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
            command = self.imageToImageMultiple
        )
        self.boton.place(x = 20, y = 110)

    def __convertirImagen1(self, input_path, output_path, format):
        try:
            image = Image.open(input_path)
            new_filename = os.path.splitext(os.path.basename(input_path))[0] + "." + format
            output_file = os.path.join(output_path, new_filename)
            image.save(output_file, format)
            return True
        except Exception as e:
            print("Error al convertir la imagen:", str(e))
            return False

    def imageToImageMultiple(self):
        correct = True
        if not self.comprobarDirectorio(self.directorio.get(), self.cajaCarpeta.get()):
            messagebox.showerror(
                title='Directorio no encontrado', 
                message='El directorio no ha sido encontrado, por favor vuelva a intentarlo'
            )
            correct = False
        else:
            if not self.comprobarExtension(self.desplegableFormato.get(), self.valores):
                messagebox.showerror(
                    title='Formato no válido', 
                    message='El formato de archivo no es válido, por favor vuelva a intentarlo'
                )
                correct = False

        if correct:
            os.chdir(self.directorio.get())
            for extension in self.extensiones:
                print(glob.glob(extension))
                for img in glob.glob(extension):
                    file_path = os.path.join(self.directorio.get(), img)
                    self.__convertirImagen1(
                        file_path,
                        os.path.join(self.directorio.get(),self.cajaCarpeta.get()),
                        self.desplegableFormato.get()
                    )

            messagebox.showinfo(
                title = 'Conversión finalizada',
                message = 'Conversión realizada correctamente'
            )

        # if os.path.isfile(self.directorio.get()):
        #     self.__convertirImagen1(
        #         self.directorio,
        #         os.path.join(self.directorio,self.cajaCarpeta.get()),
        #         self.desplegableFormato.get()
        #     )
        # elif os.path.isdir(self.directorio.get()):
        #     for extension in self.valores:
        #         for img in glob.glob(extension):
        #             file_path = os.path.join(self.directorio.get(), img)
        #             self.__convertirImagen1(
        #                 file_path,
        #                 os.path.join(self.directorio.get(),self.cajaCarpeta.get()),
        #                 self.desplegableFormato.get()
        #             )

    def __pedirDirectorio(self):
        self.directorio.set(askdirectory())