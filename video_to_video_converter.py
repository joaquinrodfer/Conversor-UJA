import os
import glob
import subprocess
from tkinter import messagebox

class VideoToVideoConverter:
    listaFormatosBusqueda = ('*.mp4', '*.flv', '*.avi', '*.mkv')
    listaFormatosVideoAudio = ('mp4', 'flv', 'avi', 'mkv', 'mp3', 'wav')
    videosRuta = ""
    formatoConversion = ""
    carpetaRuta = ""

    def __init__(self, videoRuta, formatoConversion, nombreCarpeta, progressBar, archivoActual):
        self.videoRuta = videoRuta
        self.nombreCarpeta = nombreCarpeta
        self.carpetaRuta = os.path.join(videoRuta, nombreCarpeta)
        self.formatoConversion = formatoConversion
        self.progressBar = progressBar
        self.archivoActual = archivoActual
    
    def comprobarArchivo(self):
        if os.path.isfile(self.videoRuta):
            os.chdir(os.path.dirname(self.videoRuta))
            if os.path.exists(self.nombreCarpeta) == False:
                os.mkdir(self.nombreCarpeta)
            self.carpetaRuta = os.path.join(os.path.dirname(self.videoRuta), self.nombreCarpeta)
            return True
        else:
            return False 
    
    def comprobarDirectorio(self):
        if os.path.exists(self.videoRuta):
            os.chdir(self.videoRuta)
            if os.path.exists(self.carpetaRuta) == False:
                os.mkdir(self.carpetaRuta)
            return True
        else:
            return False                

    def comprobarExtension(self):
        if self.formatoConversion not in self.listaFormatosVideoAudio:
            print("ERROR[!]: Formato no válido")
            return False
        else:
            return True

    def conversionMultiple(self):
        for extension in self.listaFormatosBusqueda:
            self.progressBar["maximum"] = len(glob.glob(extension))
            currentFile = 0
            self.progressBar["value"] = currentFile
            for video in glob.glob(extension):
                print(video)
                self.archivoActual.set(video)
                nombreArchivo = os.path.splitext(os.path.basename(video))[0] + '.' + self.formatoConversion
                output_file = os.path.join(self.carpetaRuta, nombreArchivo)
                command = ['ffmpeg', '-i', video, output_file]
                subprocess.run(command)
                currentFile += 1
                self.progressBar["value"] = currentFile

        messagebox.showinfo(
            title = 'Conversión finalizada',
            message = 'Conversión realizada correctamente'
        )

    def conversionUnica(self, video):
        self.progressBar["maximum"] = 1
        self.progressBar["value"] = 0

        self.archivoActual.set(os.path.basename(video))

        nombreArchivo = os.path.splitext(os.path.basename(video))[0] + '.' + self.formatoConversion
        output_file = os.path.join(self.carpetaRuta, nombreArchivo)
        command = ['ffmpeg', '-i', video, output_file]
        subprocess.run(command)

        self.progressBar["value"] = 1
        messagebox.showinfo(
            title = 'Conversión finalizada',
            message = 'Conversión realizada correctamente'
        )