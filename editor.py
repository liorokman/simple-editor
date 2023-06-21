#!/usr/bin/python3
from tkinter import *
from tkinter.messagebox import askyesno, askyesnocancel
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askstring, askinteger as askint
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename as openfile, asksaveasfile as savefile
from platform import system

if system() == "Windows":
  from ctypes import windll
  windll.user32.ShowWindow(windll.kernel32.GetConsoleWindow(), 0)

try:
    f = open("font.txt")
except FileNotFoundError:
    f = open("font.txt", 'w')
    f.write("Courier New\n10\n#000000")
    f.close()
    f = open("font.txt")
font_properties = f.readlines()
f.close()
font = font_properties[0].strip()
font_size = font_properties[1].strip()
font_color = font_properties[2].strip()
file_opened = None
is_file_saved = True


def save_as():
    global file_opened, is_file_saved
    f = savefile(mode="w", defaultextension=".txt")
    if f is None:
       return
    text_to_save = str(txt.get("1.0", END))
    f.write(text_to_save)
    file_opened = f"{f.name}"
    f.close()
    is_file_saved = True
    statusbar.config(text="")


def save_file():
    global file_opened
    if file_opened is None:
        save_as()
    else:
        with open(file_opened, 'w') as f:
            f.write(txt.get("1.0", END))
    statusbar.config(text="")


def open_file():
    global file_opened
    file_opened = openfile(title="Open")
    with open(file_opened, encoding="utf-8") as f:
        txt.delete("0.0", "end-1c")
        txt.insert("0.0", f.read())


def change_font():
    global font
    new_font = askstring("Font", "What's the new font?")
    if askyesno("Question", "Do you want to determine the font " + new_font + " to default?"):
        with open("font.txt", "w") as f:
            f.write(new_font + "\n" + str(font_size) + "\n" + font_color)
    txt.config(font=(new_font, font_size))
    font = new_font


def change_font_size():
    global font_size
    new_size = askint("Font", "What's the new font size?")
    if new_size == None:
        return
    if askyesno("Question", f"Do you want to make font size {new_size} to default?"):
        with open("font.txt", "w") as f:
            f.write(font + "\n" + str(new_size) + "\n" + font_color)
    txt.config(font=(font, new_size))
    font_size = new_size


def change_color():
    global font_color
    new_color = askcolor(title="Color")[1]
    if askyesno("Question", f"Do you want to make font color {new_color} to default?"):
        with open("font.txt", 'w') as f:
            f.write(font + "\n" + str(font_size) + "\n" + new_color)
    txt.config(fg=new_color)
    font_color = new_color


def back_default():
    global font, font_size, font_color
    with open("font.txt", "w") as f:
        f.write("Courier New\n10\n#000000")
    txt.config(font=("Courier New", 10), fg="#000000")
    font_color = "#000000"
    font = "Courier New"
    font_size = 10


def unsaved():
    global is_file_saved
    is_file_saved = False
    statusbar.config(text="Changes not saved")


def exit_from_root():
    if not is_file_saved:
        answer = askyesnocancel("Question", "Changes Not Saved.\nDo You want to save changes?", icon="warning")
        if answer:
            save_file()
            root.destroy()
        elif answer is False:
            root.destroy()
    else:
        root.destroy()


def main(text=""):
    global is_file_saved, txt, root, statusbar
    root = Tk()
    root.title("Text Editor")
    root.geometry("500x500+0+0")
    root.bind("<Key>", lambda x: unsaved())
    statusbar = Label(root, text="", bd=1, relief="sunken", anchor="w")
    statusbar.pack(side=BOTTOM, fill="x")
    txt = ScrolledText(root, width=500, height=500, font=(font, font_size) or ("Courier New", font_size), fg=font_color)
    txt.insert("0.0", text)
    txt.pack()
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    fontmenu = Menu(menubar, tearoff=1)
    filemenu.add_command(label="Open", command=open_file)
    filemenu.add_command(label="Save", command=save_file)
    filemenu.add_command(label="Save As", command=save_as)
    fontmenu.add_command(label="Change Font", command=change_font)
    fontmenu.add_command(label="Change Font Size", command=change_font_size)
    fontmenu.add_command(label="Change Font Color", command=change_color)
    fontmenu.add_command(label="Return To Default", command=back_default)
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Font", menu=fontmenu)
    menubar.add_command(label="Quit", command=exit_from_root)
    root.config(menu=menubar)
    root.mainloop()


if __name__ == "__main__":
    main()
