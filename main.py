# Students Attendence  
# Auther: Mahmoud Abdelatey
# Github Account:Mahmoudsotpro
# E-Mail: mahmoudsoftpro@hotmail.com

import tkinter
from tkinter import PhotoImage
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

global counter
counter = 0

global cam_index
cam_index = 0

global counter2
counter2 = 0
global counter3
counter3 = 0
global att_name
att_name = []
global stu_att_name
stu_att_name = []

global absent_name
absent_name = []
global stu_absent_name
stu_absent_name = []

global Class_Name
Class_Name = ''
global run_camera
run_camera = False
global run_cap
run_cap = False


# ====================================== Functions


def list_webcams():
    """List all available webcams."""
    index = 0
    webcams = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            webcams.append(f"Webcam {index}")
        cap.release()
        index += 1
    return webcams

def on_select(event):
    """Handle the selection event."""
    selected_webcam = webcam_combobox.get()
    
    print(f"Selected Webcam: {selected_webcam}")




#================================================

def findEncodings (images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
        #============================

        """
        with open('encode.txt', 'w') as f:
            f.write(str(encode) + "\n")
            """
        #=======================================

    return encodelist


# =======================================
def stopc():
    global run_cap
    global run_camera
    run_cap = False
    run_camera = False
    btnAbsent['state'] = 'normal'
    cap.release()


# ========================================
def exitc():
    win.quit()


# ========================================
def startc():
    global absent_name
    absent_name = []
    global run_cap
    if not run_cap:
        run_cap = True
    btnAbsent['state'] = 'disabled'
    global encodeListknown
    encodeListknown = findEncodings(images)
    print(encodeListknown)

    print('Encodeing Complet')
    global run_camera
    if not run_camera:
        run_camera = True
        update_image()

# =========================================
def startc1():
    global absent_name
    absent_name = []
    global run_cap
    if not run_cap:
        run_cap = True
    btnAbsent['state'] = 'disabled'

    global encodeListknown1
    encodeListknown1 = []
    with open('encode.txt', 'r+') as f:
        for line in f:
            encodeListknown1.append(float(line.strip()))

    print(encodeListknown1)
    # =====================================
    """with open('encode.csv', 'r+') as f:
        f.write(str(encodeListknown))"""
    # =======================================
    print('Encodeing Complet')
    global run_camera
    if not run_camera:
        run_camera = True
        update_image1()

# ========================================
def showAbsent():
    btnsave['state'] = 'normal'
    global classNames
    global att_name
    global absent_name
    absent_name = []
    global counter3

    for ii in my_tree2.get_children():
        my_tree2.delete(ii)

    for p in classNames:
        for pp in att_name:
            if not p == pp:
                absent_name.append(p)

    for i in absent_name:
        if i not in my_tree2.get_children():
            counter3 = counter3 + 1
            my_tree2.insert(parent='', index='end', iid=counter3, text="", values=i)
    stu_absent_count = absent_name.__len__()
    l9title.config(text=stu_absent_count)



def update_image():
    global run_cap
    print(run_cap)
    if run_cap:
        ret, frame = cap.read()

        imgs = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgs)
        encodeCurFrame = face_recognition.face_encodings(imgs, facesCurFrame)

        for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListknown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListknown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                global name, counter
                name = classNames[matchIndex]
                print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), (cv2.FILLED))
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                counter = counter + 1
                markAttendance(name, counter)
            else:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (255, 0, 0), (cv2.FILLED))
                cv2.putText(frame, 'Unknown', (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            image = Image.fromarray(frame)
            photo.paste(image)

        if run_camera:
            win.after(1, update_image)

# ==========================================

def update_image1():
    global run_cap
    print(run_cap)
    global encodeListknown1

    if run_cap:
        ret, frame = cap.read()

        imgs = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgs)
        encodeCurFrame = face_recognition.face_encodings(imgs, facesCurFrame)

        for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
            print(encodeFace)
            print(encodeListknown1)

            matches = face_recognition.compare_faces(encodeListknown1, encodeFace)
            faceDis = face_recognition.face_distance(encodeListknown1, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                global name, counter
                name = classNames[matchIndex]
                print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), (cv2.FILLED))
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                counter = counter + 1
                markAttendance(name, counter)
            else:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (255, 0, 0), (cv2.FILLED))
                cv2.putText(frame, 'Unknown', (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            image = Image.fromarray(frame)
            photo.paste(image)

        if run_camera:
            win.after(1, update_image1)

# ===========================================
def markAttendance(name, counter):
    global att_name
    if name not in att_name:
        att_name.append(name)
        my_tree1.insert(parent='', index='end', iid=counter, text="", values=(name, dtString))

        l8title.config(text=att_name.__len__())


def remov_from_att(e):
    global counter2
    global att_name
    global stu_att_name
    global absent_name
    global stu_absent_name

    stu_absent_name = []
    stu_att_name = []

    x = my_tree1.selection()
    selected = my_tree1.focus()
    val = my_tree1.item(selected, 'val')

    #print(val[0])
    if val[0] in att_name:
        att_name.remove(val[0])
    absent_name.append(val)
    print('Absent: ' + str(absent_name.__len__()))
    print('Attend: ' + str(att_name.__len__()))

    my_tree2.insert(parent='', index='end', iid=counter2, text="", values=(val[0]))
    counter2 += 1
    my_tree1.delete(x)

    for iii in my_tree2.get_children():
        stu_absent_name.append(iii)
    for iii in my_tree1.get_children():
        stu_att_name.append(iii)

    l8title.config(text=stu_att_name.__len__())
    l9title.config(text=stu_absent_name.__len__())


def remov_from_absent(e):
    global counter2
    global att_name
    global stu_att_name
    global absent_name
    global stu_absent_name

    stu_absent_name = []
    stu_att_name = []

    x = my_tree2.selection()
    selected = my_tree2.focus()
    val = my_tree2.item(selected, 'val')
    print(val[0])

    if val[0] not in absent_name:
        absent_name.remove(val[0])
    att_name.append(val)
    print('Absent: ' + str(absent_name.__len__()))
    print('Attend: ' + str(att_name.__len__()))

    now = datetime.now()
    dtString = now.strftime('%d-%m-%Y')
    my_tree1.insert(parent='', index='end', iid=counter2, text="", values=(val[0], str(dtString)))
    counter2 += 1
    my_tree2.delete(x)

    for iii in my_tree2.get_children():
        stu_absent_name.append(iii)
    for iii in my_tree1.get_children():
        stu_att_name.append(iii)

    l8title.config(text=stu_att_name.__len__())
    l9title.config(text=stu_absent_name.__len__())


def view_image(e):
    pass


def save_report():
    # =============================== Absents names report
    absent_name_test = []
    for ij in my_tree2.get_children():
        absent_name_test.append(my_tree2.item(str(ij)))
    absent_name_test_2 = []
    for i in absent_name_test:
        absent_name_test_2.append(i['values'])
    # print(absent_name_test_2)
    # ========================================
    global Class_Name
    Class_Name = variable.get()
    global Class_count
    Class_count = []
    for i in my_tree0.get_children():
        Class_count.append(i)
    Class_Attendance_count = []
    for i in my_tree1.get_children():
        Class_Attendance_count.append(i)
    Class_absent_count = []
    for i in my_tree2.get_children():
        Class_absent_count.append(i)

    with open('Absent_report.csv', 'r+') as f:
        now = datetime.now()
        dtString = now.strftime('%d-%m-%Y')

        f.write(f'\n\n Date:,{dtString}')
        f.write(f'\n Class:,{Class_Name}')

        f.write(f'\n Class Count #:,{Class_count.__len__()}')
        f.write(f'\n Class Attendance Count #: ,{Class_Attendance_count.__len__()}')
        f.write(f'\n Class Absents Count #:, {Class_absent_count.__len__()}')

        f.write(f'\n Class Absents Names:')
        for i in absent_name_test_2:
            f.write(f'\n{i}')

        f.close()


# ===============================================================
def load_figuring_file():
    """figuring_file = askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
    if figuring_file is not None:
        content = figuring_file.read()
        print(content)"""
    update_image1()


# ===================================== End of Functions

win = tkinter.Tk()
win.title('Mahmoud AI Development app')
win.geometry('1100x645')



ltitle = tkinter.Label(text='Students Attendance ', font='250')
ltitle.place(x=10,y=10)

#.grid(column=0, row=0, columnspan=5)

now = datetime.now()
dtString = now.strftime('%d-%m-%Y')


ldate = tkinter.Label(text='Date: ' + str(dtString), font='72')
ldate.place(x=500,y=10)
#.grid(column=6, row=0)
#============================== Cam code


 
label = ttk.Label(win, text="Select a Webcam:")
label.place(x=700,y=10)

# Create a drop-down list (combobox)
webcam_combobox = ttk.Combobox(win, state="readonly")
webcam_combobox.place(x=820,y=10)

# List all connected webcams
webcams = list_webcams()
webcam_combobox['values'] = webcams

# Set the default value to the first webcam if available
if webcams:
    webcam_combobox.current(0)


print(webcam_combobox.current(0))

# Bind the selection event
webcam_combobox.bind("<<ComboboxSelected>>", on_select)




#================================================

l2title = tkinter.Label(text='chose class', font='20')
l2title.place(x=10,y=40)
#.grid(column=0, row=1, pady=10, padx=10)

variable = tkinter.StringVar(win)
variable.set("10-A")  # default value
dgrade = tkinter.OptionMenu(win, variable, "10-A", "10-B", "10-C", "10-D", "10-E", "10-F", "11-A", "11-B", "11-C",
                            "11-D", "11-E", "11-F")
dgrade.place(x=150,y=40)
#.grid(column=1, row=1)


l3title = tkinter.Label(text='chose pics path', font='20')
l3title.place(x=10,y=80)
#.grid(column=0, row=2, pady=10, padx=10)


# ===============================================
def browspicfplder():
    Folder_pics_path = askdirectory(title='Select your folder')
    print(Folder_pics_path)
    lselected = tkinter.Label(text=Folder_pics_path)
    lselected.place(x=10,y=120)
    #.grid(column=0, row=3, columnspan=1)
    if lselected:
        btnincodeing['state'] = 'normal'
        btnstopincodeing['state'] = 'normal'
        btnload['state'] = 'normal'

        global images
        images = []
        global classNames
        classNames = []
        mylist = os.listdir(Folder_pics_path)
        print(mylist)
        global counter2
        for cl in mylist:
            curImg = cv2.imread(f'{Folder_pics_path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        for item in my_tree0.get_children():
            my_tree0.delete(item)
        for p in classNames:
            counter2 = counter2 + 1
            my_tree0.insert(parent='', index='end', iid=counter2, text="", values=(p))
        print("class list")
        print(classNames)
        stu_count = classNames.__len__()
        l7title.config(text=stu_count)
    return (images)


# ==================================================



bselectclasspics = tkinter.Button(text='Brows', width=15, command=browspicfplder)
bselectclasspics.place(x=150,y=80)
#grid(column=1, row=2, columnspan=1, rowspan=1)


btnincodeing = tkinter.Button(text='Start Figuring', width=20, command=startc)
btnincodeing['state'] = 'disabled'
btnincodeing.place(x=10,y=150)
#.grid(column=0, row=4, pady=10, padx=10, columnspan=1, rowspan=2)

btnload = tkinter.Button(text='Load Figuring File', width=20, command=startc1)
btnload['state'] = 'disabled'
btnload.place(x=10,y=190)
#.grid(column=1, row=4, pady=10, padx=10, columnspan=1, rowspan=2)

btnstopincodeing = tkinter.Button(text='Stop', width=20, command=stopc)
btnstopincodeing['state'] = 'disabled'
btnstopincodeing.place(x=10,y=230)
#.grid(column=0, row=5, pady=10, padx=10, columnspan=1, rowspan=1)

#==============================================================
l4title = tkinter.Label(text='Class Count:', font='20')
l4title.place(x=10,y=400)
#.grid(column=2, row=5, pady=10, padx=10)

my_tree0 = ttk.Treeview(win, height=6)
my_tree0['columns'] = ("Names")
my_tree0.column("#0", width=0, minwidth=25)
my_tree0.column("Names", width=180)

my_tree0.heading("#0", text="#")
my_tree0.heading("Names", text="Names")

my_tree0.place(x=10,y=440)
#.grid(column=2, row=6, padx=10)
my_tree0.bind("<ButtonRelease-1>", view_image)

l7title = tkinter.Label(text='0', font='20')
l7title.place(x=50,y=585)
#.grid(column=2, row=7, pady=5, padx=5)

#================================================================

l5title = tkinter.Label(text='Attendance:', font='20')
l5title.place(x=250,y=400)
#.grid(column=3, row=5, pady=10, padx=10)

my_tree1 = ttk.Treeview(win, height=6)
my_tree1['columns'] = ("Names", "Date")
my_tree1.column("#0", width=0, minwidth=25)
my_tree1.column("Names", width=100)
my_tree1.column("Date", width=100)

my_tree1.heading("#0", text="#")
my_tree1.heading("Names", text="Names")
my_tree1.heading("Date", text="Date")

my_tree1.place(x=250,y=440)
#.grid(column=3, row=6, padx=10)

my_tree1.bind("<Double-1>", remov_from_att)
my_tree1.bind("<ButtonRelease-1>", view_image)

l8title = tkinter.Label(text='0', font='20', fg='green', bg='light green')
l8title.place(x=270,y=585)
#.grid(column=3, row=7, pady=5, padx=5)




# =========================================
l6title = tkinter.Label(text='Absent:', font='20')
l6title.place(x=500,y=400)

my_tree2 = ttk.Treeview(win, height=6)
my_tree2['columns'] = ("Names")
my_tree2.column("#0", width=0, minwidth=25)
my_tree2.column("Names", width=180)

my_tree2.heading("#0", text="#")
my_tree2.heading("Names", text="Names")

my_tree2.place(x=500,y=440)
#.grid(column=4, row=6, padx=10)
my_tree2.bind("<Double-1>", remov_from_absent)
my_tree2.bind("<ButtonRelease-1>", view_image)


l9title = tkinter.Label(text='0', font='20', fg='red', bg='pink')
l9title.place(x=520,y=585)
#.grid(column=4, row=7, pady=5, padx=5)

# ===========================================================

btnAbsent = tkinter.Button(text='Show Absents', width=15, command=showAbsent)
btnAbsent['state'] = 'disabled'
btnAbsent.place(x=50,y=608)
#.grid(column=0, row=6, rowspan=2, columnspan=1, padx=5)

btnsave = tkinter.Button(text='Save', width=15, command=save_report)
btnsave['state'] = 'disabled'
btnsave.place(x=300,y=608)
#.grid(column=0, row=7, padx=5)

btnexit = tkinter.Button(text='Exit', width=15, command=exitc)
btnexit.place(x=850,y=608)
#.grid(column=0, row=8, padx=5)

####################################
cap = cv2.VideoCapture(0)  # local (built-in) camera
global ret, frame
ret, frame = cap.read()

image = Image.fromarray(frame)
photo = ImageTk.PhotoImage(image)

canvas = tkinter.Canvas(win, width=600, height=350, bd=1, bg='pink')
canvas.create_image((0, 0), image=photo, anchor='nw')
canvas.place(x=420,y=40)


#.grid(column=2, row=1, columnspan=5, rowspan=4, pady=5, padx=5)

win.mainloop()
