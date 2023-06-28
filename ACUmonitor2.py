import customtkinter
import getTime as time

FONT_TYPE = "Segoe UI"

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, text="none_text",text_size=11,corner=-1):
        super().__init__(master)

        # add widgets onto the frame...
        if corner==-1:
            self.label = customtkinter.CTkLabel(self,text=text, font=(FONT_TYPE, text_size))
        else:
            self.label = customtkinter.CTkLabel(self,text=text, font=(FONT_TYPE, text_size),corner_radius=corner)
        self.label.grid(row=0, column=0, padx=10)


class App(customtkinter.CTk):
    def __init__(self):
        time.updateAllTime()
        def updateTimer():
            time.updateAllTime()
            YearTime_F.label.configure(text=time.Year_Time)
            JstTime_F.label.configure(text=time.JSTformat)
            UctTime_F.label.configure(text=time.UTCformat)
            LstTime_F.label.configure(text=time.LSTformat)
            YearTime_F.after(1000,updateTimer)
        def setYearTime(S):
            return MyFrame(master=S,text=time.Year_Time,text_size=30)
        def setJST(S):
            return MyFrame(master=S,text=time.JSTformat,text_size=30)
        def setUCT(S):
            return MyFrame(master=S,text=time.UTCformat,text_size=30)
        def setLST(S):
            return MyFrame(master=S,text=time.LSTformat,text_size=30)
        super().__init__()
        self.geometry("1250x600")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        ACU_F=customtkinter.CTkFrame(self.master,width=750,height=400,corner_radius=5)
        ACU_F.place(x=25, y=60)
        
        JstTime_F = setJST(self)
        JstTime_F.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        JstTime_F.place(x=165,y=0)#110
        
        UctTime_F = setUCT(self)
        UctTime_F.grid(row=2, column=0, padx=0, pady=0, sticky="w")
        UctTime_F.place(x=368,y=0)#245
        
        LstTime_F = setLST(self)
        LstTime_F.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        LstTime_F.place(x=583,y=0)
        
        YearTime_F = setYearTime(self)
        YearTime_F.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        YearTime_F.place(x=0,y=0)
        YearTime_F.after(1000,updateTimer)

        Place_F = MyFrame(master=self,text="あわらキャンパス",text_size=30)
        Place_F.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        Place_F.place(x=798,y=0)

        Place_F = MyFrame(master=ACU_F,text="Azmiz",text_size=30)
        Place_F.grid(row=0, column=0, padx=0, pady=0,sticky="s")
        Place_F.place(x=100,y=50)
        Place_F.label.configure(fg_color="gray")



customtkinter.set_appearance_mode("green")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = App()
app.mainloop()