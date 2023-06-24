import os
from shutil import move


class Converter:
    def comprobarDirectorio(self, ruta, nombreCarpeta):
        if os.path.exists(ruta):
            os.chdir(ruta)
            if os.path.exists(os.path.join(ruta, nombreCarpeta)) == False:
                os.mkdir(os.path.join(ruta, nombreCarpeta))
            return True
        else:
            return False
        
    def comprobarExtension(self, extension, listaExtensiones):
        if extension not in listaExtensiones:
            print("ERROR[!]: Formato no válido")
            return False
        else:
            return True
        
    def comprobarArchivo(self, imgRuta, nombreCarpeta):
        if os.path.isfile(imgRuta):
            os.chdir(os.path.dirname(imgRuta))
            if os.path.exists(nombreCarpeta) == False:
                os.mkdir(nombreCarpeta)
            return True
        else:
            return False 