import customtkinter
import getTime as time
import ACUbackend as BackEnd
import threading
import time as Timer
import copy
import math

FONT_TYPE = "Segoe UI"
DEFAULT_WINDOW_WIDTH=1110
DEFAULT_WINDOW_HEIGHT=600
SELECTED_COM="NONE"

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
    def is_integer_num(self,n):
        if isinstance(n, int):
            return True
        if isinstance(n, float):
            return n.is_integer()
        return False
    def setGUI(self):
        self.directBody = customtkinter.CTkLabel(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey)
        self.directBody.grid(row=0, column=0, padx=10)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def UPDATEGUI(self):
        self.directBody.configure(text=self.text)
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
        if type(self.master) is CustomFlame:
            mas_win_width=self.master.sizex
            mas_win_height=self.master.sizey
        if self.master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        scw = mas_win_width*self.X/100
        sch = mas_win_height*self.Y/100
        if self.parent is not None:
            scw,sch=self.parent.getWorldpos(self.X,self.Y)
        sw = mas_win_width*self.sizeX/100
        sh = mas_win_height*self.sizeY/100
        if text=="Conect":   
            print("w1="+str(sw))
        self.sizex=sw
        self.sizey=sh
        if self.inited is False:
            self.setGUI()
        else:
            self.UPDATEGUI()
        self.update()
        w=self.directBody.winfo_reqwidth()
        h=self.directBody.winfo_reqheight()
        scw-=(w/2)
        sch-=(h/2)
        self.place(x=scw,y=sch)
        self.posx=scw
        self.posx=sch
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
        
class CustomFlame(customtkinter.CTkFrame):
    posx=0
    posy=0
    sizex=0
    sizey=0
    def setDisable(self):
        self.label.configure(state=customtkinter.DISABLED)
    def setEnable(self):
        self.label.configure(state=customtkinter.NORMAL)
    def getWorldpos(self,x=50,y=50):
        X=x/100
        Y=y/100
        X=self.sizex*X
        Y=self.sizey*Y
        return (self.posx+X),(self.posy+Y)
    def __init__(self, master, text="none_text",text_size=11,corner=-1,curb=10,X=50,Y=50,sizeX=20,sizeY=20,parent=None):
        super().__init__(master)
        '''
        X,Yは0~1の間をとる
        '''
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
        scw = mas_win_width*X/100
        sch = mas_win_height*Y/100
        if parent is not None:
            scw,sch=parent.getWorldpos(X,Y)
        sw = mas_win_width*sizeX/100
        sh = mas_win_height*sizeY/100
        if text=="Conect":   
            print("w="+str(sw))
        self.sizex=sw
        self.sizey=sh
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
        self.posx=scw
        self.posx=sch
        
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

class CustomButton(customtkinter.CTkFrame):
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
    def __init__(self, master, text="none_text",text_size=11,sizeX=20,sizeY=20,X=0,Y=0,texcolor="white",fg="#3B8ED0",hg="red",com=None,cornerradius=10,parent=None):
        super().__init__(master)
        # add widgets onto the frame...
        self.update()
        mas_win_width=master.winfo_reqwidth()
        mas_win_height=master.winfo_reqheight()
        if type(master) is CustomFlame:
            mas_win_width=master.sizex
            mas_win_height=master.sizey
        if master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
        print("CustomButton1:"+str(mas_win_width))
        print("CustomButton2:"+str(mas_win_height))
        scw = mas_win_width*sizeX/100
        sch = mas_win_height*sizeY/100
        sw = mas_win_width*X/100
        sh = mas_win_height*Y/100
        if parent is not None:
            sw,sh=parent.getWorldpos(X,Y)
        if com is None:
            self.button1  = customtkinter.CTkButton(self,text=text, font=(FONT_TYPE, text_size),width=scw,height=sch,corner_radius=cornerradius,text_color=texcolor,fg_color=fg,hover_color=hg)
        else:
            self.button1  = customtkinter.CTkButton(self,text=text, font=(FONT_TYPE, text_size),width=scw,height=sch,corner_radius=cornerradius,text_color=texcolor,fg_color=fg,command=com,hover_color=hg)
        self.button1.grid(row=0, column=0, padx=0)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        self.update()
        self.button1.update()
        w=self.button1.winfo_reqwidth()
        h=self.button1.winfo_reqheight()
        sw-=(w/2)
        sh-=(h/2)
        self.place(x=sw,y=sh)

class CustomButton2(CustomBase):
    texcolor="white"
    fg="#3B8ED0"
    hg="red"
    com=None
    cornerradius=10
    def selfUpdateValue(self,texcolor="white",fg="#3B8ED0",hg="red",com=None,cornerradius=10):
        if texcolor!="none":
            self.text=text
        self.fg=fg
        self.hg=hg
        if com is not None:
            self.com=com
        if self.is_integer_num(cornerradius):
            self.cornerradius=cornerradius
    def UPDATEGUI(self):
        super(CustomButton2,self).UPDATEGUI()
        if self.com is not None:
            self.directBody.configure(text=self.text,command=self.com)
        else:
            self.directBody.configure(text=self.text)
    def setGUI(self):
        super(CustomButton2,self).setGUI()
        if self.com is not None:
            self.directBody  = customtkinter.CTkButton(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.texcolor,fg_color=self.fg,command=self.com,hover_color=self.hg)
        else:
            self.directBody  = customtkinter.CTkButton(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.texcolor,fg_color=self.fg,hover_color=self.hg)
        self.directBody.grid(row=0, column=0, padx=0)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master, text="none_text",text_size=11,X=50,Y=50,sizeX=20,sizeY=20,parent=None,texcolor="white",fg="#3B8ED0",hg="red",com=None,cornerradius=10):
        super().__init__(master, text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent)
        self.selfUpdateValue(texcolor=texcolor,fg=fg,hg=hg,com=com,cornerradius=cornerradius)
        self.update_gui(text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY)

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

class CustomFlame5(CustomBase):
    def setGUI(self):
        super(CustomFlame5,self).setGUI()
        self.directBody = customtkinter.CTkLabel(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey)
        self.directBody.grid(row=0, column=0, padx=10)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master, text="none_text",text_size=11,corner=-1,curb=10,X=50,Y=50,sizeX=20,sizeY=20,parent=None):
        super().__init__(master, text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent)
        self.update_gui(text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY)
        
class CustomText(CustomBase):
    def UPDATEGUI(self):
        super(CustomText,self).UPDATEGUI()
        self.directBody.configure(text=self.text)
    def setGUI(self):
        super(CustomText,self).setGUI()
        self.directBody = customtkinter.CTkLabel(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,bg_color=self.master.cget("bg_color"),fg_color=self.master.cget("fg_color"))
        self.directBody.grid(row=0, column=0, padx=0)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master, text="none_text",text_size=11,X=50,Y=50,sizeX=20,sizeY=20,parent=None):
        super().__init__(master, text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent)
        self.update_gui(text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY)

class LCU_Controller(customtkinter.CTkFrame):
    '''
    LCUのコントローラーを設置するクラス
    '''
    Az_Real_F=None
    Az_Prog_F=None
    Az_RePr_F=None
    Az_SPEED_S=None
    Az_SPEED_F=None
    Az_STOW=None
    
    def change_Az_Speed_F(self,str):
        self.Az_SPEED_F.update_gui(text=str)
    
    def __init__(self, master,win_height=400,win_width=750,win_posx=0,win_posy=0):
        super().__init__(master)
        # add widgets onto the frame...
        ACU_F=CustomFlame(master=master,sizeX=50,sizeY=30,corner=5,text="",X=30)
        ACU_F.update()
        ACU_F.label.update()
        Azimuth_T= CustomFlame(master=ACU_F,text="Azmizu",text_size=20,X=50,Y=50)
        self.Az_SPEED_S=CustomScaler(master=ACU_F,sizeX=30,sizeY=20,com=self.change_Az_Speed_F)
        self.Az_SPEED_F=CustomText(master=ACU_F,parent=self.Az_SPEED_S,X=50,Y=-50,text="0",text_size=25)
        self.change_Az_Speed_F(self.Az_SPEED_S.scaler.get())
        
        #self=CustomCheckBox(master=ACU_F,text="TEST")

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
    
    COM_LIST=[]
    SELECTED_COM="NONE"
    SELECTED_COM_ENABLE=False
    
    SLAVE_MODE=False
    INDIV_MODE=True
    AUTO_MODE=True

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
        
        
    def ApperGUI(self):
        global DEFAULT_WINDOW_HEIGHT
        global DEFAULT_WINDOW_WIDTH
        global SELECTED_COM
        print("ACU_GUI_BEGUN!")
        customtkinter.set_appearance_mode("green")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
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
        
        self.CONECT_B=CustomFlame(master=self,text="Conect",text_size=20,X=80,Y=21,sizeX=30,sizeY=6)
        
        self.DisConect_B=CustomFlame5(master=self,text="Conect",text_size=20,X=80,Y=30,sizeX=30,sizeY=6)

        ACU=LCU_Controller(master=self,win_posx=100,win_posy=60)
    

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
    