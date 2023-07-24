import customtkinter
import getTime as time
import ACUbackend as BackEnd
import threading
import time as Timer
import copy
import math

FONT_TYPE = "Segoe UI"
DEFAULT_WINDOW_WIDTH=1110
DEFAULT_WINDOW_HEIGHT=700
SELECTED_COM="NONE"
RADIO_BUTTOM_NUM=0
ANTTENA_AZMIZTH=3600000
AZMIZTH_STR="3 6 0. 0 0 0 0"
AZMIZTH_MAX=3600000
AZMIZTH_MIN=0
ANTENA_ELEVATION=900000
ELEVATION_STR="9 0. 0 0 0 0"
ELEVATION_MAX=900000
ELEVATION_MIN=0

IS_SLAVE_MODE=False
IS_INDIVISUAL_MODE=True

class CustomBase(customtkinter.CTkFrame):
    posx=0
    posy=0
    sizex=0
    sizey=0
    master=None
    X=0
    Y=0
    inited=False
    parent=None
    text="None"
    text_size=11
    sizeX=20
    sizeY=20
    directBody=None
    def setDisable(self):
        self.directBody.configure(state="disabled")
    def setNormal(self):
        self.directBody.configure(state="normal")
    def is_integer_num(self,n):
        if isinstance(n, int):
            return True
        if isinstance(n, float):
            return n.is_integer()
        return False
    def setGUI(self):
        i=0
        #self.directBody = customtkinter.CTkLabel(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey)
        #self.directBody.grid(row=0, column=0, padx=10)
        #self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def UPDATEGUI(self):
        i=0
        #self.directBody.configure(text=self.text)
    def update_gui(self,text="none_text",text_size=1.1,X=1.1,Y=1.1,sizeX=1.1,sizeY=1.1):
        if text!="none_text":
            self.text=text
        if self.is_integer_num(text_size):
            self.text_size=text_size
        if self.is_integer_num(X):
            self.X=X
        if self.is_integer_num(Y):
            self.Y=Y
        if self.is_integer_num(sizeX):
            self.sizeX=sizeX
        if self.is_integer_num(sizeY):
            self.sizeY=sizeY
        self.update()
        mas_win_width=self.master.winfo_reqwidth()
        mas_win_height=self.master.winfo_reqheight()
        if isinstance(self.master,CustomBase):
            mas_win_width=self.master.sizex
            mas_win_height=self.master.sizey
        if self.master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        scw = mas_win_width*self.X/100
        sch = mas_win_height*self.Y/100
        sw = mas_win_width*self.sizeX/100
        sh = mas_win_height*self.sizeY/100
        if text=="Conect":   
            print("w1="+str(sw))
        self.sizex=sw
        self.sizey=sh
        if self.parent is not None:
            scw,sch=self.parent.getWorldpos(x=self.X,y=self.Y)
        if self.inited is False:
            self.setGUI()
        else:
            self.UPDATEGUI()
        self.update()
        w=self.sizex
        h=self.sizey
        scw-=(w/2)
        sch-=(h/2)
        #scw-=(req_w/2)
        #sch-=(req_h/2)
        self.place(x=scw,y=sch)
        self.posx=scw
        self.posy=sch
        self.inited=True
    def getWorldpos(self,x=50,y=50):
        X=x/100
        Y=y/100
        X=self.sizex*X
        Y=self.sizey*Y
        return (self.posx+X),(self.posy+Y)
    def __init__(self, master, text="none_text",text_size=11,X=50,Y=50,sizeX=20,sizeY=20,parent=None):
        super().__init__(master)
        self.master=master
        self.parent=parent

class CustomRadioButtom(CustomBase):
    selfNum=0
    texcolor="white"
    fg="#3B8ED0"
    hg="red"
    def selfUpdateValue(self,texcolor="white",fg="#3B8ED0",hg="red",com=None,cornerradius=10):
        if texcolor!="none":
            self.texcolor=texcolor
        self.fg=fg
        self.hg=hg
    def setGUI(self):
        super(CustomRadioButtom,self).setGUI()
        self.directBody  = customtkinter.CTkRadioButton(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,text_color=self.texcolor,fg_color=self.fg,hover_color=self.hg,bg_color=self.master.cget("fg_color"))
        self.directBody.grid(row=0, column=0, padx=0)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master, text="none_text",text_size=11,X=50,Y=50,sizeX=20,sizeY=20,parent=None,texcolor="white",fg="#3B8ED0",hg="red"):
        super().__init__(master, text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent)
        global RADIO_BUTTOM_NUM
        RADIO_BUTTOM_NUM+=1
        self.selfNum=RADIO_BUTTOM_NUM
        self.selfUpdateValue(texcolor=texcolor,fg=fg,hg=hg)
        self.update_gui(text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY)

class CustomScaler(customtkinter.CTkFrame):
    scaler=None
    posx=0
    posy=0
    sizex=0
    sizey=0
    def getWorldpos(self,x=50,y=50):
        X=x/100
        Y=y/100
        X=self.sizex*X
        Y=self.sizey*Y
        return (self.posx+X),(self.posy+Y)
    def __init__(self, master,text_size=30,sizeX=13,sizeY=5,X=50,Y=50,texcolor="white",bg="red",fg="#3B8ED0",cornerradius=10,com=None,first_value=0,end_value=100,parent=None):
        super().__init__(master)
        # add widgets onto the frame...
        self.update()
        mas_win_width=master.winfo_reqwidth()
        mas_win_height=master.winfo_reqheight()
        mas_win_width=0
        mas_win_height=0
        if type(master) is CustomFlame:
            mas_win_width=master.sizex
            mas_win_height=master.sizey
        if master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        scw = mas_win_width*sizeX/100
        sch = mas_win_height*sizeY/100
        sw = mas_win_width*X/100
        sh = mas_win_height*Y/100
        if parent is not None:
            sw,sh=parent.getWorldpos(x=X,y=Y)
        self.sizex=scw
        self.sizey=sch
        if com is not None:
            self.scaler  = customtkinter.CTkSlider(master,width=scw,height=sch,corner_radius=cornerradius,fg_color=fg,command=com,bg_color=bg,from_=first_value,to=end_value,number_of_steps=10)
        else:
            self.scaler  = customtkinter.CTkSlider(master,width=scw,height=sch,corner_radius=cornerradius,fg_color=fg,bg_color=bg,from_=first_value,to=end_value,number_of_steps=10)
        #self.scaler.pack(pady=10, padx=10)
        self.scaler.update()
        w=self.scaler.winfo_reqwidth()
        h=self.scaler.winfo_reqheight()
        sw-=(w/2)
        sh-=(h/2)
        self.scaler.place(x=sw,y=sh)
        self.posx=sw
        self.posy=sh

class CustomTextBox2(CustomBase):
    corner=1
    curb=10
    num=0
    def Insert(self,text):
        self.directBody.insert("0.0",str(self.num)+":"+text)
        self.num+=1
    def setGUI(self):
        super(CustomTextBox2,self).setGUI()
        self.directBody =customtkinter.CTkTextbox(self, font=(FONT_TYPE, self.text_size),corner_radius=self.corner,width=self.sizex,height=self.sizey)
        self.Insert(self.text)
        self.directBody.grid(row=0, column=0, padx=self.curb)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master, text="none_text",text_size=11,corner=-1,curb=10,X=50,Y=50,sizeX=20,sizeY=20,parent=None):
        super().__init__(master=master, text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent)
        self.corner=corner
        self.curb=curb
        self.update_gui(text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY)

class CustomTextBox(customtkinter.CTkFrame):
    textBox=None
    num=0
    posx=0
    posy=0
    sizex=0
    sizey=0
    def getWorldpos(self,x=50,y=50):
        X=x/100
        Y=y/100
        X=self.sizex*X
        Y=self.sizey*Y
        return (self.posx+X),(self.posy+Y)
    def Insert(self,text):
        self.textBox.insert("0.0",str(self.num)+":"+text)
        self.num+=1
    def __init__(self, master, text="none_text",text_size=11,corner=-1,curb=10,X=50,Y=50,sizeX=20,sizeY=20,parent=None):
        super().__init__(master)
        '''
        X,Yは0~1の間をとる
        '''
        # add widgets onto the frame...
        self.update()
        mas_win_width=master.winfo_reqwidth()
        mas_win_height=master.winfo_reqheight()
        mas_win_width=0
        mas_win_height=0
        if type(master) is CustomFlame:
            mas_win_width=master.sizex
            mas_win_height=master.sizey
        #mas_win_width=master.winfo_reqwidth()
        #mas_win_height=master.winfo_reqheight()
        if master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        scw = mas_win_width*X/100
        sch = mas_win_height*Y/100
        if parent is not None:
            scw,sch=parent.getWorldpos(X,Y)
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
           
class TEXT(customtkinter.CTkFrame):
    posx=0
    posy=0
    sizex=0
    sizey=0
    scw=0
    sch=0
    master=None
    X=0
    Y=0
    GRITED=False
    Parent=None
    def update_scs(self):
        self.update()
        mas_win_width=self.master.winfo_reqwidth()
        mas_win_height=self.master.winfo_reqheight()
        if type(self.master) is CustomFlame:
            mas_win_width=self.master.sizex
            mas_win_height=self.master.sizey
        if self.master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        self.scw = mas_win_width*self.X/100
        self.sch = mas_win_height*self.Y/100
        if self.Parent is not None:
            self.scw,self.sch=self.Parent.getWorldpos(self.X,self.Y)
    def update_pos(self):
        self.update()
        w=self.label.winfo_reqwidth()
        h=self.label.winfo_reqheight()
        self.sizex=w
        self.sizey=h
        if self.GRITED is False:
            self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
            self.GRITED=True
        self.scw-=(w/2)
        self.sch-=(h/2)
        self.place(x=self.scw,y=self.sch)
        self.posx=self.scw
        self.posy=self.sch
    def update_text(self,T):
        self.label.configure(text=T)
        self.update_scs()
        self.update_pos()
    def getWorldpos(self,x=50,y=50):
        X=x/100
        Y=y/100
        X=self.sizex*X
        Y=self.sizey*Y
        return (self.posx+X),(self.posy+Y)
    def __init__(self, master, text="none_text",text_size=11,X=50,Y=50,parent=None,bg="gray"):
        super().__init__(master)
        self.master=master
        self.Parent=parent
        self.X=X
        self.Y=Y
        self.update_scs()
        '''
        mas_win_width=master.winfo_reqwidth()
        mas_win_height=master.winfo_reqheight()
        if type(master) is CustomFlame:
            mas_win_width=master.sizex
            mas_win_height=master.sizey
        if master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        self.scw = mas_win_width*X/100
        self.sch = mas_win_height*Y/100
        if parent is not None:
            self.Parent=parent
            self.scw,self.sch=parent.getWorldpos(X,Y)
        if parent is not None:
            self.Parent=parent
            self.scw,self.sch=parent.getWorldpos(X,Y)
        '''
        self.label = customtkinter.CTkLabel(self,text=text, font=(FONT_TYPE, text_size),bg_color=master.cget("bg_color"),fg_color=master.cget("fg_color"))
        self.label.grid(row=0, column=0, padx=0)
        self.update_pos()
        '''
        self.update()
        w=self.label.winfo_reqwidth()
        h=self.label.winfo_reqheight()
        self.sizex=w
        self.sizey=h
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        scw-=(w/2)
        sch-=(h/2)
        self.place(x=scw,y=sch)
        self.posx=scw
        self.posy=sch
                # add widgets onto the frame...
        '''

class CustomButton(CustomBase):
    texcolor="black"
    fg="#3B8ED0"
    hg="red"
    bg="#3B8ED0"
    com=None
    cornerradius=10
    def setDefaultColor(self):
        self.directBody.configure(fg_color="#3B8ED0")
        self.fg="#3B8ED0"
    def setColor(self,color="red"):
        self.directBody.configure(fg_color=color)
        self.fg=color
    def selfUpdateValue(self,texcolor="white",fg="#3B8ED0",hg="red",com=None,cornerradius=10,bg="#3B8ED0"):
        if texcolor!="none":
            self.texcolor=texcolor
        self.fg=fg
        self.hg=hg
        self.bg=bg
        if com is not None:
            print("COM!!!!!!!!!!")
            self.com=com
        if self.is_integer_num(cornerradius):
            self.cornerradius=cornerradius
    def UPDATEGUI(self):
        super(CustomButton,self).UPDATEGUI()
        self.directBody.configure(text=self.text)
    def setGUI(self):
        super(CustomButton,self).setGUI()
        if self.com is not None:
            self.directBody  = customtkinter.CTkButton(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.texcolor,fg_color=self.fg,command=self.com,hover_color=self.hg,bg_color=self.bg)
        else:
            self.directBody  = customtkinter.CTkButton(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.texcolor,fg_color=self.fg,hover_color=self.hg,bg_color=self.bg)
        self.directBody.grid(row=0, column=0, padx=0,pady=0)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master, text="none_text",text_size=11,X=50,Y=50,sizeX=20,sizeY=20,parent=None,texcolor="black",fg="#3B8ED0",hg="red",bg="#3B8ED0",com=None,cornerradius=10):
        if com is None:
            print("COOOOOOOOOOOM")
        super().__init__(master, text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent)
        self.selfUpdateValue(texcolor=texcolor,fg=fg,hg=hg,com=com,cornerradius=cornerradius,bg=bg)
        self.update_gui(text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY)

class CustomChekButton(CustomButton):
    def setGUI(self):
        super(CustomChekButton,self).setGUI()
        if self.com is not None:
            self.directBody  = customtkinter.CTkCheckBox(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.texcolor,fg_color=self.fg,command=self.com,hover_color=self.hg,bg_color=self.master.cget("fg_color"))
        else:
            self.directBody  = customtkinter.CTkCheckBox(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.texcolor,fg_color=self.fg,hover_color=self.hg,bg_color=self.master.cget("fg_color"))
        self.directBody.grid(row=0, column=0, padx=0)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master, text="none_text",text_size=11,X=50,Y=50,sizeX=20,sizeY=20,parent=None,texcolor="black",fg="#3B8ED0",hg="red",com=None,cornerradius=10):
        super().__init__(master, text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent,texcolor=texcolor,fg=fg,hg=hg,com=com,cornerradius=cornerradius)

class CustomCombobox (customtkinter.CTkFrame):
    posx=0
    posy=0
    sizex=0
    sizey=0
    def setDisable(self):
        print("DIS!")
        self.combbox.label.configure(state=customtkinter.DISABLED)
    def setEnable(self):
        self.combbox.configure(state=customtkinter.NORMAL)
    def getWorldpos(self,x=50,y=50):
        X=x/100
        Y=y/100
        X-=0.5
        Y-=0.5
        X=self.sizex*X
        Y=self.sizey*Y
        return (self.posx+X),(self.posy+Y)
    combbox=None
    def setDisconected(self):
        self.combbox.configure(values=["Disconected"],fg_color="red")
    def setValue(self,value=["something"]):
        if len(value)==0:
            self.setDisconected()
        else:
            self.combbox.configure(values=value,fg_color="#3B8ED0")
    def __init__(self, master,text_size=30,sizeX=13,sizeY=5,X=50,Y=50,texcolor="white",fg="#3B8ED0",cornerradius=10,value=["None1","None2","None3","None4"],com=None,parent=None):
        super().__init__(master)
        # add widgets onto the frame...
        self.update()
        mas_win_width=master.winfo_reqwidth()
        mas_win_height=master.winfo_reqheight()
        if type(master) is CustomFlame:
            mas_win_width=master.sizex
            mas_win_height=master.sizey
        #mas_win_width=master.winfo_reqwidth()
        #mas_win_height=master.winfo_reqheight()
        if master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        scw = mas_win_width*sizeX/100
        sch = mas_win_height*sizeY/100
        sw = mas_win_width*X/100
        sh = mas_win_height*Y/100
        if parent is not None:
            sw,sh=parent.getWorldpos(X,Y)
        if len(value)==0:
            value=["Disconected"]
            fg="red"
        if com is not None:
            self.combbox  = customtkinter.CTkComboBox(master, font=(FONT_TYPE, text_size),width=scw,height=sch,corner_radius=cornerradius,text_color=texcolor,fg_color=fg,values=value,command=com)
        else:
            self.combbox  = customtkinter.CTkComboBox(master,font=(FONT_TYPE, text_size),width=scw,height=sch,corner_radius=cornerradius,text_color=texcolor,fg_color=fg,values=value)
        #if com is not None and self.commandClass is not None:
            #print(self.commandClass.__name__)
            #self.combbox.bind("<<ComboboxSelected>>", getattr(self.commandClass, com.__name__))
        self.combbox.pack(pady=10, padx=10)
        #combbox.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        self.update()
        self.combbox.update()
        w=self.combbox.winfo_reqwidth()
        h=self.combbox.winfo_reqheight()
        sw-=(w/2)
        sh-=(h/2)
        self.combbox.place(x=sw,y=sh)

class CustomCheckBox(customtkinter.CTkFrame):
    posx=0
    posy=0
    sizex=0
    sizey=0
    def getWorldpos(self,x=50,y=50):
        X=x/100
        Y=y/100
        X-=0.5
        Y-=0.5
        X=self.sizex*X
        Y=self.sizey*Y
        return (self.posx+X),(self.posy+Y)
    def __init__(self, master, text="none_text",text_size=11,sizeX=1,sizeY=1,X=50,Y=50,texcolor="white",fg="#3B8ED0",hg="red",com=None,cornerradius=10,parent=None):
        super().__init__(master)
        # add widgets onto the frame...
        self.update()
        mas_win_width=master.winfo_reqwidth()
        mas_win_height=master.winfo_reqheight()
        if type(master) is CustomFlame:
            mas_win_width=master.sizex
            mas_win_height=master.sizey
        #mas_win_width=master.winfo_reqwidth()
        #mas_win_height=master.winfo_reqheight()
        if master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        scw = mas_win_width*sizeX/100
        sch = mas_win_height*sizeY/100
        sw = mas_win_width*X/100
        sh = mas_win_height*Y/100
        if parent is not None:
            sw,sh=parent.getWorldpos(X,Y)
        if com is None:
            self.button1  = customtkinter.CTkCheckBox(self,text=text,font=(FONT_TYPE, text_size),width=scw,height=sch,corner_radius=cornerradius,text_color=texcolor,fg_color=fg)
        else:
            self.button1  = customtkinter.CTkCheckBox(self,text=text, font=(FONT_TYPE, text_size),width=scw,height=sch,corner_radius=cornerradius,text_color=texcolor,fg_color=fg,command=com)
        self.button1.grid(row=0, column=0, padx=0)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        self.update()
        self.button1.update()
        w=self.button1.winfo_reqwidth()
        h=self.button1.winfo_reqheight()
        sw-=(w/2)
        sh-=(h/2)
        self.place(x=sw,y=sh)

class CustomFlame(CustomBase):
    corner=-1
    curb=10
    bg="#3B8ED0"
    fg=""
    def UPDATEGUI(self):
        super(CustomFlame,self).UPDATEGUI()
        self.directBody.configure(text=self.text)
    def setGUI(self):
        super(CustomFlame,self).setGUI()
        self.directBody = customtkinter.CTkLabel(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,bg_color=self.bg,fg_color=self.fg)
        self.directBody.grid(row=0, column=0, padx=self.curb)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master, text="none_text",text_size=11,corner=-1,curb=10,X=50,Y=50,sizeX=20,sizeY=20,parent=None,bg="gray15",fg="gray15"):
        super().__init__(master=master, text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent)
        self.corner=corner
        self.curb=curb
        self.bg=bg
        self.fg=fg
        self.update_gui(text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY)
        
class CustomText(CustomBase):
    def getWorldpos(self,x=50,y=50):
        super(CustomText,self).getWorldpos()
        X=x/100
        Y=y/100
        X=self.sizex*X
        Y=self.sizey*Y
        return (self.posx+X),(self.posy+Y)
    def UPDATEGUI(self):
        super(CustomText,self).UPDATEGUI()
        self.directBody.configure(text=self.text)
    def setGUI(self):
        super(CustomText,self).setGUI()
        self.directBody = customtkinter.CTkLabel(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,bg_color=self.master.directBody.cget("bg_color"),fg_color=self.master.directBody.cget("fg_color"))
        self.directBody.grid(row=0, column=0, padx=0)
        #self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master, text="none_text",text_size=11,X=50,Y=50,sizeX=20,sizeY=20,parent=None):
        super().__init__(master, text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent)
        self.update_gui(text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY)

class LCU_Controller(customtkinter.CTkFrame):
    '''
    LCUのコントローラーを設置するクラス
    '''
    Commad_Line=None
    
    Az_Real_F=None
    Az_Real_V_F=None
    Az_Prog_F=None
    Az_Prog_V_F=None
    Az_RePr_F=None
    Az_RePr_V_F=None
    Az_SPEED_S=None
    Az_SPEED_F=None
    Az_SPEED_FF=None
    Az_STOW_F=None
    Az_STOW_POS_B=None
    Az_STOW_LOCK_B=None
    Az_STOW_REL_B=None
    Az_MODE_F=None
    Az_MODE_PROG_B=None
    Az_MODE_MANU_B=None
    Az_MODE_STBY_B=None
    
    Az_Limit_F=None
    Az_Limit_PLUS=None
    Az_Limit_Unko_PB1=None
    Az_Limit_Unko_PB2=None
    Az_Limit_Unko_MB1=None
    Az_Limit_Unko_MB2=None
    Az_Limit_MNUS=None
    
    Az_LEVEL_V_3=None
    Az_LEVEL_V_6=None
    Az_LEVEL_V_0=None
    Az_LEVEL_V_01=None
    Az_LEVEL_V_001=None
    Az_LEVEL_V_0001=None
    Az_LEVEL_V_00001=None
    
    Az_LEVEL_VH_F=None
    Az_LEVEL_VT_F=None
    Az_LEVEL_VO_F=None
    Az_LEVEL_V01_F=None
    Az_LEVEL_V001_F=None
    Az_LEVEL_V0001_F=None
    Az_LEVEL_V00001_F=None
    
    Az_LEVEL_VHM_F=None
    Az_LEVEL_VTM_F=None
    Az_LEVEL_VOM_F=None
    Az_LEVEL_V01M_F=None
    Az_LEVEL_V001M_F=None
    Az_LEVEL_V0001M_F=None
    Az_LEVEL_V00001M_F=None
    Az_LEVEL_PLUS_B=None
    Az_LEVEL_MNUS_B=None
    #---------------------------#
    EL_Real_F=None
    EL_Real_V_F=None
    EL_Prog_F=None
    EL_Prog_V_F=None
    EL_RePr_F=None
    EL_RePr_V_F=None
    EL_SPEED_S=None
    EL_SPEED_F=None
    EL_SPEED_FF=None
    EL_STOW_F=None
    EL_STOW_POS_B=None
    EL_STOW_LOCK_B=None
    EL_STOW_REL_B=None
    EL_MODE_F=None
    EL_MODE_PROG_B=None
    EL_MODE_MANU_B=None
    EL_MODE_STBY_B=None
    EL_LEVEL_V_F=None
    
    EL_LEVEL_VH_F=None
    EL_LEVEL_VT_F=None
    EL_LEVEL_VO_F=None
    EL_LEVEL_V01_F=None
    EL_LEVEL_V001_F=None
    EL_LEVEL_V0001_F=None
    EL_LEVEL_V00001_F=None

    EL_LEVEL_V_9=None
    EL_LEVEL_V_0=None
    EL_LEVEL_V_01=None
    EL_LEVEL_V_001=None
    EL_LEVEL_V_0001=None
    EL_LEVEL_V_00001=None

    EL_Limit_F=None
    EL_Limit_PLUS=None
    EL_Limit_Unko_PB1=None
    EL_Limit_Unko_PB2=None
    EL_Limit_Unko_MB1=None
    EL_Limit_Unko_MB2=None
    EL_Limit_MNUS=None
    
    EL_LEVEL_VHM_F=None
    EL_LEVEL_VTM_F=None
    EL_LEVEL_VOM_F=None
    EL_LEVEL_V01M_F=None
    EL_LEVEL_V001M_F=None
    EL_LEVEL_V0001M_F=None
    EL_LEVEL_V00001M_F=None
    EL_LEVEL_PLUS_B=None
    EL_LEVEL_MNUS_B=None
    
    def change_Az_Speed_F(self,str):
        self.Az_SPEED_F.update_gui(text=str)
        
    def change_El_Speed_F(self,str):
        self.EL_SPEED_F.update_gui(text=str)
        
    def set_Az(self,AzV=3600000): 
        global AZMIZTH_STR
        AZMIZTH_STR=str(AzV)
        LEN=len(AZMIZTH_STR)
        num=AzV
        unkown="-"
        Int1000000=(int(num/1000000))
        print("I1000000="+str(Int1000000))
        num-=(Int1000000*1000000)
        Int100000=(int(num/100000))
        print("I100000="+str(Int100000))
        
        num-=(Int100000*100000)
        Int10000=(int(num/10000))
        print("I10000="+str(Int10000))

        num-=(Int10000*10000)
        Int1000=(int(num/1000))
        print("I1000="+str(Int1000))
    
        num-=(Int1000*1000)
        Int100=(int(num/100))
        print("I100="+str(Int100))
        
        num-=(Int100*100)
        Int10=(int(num/10))
        print("I10="+str(Int10))
        
        num-=(Int10*10)
        Int1=(int(num))
        print("I1="+str(Int1))

        
        if Int1000000<1:
            IsHundret="0"
        else:
            IsHundret=str(Int1000000)
            
        if Int100000<1:
            IsTen="0"
        else:
            IsTen=str(Int100000)

        if Int10000<1:
            IsOne="0"
        else:
            IsOne=str(Int10000)
            
        if Int1000<1:
            Is01="0"
        else:
            Is01=str(Int1000)
            
        if Int100<1:
            Is001="0"
        else:
            Is001=str(Int100)
            
        if Int10<1:
            Is0001="0"
        else:
            Is0001=str(Int10)
            
        if Int1<1:
            Is00001="0"
        else:
            Is00001=str(Int1)

        self.Az_LEVEL_V_3.update_gui(text=IsHundret)
        self.Az_LEVEL_V_6.update_gui(text=IsTen)
        self.Az_LEVEL_V_0.update_gui(text=IsOne)
        self.Az_LEVEL_V_01.update_gui(text=Is01)
        self.Az_LEVEL_V_001.update_gui(text=Is001)
        self.Az_LEVEL_V_0001.update_gui(text=Is0001)
        self.Az_LEVEL_V_00001.update_gui(text=Is00001)
        
    def set_El(self,ElV=900000):
        global ELEVATION_STR
        ELEVATION_STR=str(ElV)
        LEN=len(ELEVATION_STR)
        num=ElV
        unkown="-"
        
        Int100000=(int(num/100000))
        num-=(Int100000*100000)
        
        Int10000=(int(num/10000))
        num-=(Int10000*10000)
        
        Int1000=(int(num/1000))
        num-=(Int1000*1000)
        
        Int100=(int(num/100))
        num-=(Int100*100)
        
        Int10=(int(num/10))
        num-=(Int10*10)
        
        Int1=(int(num))
        
        IsTen=""
        IsOne=""
        Is01=""
        Is001=""
        Is0001=""
        Is00001=""
        
        if Int100000<1:
            IsTen="0"
        else:
            IsTen=str(Int100000)

        if Int10000<1:
            IsOne="0"
        else:
            IsOne=str(Int10000)
            
        if Int1000<1:
            Is01="0"
        else:
            Is01=str(Int1000)
            
        if Int100<1:
            Is001="0"
        else:
            Is001=str(Int100)
            
        if Int10<1:
            Is0001="0"
        else:
            Is0001=str(Int10)
            
        if Int1<1:
            Is00001="0"
        else:
            Is00001=str(Int1)

        self.EL_LEVEL_V_9.update_gui(text=IsTen)
        self.EL_LEVEL_V_0.update_gui(text=IsOne)
        self.EL_LEVEL_V_01.update_gui(text=Is01)
        self.EL_LEVEL_V_001.update_gui(text=Is001)
        self.EL_LEVEL_V_0001.update_gui(text=Is0001)
        self.EL_LEVEL_V_00001.update_gui(text=Is00001)
        
    def changeAz100P(self):
        self.change_AzmizValue(rate=1000000)

    def changeAz10P(self):
        self.change_AzmizValue(rate=100000)
        
    def changeAz1P(self):
        self.change_AzmizValue(rate=10000)
    
    def changeAz01P(self):
        self.change_AzmizValue(rate=1000)
        
    def changeAz001P(self):
        self.change_AzmizValue(rate=100)
        
    def changeAz0001P(self):
        self.change_AzmizValue(rate=10)
        
    def changeAz00001P(self):
        self.change_AzmizValue(rate=1)
        
#----------------------------------------
    def changeAz100M(self):
        self.change_AzmizValue(rate=1000000,sing="-")

    def changeAz10M(self):
        self.change_AzmizValue(rate=100000,sing="-")
        
    def changeAz1M(self):
        self.change_AzmizValue(rate=10000,sing="-")
    
    def changeAz01M(self):
        self.change_AzmizValue(rate=1000,sing="-")
        
    def changeAz001M(self):
        self.change_AzmizValue(rate=100,sing="-")
        
    def changeAz0001M(self):
        self.change_AzmizValue(rate=10,sing="-")
        
    def changeAz00001M(self):
        self.change_AzmizValue(rate=1,sing="-")

#---------------------------------------

    def changeEl10P(self):
        self.change_ElevationValue(rate=100000)
        
    def changeEl1P(self):
        self.change_ElevationValue(rate=10000)
    
    def changeEl01P(self):
        self.change_ElevationValue(rate=1000)
        
    def changeEl001P(self):
        self.change_ElevationValue(rate=100)
        
    def changeEl0001P(self):
        self.change_ElevationValue(rate=10)
        
    def changeEl00001P(self):
        self.change_ElevationValue(rate=1)

#++++++++++++++++++++++++++++++++++++++++++++


    def changeEl10M(self):
        self.change_ElevationValue(rate=100000,sing="-")
        
    def changeEl1M(self):
        self.change_ElevationValue(rate=10000,sing="-")
    
    def changeEl01M(self):
        self.change_ElevationValue(rate=1000,sing="-")
        
    def changeEl001M(self):
        self.change_ElevationValue(rate=100,sing="-")
        
    def changeEl0001M(self):
        self.change_ElevationValue(rate=10,sing="-")
        
    def changeEl00001M(self):
        self.change_ElevationValue(rate=1,sing="-")

#---------------------------------------------
        
    def change_AzmizValue(self,rate=1,sing="+"):
        global ANTTENA_AZMIZTH
        global AZMIZTH_STR
        if sing=="+" and (ANTTENA_AZMIZTH+rate)<=AZMIZTH_MAX:
            ANTTENA_AZMIZTH+=rate
        if sing=="-" and (ANTTENA_AZMIZTH-rate)>=AZMIZTH_MIN:
            ANTTENA_AZMIZTH-=rate
        self.set_Az(AzV=ANTTENA_AZMIZTH)
               
    def change_ElevationValue(self,rate=1,sing="+"):
        global ANTENA_ELEVATION
        global ELEVATION_STR
        if sing=="+" and (ANTENA_ELEVATION+rate)<=ELEVATION_MAX:
            ANTENA_ELEVATION+=rate
        if sing=="-" and (ANTENA_ELEVATION-rate)>=ELEVATION_MIN:
            ANTENA_ELEVATION-=rate
        self.set_El(ElV=ANTENA_ELEVATION)
        #self.EL_LEVEL_V_F.update_gui(text=ELEVATION_STR)
    
    def printS(self):
        print("HELLOW")
                
    
    def __init__(self, master):
        super().__init__(master)
        # add widgets onto the frame...
        ACU_F=CustomFlame(master=master,sizeX=90,sizeY=76,corner=5,text="",X=50,Y=58)
        ACU_F.update()
        ACU_F.directBody.update()
        #ACU_F.label.update()
        self.Commad_Line=CustomTextBox2(master=ACU_F,text="None",text_size=20,X=90,Y=50,sizeX=30,sizeY=100)
        Azimuth_T= CustomText(master=ACU_F,text="Azmizu",text_size=20,X=16,Y=5,sizeX=10,sizeY=5)
        self.Az_Real_F=CustomText(master=ACU_F,parent=Azimuth_T,text="REAL:",text_size=30,X=-60,Y=180,sizeX=10,sizeY=5)
        self.Az_Real_V_F=CustomText(master=ACU_F,parent=self.Az_Real_F,text="169.12345",text_size=35,X=160,Y=50,sizeX=10,sizeY=5)
        self.Az_Prog_F=CustomText(master=ACU_F,parent=self.Az_Real_F,text="PROG:",text_size=30,X=50,Y=200,sizeX=10,sizeY=5)
        self.Az_Prog_V_F=CustomText(master=ACU_F,parent=self.Az_Prog_F,text="169.12345",text_size=35,X=160,Y=50,sizeX=10,sizeY=5)
        
        self.Az_RePr_F=CustomText(master=ACU_F,parent=self.Az_Prog_F,text="DIFF:",text_size=30,X=50,Y=200,sizeX=10,sizeY=5)
        self.Az_RePr_V_F=CustomText(master=ACU_F,parent=self.Az_RePr_F,text="169.12345",text_size=35,X=160,Y=50,sizeX=10,sizeY=5)
        
        self.Az_SPEED_FF=CustomText(master=ACU_F,parent=self.Az_RePr_F,X=28,Y=350,text="SPEED:",text_size=25,sizeX=5,sizeY=3)
        self.Az_SPEED_S=CustomScaler(master=ACU_F,parent=self.Az_SPEED_FF,sizeX=20,sizeY=4,com=self.change_Az_Speed_F,X=400,Y=150,bg=ACU_F.directBody.cget("bg_color"))
        self.Az_SPEED_F=CustomText(master=ACU_F,parent=self.Az_SPEED_S,X=45,Y=-130,text="0",text_size=25,sizeX=5,sizeY=3)
        self.change_Az_Speed_F(self.Az_SPEED_S.scaler.get())
        
        self.Az_STOW_F=CustomText(master=ACU_F,parent=self.Az_SPEED_FF,X=50,Y=400,text="STOW:",text_size=25,sizeX=5,sizeY=3)
        self.Az_STOW_POS_B=CustomButton(master=ACU_F,parent=self.Az_STOW_F,X=260,Y=40,text="POS",text_size=25,sizeX=6,sizeY=2)
        self.Az_STOW_LOCK_B=CustomButton(master=ACU_F,parent=self.Az_STOW_POS_B,X=200,Y=50,text="LOCK",text_size=25,sizeX=6,sizeY=2)
        self.Az_STOW_REL_B=CustomButton(master=ACU_F,parent=self.Az_STOW_LOCK_B,X=200,Y=50,text="REL",text_size=25,sizeX=6,sizeY=2)
        
        self.Az_Limit_F=CustomText(master=ACU_F,parent=self.Az_STOW_F,X=50,Y=400,text="LIMIT:",text_size=25,sizeX=5,sizeY=3)
        self.Az_Limit_MNUS=CustomText(master=ACU_F,parent=self.Az_Limit_F,X=200,Y=50,text="-",text_size=25,sizeX=1,sizeY=1)
        self.Az_Limit_Unko_MB1=CustomChekButton(master=ACU_F,parent=self.Az_Limit_MNUS,text="",X=500,Y=300,sizeX=1,sizeY=5,text_size=1,texcolor="white")
        self.Az_Limit_Unko_MB2=CustomChekButton(master=ACU_F,parent=self.Az_Limit_Unko_MB1,text="",X=400,Y=50,sizeX=1,sizeY=5,text_size=1,texcolor="white")
        self.Az_Limit_PLUS=CustomText(master=ACU_F,parent=self.Az_Limit_F,X=450,Y=50,text="+",text_size=25,sizeX=1,sizeY=1)
        self.Az_Limit_Unko_PB1=CustomChekButton(master=ACU_F,parent=self.Az_Limit_PLUS,text="",X=500,Y=300,sizeX=1,sizeY=5,text_size=1,texcolor="white")
        self.Az_Limit_Unko_PB2=CustomChekButton(master=ACU_F,parent=self.Az_Limit_Unko_PB1,text="",X=400,Y=50,sizeX=1,sizeY=5,text_size=1,texcolor="white")
        
        self.Az_MODE_F=CustomText(master=ACU_F,parent=self.Az_Limit_F,X=50,Y=400,text="MODE:",text_size=25,sizeX=5,sizeY=3)
        self.Az_MODE_PROG_B=CustomButton(master=ACU_F,parent=self.Az_MODE_F,X=260,Y=40,text="PROG",text_size=25,sizeX=6,sizeY=2)
        self.Az_MODE_MANU_B=CustomButton(master=ACU_F,parent=self.Az_MODE_PROG_B,X=200,Y=50,text="MANU",text_size=25,sizeX=6,sizeY=2)
        self.Az_MODE_STBY_B=CustomButton(master=ACU_F,parent=self.Az_MODE_MANU_B,X=200,Y=50,text="STBY",text_size=25,sizeX=6,sizeY=2)
        
        diff=20
        self.Az_LEVEL_V_3=CustomText(master=ACU_F,parent=self.Az_MODE_F,X=300,Y=500,text="3",text_size=26,sizeX=1,sizeY=2)
        self.Az_LEVEL_V_6=CustomText(master=ACU_F,parent=self.Az_LEVEL_V_3,X=200+diff,Y=50,text="6",text_size=26,sizeX=1,sizeY=2)
        self.Az_LEVEL_V_0=CustomText(master=ACU_F,parent=self.Az_LEVEL_V_6,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        commma=CustomText(master=ACU_F,parent=self.Az_LEVEL_V_0,X=200,Y=50,text=".",text_size=26,sizeX=1,sizeY=2)
        self.Az_LEVEL_V_01=CustomText(master=ACU_F,parent=commma,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        diff=40
        self.Az_LEVEL_V_001=CustomText(master=ACU_F,parent=self.Az_LEVEL_V_01,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        self.Az_LEVEL_V_0001=CustomText(master=ACU_F,parent=self.Az_LEVEL_V_001,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        self.Az_LEVEL_V_00001=CustomText(master=ACU_F,parent=self.Az_LEVEL_V_0001,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        
        a=250
        diff=100
        self.Az_LEVEL_VH_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_V_3,X=20,Y=-90,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz100P)
        self.Az_LEVEL_VT_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VH_F,X=a,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz10P)
        self.Az_LEVEL_VO_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VT_F,X=a,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz1P)
        self.Az_LEVEL_V01_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VO_F,X=a+diff,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz01P)
        diff=0
        self.Az_LEVEL_V001_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_V01_F,X=a+diff,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz001P)
        self.Az_LEVEL_V0001_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_V001_F,X=a+diff,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz0001P)
        self.Az_LEVEL_V00001_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_V0001_F,X=a+diff,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz00001P)
        self.Az_LEVEL_PLUS_B=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VH_F,X=-1*a,Y=50,text="+",text_size=10,sizeX=1,sizeY=1,cornerradius=0)
        b=100
        diff=100
        self.Az_LEVEL_VHM_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_V_3,X=20,Y=320,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz100M)
        self.Az_LEVEL_VTM_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VHM_F,X=a,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz10M)
        self.Az_LEVEL_VOM_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VTM_F,X=a,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz1M)
        self.Az_LEVEL_V01M_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VOM_F,X=a+diff,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz01M)
        diff=0
        self.Az_LEVEL_V001M_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_V01M_F,X=a+diff,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz001M)
        self.Az_LEVEL_V0001M_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_V001M_F,X=a+diff,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz0001M)
        self.Az_LEVEL_V00001M_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_V0001M_F,X=a+diff,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz00001M)
        self.Az_LEVEL_MNUS_B=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VHM_F,X=-1*a,Y=50,text="-",text_size=10,sizeX=1,sizeY=1,cornerradius=0)
        #EL_VERSION---------------------------------------------------------------------------------------------------------------------------------------#
        Elevation_T= CustomText(master=ACU_F,text="Elevation",text_size=20,X=55,Y=5,sizeX=10,sizeY=5)
        self.EL_Real_F=CustomText(master=ACU_F,parent=Elevation_T,text="REAL:",text_size=30,X=-60,Y=180,sizeX=10,sizeY=5)
        self.EL_Real_V_F=CustomText(master=ACU_F,parent=self.EL_Real_F,text="169.12345",text_size=35,X=160,Y=50,sizeX=10,sizeY=5)
        self.EL_Prog_F=CustomText(master=ACU_F,parent=self.EL_Real_F,text="PROG:",text_size=30,X=50,Y=200,sizeX=10,sizeY=5)
        self.EL_Prog_V_F=CustomText(master=ACU_F,parent=self.EL_Prog_F,text="169.12345",text_size=35,X=160,Y=50,sizeX=10,sizeY=5)
        
        self.EL_RePr_F=CustomText(master=ACU_F,parent=self.EL_Prog_F,text="DIFF:",text_size=30,X=50,Y=200,sizeX=10,sizeY=5)
        self.EL_RePr_V_F=CustomText(master=ACU_F,parent=self.EL_RePr_F,text="169.12345",text_size=35,X=160,Y=50,sizeX=10,sizeY=5)
        
        self.EL_SPEED_FF=CustomText(master=ACU_F,parent=self.EL_RePr_F,X=28,Y=350,text="SPEED:",text_size=25,sizeX=5,sizeY=3)
        self.EL_SPEED_S=CustomScaler(master=ACU_F,parent=self.EL_SPEED_FF,sizeX=20,sizeY=5,com=self.change_El_Speed_F,X=400,Y=150)
        self.EL_SPEED_F=CustomText(master=ACU_F,parent=self.EL_SPEED_S,X=45,Y=-130,text="0",text_size=25,sizeX=5,sizeY=3)
        self.change_El_Speed_F(self.EL_SPEED_S.scaler.get())
        
        self.EL_STOW_F=CustomText(master=ACU_F,parent=self.EL_SPEED_FF,X=50,Y=400,text="STOW:",text_size=25,sizeX=5,sizeY=3)
        self.EL_STOW_POS_B=CustomButton(master=ACU_F,parent=self.EL_STOW_F,X=260,Y=40,text="POS",text_size=25,sizeX=6,sizeY=2)
        self.EL_STOW_LOCK_B=CustomButton(master=ACU_F,parent=self.EL_STOW_POS_B,X=200,Y=50,text="LOCK",text_size=25,sizeX=6,sizeY=2)
        self.EL_STOW_REL_B=CustomButton(master=ACU_F,parent=self.EL_STOW_LOCK_B,X=200,Y=50,text="REL",text_size=25,sizeX=6,sizeY=2)
        
        self.EL_Limit_F=CustomText(master=ACU_F,parent=self.EL_STOW_F,X=50,Y=400,text="LIMIT:",text_size=25,sizeX=5,sizeY=3)
        self.EL_Limit_MNUS=CustomText(master=ACU_F,parent=self.EL_Limit_F,X=200,Y=50,text="-",text_size=25,sizeX=1,sizeY=1)
        self.EL_Limit_Unko_MB1=CustomChekButton(master=ACU_F,parent=self.EL_Limit_MNUS,text="",X=500,Y=300,sizeX=1,sizeY=5,text_size=1,texcolor="white")
        self.EL_Limit_Unko_MB2=CustomChekButton(master=ACU_F,parent=self.EL_Limit_Unko_MB1,text="",X=400,Y=50,sizeX=1,sizeY=5,text_size=1,texcolor="white")
        self.EL_Limit_PLUS=CustomText(master=ACU_F,parent=self.EL_Limit_F,X=450,Y=50,text="+",text_size=25,sizeX=1,sizeY=1)
        self.EL_Limit_Unko_PB1=CustomChekButton(master=ACU_F,parent=self.EL_Limit_PLUS,text="",X=500,Y=300,sizeX=1,sizeY=5,text_size=1,texcolor="white")
        self.EL_Limit_Unko_PB2=CustomChekButton(master=ACU_F,parent=self.EL_Limit_Unko_PB1,text="",X=400,Y=50,sizeX=1,sizeY=5,text_size=1,texcolor="white")
        
        self.EL_MODE_F=CustomText(master=ACU_F,parent=self.EL_Limit_F,X=50,Y=400,text="MODE:",text_size=25,sizeX=5,sizeY=3)
        self.EL_MODE_PROG_B=CustomButton(master=ACU_F,parent=self.EL_MODE_F,X=260,Y=40,text="PROG",text_size=25,sizeX=6,sizeY=2)
        self.EL_MODE_MANU_B=CustomButton(master=ACU_F,parent=self.EL_MODE_PROG_B,X=200,Y=50,text="MANU",text_size=25,sizeX=6,sizeY=2)
        self.EL_MODE_STBY_B=CustomButton(master=ACU_F,parent=self.EL_MODE_MANU_B,X=200,Y=50,text="STBY",text_size=25,sizeX=6,sizeY=2)
        
        diff=20
        self.EL_LEVEL_V_9=CustomText(master=ACU_F,parent=self.EL_MODE_F,X=300,Y=500,text="9",text_size=26,sizeX=1,sizeY=2)
        self.EL_LEVEL_V_0=CustomText(master=ACU_F,parent=self.EL_LEVEL_V_9,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        commma=CustomText(master=ACU_F,parent=self.EL_LEVEL_V_0,X=200,Y=50,text=".",text_size=26,sizeX=1,sizeY=2)
        self.EL_LEVEL_V_01=CustomText(master=ACU_F,parent=commma,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        diff=40
        self.EL_LEVEL_V_001=CustomText(master=ACU_F,parent=self.EL_LEVEL_V_01,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        self.EL_LEVEL_V_0001=CustomText(master=ACU_F,parent=self.EL_LEVEL_V_001,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        self.EL_LEVEL_V_00001=CustomText(master=ACU_F,parent=self.EL_LEVEL_V_0001,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        a=250
        d=-200
        self.EL_LEVEL_VT_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_V_9,X=a+d,Y=-90,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl10P)
        self.EL_LEVEL_VO_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_VT_F,X=a,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl1P)
        self.EL_LEVEL_V01_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_VO_F,X=a+100,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl01P)
        self.EL_LEVEL_V001_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_V01_F,X=a,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl001P)
        self.EL_LEVEL_V0001_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_V001_F,X=a,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl0001P)
        self.EL_LEVEL_V00001_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_V0001_F,X=a,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl00001P)
        self.EL_LEVEL_PLUS_B=CustomButton(master=ACU_F,parent=self.EL_LEVEL_VT_F,X=-1*a,Y=50,text="+",text_size=10,sizeX=1,sizeY=1,cornerradius=0)
        b=100
        self.EL_LEVEL_VTM_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_V_9,X=a+d,Y=320,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl10M)
        self.EL_LEVEL_VOM_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_VTM_F,X=a,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl1M)
        self.EL_LEVEL_V01M_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_VOM_F,X=a+100,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl01M)
        self.EL_LEVEL_V001M_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_V01M_F,X=a,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl001M)
        self.EL_LEVEL_V0001M_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_V001M_F,X=a,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl0001M)
        self.EL_LEVEL_V00001M_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_V0001M_F,X=a,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl00001M)
        self.EL_LEVEL_MNUS_B=CustomButton(master=ACU_F,parent=self.EL_LEVEL_VTM_F,X=-1*a,Y=50,text="-",text_size=10,sizeX=1,sizeY=1,cornerradius=0)


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
    COM_STATS_F=None
    QUIET_BUTTON=None
    TEST_ASYNC=None
    ASYNC_LIST=[]
    eASYNC_LIST=[]
    CONECT_B=None
    DisConect_B=None
    LOCK_BUTTOM=None
    SLAVE_MODE_BUTTOM=False
    INDIV_MODE_BUTTOM=True
    OPTICAL_TRAKING_BUTTOM=None
    
    COM_LIST=[]
    SELECTED_COM="NONE"
    SELECTED_COM_ENABLE=False
    
    SLAVE_MODE=False
    INDIV_MODE=True
    AUTO_MODE=True

    def updateTimer(self):
        time.updateAllTime()
        self.YearTime_F.directBody.configure(text=time.Year_Time)
        self.JstTime_F.directBody.configure(text=time.JSTformat)
        self.UctTime_F.directBody.configure(text=time.UTCformat)
        self.LstTime_F.directBody.configure(text=time.LSTformat)
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
    
    def MonitorComPorts(self):
        before_com_list=[]
        before_com_list=(copy.deepcopy(self.COM_LIST))  
        self.COM_LIST=copy.deepcopy(self.ACU_Monitor.BackEnd.getSerialPorts())
        isSelecedComInList=False
        somethingChange=False
        if set(before_com_list)!=set(self.COM_LIST):
            if len(before_com_list)>0 and len(self.COM_LIST)>0:
                if self.SELECTED_COM in self.COM_LIST:
                    index=self.COM_LIST.index(self.SELECTED_COM)
                    first_value=self.COM_LIST[0]
                    selectedComIndex=self.COM_LIST[index]
                    self.COM_LIST[0]=self.SELECTED_COM
                    self.COM_LIST[index]=first_value
            self.COM_F.setValue(value=self.COM_LIST)
        #self.SELECTED_COM=self.COM_F.combbox.get()
        #if self.SELECTED_COM=="Disconected" or self.SELECTED_COM=="":
            #self.COM_STATS_F.label.configure(text="Disconected",bg_color="red")
        '''
        else:
            if self.ACU_Monitor.BackEnd.comTest(PORT=self.SELECTED_COM):
                self.COM_STATS_F.label.configure(text=(self.SELECTED_COM+" is Enable!"),bg_color="#3B8ED0")
            else:
                self.COM_STATS_F.label.configure(text=(self.SELECTED_COM+" is Disable!"),bg_color="red")
        '''
        self.COM_F.after(10,self.MonitorComPorts)
        
    def setSlaveMode(self):
        global IS_INDIVISUAL_MODE
        global IS_SLAVE_MODE
        IS_INDIVISUAL_MODE=False
        IS_SLAVE_MODE=True
        self.SLAVE_MODE_BUTTOM.setDefaultColor()
        self.INDIV_MODE_BUTTOM.setColor(color="gray")

    def setIndivMode(self):
        global IS_INDIVISUAL_MODE
        global IS_SLAVE_MODE
        IS_INDIVISUAL_MODE=True
        IS_SLAVE_MODE=False
        self.INDIV_MODE_BUTTOM.setDefaultColor()
        self.SLAVE_MODE_BUTTOM.setColor(color="gray")
        
        
        
    BUTTON_UNENABLE_COLOR="gray"
    def ApperGUI(self):
        global DEFAULT_WINDOW_HEIGHT
        global DEFAULT_WINDOW_WIDTH
        global SELECTED_COM
        print("ACU_GUI_BEGUN!")
        customtkinter.set_appearance_mode("Dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
        time.updateAllTime()
        
        self.geometry(str(DEFAULT_WINDOW_WIDTH)+"x"+str(DEFAULT_WINDOW_HEIGHT))
        self.resizable(False,False)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        self.protocol('WM_DELETE_WINDOW', self.quit1)
        
        self.JstTime_F = self.setJST(self)
        self.JstTime_F.place(x=165,y=0)#110
        
        self.UctTime_F = self.setUCT(self)
        self.UctTime_F.place(x=368,y=0)#245
        
        self.LstTime_F = self.setLST(self)
        self.LstTime_F.place(x=583,y=0)
        
        self.YearTime_F = self.setYearTime(self)
        self.YearTime_F.place(x=0,y=0)
        self.YearTime_F.after(1000,self.updateTimer)
        
        #X=73,Y=5
        #self.QUIET_BUTTON=CustomButton(master=self,text="EXIT",text_size=27,X=95,Y=4,sizeX=10,sizeY=5,com=self.quit1)
        #X=91,Y=12
        #Place_F = CustomFlame(master=self,text="あわらキャンパス",text_size=30,sizeX=10,sizeY=7,X=90,Y=14)
        
        self.COM_STATS_F=CustomFlame(master=self,text="Unkown",X=80,Y=11,sizeX=16,sizeY=6,text_size=20)
        self.COM_F=CustomCombobox(master=self,value=self.ACU_Monitor.BackEnd.getSerialPorts(),X=81,Y=4,sizeX=18,sizeY=6,text_size=27)
        self.COM_LIST=(copy.deepcopy(self.ACU_Monitor.BackEnd.getSerialPorts()))
        #self.SELECTED_COM=self.COM_F.combbox.get()
        self.COM_F.after(10,self.MonitorComPorts)
        
        #self.CONECT_B=CustomFlame(master=self,text="Conect",text_size=20,X=50,Y=50,sizeX=30,sizeY=6)
        
        self.DisConect_B=CustomFlame(master=self,text="Conect",text_size=20,X=50,Y=50,sizeX=30,sizeY=6)

        self.SLAVE_MODE_BUTTOM=CustomButton(master=self,text="SLAVE",X=40,Y=11,sizeX=10,sizeY=5,cornerradius=5,text_size=30,com=self.setSlaveMode)
        self.INDIV_MODE_BUTTOM=CustomButton(master=self,text="INDIV",X=55,Y=11,sizeX=10,sizeY=5,cornerradius=5,text_size=30,com=self.setIndivMode)
        self.setIndivMode()
        
        self.LOCK_BUTTOM=CustomButton(master=self,text="LOCK",X=5,Y=11,sizeX=10,sizeY=5,cornerradius=5,text_size=30)
        self.OPTICAL_TRAKING_BUTTOM=CustomChekButton(master=self,text="OPTICAL TRAKING MODE",X=20,Y=13,sizeX=10,sizeY=5,text_size=15,texcolor="white")
        ACU=LCU_Controller(master=self)
    

        #self.COM_F.combbox.configure(command=self.ThrowSelectedCom2Backend)
        
        #textbox=CustomTextBox(master=self,text="FUCKYOU!",text_size=30,sizeX=30,sizeY=30)
        
        
        
        #self.COM_Monitor=threading.Thread(target=self.ThrowSelectedCom2Backend)
        #self.COM_Monitor.start()
        
        self.enableAsync()
        
        
    
        #button=CustomButton(master=self,text="HELLO!",text_size=30,X=50,Y=50,com=self.selected)
        

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
    