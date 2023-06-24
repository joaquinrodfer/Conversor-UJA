import os
import glob
from pydub import AudioSegment
from shutil import move
from tkinter import messagebox

class ImageToImageConverter:
    listaFormatosBusqueda = ('*.jpg', '*.png', '*.jpeg', '*.raw')
    listaFormatosAudios = ('png', 'jpg', 'jpeg')
    carpetaRuta = ""
    formatoConversion = ""

    def __init__(self, imageRuta, formatoConversion, nombreCarpeta, progressBar):
        self.imageRuta = imageRuta
        self.carpetaRuta = os.path.join(imageRuta, nombreCarpeta)
        self.formatoConversion = formatoConversion
        self.progressBar = progressBar
    
    def comprobarDirectorio(self):
        if os.path.exists(self.imageRuta):
            os.chdir(self.imageRuta)
            if os.path.exists(self.carpetaRuta) == False:
                os.mkdir(self.carpetaRuta)
            return True
        else:
            return False                

    def comprobarExtension(self):
        if self.formatoConversion not in self.listaFormatosAudios:
            print("ERROR[!]: Formato no válido")
            return False
        else:
            return True

    def conversionMultiple(self):
        for extension in self.listaFormatosBusqueda:

            self.progressBar["maximum"] = len(glob.glob(extension))
            currentFile = 0

            self.progressBar["value"] = currentFile

            for image in glob.glob(extension):
                print(image)
                if '.' + self.formatoConversion != os.path.splitext(os.path.basename(image))[1]:
                    nombreArchivo = os.path.splitext(os.path.basename(image))[0] + '.' + self.formatoConversion
                    AudioSegment.from_file(image).export(nombreArchivo, format=self.formatoConversion)
                    audioRuta = os.path.join(self.audioRuta,nombreArchivo)
                    nuevaAudioRuta = os.path.join(self.carpetaRuta,nombreArchivo)
                    move(audioRuta,nuevaAudioRuta)

                currentFile += 1
                self.progressBar["value"] = currentFile

        messagebox.showinfo(
                title = 'Conversión finalizada',
                message = 'Conversión realizada correctamente'
            )

    def conversionUnica(self, audio):
        if not os.path.exists(os.path.join(self.audioRuta, audio)):
            print("ERROR[!]: Archivo no encontrado")
            exit(-1)
        if '.' + self.formatoConversion != os.path.splitext(os.path.basename(audio))[1]:
            nombreArchivo = os.path.splitext(os.path.basename(audio))[0] + '.' + self.formatoConversion
            AudioSegment.from_file(audio).export(nombreArchivo, format=self.formatoConversion)
            audioConvertidoRuta = os.path.join(self.audioRuta, nombreArchivo)
            nuevaAudioRuta = os.path.join(self.carpetaRuta,nombreArchivo)
            move(audioConvertidoRuta,nuevaAudioRuta)