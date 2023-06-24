from pantalla_audio_to_audio import PantallaAudioToAudio
from pantalla_menu import PantallaMenu
from time import sleep
from tkinter import *

ventana = Tk()
ventana.title('Conversor')
ventana.config(width = 700,height = 500)

audioToAudioPantalla = PantallaAudioToAudio(ventana)
audioToAudioPantalla.config(width=700, height= 450)
audioToAudioPantalla.place(x = 0, y = 0) 
audioToAudioPantalla.pack()

ventana.mainloop()

while ventana.winfo_exists():
    sleep(0.5)
    audioToAudioPantalla.update_idletasks()