import tkinter
import tkinter.filedialog
import tkinter.messagebox
from tkinter import ttk
import os

import xml.etree.ElementTree as ET

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass


main = tkinter.Tk()
main.withdraw()

main.attributes('-topmost', True)
main.lift()
main.focus_force()

fTyp = [("",".xml")]
iDir = os.path.abspath(os.path.dirname(__file__))
tkinter.messagebox.showinfo('ファイル選択','xmlファイルを選んでください')
file = tkinter.filedialog.askopenfilename(filetypes = fTyp, initialdir = iDir)

main.quit()


tree = ET.parse(file)
root = tree.getroot()

# root = ET.fromstring(tree)

tag_timebase = 'timebase'
tag_base = 'clipitem'
tag_start = 'start'
tag_end = 'end'
start_frame = [0]


# for child in root.iter(tag_base):
#     start_frame.append(int(child.tag(tag_start)))
#     print(start_frame)
timebase = int(root.find(f".//{tag_timebase}").text)

child = root.findall(f".//{tag_base}")
# for elem in child:
#     start_frame.append(elem.find(tag_start))
#     print(start_frame)
# subchild = root.findall(f'.//{tag_start}')
#start_frame = [int(element.text) for element in subchild]
for element in child:
    element_start = element.find(tag_start)
    start_frame.append(int(element_start.text))
print(start_frame)
start_frame = list(set(start_frame))
start_frame.sort()
print(start_frame)


input_diff = tkinter.Tk()
input_diff.geometry('280x120')
input_diff.title("検知フレーム数入力")

label_from = ttk.Label(input_diff, text = 'f ~')
entry_from = ttk.Entry(input_diff, width = 5, justify = 'center')
label_to = ttk.Label(input_diff, text = 'f')
entry_to = ttk.Entry(input_diff, width = 5, justify = 'center')
button = ttk.Button(input_diff, width = 5, text = 'OK', command=lambda :btn_click())

entry_from.pack(side = tkinter.LEFT, padx = 20)
label_from.pack(side = tkinter.LEFT)
entry_to.pack(side = tkinter.LEFT, padx = 20)
label_to.pack(side = tkinter.LEFT)
button.pack(side = tkinter.LEFT, padx = 20)
#label.place(x=30, y=70)

#txt = tkinter.Entry(width=20)
#txt.place(x=90, y=70)

frame_diff_min = 0
frame_diff_max = 0

def btn_click():
    global frame_diff_min, frame_diff_max
    entry_number_from = entry_from.get()
    entry_number_to = entry_to.get()
    if (entry_number_from != '' and
        entry_number_from.isdecimal() == True and
        entry_number_to != '' and
        entry_number_to.isdecimal() == True):
        frame_diff_min = int(entry_from.get())
        frame_diff_max = int(entry_to.get())
        input_diff.quit()

#entry.bind("<Return>", btn_click)

# btn = tkinter.Button(input_diff, text='OK', command=btn_click)
# btn.place(x=140, y=170)


input_diff.mainloop()


previous_frame_number = -100

for frame_number in start_frame:
    if frame_number < previous_frame_number:
        continue

    if frame_number <= 0:
        continue

    if (frame_number - previous_frame_number <= frame_diff_max and
        frame_number - previous_frame_number >= frame_diff_min):
        frame_minute = frame_number // (timebase * 60)
        frame_second = (frame_number - (frame_minute * timebase * 60)) // timebase
        frame_mod = frame_number % timebase
        print(f"{frame_minute:02}:{frame_second:02}:{frame_mod:02}で検出！ ")

    previous_frame_number = frame_number
