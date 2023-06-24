import os
import glob
from pydub import AudioSegment
from shutil import move
from tkinter import messagebox

class AudioToAudioConverter:
    listaFormatosBusqueda = ('*.mp3', '*.wav')
    listaFormatosAudios = ('mp3', 'wav')
    carpetaRuta = ""
    formatoConversion = ""

    def __init__(self, audioRuta, formatoConversion, nombreCarpeta, progressBar, archivoActual):
        self.audioRuta = audioRuta
        self.nombreCarpeta = nombreCarpeta
        self.carpetaRuta = os.path.join(audioRuta, nombreCarpeta)
        self.formatoConversion = formatoConversion
        self.progressBar = progressBar
        self.archivoActual = archivoActual

    def comprobarArchivo(self):
        if os.path.isfile(self.audioRuta):
            os.chdir(os.path.dirname(self.audioRuta))
            if os.path.exists(self.nombreCarpeta) == False:
                os.mkdir(self.nombreCarpeta)
            self.carpetaRuta = os.path.join(os.path.dirname(self.audioRuta), self.nombreCarpeta)
            return True
        else:
            return False 
    
    def comprobarDirectorio(self):
        if os.path.exists(self.audioRuta):
            os.chdir(self.audioRuta)
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

            for audio in glob.glob(extension):
                self.archivoActual.set(audio)
                if '.' + self.formatoConversion != os.path.splitext(os.path.basename(audio))[1]:
                    nombreArchivo = os.path.splitext(os.path.basename(audio))[0] + '.' + self.formatoConversion
                    AudioSegment.from_file(audio).export(nombreArchivo, format=self.formatoConversion)
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
            messagebox.showwarning(
                title = 'Archivo no encontrado',
                message = 'La ruta especificada no contiene archivo. Por favor, vuelva a intentarlo'
            )
            exit(-1)
        elif '.' + self.formatoConversion != os.path.splitext(os.path.basename(audio))[1]:
            self.progressBar["maximum"] = 1
            self.progressBar["value"] = 0

            self.archivoActual.set(os.path.basename(audio))

            nombreArchivo = os.path.splitext(os.path.basename(audio))[0] + '.' + self.formatoConversion
            AudioSegment.from_file(audio).export(nombreArchivo, format=self.formatoConversion)
            audioConvertidoRuta = os.path.join(os.path.dirname(self.audioRuta), nombreArchivo)
            move(audioConvertidoRuta,self.carpetaRuta)

            self.progressBar["value"] = 1
            messagebox.showinfo(
                title = 'Conversión finalizada',
                message = 'Conversión realizada correctamente'
            )