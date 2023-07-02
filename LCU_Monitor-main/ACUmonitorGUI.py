import customtkinter
import getTime as time
import ACUbackend as BackEnd
import threading
import time as Timer

FONT_TYPE = "Segoe UI"
DEFAULT_WINDOW_WIDTH=1250
DEFAULT_WINDOW_HEIGHT=600
SELECTED_COM="NONE"

class CustomScaler(customtkinter.CTkFrame):
    scaler=None
    def __init__(self, master,text_size=30,sizeX=13,sizeY=5,X=50,Y=50,texcolor="white",bg="red",fg="#3B8ED0",cornerradius=10,com=None,first_value=0,end_value=100):
        super().__init__(master)
        # add widgets onto the frame...
        self.update()
        mas_win_width=master.winfo_reqwidth()
        mas_win_height=master.winfo_reqheight()
        if master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        scw = mas_win_width*sizeX/100
        sch = mas_win_height*sizeY/100
        sw = mas_win_width*X/100
        sh = mas_win_height*Y/100
        if com is not None:
            self.scaler  = customtkinter.CTkSlider(master,width=scw,height=sch,corner_radius=cornerradius,fg_color=fg,command=com,bg_color=bg,from_=first_value,to=end_value)
        else:
            self.scaler  = customtkinter.CTkSlider(master,width=scw,height=sch,corner_radius=cornerradius,fg_color=fg,bg_color=bg,from_=first_value,to=end_value)
        #if com is not None and self.commandClass is not None:
            #print(self.commandClass.__name__)
            #self.combbox.bind("<<ComboboxSelected>>", getattr(self.commandClass, com.__name__))
        self.scaler.pack(pady=10, padx=10)
        #combbox.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        self.scaler.update()
        w=self.scaler.winfo_reqwidth()
        h=self.scaler.winfo_reqheight()
        sw-=(w/2)
        sh-=(h/2)
        self.scaler.place(x=sw,y=sh)

class CustomTextBox(customtkinter.CTkFrame):
    textBox=None
    num=0
    def Insert(self,text):
        self.textBox.insert("0.0",str(self.num)+":"+text)
        self.num+=1
    def __init__(self, master, text="none_text",text_size=11,corner=-1,curb=10,X=50,Y=50,sizeX=20,sizeY=20):
        super().__init__(master)
        '''
        X,Yは0~1の間をとる
        '''
        # add widgets onto the frame...
        self.update()
        mas_win_width=master.winfo_reqwidth()
        mas_win_height=master.winfo_reqheight()
        if master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        scw = mas_win_width*X/100
        sch = mas_win_height*Y/100
        sw = mas_win_width*sizeX/100
        sh = mas_win_height*sizeY/100
        if corner==-1:
            self.textBox = customtkinter.CTkTextbox(self, font=(FONT_TYPE, text_size),width=sw,height=sh)
        else:
            self.textBox = customtkinter.CTkTextbox(self, font=(FONT_TYPE, text_size),corner_radius=corner,width=sw,height=sh)
        self.Insert(text)
        self.textBox.grid(row=0, column=0, padx=curb)
        self.update()
        w=self.textBox.winfo_reqwidth()
        h=self.textBox.winfo_reqheight()
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        scw-=(w/2)
        sch-=(h/2)
        self.place(x=scw,y=sch)

class CustomFlame(customtkinter.CTkFrame):
    def __init__(self, master, text="none_text",text_size=11,corner=-1,curb=10,X=50,Y=50,sizeX=20,sizeY=20):
        super().__init__(master)
        '''
        X,Yは0~1の間をとる
        '''
        # add widgets onto the frame...
        self.update()
        mas_win_width=master.winfo_reqwidth()
        mas_win_height=master.winfo_reqheight()
        if master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        scw = mas_win_width*X/100
        sch = mas_win_height*Y/100
        sw = mas_win_width*sizeX/100
        sh = mas_win_height*sizeY/100
        if corner==-1:
            self.label = customtkinter.CTkLabel(self,text=text, font=(FONT_TYPE, text_size),width=sw,height=sh)
        else:
            self.label = customtkinter.CTkLabel(self,text=text, font=(FONT_TYPE, text_size),corner_radius=corner,width=sw,height=sh)
        self.label.grid(row=0, column=0, padx=curb)
        self.update()
        w=self.label.winfo_reqwidth()
        h=self.label.winfo_reqheight()
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        scw-=(w/2)
        sch-=(h/2)
        self.place(x=scw,y=sch)
        
class TEXT(customtkinter.CTkFrame):
    def __init__(self, master, text="none_text",text_size=11,X=50,Y=50):
        super().__init__(master)
        # add widgets onto the frame...
        self.label = customtkinter.CTkLabel(self,text=text, font=(FONT_TYPE, text_size))
        self.label.grid(row=0, column=0, padx=0)
        self.update()
        if master is not None:
            mas_win_width=master.winfo_reqwidth()
            mas_win_height=master.winfo_reqheight()
            if master.master is None:
                mas_win_width=DEFAULT_WINDOW_WIDTH
                mas_win_height=DEFAULT_WINDOW_HEIGHT
            scw = mas_win_width*X
            sch = mas_win_height*Y
            w=self.label.winfo_reqwidth()
            h=self.label.winfo_reqheight()
            self.label.configure(fg_color=master.cget("fg_color"))
            self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
            scw-=(w/2)
            sch-=(h/2)
            self.place(x=scw,y=sch)
        else:
            self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
            self.place(x=X,y=Y)

class CustomButton(customtkinter.CTkFrame):
    def __init__(self, master, text="none_text",text_size=11,sizeX=20,sizeY=20,X=0,Y=0,texcolor="white",fg="blue",com=None,cornerradius=10):
        super().__init__(master)
        # add widgets onto the frame...
        self.update()
        mas_win_width=master.winfo_reqwidth()
        mas_win_height=master.winfo_reqheight()
        if master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        scw = mas_win_width*sizeX/100
        sch = mas_win_height*sizeY/100
        sw = mas_win_width*X/100
        sh = mas_win_height*Y/100
        if com is None:
            self.button1  = customtkinter.CTkButton(self,text=text, font=(FONT_TYPE, text_size),width=scw,height=sch,corner_radius=cornerradius,text_color=texcolor,fg_color=fg)
        else:
            self.button1  = customtkinter.CTkButton(self,text=text, font=(FONT_TYPE, text_size),width=scw,height=sch,corner_radius=cornerradius,text_color=texcolor,fg_color=fg,command=com)
        self.button1.grid(row=0, column=0, padx=0)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        self.update()
        w=self.button1.winfo_reqwidth()
        h=self.button1.winfo_reqheight()
        sw-=(w/2)
        sh-=(h/2)
        self.place(x=sw,y=sh)

class CustomCombobox (customtkinter.CTkFrame):
    combbox=None
    def __init__(self, master,text_size=30,sizeX=13,sizeY=5,X=50,Y=50,texcolor="white",fg="#3B8ED0",cornerradius=10,value=["None1","None2","None3","None4"],com=None):
        super().__init__(master)
        # add widgets onto the frame...
        self.update()
        mas_win_width=master.winfo_reqwidth()
        mas_win_height=master.winfo_reqheight()
        if master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        scw = mas_win_width*sizeX/100
        sch = mas_win_height*sizeY/100
        sw = mas_win_width*X/100
        sh = mas_win_height*Y/100
        if com is not None:
            self.combbox  = customtkinter.CTkComboBox(master, font=(FONT_TYPE, text_size),width=scw,height=sch,corner_radius=cornerradius,text_color=texcolor,fg_color=fg,values=value,command=com)
        else:
            self.combbox  = customtkinter.CTkComboBox(master, font=(FONT_TYPE, text_size),width=scw,height=sch,corner_radius=cornerradius,text_color=texcolor,fg_color=fg,values=value)
        #if com is not None and self.commandClass is not None:
            #print(self.commandClass.__name__)
            #self.combbox.bind("<<ComboboxSelected>>", getattr(self.commandClass, com.__name__))
        self.combbox.pack(pady=10, padx=10)
        #combbox.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        self.combbox.update()
        w=self.combbox.winfo_reqwidth()
        h=self.combbox.winfo_reqheight()
        sw-=(w/2)
        sh-=(h/2)
        self.combbox.place(x=sw,y=sh)

class LCU_Controller(customtkinter.CTkFrame):
    '''
    LCUのコントローラーを設置するクラス
    '''
    def __init__(self, master,win_height=400,win_width=750,win_posx=0,win_posy=0):
        super().__init__(master)
        # add widgets onto the frame...
        ACU_F=customtkinter.CTkFrame(self.master,width=win_width,height=win_height,corner_radius=5)
        ACU_F.grid(row=0, column=0, padx=0)
        ACU_F.place(x=win_posx, y=win_posy)
        scw = ACU_F.winfo_screenwidth()
        sch = ACU_F.winfo_screenheight()
        Azimuth_T= TEXT(master=ACU_F,text="Azmizu",text_size=20,X=0.5,Y=0.5)

class ACU_GUI(customtkinter.CTk):
    ACU_Monitor=None
    NAME="TEST"
    YearTime_F=None
    JstTime_F=None
    UctTime_F=None
    LstTime_F=None
    COM_F=None
    Scaler=None
    COM_Monitor=None
    QUIET_BUTTON=None
    TEST_ASYNC=None
    ASYNC_LIST=[]
    eASYNC_LIST=[]

    def updateTimer(self):
        time.updateAllTime()
        self.YearTime_F.label.configure(text=time.Year_Time)
        self.JstTime_F.label.configure(text=time.JSTformat)
        self.UctTime_F.label.configure(text=time.UTCformat)
        self.LstTime_F.label.configure(text=time.LSTformat)
        self.YearTime_F.after(1000,self.updateTimer)
    def setYearTime(self,S):
        return CustomFlame(master=S,text=time.Year_Time,text_size=30,sizeY=5,sizeX=10)
    def setJST(self,S):
        return CustomFlame(master=S,text=time.JSTformat,text_size=30,sizeY=5,sizeX=10)
    def setUCT(self,S):
        return CustomFlame(master=S,text=time.UTCformat,text_size=30,sizeY=5,sizeX=10)
    def setLST(self,S):
        return CustomFlame(master=S,text=time.LSTformat,text_size=30,sizeY=5,sizeX=10)

    def __init__(self,async_list=None,asynctest=None):
        super().__init__()
    
    def setupAsyncList(self,async_list=None):
        if async_list is not None:
            if len(async_list)>0:
                for i in range(len(async_list)):
                    self.ASYNC_LIST.append(async_list[i])
                    print("APPEND!")#BackEnd.Async(async_list[i])

    def setupAsync2List(self,Asyncs=None):
        if Asyncs is not None:
            self.ASYNC_LIST.append(Asyncs)
            print("APPEND!")
            
    def enableAsync(self):
        if self.ASYNC_LIST is not None:
            if len(self.ASYNC_LIST)>0:
                for i in range(len(self.ASYNC_LIST)):
                    self.eASYNC_LIST.append(BackEnd.Async(self.ASYNC_LIST[i]))
        
    def quit1(self):
        if self.eASYNC_LIST is not None:
            if len(self.eASYNC_LIST)>0:
                for i in range(len(self.eASYNC_LIST)):
                    self.eASYNC_LIST[i].kill()
        #self.COM_Monitor.join()
        self.destroy()
        
    def Nothig(self):
        print("")
        
        
    def ApperGUI(self):
        global SELECTED_COM
        print("ACU_GUI_BEGUN!")
        customtkinter.set_appearance_mode("green")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        time.updateAllTime()
        
        self.geometry("1250x600")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        self.protocol('WM_DELETE_WINDOW', self.Nothig)
        
        self.JstTime_F = self.setJST(self)
        self.JstTime_F.place(x=165,y=0)#110
        
        self.UctTime_F = self.setUCT(self)
        self.UctTime_F.place(x=368,y=0)#245
        
        self.LstTime_F = self.setLST(self)
        self.LstTime_F.place(x=583,y=0)
        
        self.YearTime_F = self.setYearTime(self)
        self.YearTime_F.place(x=0,y=0)
        self.YearTime_F.after(1000,self.updateTimer)
        
        self.QUIET_BUTTON=CustomButton(master=self,text="QUIET!",text_size=30,X=80,Y=20,sizeX=10,sizeY=5,com=self.quit1,fg="red")

        Place_F = CustomFlame(master=self,text="あわらキャンパス",text_size=30,sizeX=10,sizeY=5)
        Place_F.place(x=798,y=0)
        
        self.Scaler=CustomScaler(master=self)
        
        self.COM_F=CustomCombobox(master=self,value=self.ACU_Monitor.BackEnd.getSerialPorts(),X=92,Y=3,sizeX=15,sizeY=4)
        SELECTED_COM=self.COM_F.combbox.get()
        #self.COM_F.combbox.configure(command=self.ThrowSelectedCom2Backend)
        
        #textbox=CustomTextBox(master=self,text="FUCKYOU!",text_size=30,sizeX=30,sizeY=30)
        
        
        
        #self.COM_Monitor=threading.Thread(target=self.ThrowSelectedCom2Backend)
        #self.COM_Monitor.start()
        
        self.enableAsync()
        
        
    
        #button=CustomButton(master=self,text="HELLO!",text_size=30,X=50,Y=50,com=self.selected)
        #ACU=LCU_Controller(master=self,win_posx=100,win_posy=60)
    


class StartGUI():
    gui=None
    def __init__(self):
        print("StartGUI")
        self.gui=ACU_GUI()
    def getGUI(self):
        return self.gui
    def LoopGui(self):
        self.gui.mainloop()
    def ApperGUI(self):
        self.gui.ApperGUI()
    def setAsync_Class(self,Async):
        self.gui.Async_Class=Async
    