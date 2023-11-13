import customtkinter
import getTime as time
import ACUbackend as BackEnd
import threading
import time as Timer
import copy
import math
import os
from customtkinter import filedialog

from PIL import Image,ImageTk


FONT_TYPE = "x14y24pxHeadUpDaisy"
DEFAULT_WINDOW_WIDTH=1110
DEFAULT_WINDOW_HEIGHT=600
RADIO_BUTTOM_NUM=0
ANTTENA_AZMIZTH=3600000
ANTTENA_AZMIZTH_PROG=3600000
AZMIZTH_STR="3 6 0. 0 0 0 0"
AZMIZTH_MAX=3600000
AZMIZTH_MIN=0
ANTENA_ELEVATION=900000
ANTENA_ELEVATION_PROG=900000
ELEVATION_STR="9 0. 0 0 0 0"
ELEVATION_MAX=900000
ELEVATION_MIN=0

IS_SLAVE_MODE=False
IS_INDIVISUAL_MODE=True

STOW_IS_POS=False
STOW_IS_REL=False
STOW_IS_LOCK=True

AZ_IS_STBY=False
AZ_IS_PROG=True
AZ_IS_MAN=False

EL_IS_STBY=False
EL_IS_PROG=True
EL_IS_MAN=False

IS_COMPLETALLY_CONECTED=FalseNotConect=True
Conect=False
AnttenaMoving=False

WINDOW_X_POS=0
WINDOW_Y_POS=0

IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

GUI_APP=None

NotConect=True
Conect=False
AnttenaMoving=False
SELECTED_COM="NONE"

def SetWindowPos(y=0,x=0):
    WINDOW_X_POS=x
    WINDOW_Y_POS=y

class CustomBase(customtkinter.CTkFrame):
    image=None
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
    bd_width=0
    bd_color="gray74"
    fg_color="gray50"
    bg_color="none"
    textcolor="black"
    disableColor="gray10"
    cornerradius=10
    AppearWindow=None
    CarsolisOn=False
    isCrasolMode=False
    
    #GIFようの変数
    isGifMode=False
    duration = []  # フレーム表示間隔
    frames = []  # 読み込んだGIFの画像フレーム
    executeFrames=[]
    last_frame_index = None
    frame_index_counter=0
    gif_time=60
    
    #ステータス管理変数
    Stats=True
    Stats_mode="Strong"
    
    
    def setDeath(self):
        if self.directBody is not None:
            self.directBody.destroy()
    
    def load_gifFrames(self,path="hogehoge.gif"):#使わないが一応年の為、残しておく
        if isinstance(path, str):
            global IMAGE_PATH
            img = Image.open(os.path.join(IMAGE_PATH, path))
            frames = []

        frame_index = 0
        try:
            while True:
                frames.append(ImageTk.PhotoImage(img.copy()))
                img.seek(frame_index)
                frame_index += 1
        except EOFError:
            self.frames = frames
            self.last_frame_index = frame_index
            
    def load_gifFrames2(self,path="hogehoge.gif"):
        if self.getStats4GIF():
            if isinstance(path, str):
                global IMAGE_PATH
                img = Image.open(os.path.join(IMAGE_PATH, path))
                frames = []

            frame_index = 0
            try:
                while True:#frames.append(ImageTk.PhotoImage(img.copy()))
                    frames.append(customtkinter.CTkImage(light_image=ImageTk.getimage(ImageTk.PhotoImage(img.copy())),
                                                        dark_image=ImageTk.getimage(ImageTk.PhotoImage(img.copy())), size=(self.sizex, self.sizey)))
                    img.seek(frame_index)
                    frame_index += 1
            except EOFError:
                self.executeFrames = frames
                self.last_frame_index = frame_index
            
    def getStats(self):
        return self.Stats
    
    def getStats4GIF(self):
        return self.getStats() and self.isGifMode
            
    def setGifFrames(self):
        global IMAGE_PATH
        if self.getStats4GIF():
            img=self.executeFrames[self.frame_index_counter]
            self.directBody.configure(image=img)
            self.frame_index_counter += 1
            #最終フレームになったらフレームを０に戻す  ImageTk.getimage( imgtk )
            if self.frame_index_counter > self.last_frame_index:
                self.frame_index_counter = 0
            self.directBody.after(self.gif_time,self.setGifFrames)

    def setCarsolon(self,event):
        self.CarsolisOn=True
    def setCarsolOut(self,event):
        self.CarsolisOn=False
    def setStats(self,stats=None,mode="Strong"):
        BeforeStats=self.Stats
        self.Stats=stats
        change=BeforeStats ^ self.Stats
        if stats is not None:
            if stats is True and change:
                if mode is "Strong":
                    self.setNormal()
                    self.frame_index_counter=0
                    self.setGifFrames()
                elif mode is "OnlyColor":
                    self.setnormalColor()
            if stats is False and change:
                if mode is "Strong":
                    self.setDisable()
                elif mode is "OnlyColor":
                    self.setdisableColor()
    def isWindowisCustom(self):
        if self.AppearWindow is None:
            return False
        else:
            return True
    def getWindow(self):
        if self.AppearWindow is None:
            return self
        elif self.AppearWindow is "void":
            return None
        else:
            return self.AppearWindow.Window
            
    def disable_child(self):
        children = self.winfo_children()
        for child in children:
            if isinstance(child,CustomBase):
                child.setDisable()
    def enable_child(self):
        children = self.winfo_children()
        for child in children:
            if isinstance(child,CustomBase):
                child.setNormal()
    def setdisableColor(self):
        self.directBody.configure(fg_color=self.disableColor)
    def setnormalColor(self):
        self.directBody.configure(fg_color=self.fg_color)
        if self.bd_width>0:
            self.directBody.configure(border_color=self.bd_color)
    def setDisable(self):
        self.directBody.configure(state="disabled")
        self.setdisableColor()
        self.disable_child()
    def setNormal(self):
        self.directBody.configure(state="normal")
        self.setnormalColor()
        self.enable_child()
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
        self.directBody.configure(self.getWindow())
        #self.directBody.configure(text=self.text)
    def update_gui(self,image_name="none",gif_name="none",gif_time=1.1,text="none_text",text_size=1.1,X=1.1,Y=1.1,sizeX=1.1,sizeY=1.1,bd_width=1.1,bd_color="none",fg="none",bg="none",textcolor="none"):
        global IMAGE_PATH
        #if image_name!="none":
            #global IMAGE_PATH
            #self.image = customtkinter.CTkImage(light_image=Image.open(os.path.join(IMAGE_PATH, image_name)),
                                                # dark_image=Image.open(os.path.join(IMAGE_PATH, image_name)), size=(20, 20))
        if gif_name!="none":
            self.image = customtkinter.CTkImage(light_image=Image.open(os.path.join(IMAGE_PATH, "kousin.png")),
                                                 dark_image=Image.open(os.path.join(IMAGE_PATH, "kousin.png")), size=(20, 20))
            self.isGifMode=True
        else:
            self.isGifMode=False
        if text!="none_text":
            self.text=text
        if self.is_integer_num(gif_time):
            self.gif_time=gif_time
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
        if self.is_integer_num(bd_width):
            self.bd_width=bd_width
        if bd_color!="none":
            self.bd_color=bd_color
        if fg!="none":
            self.fg_color=fg
        if bg!="none":
            self.bg_color=bg
        if textcolor!="none":
            self.textcolor=textcolor
        if self.bd_color=="none":
            self.bd_color=self.bg
            self.bd_width=0
            
        if self.master is None:
            return
        
        self.update()
        mas_win_width=self.master.winfo_reqwidth()
        mas_win_height=self.master.winfo_reqheight()
        if isinstance(self.master,CustomBase):
            mas_win_width=self.master.sizex
            mas_win_height=self.master.sizey
            if self.bg_color=="none":
                self.bg_color=self.master.fg_color
        if self.master.master is None:
            mas_win_width=DEFAULT_WINDOW_WIDTH
            mas_win_height=DEFAULT_WINDOW_HEIGHT
            if self.bg_color=="none":
                self.bg_color=self.master.cget("fg_color")
                if isinstance(self.AppearWindow,CustomWindow):
                    self.bg_color=self.AppearWindow.Window.cget("fg_color")
            if isinstance(self.AppearWindow,CustomWindow):
                mas_win_width=self.AppearWindow.sizeX
                mas_win_height=self.AppearWindow.sizeY
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

        w=self.sizex
        h=self.sizey
        if image_name!="none":
            self.image = customtkinter.CTkImage(light_image=Image.open(os.path.join(IMAGE_PATH, image_name)),
                                                 dark_image=Image.open(os.path.join(IMAGE_PATH, image_name)), size=(20, 20))
        if self.inited is False:
            self.setGUI()
        else:
            self.UPDATEGUI()
        self.update()
        scw-=(w/2)
        sch-=(h/2)
        self.posx=scw
        self.posy=sch
        if isinstance(self.AppearWindow,CustomWindow):
            self.directBody.place(x=self.posx,y=self.posy)
        else:
            self.place(x=scw,y=sch)
        self.inited=True
        self.load_gifFrames2(path=gif_name+".gif")
        #self.finalGifInit()
        self.setGifFrames()
        if image_name!="none":
            img = customtkinter.CTkImage(light_image=Image.open(os.path.join(IMAGE_PATH, image_name)),
                                                 dark_image=Image.open(os.path.join(IMAGE_PATH, image_name)), size=(self.sizex, self.sizey))
            self.directBody.configure(image=img)
    def getWorldpos(self,x=50,y=50):
        X=x/100
        Y=y/100
        X=self.sizex*X
        Y=self.sizey*Y
        return (self.posx+X),(self.posy+Y)
    def __init__(self, master, carsol=False,text="none_text",text_size=11,X=50,Y=50,sizeX=20,sizeY=20,parent=None,putWindow=None):
        super().__init__(master)
        self.isCrasolMode=carsol
        self.master=master
        self.parent=parent
        self.AppearWindow=putWindow

class CustomRadioButtom(CustomBase):
    selfNum=0
    textcolor="white"
    fg="#3B8ED0"
    hg="red"
    def selfUpdateValue(self,textcolor="white",fg="#3B8ED0",hg="red",com=None,cornerradius=10):
        if textcolor!="none":
            self.textcolor=textcolor
        self.fg=fg
        self.hg=hg
    def setGUI(self):
        super(CustomRadioButtom,self).setGUI()
        self.directBody  = customtkinter.CTkRadioButton(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,text_color=self.textcolor,fg_color=self.fg,hover_color=self.hg,bg_color=self.master.cget("fg_color"))
        self.directBody.grid(row=0, column=0, padx=0)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master, text="none_text",text_size=11,X=50,Y=50,sizeX=20,sizeY=20,parent=None,textcolor="white",fg="#3B8ED0",hg="red"):
        super().__init__(master, text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent)
        global RADIO_BUTTOM_NUM
        RADIO_BUTTOM_NUM+=1
        self.selfNum=RADIO_BUTTOM_NUM
        self.selfUpdateValue(textcolor=textcolor,fg=fg,hg=hg)
        self.update_gui(text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY)

class CustomScaler(customtkinter.CTkFrame):
    scaler=None
    posx=0
    posy=0
    sizex=0
    sizey=0
    st=0
    goal=0
    ScaleWidth=0

    def getWorldpos(self,x=50,y=50):
        X=x/100
        Y=y/100
        X=self.sizex*X
        Y=self.sizey*Y
        return (self.posx+X),(self.posy+Y)
    def __init__(self, master,text_size=30,sizeX=13,sizeY=5,X=50,Y=50,textcolor="white",bg="#0D1015",fg="#0D1015",cornerradius=10,com=None,first_value=0,end_value=100,parent=None):
        super().__init__(master)
        # add widgets onto the frame...
        self.update()
        self.st=first_value
        self.goal=end_value
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
    def setReadonly(self):
        print("")
        #self.directBody.configure(state='disabled')
    def Insert(self,text):
        self.directBody.insert("0.0",str(self.num)+":"+text+"\n")
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
    hg="red"
    com=None
    cornerradius=10
    pussingButtomMode=False
    changeColor="gray"
    ButtomStats=False #Falseが選択されていないとき、Trueが選択されていると
    timermode=False
    def setdisableColor(self):
        super(CustomButton,self).setdisableColor()
        if self.timermode:
            self.directBody.configure(text_color=self.textcolor)
        else:
            self.directBody.configure(text_color="gray")
            if self.bd_width>0:
                self.directBody.configure(border_color="gray50")
    def setnormalColor(self):
        super(CustomButton,self).setnormalColor()
        self.directBody.configure(text_color=self.textcolor)
    def setTextColor(self,event):
        if self.pussingButtomMode is True and self.text!="none":
            self.ButtomStats=not (self.ButtomStats)
            if self.ButtomStats is True:
                self.directBody.configure(hover_color=self.fg_color)
                self.directBody.configure(text_color=self.fg_color)
                self.directBody.configure(fg_color=self.hg)
            if self.ButtomStats is False:
                self.directBody.configure(hover_color=self.hg)
                self.directBody.configure(text_color=self.textcolor)
                self.directBody.configure(fg_color=self.fg_color)
    def setDefaultColor(self):
        self.directBody.configure(fg_color="#3B8ED0")
        self.fg="#3B8ED0"
    def setColor(self,color="red"):
        self.directBody.configure(fg_color=color)
    def selfUpdateValue(self,textcolor="white",fg="#3B8ED0",hg="red",com=None,cornerradius=10,bg="#3B8ED0"):
        if textcolor!="none":
            self.textcolor=textcolor
        self.hg=hg
        if com is not None:
            self.com=com
        if self.is_integer_num(cornerradius):
            self.cornerradius=cornerradius
    def UPDATEGUI(self):
        super(CustomButton,self).UPDATEGUI()
    def setGUI(self):
        super(CustomButton,self).setGUI()
        if self.timermode:
            self.hg=self.fg_color
        if self.isGifMode and self.com is not None:
            self.directBody  = customtkinter.CTkButton(master=self.getWindow(),border_width=self.bd_width,hover_color=self.hg,border_color=self.bd_color,image=self.image,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.textcolor,fg_color=self.fg_color,command=self.com,bg_color=self.bg_color)
        elif self.isGifMode and self.com is None:
            self.directBody  = customtkinter.CTkButton(master=self.getWindow(),border_width=self.bd_width,hover_color=self.hg,border_color=self.bd_color,image=self.image,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.textcolor,fg_color=self.fg_color,bg_color=self.bg_color)
        elif self.com is not None and self.image is not None:
            self.directBody  = customtkinter.CTkButton(master=self.getWindow(),border_width=self.bd_width,hover_color=self.hg,border_color=self.bd_color,image=self.image,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.textcolor,fg_color=self.fg_color,command=self.com,bg_color=self.bg_color)
        elif self.com is not None:
            self.directBody  = customtkinter.CTkButton(master=self.getWindow(),border_width=self.bd_width,hover_color=self.hg,border_color=self.bd_color,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.textcolor,fg_color=self.fg_color,command=self.com,bg_color=self.bg_color)
        elif self.image is not None:
            self.directBody  = customtkinter.CTkButton(master=self.getWindow(),border_width=self.bd_width,hover_color=self.hg,border_color=self.bd_color,image=self.image,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.textcolor,fg_color=self.fg_color,bg_color=self.bg_color)
        else:
            self.directBody  = customtkinter.CTkButton(master=self.getWindow(),border_width=self.bd_width,hover_color=self.hg,border_color=self.bd_color,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.textcolor,fg_color=self.fg_color,bg_color=self.bg_color)
        

        if  not self.isWindowisCustom():
            self.directBody.grid(row=0, column=0, padx=0,pady=0)
            self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        
        if self.isCrasolMode:
            self.directBody.bind("<Enter>", self.setCarsolon)
            self.directBody.bind("<Leave>", self.setCarsolOut)

        if self.pussingButtomMode is True:#ほとんど使わない。と言うか非推奨　何故なら見にくいから
            self.directBody.bind("<Button-1>",self.setTextColor)
            self.directBody.bind("<Enter>",self.setTextColor)
            self.directBody.bind("<Leave>",self.setTextColor)
    def __init__(self,master,gif_name="none",gif_time=1.1,carsol=False,putWindow=None,Timermode=False,pussingButtomMode=False,image_name="none", text="none_text",text_size=11,X=50,Y=50,sizeX=20,sizeY=20,parent=None,textcolor="black",fg="gray50",hg="gray74",bg="none",com=None,cornerradius=10,bd_width=0,bd_color="none"):
        super().__init__(master,carsol=carsol, putWindow=putWindow,text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent)
        self.pussingButtomMode=pussingButtomMode
        self.timermode=Timermode
        self.selfUpdateValue(textcolor=textcolor,fg=fg,hg=hg,com=com,cornerradius=cornerradius,bg=bg)
        self.update_gui(text=text,gif_name=gif_name,gif_time=gif_time,image_name=image_name,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,bd_color=bd_color,bd_width=bd_width,bg=bg,fg=fg,textcolor=textcolor)

class CustomChekButton(CustomButton):
    def setGUI(self):
        super(CustomChekButton,self).setGUI()
        if self.com is not None:
            self.directBody  = customtkinter.CTkCheckBox(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.textcolor,fg_color=self.fg_color,command=self.com,hover_color=self.hg,bg_color=self.bg_color)
        else:
            self.directBody  = customtkinter.CTkCheckBox(self,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,text_color=self.textcolor,fg_color=self.fg_color,hover_color=self.hg,bg_color=self.bg_color)
        self.directBody.grid(row=0, column=0, padx=0)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master, text="none_text",text_size=11,X=50,Y=50,sizeX=20,sizeY=20,parent=None,textcolor="black",fg="#3B8ED0",hg="red",com=None,cornerradius=10):
        super().__init__(master, text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent,textcolor=textcolor,fg=fg,hg=hg,com=com,cornerradius=cornerradius)

class CustomCombobox2 (customtkinter.CTkFrame):
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
    def __init__(self, master,text_size=30,sizeX=13,sizeY=5,X=50,Y=50,textcolor="white",fg="#3B8ED0",cornerradius=10,value=["None1","None2","None3","None4"],com=None,parent=None):
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

class CustomCombobox(CustomBase):
    corner=-1
    curb=10
    tex_color=""
    value=["none"]
    def setValue(self,value=["something"]):
        self.value=value
    def UPDATEGUI(self):
        super(CustomCombobox,self).UPDATEGUI()
        self.directBody.configure(values=self.value,fg_color=self.fg)
    def setGUI(self):
        super(CustomCombobox,self).setGUI()
        self.directBody = customtkinter.CTkComboBox(master=self.getWindow(),border_width=self.bd_width,border_color=self.bd_color,font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.corner,fg_color=self.fg_color,values=self.value)
        self.directBody.grid(row=0, column=0, padx=0)#self.curb
        #self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master, putWindow=None,text="none_text",text_size=11,corner=-1,curb=10,X=50,Y=50,sizeX=20,sizeY=20,parent=None,bg="none",fg="gray50",value=["None1"],bd_width=0,bd_color="none"):
        super().__init__(master=master,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent,putWindow=putWindow)
        self.corner=corner
        self.curb=curb
        self.value=value
        self.update_gui(text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,bd_color=bd_color,bd_width=bd_width,bg=bg,fg=fg)

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
    def UPDATEGUI(self):
        super(CustomFlame,self).UPDATEGUI()
        self.directBody.configure(text=self.text)
    def setGUI(self):
        super(CustomFlame,self).setGUI()
        if self.isGifMode:
            self.directBody  = customtkinter.CTkLabel(master=self.getWindow(),image=self.image,text=self.text, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,corner_radius=self.cornerradius,fg_color=self.fg_color,bg_color=self.bg_color)
        elif self.image is not None:
            self.directBody = customtkinter.CTkLabel(master=self.getWindow(),text=self.text,corner_radius=self.cornerradius, image=self.image, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,bg_color=self.bg_color,fg_color=self.fg_color)
        else:
            self.directBody = customtkinter.CTkLabel(master=self.getWindow(),text=self.text,corner_radius=self.cornerradius, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,bg_color=self.bg_color,fg_color=self.fg_color)
        self.directBody.grid(row=0, column=0, padx=0)
        self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master,gif_name="none",gif_time=1.1,carsol=False,image_name="none",cornerradius=10 ,text="none_text",text_size=11,corner=-1,curb=10,X=50,Y=50,sizeX=20,sizeY=20,parent=None,bg="none",fg="gray50",bd_width=0,bd_color="none"):
        super().__init__(master=master,carsol=carsol,text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent)
        self.corner=corner
        self.curb=curb
        self.cornerradius=cornerradius
        self.update_gui(text=text,gif_name=gif_name,gif_time=gif_time,image_name=image_name,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,bd_color=bd_color,bd_width=bd_width,bg=bg,fg=fg)
        
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
        self.directBody = customtkinter.CTkLabel(self.getWindow(),text=self.text,text_color=self.textcolor, font=(FONT_TYPE, self.text_size),width=self.sizex,height=self.sizey,bg_color=self.bg_color,fg_color=self.bg_color)
        self.directBody.grid(row=0, column=0, padx=0)
        #self.grid(row=0, column=0, padx=0, pady=0, sticky="w")
    def __init__(self, master,putWindow=None,textcolor="DarkSlateGray2", text="none_text",text_size=11,X=50,Y=50,sizeX=20,sizeY=20,parent=None):
        super().__init__(master, text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,parent=parent,putWindow=putWindow)
        self.update_gui(text=text,text_size=text_size,X=X,Y=Y,sizeX=sizeX,sizeY=sizeY,textcolor=textcolor)

class CustomWindow(customtkinter.CTkFrame):
    sizeX=0
    sizeY=0
    posX=0
    posY=0
    ismodel=False
    Window=None
    title=""
    def __init__(self, master,sizex=100,sizey=100,posx=0,posy=0,isModal=False,title="none"):
        super().__init__(master)
        self.sizeX=sizex
        self.sizeY=sizey
        self.posX=posx
        self.posY=posy
        self.ismodel=isModal
        self.title=title
        self.setGUI()
    def setGUI(self):
        self.Window=customtkinter.CTkToplevel(self)
        self.Window.title(self.title)   # ウィンドウタイトル
        self.Window.geometry(str(self.sizeX)+"x"+str(self.sizeY)+"+"+str(self.posX)+"+"+str(self.posY))
        self.Window.configure(fg_color="#0D1015")
        self.Window.update()# ウィンドウサイズ(幅x高さ)fg_color="#0D1015"
        if self.ismodel:
            global GUI_APP
            # モーダルにする設定
            self.Window.grab_set()        # モーダルにする
            self.Window.focus_set()       # フォーカスを新しいウィンドウをへ移す
            self.Window.transient(self.master)   # タスクバーに表示しない

            # ダイアログが閉じられるまで待つ
           # GUI_APP.wait_window(self.Window)  

class AnotherWIndowUIC():
    AnotherWindowUI=None
    Stats=None
    def __init__(self,UI=None,Stats=None):
        self.setUI(UI=UI)
        self.Stats=Stats
        self.setupdate()
    def setUIEnable(self):
        self.AnotherWindowUI.setNormal()
    def setUIDisable(self):
        self.AnotherWindowUI.setDisable()
    def setUI(self,UI=None):
        if UI is not None:
            self.AnotherWindowUI=UI
            if self.Stats is False:
                self.setUIDisable()
            elif self.Stats is True:
                self.setUIEnable()
    def setupdate(self):
        if self.AnotherWindowUI is not None:
            if self.Stats:
                self.setUIEnable()
            else:
                self.setUIDisable()
    def setStats(self,stats=None):
        self.Stats=stats

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

    Az_mode=None
    El_mode=None

    def getCutFloat(self,num=0):
        return round(num, 1)

    def updateAz_num(self,pnum=0,nnum=0,work_time=0,speed=0,mode="prog"):
        global ANTTENA_AZMIZTH
        global ANTTENA_AZMIZTH_PROG
        if mode is "manu":
            pnum=ANTTENA_AZMIZTH/10000
        t=('{:1.05f}'.format(pnum))
        #print(t)
        self.Az_Prog_V_F.update_gui(text=t)
        t=('{:1.05f}'.format(nnum))
        self.Az_Real_V_F.update_gui(text=t)
        t2=('{:1.04f}'.format(pnum))
        ANTTENA_AZMIZTH_PROG=float(t2)
        
        ANTTENA_AZMIZTH_PROG*=10000

        self.Az_RePr_V_F.update_gui(text=('{:1.05f}'.format(pnum-nnum)))
        Speed=speed/work_time
        self.change_Az_Speed_F(str=str(round(Speed, 1)))
        self.Az_SPEED_S.scaler.set(Speed)
        if mode is "prog":
            self.set_Az(AzV=ANTTENA_AZMIZTH_PROG)
        if mode is "manu" and self.Az_mode is "prog":
            self.set_Az(AzV=ANTTENA_AZMIZTH)
        self.Az_mode=mode


    def updateEl_num(self,pnum=0,nnum=0,work_time=0,speed=0,mode="prog"):
        global ANTENA_ELEVATION
        global ANTENA_ELEVATION_PROG
        modeIsShanged=(mode!=self.El_mode)
        if modeIsShanged and mode=="stby":
            self.set_El(ElV=ANTENA_ELEVATION)
        if mode is "manu" or mode is "stby":
            pnum=ANTENA_ELEVATION/10000
        t=('{:1.05f}'.format(pnum))
        self.EL_Prog_V_F.update_gui(text=t)
        t=('{:1.05f}'.format(nnum))
        self.EL_Real_V_F.update_gui(text=t)
        t2=('{:1.04f}'.format(pnum))
        ANTENA_ELEVATION_PROG=float(t2)
        ANTENA_ELEVATION_PROG*=10000
        self.EL_RePr_V_F.update_gui(text=('{:1.05f}'.format(pnum-nnum)))
        Speed=speed/work_time
        
        self.EL_SPEED_S.scaler.set(Speed)
        self.change_El_Speed_F(str=str(round(Speed, 1)))
        if mode is "prog":
            self.set_El(ElV=ANTENA_ELEVATION_PROG)
            print("")
        if mode is "manu" and self.El_mode is "prog":
            self.set_El(ElV=ANTENA_ELEVATION)
            print("")
        self.El_mode=mode
        #print("EL GUI")
    
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
        #print("I1000000="+str(Int1000000))
        num-=(Int1000000*1000000)
        Int100000=(int(num/100000))
        #Xprint("I100000="+str(Int100000))
        
        num-=(Int100000*100000)
        Int10000=(int(num/10000))
        #print("I10000="+str(Int10000))

        num-=(Int10000*10000)
        Int1000=(int(num/1000))
        #print("I1000="+str(Int1000))
    
        num-=(Int1000*1000)
        Int100=(int(num/100))
        #print("I100="+str(Int100))
        
        num-=(Int100*100)
        Int10=(int(num/10))
        #print("I10="+str(Int10))
        
        num-=(Int10*10)
        Int1=(int(num))
        #print("I1="+str(Int1))

        
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
        '''
        self.Az_LEVEL_V_001.update_gui(text=Is001)
        self.Az_LEVEL_V_0001.update_gui(text=Is0001)
        self.Az_LEVEL_V_00001.update_gui(text=Is00001)
        '''
        
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
        '''
        self.EL_LEVEL_V_001.update_gui(text=Is001)
        self.EL_LEVEL_V_0001.update_gui(text=Is0001)
        self.EL_LEVEL_V_00001.update_gui(text=Is00001)
        '''
        
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
        
    def change_AzmizValue(self,rate=1,sing="+",mode="prog"):
        global ANTTENA_AZMIZTH
        global AZMIZTH_STR
        if sing=="+" and (ANTTENA_AZMIZTH+rate)<=AZMIZTH_MAX:
            ANTTENA_AZMIZTH+=rate
        if sing=="-" and (ANTTENA_AZMIZTH-rate)>=AZMIZTH_MIN:
            ANTTENA_AZMIZTH-=rate
        self.set_Az(AzV=ANTTENA_AZMIZTH)
               
    def change_ElevationValue(self,rate=1,sing="+",mode="prog"):
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

    def setEL_LEVEL(self,frag=True):
        if frag:
            self.EL_LEVEL_MNUS_B.setNormal()
            self.EL_LEVEL_PLUS_B.setNormal()
            self.EL_LEVEL_V01_F.setNormal()
            self.EL_LEVEL_VTM_F.setNormal()
            self.EL_LEVEL_V01M_F.setNormal()
            self.EL_LEVEL_VO_F.setNormal()
            self.EL_LEVEL_VOM_F.setNormal()
            self.EL_LEVEL_VT_F.setNormal()
        else:
            self.EL_LEVEL_MNUS_B.setDisable()
            self.EL_LEVEL_PLUS_B.setDisable()
            self.EL_LEVEL_V01_F.setDisable()
            self.EL_LEVEL_VTM_F.setDisable()
            self.EL_LEVEL_V01M_F.setDisable()
            self.EL_LEVEL_VO_F.setDisable()
            self.EL_LEVEL_VOM_F.setDisable()
            self.EL_LEVEL_VT_F.setDisable()

    def setAZ_LEVEL(self,frag=True):
        if frag:
            self.Az_LEVEL_MNUS_B.setNormal()
            self.Az_LEVEL_PLUS_B.setNormal()
            self.Az_LEVEL_VH_F.setNormal()
            self.Az_LEVEL_VTM_F.setNormal()
            self.Az_LEVEL_VHM_F.setNormal()
            self.Az_LEVEL_VO_F.setNormal()
            self.Az_LEVEL_VOM_F.setNormal()
            self.Az_LEVEL_VT_F.setNormal()
            self.Az_LEVEL_V01_F.setNormal()
            self.Az_LEVEL_V01M_F.setNormal()
        else:
            self.Az_LEVEL_MNUS_B.setDisable()
            self.Az_LEVEL_PLUS_B.setDisable()
            self.Az_LEVEL_VH_F.setDisable()
            self.Az_LEVEL_VTM_F.setDisable()
            self.Az_LEVEL_VHM_F.setDisable()
            self.Az_LEVEL_VO_F.setDisable()
            self.Az_LEVEL_VOM_F.setDisable()
            self.Az_LEVEL_VT_F.setDisable()
            self.Az_LEVEL_V01_F.setDisable()
            self.Az_LEVEL_V01M_F.setDisable()

    
    def setAzProg(self):
        global AZ_IS_MAN
        global AZ_IS_STBY
        global AZ_IS_PROG
        global ANTTENA_AZMIZTH_PROG
        AZ_IS_MAN=False
        AZ_IS_STBY=False
        AZ_IS_PROG=True
        self.Az_MODE_PROG_B.setnormalColor()
        self.Az_MODE_MANU_B.setdisableColor()
        self.Az_MODE_STBY_B.setdisableColor()
        self.setAZ_LEVEL(frag=False)
        self.set_Az(AzV=ANTTENA_AZMIZTH_PROG)

    def setAzMan(self):
        global AZ_IS_MAN
        global AZ_IS_STBY
        global AZ_IS_PROG
        global ANTTENA_AZMIZTH
        AZ_IS_MAN=True
        AZ_IS_STBY=False
        AZ_IS_PROG=False
        self.Az_MODE_PROG_B.setdisableColor()
        self.Az_MODE_MANU_B.setnormalColor()
        self.Az_MODE_STBY_B.setdisableColor()
        self.setAZ_LEVEL(frag=True)
        self.set_Az(AzV=ANTTENA_AZMIZTH)

    def setAzStby(self):
        global AZ_IS_MAN
        global AZ_IS_STBY
        global AZ_IS_PROG
        global ANTTENA_AZMIZTH
        AZ_IS_MAN=False
        AZ_IS_STBY=True
        AZ_IS_PROG=False
        self.Az_MODE_PROG_B.setdisableColor()
        self.Az_MODE_MANU_B.setdisableColor()
        self.Az_MODE_STBY_B.setnormalColor()
        self.setAZ_LEVEL(frag=True)
        self.set_Az(AzV=ANTTENA_AZMIZTH)

    def setELProg(self):
        global EL_IS_MAN
        global EL_IS_STBY
        global EL_IS_PROG
        global ANTENA_ELEVATION_PROG
        EL_IS_MAN=False
        EL_IS_STBY=False
        EL_IS_PROG=True
        self.EL_MODE_PROG_B.setnormalColor()
        self.EL_MODE_MANU_B.setdisableColor()
        self.EL_MODE_STBY_B.setdisableColor()
        self.setEL_LEVEL(frag=False)
        self.set_El(ElV=ANTENA_ELEVATION_PROG)

    def setELMan(self):
        global EL_IS_MAN
        global EL_IS_STBY
        global EL_IS_PROG
        global ANTENA_ELEVATION
        EL_IS_MAN=True
        EL_IS_STBY=False
        EL_IS_PROG=False
        self.EL_MODE_PROG_B.setdisableColor()
        self.EL_MODE_MANU_B.setnormalColor()
        self.EL_MODE_STBY_B.setdisableColor()
        self.setEL_LEVEL(frag=True)
        self.set_El(AzV=ANTENA_ELEVATION)

    def setELStby(self):
        global EL_IS_MAN
        global EL_IS_STBY
        global EL_IS_PROG
        global ANTENA_ELEVATION
        EL_IS_MAN=False
        EL_IS_STBY=True
        EL_IS_PROG=False
        self.EL_MODE_PROG_B.setdisableColor()
        self.EL_MODE_MANU_B.setdisableColor()
        self.EL_MODE_STBY_B.setnormalColor()
        self.setEL_LEVEL(frag=True)
        self.set_El(AzV=ANTENA_ELEVATION)

    def setIndivMode(self):
        self.Az_MODE_MANU_B.setDisable()
        self.Az_MODE_PROG_B.setDisable()
        self.Az_MODE_STBY_B.setDisable()
        self.EL_MODE_MANU_B.setDisable()
        self.EL_MODE_PROG_B.setDisable()
        self.EL_MODE_STBY_B.setDisable()
        

    def setSlaveMode(self):
        self.Az_MODE_MANU_B.setNormal()
        self.Az_MODE_PROG_B.setNormal()
        self.Az_MODE_STBY_B.setNormal()
        self.EL_MODE_MANU_B.setNormal()
        self.EL_MODE_PROG_B.setNormal()
        self.EL_MODE_STBY_B.setNormal()
        self.setAzProg()
        self.setELProg()
        
        

    def __init__(self, master):
        super().__init__(master)
        # add widgets onto the frame...
        bd="DarkSlateGray2"
        ACU_F=CustomFlame(master=master,sizeX=90,sizeY=76,corner=0,text="",X=50,Y=81,fg="#0D1015",cornerradius=0)
        ACU_F.update()
        ACU_F.directBody.update()
        #ACU_F.label.update()
        self.Commad_Line=CustomTextBox2(master=ACU_F,text="None",text_size=20,X=90,Y=50,sizeX=30,sizeY=100)
        self.Commad_Line.setReadonly()
        Azimuth_T= CustomText(master=ACU_F,text="Azmizu",text_size=20,X=16,Y=5,sizeX=10,sizeY=5)
        self.Az_Real_F=CustomText(master=ACU_F,parent=Azimuth_T,text="REAL:",text_size=30,X=-60,Y=180,sizeX=10,sizeY=5)
        self.Az_Real_V_F=CustomText(master=ACU_F,parent=self.Az_Real_F,text="169.12345",text_size=35,X=160,Y=50,sizeX=10,sizeY=5)
        self.Az_Prog_F=CustomText(master=ACU_F,parent=self.Az_Real_F,text="PROG:",text_size=30,X=50,Y=200,sizeX=10,sizeY=5)
        self.Az_Prog_V_F=CustomText(master=ACU_F,parent=self.Az_Prog_F,text="169.12345",text_size=35,X=160,Y=50,sizeX=10,sizeY=5)
        
        self.Az_RePr_F=CustomText(master=ACU_F,parent=self.Az_Prog_F,text="DIFF:",text_size=30,X=50,Y=200,sizeX=10,sizeY=5)
        self.Az_RePr_V_F=CustomText(master=ACU_F,parent=self.Az_RePr_F,text="169.12345",text_size=35,X=160,Y=50,sizeX=10,sizeY=5)
        
        self.Az_SPEED_FF=CustomText(master=ACU_F,parent=self.Az_RePr_F,X=28,Y=350,text="SPEED:",text_size=25,sizeX=5,sizeY=3)
        self.Az_SPEED_S=CustomScaler(master=ACU_F,parent=self.Az_SPEED_FF,sizeX=20,sizeY=4,com=self.change_Az_Speed_F,X=430,Y=100,first_value=-2,end_value=2)
        self.Az_SPEED_F=CustomText(master=ACU_F,parent=self.Az_SPEED_S,X=45,Y=-130,text="0",text_size=25,sizeX=5,sizeY=3)
        self.change_Az_Speed_F(self.Az_SPEED_S.scaler.get())
        
        self.Az_MODE_F=CustomText(master=ACU_F,parent=self.Az_SPEED_FF,X=50,Y=400,text="MODE:",text_size=25,sizeX=5,sizeY=3)
        self.Az_MODE_PROG_B=CustomButton(master=ACU_F,parent=self.Az_MODE_F,X=260,Y=40,text="PROG",text_size=25,sizeX=6,sizeY=2,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setAzProg)
        self.Az_MODE_MANU_B=CustomButton(master=ACU_F,parent=self.Az_MODE_PROG_B,X=200,Y=50,text="MANU",text_size=25,sizeX=6,sizeY=2,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setAzMan)
        self.Az_MODE_STBY_B=CustomButton(master=ACU_F,parent=self.Az_MODE_MANU_B,X=200,Y=50,text="STBY",text_size=25,sizeX=6,sizeY=2,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setAzStby)
        
        diff=20
        self.Az_LEVEL_V_3=CustomText(master=ACU_F,parent=self.Az_MODE_F,X=300,Y=500,text="3",text_size=26,sizeX=1,sizeY=2)
        self.Az_LEVEL_V_6=CustomText(master=ACU_F,parent=self.Az_LEVEL_V_3,X=200+diff,Y=50,text="6",text_size=26,sizeX=1,sizeY=2)
        self.Az_LEVEL_V_0=CustomText(master=ACU_F,parent=self.Az_LEVEL_V_6,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        commma=CustomText(master=ACU_F,parent=self.Az_LEVEL_V_0,X=200,Y=50,text=".",text_size=26,sizeX=1,sizeY=2)
        self.Az_LEVEL_V_01=CustomText(master=ACU_F,parent=commma,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        diff=40
        
        a=250
        diff=100
        self.Az_LEVEL_VH_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_V_3,X=20,Y=-150,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz100P,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        self.Az_LEVEL_VT_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VH_F,X=a,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz10P,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        self.Az_LEVEL_VO_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VT_F,X=a,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz1P,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        self.Az_LEVEL_V01_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VO_F,X=a+diff,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz01P,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        diff=0
        self.Az_LEVEL_PLUS_B=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VH_F,X=-1*a,Y=50,text="+",text_size=10,sizeX=1,sizeY=1,cornerradius=0,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        b=100
        diff=100
        self.Az_LEVEL_VHM_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_V_3,X=20,Y=300,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz100M,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        self.Az_LEVEL_VTM_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VHM_F,X=a,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz10M,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        self.Az_LEVEL_VOM_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VTM_F,X=a,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz1M,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        self.Az_LEVEL_V01M_F=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VOM_F,X=a+diff,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeAz01M,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        diff=0
        self.Az_LEVEL_MNUS_B=CustomButton(master=ACU_F,parent=self.Az_LEVEL_VHM_F,X=-1*a,Y=50,text="-",text_size=10,sizeX=1,sizeY=1,cornerradius=0,fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        #EL_VERSION---------------------------------------------------------------------------------------------------------------------------------------#
        Elevation_T= CustomText(master=ACU_F,text="Elevation",text_size=20,X=55,Y=5,sizeX=10,sizeY=5)
        self.EL_Real_F=CustomText(master=ACU_F,parent=Elevation_T,text="REAL:",text_size=30,X=-60,Y=180,sizeX=10,sizeY=5)
        self.EL_Real_V_F=CustomText(master=ACU_F,parent=self.EL_Real_F,text="169.12345",text_size=35,X=160,Y=50,sizeX=10,sizeY=5)
        self.EL_Prog_F=CustomText(master=ACU_F,parent=self.EL_Real_F,text="PROG:",text_size=30,X=50,Y=200,sizeX=10,sizeY=5)
        self.EL_Prog_V_F=CustomText(master=ACU_F,parent=self.EL_Prog_F,text="169.12345",text_size=35,X=160,Y=50,sizeX=10,sizeY=5)
        
        self.EL_RePr_F=CustomText(master=ACU_F,parent=self.EL_Prog_F,text="DIFF:",text_size=30,X=50,Y=200,sizeX=10,sizeY=5)
        self.EL_RePr_V_F=CustomText(master=ACU_F,parent=self.EL_RePr_F,text="169.12345",text_size=35,X=160,Y=50,sizeX=10,sizeY=5)
        
        self.EL_SPEED_FF=CustomText(master=ACU_F,parent=self.EL_RePr_F,X=28,Y=350,text="SPEED:",text_size=25,sizeX=5,sizeY=3)
        self.EL_SPEED_S=CustomScaler(master=ACU_F,parent=self.EL_SPEED_FF,sizeX=20,sizeY=4,com=self.change_El_Speed_F,X=430,Y=100,first_value=-2,end_value=2)
        self.EL_SPEED_F=CustomText(master=ACU_F,parent=self.EL_SPEED_S,X=45,Y=-130,text="0",text_size=25,sizeX=5,sizeY=3)
        self.change_El_Speed_F(self.EL_SPEED_S.scaler.get())

        self.EL_MODE_F=CustomText(master=ACU_F,parent=self.EL_SPEED_FF,X=50,Y=400,text="MODE:",text_size=25,sizeX=5,sizeY=3)
        self.EL_MODE_PROG_B=CustomButton(master=ACU_F,parent=self.EL_MODE_F,X=260,Y=40,text="PROG",text_size=25,sizeX=6,sizeY=2,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setELProg)
        self.EL_MODE_MANU_B=CustomButton(master=ACU_F,parent=self.EL_MODE_PROG_B,X=200,Y=50,text="MANU",text_size=25,sizeX=6,sizeY=2,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setELMan)
        self.EL_MODE_STBY_B=CustomButton(master=ACU_F,parent=self.EL_MODE_MANU_B,X=200,Y=50,text="STBY",text_size=25,sizeX=6,sizeY=2,textcolor="DarkSlateGray2",fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setELStby)
        

        diff=20
        self.EL_LEVEL_V_9=CustomText(master=ACU_F,parent=self.EL_MODE_F,X=300,Y=500,text="9",text_size=26,sizeX=1,sizeY=2)
        self.EL_LEVEL_V_0=CustomText(master=ACU_F,parent=self.EL_LEVEL_V_9,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        commma=CustomText(master=ACU_F,parent=self.EL_LEVEL_V_0,X=200,Y=50,text=".",text_size=26,sizeX=1,sizeY=2)
        self.EL_LEVEL_V_01=CustomText(master=ACU_F,parent=commma,X=200+diff,Y=50,text="0",text_size=26,sizeX=1,sizeY=2)
        diff=40
        a=250
        d=-200
        self.EL_LEVEL_VT_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_V_9,textcolor="DarkSlateGray2",X=a+d,Y=-150,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl10P,fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        self.EL_LEVEL_VO_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_VT_F,textcolor="DarkSlateGray2",X=a,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl1P,fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        self.EL_LEVEL_V01_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_VO_F,textcolor="DarkSlateGray2",X=a+100,Y=50,text="↑",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl01P,fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        self.EL_LEVEL_PLUS_B=CustomButton(master=ACU_F,parent=self.EL_LEVEL_VT_F,textcolor="DarkSlateGray2",X=-1*a,Y=50,text="+",text_size=10,sizeX=1,sizeY=1,cornerradius=0,fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        b=100
        self.EL_LEVEL_VTM_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_V_9,textcolor="DarkSlateGray2",X=a+d,Y=300,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl10M,fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        self.EL_LEVEL_VOM_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_VTM_F,textcolor="DarkSlateGray2",X=a,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl1M,fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        self.EL_LEVEL_V01M_F=CustomButton(master=ACU_F,parent=self.EL_LEVEL_VOM_F,textcolor="DarkSlateGray2",X=a+100,Y=50,text="↓",text_size=10,sizeX=1,sizeY=1,cornerradius=0,com=self.changeEl01M,fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)        
        self.EL_LEVEL_MNUS_B=CustomButton(master=ACU_F,parent=self.EL_LEVEL_VTM_F,textcolor="DarkSlateGray2",X=-1*a,Y=50,text="-",text_size=10,sizeX=1,sizeY=1,cornerradius=0,fg=ACU_F.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        self.setAzProg()
        self.setELProg()

class ACU_GUI(customtkinter.CTk):
#+++++++++++++++++++++++++++++++++++++
    ACU_Monitor=None
    NAME="TEST"
    YearTime_F=None
    JstTime_F=None
    UctTime_F=None
    LstTime_F=None
    LOC_F=None
    COM_F=None
    Scaler=None
    COM_Monitor=None
    COM_STATS_F=None
    BACKFROUND_F=None
    QUIET_BUTTON=None
    TEST_ASYNC=None
    ASYNC_LIST=[]
    eASYNC_LIST=[]
    CONECT_B=None
    DisConect_B=None
    SLAVE_MODE_BUTTOM=False
    INDIV_MODE_BUTTOM=True
    
    UPDATE_COM_BUTTOM=None
    SETTING_BUTTOM=None
    
    CONECT_BUTTOM=None
    DISCONECT_BUTTOM=None
    
    COM_LIST=[]
    SELECTED_COM="NONE"
    SELECTED_COM_ENABLE=False
    
    SLAVE_MODE=False
    INDIV_MODE=True
    AUTO_MODE=True
    
    CONECT_BUTTOM_STATS=False
    DISCONECT_BUTTOM_STATS=False

    STOW_F=None
    STOW_POS_B=None
    STOW_LOCK_B=None
    STOW_REL_B=None
    
    MOUCE_POS_X=0
    MOUCE_POS_Y=0
    
    LCU=None
#+++++++++++++++++++++++++++++++++++++
#----------------------------------------------------

    '''    
    AGUIBG=None
    AGUISettingButtom=None
    
    AntenaBG=None
    
    MyPCpic=None
    Antenapic=None
    Antenagif=None
    Acupic=None
    
    
    Antena2Acugif=None
    
    Acu2Mypcgif=None
    Mypc2Acugif=None
    Mypc2AcuDis=None
    '''
    def getStats(self):
        global IS_SLAVE_MODE
        global IS_INDIVISUAL_MODE

        global STOW_IS_POS
        global STOW_IS_REL
        global STOW_IS_LOCK

        global AZ_IS_STBY
        global AZ_IS_PROG
        global AZ_IS_MAN

        global EL_IS_STBY
        global EL_IS_PROG
        global EL_IS_MAN
        
        return IS_SLAVE_MODE,IS_INDIVISUAL_MODE,STOW_IS_POS,STOW_IS_REL,STOW_IS_LOCK,AZ_IS_STBY,AZ_IS_PROG,AZ_IS_MAN,EL_IS_STBY,EL_IS_PROG,EL_IS_MAN
    
    Acu2MypcDis=None
    def Setnotconect2Antenna(self):
        self.Antenapic.setStats(stats=False)
        self.Acupic.setStats(stats=False)
        self.Antena2Acugif.setStats(stats=False)
        self.Acu2Mypcgif.setStats(stats=False)
        self.Mypc2Acugif.setStats(stats=False)
        self.Mypc2AcuDis=CustomFlame(master=self.AGUIBG,parent=self.Mypc2Acugif,image_name="batu.png",fg="transparent",text="",X=43,Y=50,sizeX=6,sizeY=20,cornerradius=0)
        self.Acu2MypcDis=CustomFlame(master=self.AGUIBG,parent=self.Acu2Mypcgif,image_name="batu.png",fg="transparent",text="",X=43,Y=50,sizeX=6,sizeY=20,cornerradius=0)
        if isinstance(self.SLAVE_MODE_BUTTOM,CustomBase):
            self.SLAVE_MODE_BUTTOM.setStats(stats=False)
            self.INDIV_MODE_BUTTOM.setStats(stats=False)
            self.STOW_POS_B.setStats(stats=False)
            self.STOW_LOCK_B.setStats(stats=False)
            self.STOW_REL_B.setStats(stats=False)
        
    def Setconect2Antenna(self):
        self.Antenapic.setStats(stats=True)
        self.Acupic.setStats(stats=True)
        self.Antena2Acugif.setStats(stats=True)
        self.Acu2Mypcgif.setStats(stats=True)
        self.Mypc2Acugif.setStats(stats=True)
        if self.Mypc2AcuDis is not None:
            self.Mypc2AcuDis.setDeath()
        if self.Acu2Mypcgif is not None:
            self.Acu2Mypcgif.setDeath()
        if isinstance(self.SLAVE_MODE_BUTTOM,CustomBase):
            self.SLAVE_MODE_BUTTOM.setStats(stats=True)
            self.INDIV_MODE_BUTTOM.setStats(stats=True)
            self.STOW_POS_B.setStats(stats=True)
            self.STOW_LOCK_B.setStats(stats=True)
            self.STOW_REL_B.setStats(stats=True)    
            
    def SetAntennaMoving(self):
        self.Antenapic=CustomFlame(master=self.AntenaBG,gif_name="movingnew2",fg="transparent",gif_time=100,text="",X=20,Y=50,sizeX=38,sizeY=80,cornerradius=0)
        self.Acupic.setStats(stats=True)
        self.Antena2Acugif.setStats(stats=True)
        self.Acu2Mypcgif.setStats(stats=True)
        self.Mypc2Acugif.setStats(stats=True)
        if self.Mypc2AcuDis is not None:
            self.Mypc2AcuDis.setDeath()
        if self.Acu2Mypcgif is not None:
            self.Acu2Mypcgif.setDeath()
        if isinstance(self.SLAVE_MODE_BUTTOM,CustomBase):
            self.SLAVE_MODE_BUTTOM.setStats(stats=True)
            self.INDIV_MODE_BUTTOM.setStats(stats=True)
            self.STOW_POS_B.setStats(stats=True)
            self.STOW_LOCK_B.setStats(stats=True)
            self.STOW_REL_B.setStats(stats=True)
        

    def getMode(self):
        global IS_INDIVISUAL_MODE
        global IS_SLAVE_MODE
        return IS_INDIVISUAL_MODE,IS_SLAVE_MODE

    def getAzmode(self):
        global AZ_IS_STBY
        global AZ_IS_PROG
        global AZ_IS_MAN
        return AZ_IS_STBY,AZ_IS_PROG,AZ_IS_MAN
    
    def getElmode(self):
        global EL_IS_STBY
        global EL_IS_PROG
        global EL_IS_MAN
        return EL_IS_STBY,EL_IS_PROG,EL_IS_MAN
    
    def getAzManualRot(self):
        global ANTTENA_AZMIZTH
        return ANTTENA_AZMIZTH
    
    def getElManualRot(self):
        global ANTENA_ELEVATION
        return ANTENA_ELEVATION
    
    def updateTimerbybackend(self,Year_Time="0000.00.00",JSTformat="JST:00:00:00",UTCformat="UTC:00:00:00",LSTformat="LST:00:00:00",UTC="09"):
        self.YearTime_F.directBody.configure(text=Year_Time,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)
        self.JstTime_F.directBody.configure(text=JSTformat,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)
        self.UctTime_F.directBody.configure(text=UTCformat,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)
        self.LstTime_F.directBody.configure(text=LSTformat,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)
        self.LOC_F.directBody.configure(text=UTC,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)

    def updateTimer(self):
        time.updateAllTime()
        self.YearTime_F.directBody.configure(text=time.Year_Time,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)
        self.JstTime_F.directBody.configure(text=time.JSTformat,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)
        self.UctTime_F.directBody.configure(text=time.UTCformat,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)
        self.LstTime_F.directBody.configure(text=time.LSTformat,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)
        self.YearTime_F.after(1000,self.updateTimer)
        
    def setupdateTimer(self):
        self.YearTime_F.directBody.configure(text=time.Year_Time,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)
        self.JstTime_F.directBody.configure(text=time.JSTformat,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)
        self.UctTime_F.directBody.configure(text=time.UTCformat,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)
        self.LstTime_F.directBody.configure(text=time.LSTformat,fg_color=self.cget("fg_color"),text_color=self.YearTime_F.textcolor)

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
        
    def setSlaveModeFlag(self):
        global IS_INDIVISUAL_MODE
        global IS_SLAVE_MODE
        IS_INDIVISUAL_MODE=False
        IS_SLAVE_MODE=True
        
    def setSlaveMode(self):
        self.setSlaveModeFlag()
        self.setConectModeUI()
        self.LCU.setSlaveMode()
        #self.Mypc2AcuDis=CustomFlame(master=self.AGUIBG,parent=self.Mypc2Acugif,image_name="batu.png",fg="#131519",text="",X=50,Y=50,sizeX=10,sizeY=10,cornerradius=0)
        #self.Acu2Mypcgif=CustomFlame(master=self.AGUIBG,gif_name="rightStripe",gif_time=40,fg=AGUIBGcolor,text="",X=60,Y=80,sizeX=50,sizeY=10,cornerradius=0)
        #self.Mypc2Acugif
        #LCU_Setting
        
    def setIndivModeFlag(self):
        global IS_INDIVISUAL_MODE
        global IS_SLAVE_MODE
        IS_INDIVISUAL_MODE=True
        IS_SLAVE_MODE=False
    
    #OnlyColor
    def setConectModeUI(self):
        global IS_INDIVISUAL_MODE
        global IS_SLAVE_MODE   
        self.INDIV_MODE_BUTTOM.setStats(stats=IS_INDIVISUAL_MODE,mode="OnlyColor")
        self.SLAVE_MODE_BUTTOM.setStats(stats=IS_SLAVE_MODE,mode="OnlyColor")
        if IS_INDIVISUAL_MODE:
            self.Mypc2Acugif.setStats(stats=False)
            self.Mypc2AcuDis=CustomFlame(master=self.AGUIBG,parent=self.Mypc2Acugif,image_name="batu.png",fg="transparent",text="",X=43,Y=50,sizeX=6,sizeY=20,cornerradius=0)
        if IS_SLAVE_MODE:
            self.Mypc2Acugif.setStats(stats=True)
            if self.Mypc2AcuDis is not None:
                self.Mypc2AcuDis.setDeath()
        

    def setIndivMode(self):
        self.setIndivModeFlag()
        self.setConectModeUI()
        self.LCU.setIndivMode()
        #if self.Mypc2AcuDis is not None:
           # self.Mypc2AcuDis.setDeath()

    def setControllMode2Button(self):
        global IS_INDIVISUAL_MODE
        global IS_SLAVE_MODE
        self.SLAVE_MODE_BUTTOM.setStats(stats=IS_SLAVE_MODE,mode="OnlyColor")
        self.INDIV_MODE_BUTTOM.setStats(stats=IS_INDIVISUAL_MODE,mode="OnlyColor")
        
    def setStowRELFlag(self):
        global STOW_IS_POS
        global STOW_IS_LOCK
        global STOW_IS_REL
        STOW_IS_POS=False
        STOW_IS_REL=True
        STOW_IS_LOCK=False

    def setStowREL(self):
        self.setStowRELFlag()
        self.setStowMode2Button()
        
    def setStowLOCKFlag(self):
        global STOW_IS_POS
        global STOW_IS_LOCK
        global STOW_IS_REL
        STOW_IS_POS=False
        STOW_IS_REL=False
        STOW_IS_LOCK=True

    def setStowLOCK(self):
        self.setStowLOCKFlag()
        self.setStowMode2Button()
        
    def setStowPosFlag(self):
        global STOW_IS_POS
        global STOW_IS_LOCK
        global STOW_IS_REL
        STOW_IS_POS=True
        STOW_IS_REL=False
        STOW_IS_LOCK=False

    def setStowPos(self):
        self.setStowPosFlag()
        self.setStowMode2Button()
        
    def setStowMode2Button(self):
        global STOW_IS_POS
        global STOW_IS_LOCK
        global STOW_IS_REL
        self.STOW_POS_B.setStats(stats=STOW_IS_POS,mode="OnlyColor")
        self.STOW_LOCK_B.setStats(stats=STOW_IS_LOCK,mode="OnlyColor")
        self.STOW_REL_B.setStats(stats=STOW_IS_REL,mode="OnlyColor")
        
    def setConectStats(self):
        self.CONECT_BUTTOM_STATS=True
        
    def setDIsconectStats(self):
        self.DISCONECT_BUTTOM_STATS=True
        self.COM_F.value=self.ACU_Monitor.BackEnd.getSerialPorts()
        self.COM_F.UPDATEGUI()
        self.COM_F.setStats(stats=True)
        
    BUTTON_UNENABLE_COLOR="gray"

    def updateComList(self):
        self.COM_F.setValue(value=self.ACU_Monitor.BackEnd.getSerialPorts())
        self.COM_F.update_gui()
            
    def AppearAntennaSettingWindow(self):
        bd="DarkSlateGray2"
        x,y=self.GetWindowPos()
        global NotConect
        global Conect
        global AnttenaMoving
        window=CustomWindow(master=self,sizex=400,sizey=400,posx=x+1110,posy=y,isModal=True)
        
        modestring=CustomText(putWindow=window,master=self,text="CONTROLL MODE",text_size=30,X=10,Y=5,sizeX=20,sizeY=6)
        self.SLAVE_MODE_BUTTOM=CustomButton(putWindow=window,master=self,parent=modestring,text="SLAVE",textcolor="DarkSlateGray2",X=50,Y=180,sizeX=10,sizeY=5,cornerradius=0,text_size=30,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setSlaveMode)
        self.INDIV_MODE_BUTTOM=CustomButton(putWindow=window,master=self,parent=self.SLAVE_MODE_BUTTOM,text="INDIV",textcolor="DarkSlateGray2",X=380,Y=50,sizeX=10,sizeY=5,cornerradius=0,text_size=30,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setIndivMode)

        self.STOW_F=CustomText(master=self,putWindow=window,text="STOW MODE",text_size=30,X=16,Y=25,sizeX=30,sizeY=6)
        self.STOW_POS_B=CustomButton(putWindow=window,master=self,parent=self.STOW_F,text="POS",textcolor="DarkSlateGray2",X=50,Y=180,sizeX=10,sizeY=5,cornerradius=0,text_size=30,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setStowPos)
        self.STOW_LOCK_B=CustomButton(putWindow=window,master=self,parent=self.STOW_POS_B,text="LOCK",textcolor="DarkSlateGray2",X=220,Y=50,sizeX=10,sizeY=5,cornerradius=0,text_size=30,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setStowLOCK)
        self.STOW_REL_B=CustomButton(putWindow=window,master=self,parent=self.STOW_LOCK_B,text="REL",textcolor="DarkSlateGray2",X=250,Y=50,sizeX=10,sizeY=5,cornerradius=0,text_size=30,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setStowREL)

        if NotConect:
            self.SLAVE_MODE_BUTTOM.setStats(stats=False)
            self.INDIV_MODE_BUTTOM.setStats(stats=False)
            self.STOW_POS_B.setStats(stats=False)
            self.STOW_LOCK_B.setStats(stats=False)
            self.STOW_REL_B.setStats(stats=False)
        
        if (not NotConect) and Conect or AnttenaMoving:
            self.setConectModeUI()
            self.setStowMode2Button() 
            
        
        if "COM" in  self.SELECTED_COM or "com" in  self.SELECTED_COM:
            self.COM_F=CustomCombobox(master=self,putWindow=window,value=[self.SELECTED_COM],X=30,Y=60,sizeX=28,sizeY=6,text_size=27,fg=self.cget("fg_color"),bd_width=1,bd_color=bd)
            self.COM_F.setStats(stats=False)
        else:
            self.COM_F=CustomCombobox(master=self,putWindow=window,value=self.ACU_Monitor.BackEnd.getSerialPorts(),X=30,Y=60,sizeX=28,sizeY=6,text_size=27,fg=self.cget("fg_color"),bd_width=1,bd_color=bd)
        self.UPDATE_COM_BUTTOM=CustomButton(parent=self.COM_F,putWindow=window,master=self,image_name="kousin.png",text="",X=-19,Y=50,sizeX=5,sizeY=5,cornerradius=0,text_size=1,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.updateComList)
        self.CONECT_BUTTOM=CustomButton(parent=self.COM_F,putWindow=window,master=self,textcolor="DarkSlateGray2",text=" CONECT ",X=-3,Y=220,sizeX=16,sizeY=5,cornerradius=0,text_size=20,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setConectStats)
        self.DISCONECT_BUTTOM=CustomButton(parent=self.CONECT_BUTTOM,putWindow=window,master=self,textcolor="DarkSlateGray2",text="DISCONECT",X=25,Y=210,sizeX=8,sizeY=5,cornerradius=0,text_size=20,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setDIsconectStats)
        self.DISCONECT_BUTTOM.setDisable()

    #-----Relayted Install Program-----------------
    
    Files=[]
    
    
    
    #-----Relayted Install Program-----------------
                
    def GetWindowPos(self):
        text=self.geometry()
        array=text.split('+')
        return int(array[1]),int(array[2])

        
    def setDisconect2Antena(self):
        self.SLAVE_MODE_BUTTOM.setDisable()
        self.INDIV_MODE_BUTTOM.setDisable()
        if self.STOW_POS_B is not None:
            self.STOW_POS_B.setDisable()
            self.STOW_LOCK_B.setDisable()
            self.STOW_REL_B.setDisable()
    
    def setConect2Antena(self):
        self.SLAVE_MODE_BUTTOM.setNormal()
        self.INDIV_MODE_BUTTOM.setNormal()
        if self.STOW_POS_B is not None:
            self.STOW_POS_B.setNormal()
            self.STOW_LOCK_B.setNormal()
            self.STOW_REL_B.setNormal()
            self.setStowMode2Button()
        self.setControllMode2Button()
        
        
        
    TEST_BUTTON=None
        
    def set_mouce_position(self, event):
        x, y = event.x, event.y     # x,y座標取得
        if self.SETTING_BUTTOM.CarsolisOn:
            self.TEST_BUTTON=CustomFlame(master=self,image_name="batu.png",text="",text_size=1,X=0,Y=0,sizeX=20,sizeY=20)
            self.TEST_BUTTON.directBody.place(x=x,y=y)
        elif self.TEST_BUTTON is not None:
            self.TEST_BUTTON.destroy()
        self.MOUCE_POS_X=x
        self.MOUCE_POS_Y=y
        
    
    
    #--AdvancedGUI--

    AGUIBG=None
    AGUISettingButtom=None
    
    AntenaBG=None
    
    MyPCpic=None
    Antenapic=None
    Antenagif=None
    Acupic=None
    
    
    Antena2Acugif=None
    
    Acu2Mypcgif=None
    Mypc2Acugif=None
    Mypc2AcuDis=None
    
    ObserbSettingBtm=None
    
    InstallProgBtm=None
    
    #--AdvancedGUI--
        
#----------------------------------------------------
    def ApperGUI(self):
        global IS_INDIVISUAL_MODE
        global IS_SLAVE_MODE
        
        global DEFAULT_WINDOW_HEIGHT
        global DEFAULT_WINDOW_WIDTH
        global SELECTED_COM
        print("ACU_GUI_BEGUN!")
        customtkinter.set_appearance_mode("Dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
        time.updateAllTime()
        
        
        width=self.winfo_screenwidth()/2
        height=self.winfo_screenheight()/2

        self.geometry(str(DEFAULT_WINDOW_WIDTH)+"x"+str(DEFAULT_WINDOW_HEIGHT)+"+"+str(int(width-(DEFAULT_WINDOW_WIDTH/2)))+"+"+str(int(height-(DEFAULT_WINDOW_HEIGHT/2))))
        
        self.resizable(False,False)

        
        self.protocol('WM_DELETE_WINDOW', self.quit1)

        self.configure(fg_color="#0D1015")
        
        
        bd="DarkSlateGray2"
        
        AGUIBGcolor="#131519"#151618
        self.AGUIBG=CustomButton(master=self,text="",Timermode=True,sizeX=74,sizeY=35,X=38,Y=25,fg=AGUIBGcolor,bd_width=1,bd_color="DarkSlateGray2",cornerradius=0)
        
        
        #self.AGUIBG=CustomFlame(master=self,sizeX=74,sizeY=35,corner=0,text="",X=38,Y=25,fg=AGUIBGcolor,cornerradius=10,bd_width=1,bd_color=bd)
        
        self.AGUISettingButtom=CustomButton(master=self.AGUIBG,image_name="setting.png",text="",X=97,Y=8,sizeX=3,sizeY=12,cornerradius=0,text_size=1,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.AppearAntennaSettingWindow)
        self.InstallProgBtm=CustomButton(master=self.AGUIBG,parent=self.AGUISettingButtom,image_name="casette.png",text="",X=-200,Y=50,sizeX=7,sizeY=12,cornerradius=0,text_size=1,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        
        
        self.Acu2Mypcgif=CustomFlame(master=self.AGUIBG,gif_name="rightStripe",gif_time=40,fg=AGUIBGcolor,text="",X=70,Y=80,sizeX=50,sizeY=10,cornerradius=0)
        
        self.Mypc2Acugif=CustomFlame(master=self.AGUIBG,gif_name="leftStripe",gif_time=40,fg=AGUIBGcolor,text="",X=70,Y=60,sizeX=50,sizeY=10,cornerradius=0)
        if IS_INDIVISUAL_MODE:
            self.Mypc2Acugif.setStats(stats=False)
        
        AntenaBGcolor="#1b1d21"#0b0e14
        self.AntenaBG=CustomButton(master=self.AGUIBG,text="",Timermode=True,sizeX=60,sizeY=95,X=31,Y=50,fg=AntenaBGcolor,bd_width=1,bd_color="DarkSlateGray2",cornerradius=0)
        
        self.Antena2Acugif=CustomFlame(master=self.AntenaBG,gif_name="stripe",gif_time=50,fg=AntenaBGcolor,text="",X=50,Y=70,sizeX=70,sizeY=8,cornerradius=0)
        #.wm_attributes("-transparentcolor", "white")
        #self.Antenapic=CustomFlame(master=self.AntenaBG,gif_name="movingnew2",fg="transparent",gif_time=100,text="",X=20,Y=50,sizeX=38,sizeY=80,cornerradius=0)
        
        self.Antenapic=CustomFlame(master=self.AntenaBG,gif_name="cute",fg="transparent",gif_time=100,text="",X=32,Y=53,sizeX=38,sizeY=80,cornerradius=0)
        
        self.ObserbSettingBtm=CustomButton(master=self.AntenaBG,parent=self.Antenapic,hg="DarkSlateGray2",image_name="star.png",text="",sizeX=10,sizeY=17,X=-19,Y=-3,fg=AntenaBGcolor,cornerradius=0)
        
        self.Acupic=CustomFlame(master=self.AntenaBG,parent=self.Antenapic,image_name="PC.png",fg=AntenaBGcolor,text="",X=180,Y=70,sizeX=32,sizeY=50,cornerradius=0)
        
        self.MyPCpic=CustomFlame(master=self.AGUIBG,image_name="PC.png",fg=AGUIBGcolor,text="",X=87,Y=60,sizeX=25,sizeY=60,cornerradius=0)#attributes('-alpha', 0.5)
        
        #self.Antena2Acugif=CustomFlame(master=self.AntenaBG,parent=self.Antenapic,gif_name="orange",gif_time=50,fg=AntenaBGcolor,text="",X=100,Y=70,sizeX=30,sizeY=10,cornerradius=0)
        
        self.YearTime_F = CustomButton(master=self,textcolor="DarkSlateGray2",Timermode=True,text=time.Year_Time,text_size=30,sizeY=5,sizeX=10,X=5,Y=3,fg=self.cget("fg_color"),bd_width=2,bd_color="DarkSlateGray2",cornerradius=0)
        self.YearTime_F.setDisable()

        self.JstTime_F = CustomButton(master=self,textcolor="DarkSlateGray2",Timermode=True,parent=self.YearTime_F,text=time.JSTformat,text_size=30,sizeY=5,sizeX=10,X=210,Y=50,fg=self.cget("fg_color"),bd_width=2,bd_color="DarkSlateGray2",cornerradius=0)
        self.JstTime_F.setDisable()
        
        self.LstTime_F = CustomButton(master=self,textcolor="DarkSlateGray2",Timermode=True,parent=self.JstTime_F,text=time.LSTformat,text_size=30,sizeY=5,sizeX=10,X=250,Y=50,fg=self.cget("fg_color"),bd_width=2,bd_color="DarkSlateGray2",cornerradius=0)
        self.LstTime_F.setDisable()
        
        self.UctTime_F = CustomButton(master=self,textcolor="DarkSlateGray2",Timermode=True,parent=self.LstTime_F,text=time.UTCformat,text_size=30,sizeY=5,sizeX=10,X=250,Y=50,fg=self.cget("fg_color"),bd_width=2,bd_color="DarkSlateGray2",cornerradius=0)
        self.UctTime_F.setDisable()
        
        self.LOC_F=CustomButton(master=self,textcolor="DarkSlateGray2",Timermode=True,parent=self.UctTime_F,text="LOC:ふくいのどっか",text_size=30,sizeY=5,sizeX=10,X=250,Y=50,fg=self.cget("fg_color"),bd_width=2,bd_color="DarkSlateGray2",cornerradius=0)
        self.LOC_F.setDisable()
        #self.UctTime_F.after(1000,self.updateTimer)  
        #self.TEST_BUTTON=AnotherWIndowUIC(UI=None,Stats=True) 
        
        
        #X=73,Y=5
        #self.QUIET_BUTTON=CustomButton(master=self,text="EXIT",text_size=27,X=95,Y=4,sizeX=10,sizeY=5,com=self.quit1)
        #X=91,Y=12
        #Place_F = CustomFlame(master=self,text="あわらキャンパス",text_size=30,sizeX=10,sizeY=7,X=90,Y=14)
        #self.COM_STATS_F=CustomFlame(master=self,text="Unkown",X=80,Y=11,sizeX=16,sizeY=6,text_size=20)
        
        '''
        self.COM_F=CustomCombobox(master=self,value=self.ACU_Monitor.BackEnd.getSerialPorts(),X=88,Y=3,sizeX=13,sizeY=6,text_size=27,fg=self.cget("fg_color"),bd_width=1,bd_color=bd)
        self.UPDATE_COM_BUTTOM=CustomButton(parent=self.COM_F,master=self,image_name="kousin.png",text="",X=-10,Y=50,sizeX=2,sizeY=4,cornerradius=0,text_size=1,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.updateComList)
        self.CONECT_BUTTOM=CustomButton(parent=self.COM_F,master=self,textcolor="DarkSlateGray2",text="CONECT",X=55,Y=155,sizeX=10,sizeY=5,cornerradius=0,text_size=20,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setConectStats)
        self.DISCONECT_BUTTOM=CustomButton(parent=self.CONECT_BUTTOM,master=self,textcolor="DarkSlateGray2",text="DISCONECT",X=40,Y=180,sizeX=8,sizeY=5,cornerradius=0,text_size=20,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setDIsconectStats)
        self.DISCONECT_BUTTOM.setDisable()
        '''
        
        #self.SELECTED_COM=self.COM_F.combbox.get()
        
        #self.CONECT_B=CustomFlame(master=self,text="Conect",text_size=20,X=50,Y=50,sizeX=30,sizeY=6)
        
        self.DisConect_B=CustomFlame(master=self,text="Conect",text_size=20,X=50,Y=50,sizeX=30,sizeY=6)

        #important!
        #modestring=CustomText(master=self,text="CONTROLL MODE:",text_size=30,X=30,Y=12,sizeX=20,sizeY=6)
        #self.SLAVE_MODE_BUTTOM=CustomButton(master=self,parent=modestring,text="SLAVE",textcolor="DarkSlateGray2",X=140,Y=38,sizeX=10,sizeY=5,cornerradius=0,text_size=30,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setSlaveMode)
        #self.INDIV_MODE_BUTTOM=CustomButton(master=self,parent=self.SLAVE_MODE_BUTTOM,text="INDIV",textcolor="DarkSlateGray2",X=180,Y=50,sizeX=10,sizeY=5,cornerradius=0,text_size=30,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd,com=self.setIndivMode)

        #CustomButton(master=self,gif_name="BAKA1",gif_time=60,parent=modestring,text="",textcolor="DarkSlateGray2",X=180,Y=50,sizeX=10,sizeY=10,cornerradius=0,text_size=30,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        #CustomButton(master=self,parent=self.SLAVE_MODE_BUTTOM,text="",textcolor="DarkSlateGray2",X=200,Y=50,sizeX=10,sizeY=10,cornerradius=0,text_size=30,fg=self.cget("fg_color"),hg="DarkSlateGray2",bd_width=1,bd_color=bd)
        
        #gif_name="hogehoge",gif_time=60
        self.LCU=LCU_Controller(master=self)

        #self.setIndivMode()
        
        #self.bind("<Motion>", self.set_mouce_position)

        
        #self.COM_F.combbox.configure(command=self.ThrowSelectedCom2Backend)
        
        #textbox=CustomTextBox(master=self,text="FUCKYOU!",text_size=30,sizeX=30,sizeY=30)
        
        
        
        #self.COM_Monitor=threading.Thread(target=self.ThrowSelectedCom2Backend)
        #self.COM_Monitor.start()
        
        self.Setnotconect2Antenna()
        
        self.setIndivModeFlag()
        
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
        global GUI_APP
        self.gui.mainloop()
        GUI_APP=self.gui
    def ApperGUI(self):
        self.gui.ApperGUI()
    def setAsync_Class(self,Async):
        self.gui.Async_Class=Async
    