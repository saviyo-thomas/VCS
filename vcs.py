from tkinter import *
from tkinter import filedialog
import cv2

lst= []
lst2= []
count_line_pos = 550
def getlst():
    return lst[0]
# Function for opening the file explorer window
def browseFiles():
	filename = filedialog.askopenfilename(  initialdir = "/",
										    title = "Select a video to analyse",
										    filetypes = (("video files","*.mp4*"),("all files","*.*")))
	lst.insert(0,filename)
	getpath()
	label_file_explorer.configure(text="File Opened: "+getlst())

def getpath():
    d = []
    d=lst[0].split("/")
    lst2.insert(0,"\\".join(d))

def centre_handle(x,y,w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx, cy

def counter(frame, count):
    cv2.putText(frame, "Vehicle Counter :"+ str(count), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5)
    cv2.line(frame, (25, count_line_pos), (1200, count_line_pos), (0,127,255), 3)
    cv2.imshow('video output', frame)

def plotter(count):
    print("Vehicle Counter :" + str(count))
    h= open("result.txt", "a")
    h.write("\n"+"Vehicle Count :" + str(count))

# analyse function
def analyse():
    vid = cv2.VideoCapture(lst2[0])

    ret, fr1 = vid.read()

    

    detect = []
    offset = 6
    cnt = 0

    while vid.isOpened():
        ret, fr2 = vid.read()
        if not ret:
            break
        frm = fr2.copy()
        msk = cv2.absdiff(fr1, fr2)

        msk = cv2.cvtColor(msk, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(msk, 25, 255, cv2.THRESH_BINARY)

        fr1 = fr2

        conts, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for c in conts:

            if cv2.contourArea(c) < 3400:
                continue
        
            x, y, w, h = cv2.boundingRect(c)

            cv2.rectangle(frm, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.putText(frm, "Vehicle"+ str(cnt), (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,244,0), 2)
            centre = centre_handle(x,y,w,h)
            detect.append(centre)
            cv2.circle(frm, centre, 4, (0,0,255), 2, -1)
            for (x, y) in detect:
                if y<(count_line_pos+ offset) and y>(count_line_pos- offset):
                    cnt+=1
                    cv2.line(frm, (25, count_line_pos), (1200, count_line_pos), (0,127,255), 3)
                    detect.remove((x,y))               
        counter(frm, cnt)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    plotter(cnt)
    #cv2.imshow('mask',msk)
    #cv2.imshow('threshould',thresh)                       
    cv2.destroyAllWindows()
    vid.release()
																							
# Create the root window
window = Tk()

# Set window title
window.title('VCS')

# Set window size
window.geometry("500x500")

#Set window background color
window.config(background = "white")

# Create a File Explorer label
label_file_explorer = Label(window,
							text = "VCS - Vehicele Counting System",
                            width="70",
							fg = "blue")

	
button_explore = Button(window,
						text = "Browse Files",
						command = browseFiles)

button_analyse = Button(window, text="Analyse",command= analyse)

button_exit = Button(window,
					text = "Exit",
					command = exit)

# Grid method is chosen for placing the widgets at respective positions in a table like structure by specifying rows and columns
label_file_explorer.grid(column = 1, columnspan=3, row = 1)

button_explore.grid(column = 1, row = 3)

button_analyse.grid(column= 2, row= 3)

button_exit.grid(column = 3,row = 3)

# Let the window wait for any events
window.mainloop()