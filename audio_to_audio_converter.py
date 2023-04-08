import os
import glob
from pydub import AudioSegment
from shutil import move

class AudioToAudioConverter:
    listaFormatosBusqueda = ('*.mp3', '*.wav')
    listaFormatosAudios = ('mp3', 'wav')
    carpetaRuta = ""
    formatoConversion = ""

    def __init__(self, audioRuta, formatoConversion, nombreCarpeta):
        self.audioRuta = audioRuta
        self.carpetaRuta = os.path.join(audioRuta, nombreCarpeta)
        self.formatoConversion = formatoConversion
    
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
            for audio in glob.glob(extension):
                if '.' + self.formatoConversion != os.path.splitext(os.path.basename(audio))[1]:
                    nombreArchivo = os.path.splitext(os.path.basename(audio))[0] + '.' + self.formatoConversion
                    AudioSegment.from_file(audio).export(nombreArchivo, format=self.formatoConversion)
                    audioRuta = os.path.join(self.audioRuta,nombreArchivo)
                    nuevaAudioRuta = os.path.join(self.carpetaRuta,nombreArchivo)
                    move(audioRuta,nuevaAudioRuta)

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