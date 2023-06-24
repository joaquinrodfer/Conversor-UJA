import fnmatch
import glob
import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from audio_to_audio_converter import AudioToAudioConverter
from video_to_video_converter import VideoToVideoConverter
from PIL import Image
from converter import Converter
import threading
import tkinter.font as font

class MenuFrame(ttk.Frame):
    def __init__(self, container, show_page):
        super().__init__(container)
        
        self.show_page = show_page

        myFont = font.Font(family='Helvetica')
        
        self.option1_button = ttk.Button(self, text="Convertir Audio 🎵", command=self.abrir_conversor_audio)
        self.option1_button.pack(fill=tk.BOTH, expand=True)
        
        self.option2_button = ttk.Button(self, text="Convertir Imagen 🖼", command=self.abrir_conversor_imagen)
        self.option2_button.pack(fill=tk.BOTH, expand=True)
        
        self.option3_button = ttk.Button(self, text="Convertir Vídeo 🎞", command=self.abrir_conversor_video)
        self.option3_button.pack(fill=tk.BOTH, expand=True)
        
    def abrir_conversor_audio(self):
        self.show_page(ConversorAudio)
        
    def abrir_conversor_imagen(self):
        self.show_page(ConversorImagen)
        
    def abrir_conversor_video(self):
        self.show_page(ConversorVideo)

class ConversorAudio(ttk.Frame):
    def __init__(self, parent, show_page):
        super().__init__(parent)
        
        self.show_page = show_page
        
        self.directorio = StringVar()
        self.directorio.set('')

        self.archivoActual = StringVar()
        self.archivoActual.set('')

        self.etiquetaConversor = ttk.Label(
            self,
            text = 'Conversor Audio',
            font = ('BOLD', 20)
        )
        self.etiquetaConversor.place(x = 250, y = 10)

        self.botonArchivo = ttk.Button(
            self,
            text = 'Seleccionar Archivo',
            command = self.__pedirArchivo
        )
        self.botonArchivo.place(x = 20, y = 50, width = 330, height=40)

        self.botonDirectorio = ttk.Button(
            self,
            text = 'Seleccionar Carpeta',
            command = self.__pedirDirectorio
        )
        self.botonDirectorio.place(x = 350, y = 50, width = 330, height=40)

        self.etiquetaDirectorio = ttk.Label(
            self,
            textvariable = self.directorio
        )
        self.etiquetaDirectorio.config(background="gray90", anchor="center")
        self.etiquetaDirectorio.place(x = 20, y = 90, width = 660, height=40)

        self.etiquetaFormato = ttk.Label(
            self,
            text='Formato del archivo:'
        )
        self.etiquetaFormato.place(x=20, y=130, width=135, height=30)

        self.desplegableFormato = ttk.Combobox(
            self,
            state = "readonly",
            values = ['mp3', 'wav']
        )
        self.desplegableFormato.place(x = 185, y = 135, width = 165)

        self.etiquetaNombreCarpeta = ttk.Label(
            self,
            text='Nombre carpeta:'
        )
        self.etiquetaNombreCarpeta.place(x=370, y=135, width=135, )

        self.cajaCarpeta = ttk.Entry(self)
        self.cajaCarpeta.place(x=520, y=135, width = 155)

        self.boton = ttk.Button(
            self,
            text = 'Convertir',
            command = self.audioToAudioMultiple
        )
        self.boton.place(x = 400, y = 180, width=100, height=50)

        back_button = ttk.Button(
            self,
            text="Volver al menú",
            command=self.go_to_menu
        )
        back_button.place(x = 200, y = 180, width=100, height=50)

        self.etiquetaArchivoActual = ttk.Label(
            self,
            textvariable = self.archivoActual
        )
        self.etiquetaArchivoActual.config(anchor="center")
        self.etiquetaArchivoActual.place(x = 50, y = 360, width = 600, height=40)

        self.progressBar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progressBar.place( x=100, y = 400, width=500)

    def audioToAudioMultiple(self):
        correct = True
        audioToAudio = AudioToAudioConverter(self.directorio.get(), self.desplegableFormato.get(), self.cajaCarpeta.get(), self.progressBar, self.archivoActual)
        if not audioToAudio.comprobarArchivo():
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
                conversion_thread = threading.Thread(target=audioToAudio.conversionMultiple)
                conversion_thread.start()
        else:
            if not audioToAudio.comprobarExtension():
                messagebox.showerror(
                    title='Formato no válido', 
                    message='El formato de archivo no es válido, por favor vuelva a intentarlo'
                )
            else:
                conversion_thread = threading.Thread(target=audioToAudio.conversionUnica, args=(audioToAudio.audioRuta,))
                conversion_thread.start()

    def __pedirDirectorio(self):
        self.directorio.set(askdirectory())

    def __pedirArchivo(self):
        tipos_archivo = (
            ("Audio", "*.mp3;*.wav"),
        )
        self.directorio.set(askopenfilename(filetypes=tipos_archivo))

    def go_to_menu(self):
        self.show_page(MenuFrame)
        
class ConversorImagen(ttk.Frame, Converter):
    def __init__(self, parent, show_page):
        super().__init__(parent)
        
        self.show_page = show_page
        
        self.directorio = StringVar()
        self.directorio.set('')

        self.archivoActual = StringVar()
        self.archivoActual.set('')

        self.valores = ['png', 'jpg', 'jpeg', 'gif', 'tiff']
        self.extensiones = ('*.png', '*.jpg', '*.jpeg', '*.gif', '*.tiff')

        self.etiquetaConversor = ttk.Label(
            self,
            text = 'Conversor Imagen',
            font = ('BOLD', 20)
        )
        self.etiquetaConversor.place(x = 250, y = 10)

        self.botonArchivo = ttk.Button(
            self,
            text = 'Seleccionar Archivo',
            command = self.__pedirArchivo
        )
        self.botonArchivo.place(x = 20, y = 50, width = 330, height=40)

        self.botonDirectorio = ttk.Button(
            self,
            text = 'Seleccionar Carpeta',
            command = self.__pedirDirectorio
        )
        self.botonDirectorio.place(x = 350, y = 50, width = 330, height=40)

        self.etiquetaDirectorio = ttk.Label(
            self,
            textvariable = self.directorio
        )
        self.etiquetaDirectorio.config(background="gray90", anchor="center")
        self.etiquetaDirectorio.place(x = 20, y = 90, width = 660, height=40)

        self.etiquetaFormato = ttk.Label(
            self,
            text='Formato del archivo:'
        )
        self.etiquetaFormato.place(x=20, y=130, width=135, height=30)

        self.desplegableFormato = ttk.Combobox(
            self,
            state = "readonly",
            values = self.valores
        )
        self.desplegableFormato.place(x = 185, y = 135, width = 165)

        self.etiquetaNombreCarpeta = ttk.Label(
            self,
            text='Nombre carpeta:'
        )
        self.etiquetaNombreCarpeta.place(x=370, y=135, width=135, )

        self.cajaCarpeta = ttk.Entry(self)
        self.cajaCarpeta.place(x=520, y=135, width = 155)

        self.boton = ttk.Button(
            self,
            text = 'Convertir',
            command = self.imageToImage
        )
        self.boton.place(x = 400, y = 180, width=100, height=50)

        back_button = ttk.Button(
            self,
            text="Volver al menú",
            command=self.go_to_menu
        )
        back_button.place(x = 200, y = 180, width=100, height=50)

        self.etiquetaArchivoActual = ttk.Label(
            self,
            textvariable = self.archivoActual
        )
        self.etiquetaArchivoActual.config(anchor="center")
        self.etiquetaArchivoActual.place(x = 50, y = 360, width = 600, height=40)

        self.progressBar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progressBar.place( x=100, y = 400, width=500)

    def __convertirImagen1(self, input_path, output_path, format):
        try:
            if format == 'jpg':
                format = 'jpeg'
            image = Image.open(input_path)
            rgb_im = image.convert('RGB')
            new_filename = os.path.splitext(os.path.basename(input_path))[0] + "." + format
            output_file = os.path.join(output_path, new_filename)
            rgb_im.save(output_file, format)
            return 0
        except Exception as e:
            print("Error al convertir la imagen:", str(e))
            return 1

    def imageToImage(self):
        correct = True
        if not self.comprobarArchivo(self.directorio.get(), self.cajaCarpeta.get()):
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
                conversion_thread = threading.Thread(target=self.conversionMultiple)
                conversion_thread.start()
        else:
            correct = False
            for patron in self.extensiones:
                if fnmatch.fnmatch(os.path.basename(self.directorio.get()), patron):
                    correct = True
            
            if correct:
                conversion_thread = threading.Thread(target=self.conversionUnica)
                conversion_thread.start()
            else:
                messagebox.showerror(
                    title='Formato no válido', 
                    message='El formato de archivo no es válido, por favor vuelva a intentarlo'
                )

    def conversionMultiple(self):
        error = 0
        numArchivos = 0
        os.chdir(self.directorio.get())
        for extension in self.extensiones:

            self.progressBar["maximum"] = len(glob.glob(extension))
            currentFile = 0

            self.progressBar["value"] = currentFile

            for img in glob.glob(extension):
                self.archivoActual.set(img)
                file_path = os.path.join(self.directorio.get(), img)
                numArchivos += 1
                currentFile += 1
                error += self.__convertirImagen1(
                    file_path,
                    os.path.join(self.directorio.get(),self.cajaCarpeta.get()),
                    self.desplegableFormato.get()
                )

                self.progressBar["value"] = currentFile

        if error == 0:
            messagebox.showinfo(
                title = 'Conversión finalizada',
                message = 'Conversión realizada correctamente'
            )
        else:
            messagebox.showwarning(
                title = 'Conversión finalizada',
                message = 'No se han podido convertir ' + str(error) + ' archivos del total de ' + str(numArchivos) + ' que se han intentado convertir'
            )

    def conversionUnica(self):
        if not os.path.exists(self.directorio.get()):
            messagebox.showwarning(
                title = 'Archivo no encontrado',
                message = 'La ruta especificada no contiene archivo. Por favor, vuelva a intentarlo'
            )
            exit(-1)
        elif '.' + self.desplegableFormato.get() != os.path.splitext(os.path.basename(self.directorio.get()))[1]:
            self.progressBar["maximum"] = 1
            self.progressBar["value"] = 0

            self.archivoActual.set(os.path.basename(self.directorio.get()))
            file_path = os.path.join(self.directorio.get())
            output_path = os.path.join(os.path.dirname(self.directorio.get()), self.cajaCarpeta.get())
            self.__convertirImagen1(file_path, output_path, self.desplegableFormato.get())

            self.progressBar["value"] = 1
            messagebox.showinfo(
                title = 'Conversión finalizada',
                message = 'Conversión realizada correctamente'
            )
        else:
            messagebox.showerror(
                title = 'Conversión no realizada',
                message = 'Estás tratando de convertir un archivo al mismo tipo'
            )

    def __pedirDirectorio(self):
        self.directorio.set(askdirectory())

    def __pedirArchivo(self):
        tipos_archivo = (
            ("Imágenes", "*.png;*.jpg;*.jpeg;*.gif;*.tiff"),
        )
        self.directorio.set(askopenfilename(filetypes=tipos_archivo))

    def go_to_menu(self):
        self.show_page(MenuFrame)
        
class ConversorVideo(ttk.Frame):
    def __init__(self, parent, show_page):
        super().__init__(parent)
        
        self.show_page = show_page
        
        self.directorio = StringVar()
        self.directorio.set('Dirección del archivo o directorio')

        self.archivoActual = StringVar()
        self.archivoActual.set('')

        self.etiquetaConversor = ttk.Label(
            self,
            text = 'Conversor Vídeo',
            font = ('BOLD', 20)
        )
        self.etiquetaConversor.place(x = 250, y = 10)

        self.botonArchivo = ttk.Button(
            self,
            text = 'Seleccionar Archivo',
            command = self.__pedirArchivo
        )
        self.botonArchivo.place(x = 20, y = 50, width = 330, height=40)

        self.botonDirectorio = ttk.Button(
            self,
            text = 'Seleccionar Carpeta',
            command = self.__pedirDirectorio
        )
        self.botonDirectorio.place(x = 350, y = 50, width = 330, height=40)

        self.etiquetaDirectorio = ttk.Label(
            self,
            textvariable = self.directorio
        )
        self.etiquetaDirectorio.config(background="gray90", anchor="center")
        self.etiquetaDirectorio.place(x = 20, y = 90, width = 660, height=40)

        self.etiquetaFormato = ttk.Label(
            self,
            text='Formato del archivo:'
        )
        self.etiquetaFormato.place(x=20, y=130, width=135, height=30)

        self.desplegableFormato = ttk.Combobox(
            self,
            state = "readonly",
            values = ['mp4', 'flv', 'avi', 'mkv', 'mp3', 'wav']
        )
        self.desplegableFormato.place(x = 185, y = 135, width = 165)

        self.etiquetaNombreCarpeta = ttk.Label(
            self,
            text='Nombre carpeta:'
        )
        self.etiquetaNombreCarpeta.place(x=370, y=135, width=135, )

        self.cajaCarpeta = ttk.Entry(self)
        self.cajaCarpeta.place(x=520, y=135, width = 155)

        self.boton = ttk.Button(
            self,
            text = 'Convertir',
            command = self.VideoToVideoMultiple
        )
        self.boton.place(x = 400, y = 180, width=100, height=50)

        back_button = ttk.Button(
            self,
            text="Volver al menú",
            command=self.go_to_menu
        )
        back_button.place(x = 200, y = 180, width=100, height=50)

        self.etiquetaArchivoActual = ttk.Label(
            self,
            textvariable = self.archivoActual
        )
        self.etiquetaArchivoActual.config(anchor="center")
        self.etiquetaArchivoActual.place(x = 50, y = 360, width = 600, height=40)

        self.progressBar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progressBar.place( x=100, y = 400, width=500)

    def VideoToVideoMultiple(self):
        correct = True
        videoToVideo = VideoToVideoConverter(self.directorio.get(), self.desplegableFormato.get(), self.cajaCarpeta.get(), self.progressBar, self.archivoActual)
        if not videoToVideo.comprobarArchivo():
            if not videoToVideo.comprobarDirectorio():
                messagebox.showerror(
                    title='Directorio no encontrado', 
                    message='El directorio no ha sido encontrado, por favor vuelva a intentarlo'
                )
                correct = False
            else:
                if not videoToVideo.comprobarExtension():
                    messagebox.showerror(
                        title='Formato no válido', 
                        message='El formato de archivo no es válido, por favor vuelva a intentarlo'
                    )
                    correct = False

            if correct:
                conversion_thread = threading.Thread(target=videoToVideo.conversionMultiple)
                conversion_thread.start()
        else:
            if not videoToVideo.comprobarExtension():
                messagebox.showerror(
                    title='Formato no válido', 
                    message='El formato de archivo no es válido, por favor vuelva a intentarlo'
                )
            else:
                conversion_thread = threading.Thread(target=videoToVideo.conversionUnica, args=(videoToVideo.videoRuta,))
                conversion_thread.start()

    def __pedirDirectorio(self):
        self.directorio.set(askdirectory())

    def __pedirArchivo(self):
        tipos_archivo = (
            ("Video", "*.mp4;*.flv;*.avi;*.mkv"),
        )
        self.directorio.set(askopenfilename(filetypes=tipos_archivo))

    def go_to_menu(self):
        self.show_page(MenuFrame)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conversor")
        self.geometry("700x450")
        self.resizable(False, False)
        self.iconbitmap("logo.ico")

        icon = tk.PhotoImage(file="logo.png")
        self.iconphoto(True, icon)
        
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        self.pages = {}
        
        self.show_page(MenuFrame)
        
    def show_page(self, page):
        if page not in self.pages:
            self.pages[page] = page(self.container, self.show_page)
            self.pages[page].pack(fill=tk.BOTH, expand=True)
        
        for p in self.pages.values():
            p.pack_forget()
            
        self.pages[page].pack(fill=tk.BOTH, expand=True)

# Iniciar la aplicación principal
app = MainApp()
app.mainloop()
