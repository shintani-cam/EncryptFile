from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from PIL import ImageTk, Image
from cryptography.fernet import Fernet
from tkinter import messagebox
import time
import logging
import os

#setup logging
logging.basicConfig(filename="encryption.log", level=logging.INFO)

#file key
keyPath = "myKey.Key"


root =  Tk()
root.title("Encrypt File")
root.geometry("550x300")
root.iconbitmap(default="icon.ico")
root.resizable(width= False, height= False)

#image key1
imgKey = Image.open("image/key.png")
resized = imgKey.resize((30,30), Image.ADAPTIVE)
imageKey = ImageTk.PhotoImage(resized)

#image key 2
imgKey2 = Image.open("image/key2.png")
resized2 = imgKey2.resize((30,30), Image.ADAPTIVE)
imageKey2 = ImageTk.PhotoImage(resized2)

#folder icon
imageFolder = ImageTk.PhotoImage(Image.open("image/folder.png"))
#lock icon
imgLock = ImageTk.PhotoImage(Image.open("image/locked.png"))
#unlock icon
imgUnlock = ImageTk.PhotoImage(Image.open("image/unlock.png"))
choice = IntVar(value=1)  


def generate_key():
    try:
        file = filedialog.asksaveasfilename(initialfile="myKey.key", defaultextension=".key", filetypes=[("key file", "*.key"),])

        #labelKey.config(text=f"Angui: {nameFile[-1]}")

        key = Fernet.generate_key()

        with open(file, "wb") as f:
            f.write(key)
        messagebox.showinfo("Information", "Key generated!")
        #logging encrypt file
        logging.info(f"{time.strftime('%H:%M %d-%m-%y ')} Created Key : {file}")
        
    except FileNotFoundError:
        messagebox.showwarning("Warning", "you don't have created key!")

def choiceKey():
    try:
        file = filedialog.askopenfilename(initialfile="myKey.key", defaultextension=".key", filetypes=[("key file", "*.key"),])
        #nameFile = file.split("/")
        with open(file, "rb") as f:
            global key
            key = f.read()
        
        labelchoiceKey.config(text=f"Using key: {file}")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "You have not selected a key")


def browseFiles():
    global filePath

    if choice.get() != 1:
        filePath = filedialog.askopenfilenames(initialdir="/", title="Ruah file", filetypes=(("text", "*.txt"), ("All Files", "*.*")))
    else:
        filePath = filedialog.askopenfilename(initialdir="/", title="Ruah file", filetypes=(("text", "*.txt"), ("All Files", "*.*")))

    
    fileNameText.insert(0, filePath)


def encrypt():
    try:
        #key = Fernet.generate_key()
        fernet = Fernet(key)
        
        #encrypt multi files
        if choice.get() != 1:
            for i in filePath:

                with open(i, "rb") as f:
                    dataFile = f.read()
                encrypted = fernet.encrypt(dataFile)

                with open(i, "wb") as f:
                    f.write(encrypted)

            #logging encrypt file
            logging.info(f"{time.strftime('%H:%M %d-%m-%y')} Encrypted file : {filePath}")




        
        else:
            with open(filePath, "rb") as f:
                dataFile = f.read()

            encrypted = fernet.encrypt(dataFile)

            with open(filePath, "wb") as f:
                f.write(encrypted)

            #logging encrypt file
            logging.info(f"{time.strftime('%H:%M')} Encrypted file : {filePath}")

            
            

        messagebox.showinfo("Information", "Done!")
    except:
        messagebox.showerror("Error","You must create a key first or choose a key")


def decrypt():
    try:
        fernet = Fernet(key)

        if choice.get() != 1:
            try:
                for i in filePath:
                    with open(i, "rb") as f:
                        message = f.read()

                    decrypted = fernet.decrypt(message)
                        
                    with open(i, "wb") as f:
                            f.write(decrypted)
                            
                
                messagebox.showinfo("Information", "Decryption successful!")
                #logging decrypt file
                logging.info(f"{time.strftime('%H:%M %d-%m-%y')} Decrypted file : {filePath}")


            except:
                messagebox.showerror("Error", "Wrong key!")
                #logging decrypt file
                logging.info(f"{time.strftime('%H:%M ')} Wrong key in files : {filePath}")

        else:
            with open(filePath, "rb") as f:
                message = f.read()

            decrypted = fernet.decrypt(message)
                        
            with open(filePath, "wb") as f:
                f.write(decrypted)
            messagebox.showinfo("Information", "Decryption successful!")
            #logging decrypt file
            logging.info(f"{time.strftime('%H:%M %d-%m-%y')} Decrypted file : {filePath}")

    except:
        messagebox.showerror("Error", "Wrong key!")


#frame0
fileNameLabel = Label(root,text="File: ")
fileNameText = Entry(root, width=75)

button = Button(root, text="Select file", image=imageFolder, command=browseFiles)

fileNameLabel.place(x=0, y=10)
fileNameText.place(x= 30, y=10)
button.place(x=500, y=5)


#label for radio button
labelRadioButton = Label(root, text="Select:")
labelRadioButton.place(x=0, y=35)
#radio button
radioButton1 = Radiobutton(root, text="Single file", variable=choice, value=1)
radioButton2 = Radiobutton(root, text="Many files", variable=choice, value=2)

radioButton1.place(x=40, y=35)
radioButton2.place(x=120, y=35)

#label gernerate key
labelGenerateKey = Label(root, text="Create key: ")
labelGenerateKey.place(x=0, y=70)

btnGenerateKey = Button(image=imageKey, command=generate_key)
btnGenerateKey.place(x=500, y=55)

#choice key
labelchoiceKey = Label(root, text="Using key: ")
labelchoiceKey.place(x=0, y=105)

#button choice key
btnChoiceKey = Button(image=imageKey2, command=choiceKey)
btnChoiceKey.place(x=500, y=105)

#label button encrypt
labelButtonEncrypt = Label(root, text="File encryption: ")
labelButtonEncrypt.place(x=0, y=155)

#button encrypt
btnEncrypt = Button(image=imgLock, command=encrypt)
btnEncrypt.place(x=500, y=155)

#label decrypt file
labelDecrypt = Label(root, text="File decryption: ")
labelDecrypt.place(x=0, y=205)

#button decrypt
btnDecrypt = Button(image=imgUnlock, command=decrypt)
btnDecrypt.place(x=500, y=205)

#version
labelVesion = Label(text="Version: 1", font=("Arial",8))
labelVesion.place(x=0, y=280)

#author
labelAuthor = Label(text="Author: thachngocdau", font=("Arial",8))
labelAuthor.place(x=350, y=280)

#check key
if os.path.exists(keyPath):
    with open(keyPath, "rb") as f:
        global key
        key = f.read()
        labelchoiceKey.config(text=f"Using key: {keyPath}")

root.mainloop()
