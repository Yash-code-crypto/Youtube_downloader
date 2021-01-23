from pytube import *
from tkinter.filedialog import *
from tkinter import *
from tkinter.messagebox import *
from threading import *
import webbrowser
from tkinter.ttk import Combobox
from urllib.error import URLError
from pytube.exceptions import RegexMatchError
file_size = 0
#updating %
def progress(stream,chunk:bytes,bytes_remaining:int):
    #getting %
    file_downloaded = (file_size-bytes_remaining)
    per= (file_downloaded/file_size)*100
    dBtn.config(text="{:00.0f} % Downloaded".format(per))


def startDownload():
    global file_size
    try:
        #url = "https://www.youtube.com/watch?v=hip-_JbR888"
        url = urlField.get()
        print(url)
       # checking = YouTube(url)
        dBtn.config(text='Please wait..')
        dBtn.config(state=DISABLED)
        ob= YouTube(url,on_progress_callback=progress)

        Title = ob.streams.first()
        strms = ob.streams
        actual_streams = {}
        quality = []
        for s in strms:
            d = str(s.filesize / 1000000)
            abc = str(s)
            x = list(abc.split(" "))
            c = x[2]
            f = x[3]
            # print(f+d)
            dd_values = str(f + " " + c + " " + d[0:4] + "MB")
            actual_streams.update({dd_values: s})
            quality.append(dd_values)
        path_to_save_video = askdirectory()
        print(path_to_save_video)
        if path_to_save_video is None:
            return
        #utube obj with url
        #ob= YouTube(url,on_progress_callback=progress)
        '''strms= ob.streams.all()
        for s in strms:
            print(s)'''

        combo = Combobox(main, values=quality, width=55)
        combo.pack(side=TOP)
        selected_combo = combo.get()
        while (selected_combo == ""):
            selected_combo = combo.get()
        vTitle.config(text=Title.title)
        vTitle.pack(side=TOP)
        strm = actual_streams[selected_combo]
        file_size=strm.filesize
        print(file_size)
        '''print(strm)
        print(strm.filesize)
        print(strm.title)'''
        strm.download(path_to_save_video)
        print("done...")
        dBtn.config(text='Start Download')
        dBtn.config(state=NORMAL)
        showinfo("Download Finished","Downloaded succesfully")
        webbrowser.open(path_to_save_video)
        urlField.delete(0,END)
        vTitle.pack_forget()
        combo.delete(0, END)
    except RegexMatchError:
        showinfo("Invalid URL","Please enter correct URL")
        urlField.delete(0,END)
        dBtn.config(text="Start Download")
        dBtn.config(state=NORMAL)
        return
    except URLError:
        showinfo('No internet','Please check internet connection')
        dBtn.config(text='Proceed')
        dBtn.config(state=NORMAL)
        return
# GUI building
def startDownloadThread():
    thread = Thread(target=startDownload)
    thread.start()
main = Tk()
main.title("YouTube Downloader")

#setting icon
#main.iconbitmap('./res/youtube-fbfeed.ico')

main.geometry("500x600")

#heading icon
#file = PhotoImage(file='./res/youtube-fbfeed.jpg')
#headingIcon = Label(main,image=file)
#headingIcon.pack(side=TOP)
#url textfield
urlField = Entry(main,font=("verdana",18),justify=CENTER)
urlField.pack(side=TOP,fill=X,padx=10)
#dwnld button
dBtn = Button(main,text="Start Download",font=("verdana",18),relief='ridge',command=lambda:startDownloadThread())
dBtn.pack(side=TOP,pady=10)
#title
vTitle = Label(main,text="Video Title")
#vTitle.pack(side=TOP)
main.mainloop()

