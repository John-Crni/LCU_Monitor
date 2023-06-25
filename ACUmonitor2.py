import customtkinter
import getTime as time

FONT_TYPE = "Segoe UI"
class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, text="none_text",text_size=11):
        super().__init__(master)

        # add widgets onto the frame...
        self.label = customtkinter.CTkLabel(self,text=text, font=(FONT_TYPE, text_size))
        self.label.grid(row=0, column=0, padx=10)


class App(customtkinter.CTk):
    def __init__(self):
        time.updateAllTime()
        def updateTimer():
            time.updateAllTime()
            YearTime_F.configure()
            #JstTime_F.configure(text=time.JSTformat)
            #UctTime_F.configure(text=time.UTCformat)
            #LstTime_F.configure(text=time.LSTformat)
            YearTime_F.after(1000,updateTimer)
        def setYearTime(S):
            return MyFrame(master=S,text=time.Year_Time,text_size=20)
        def setJST(S):
            return MyFrame(master=S,text=time.JSTformat,text_size=20)
        def setUCT(S):
            return MyFrame(master=S,text=time.UTCformat,text_size=20)
        def setLST(S):
            return MyFrame(master=S,text=time.LSTformat,text_size=20)
        super().__init__()
        self.geometry("400x200")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        JstTime_F = setJST(self)
        JstTime_F.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        JstTime_F.place(x=110,y=0)
        
        UctTime_F = setUCT(self)
        UctTime_F.grid(row=2, column=0, padx=0, pady=0, sticky="w")
        UctTime_F.place(x=245,y=0)
        
        LstTime_F = setLST(self)
        LstTime_F.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        LstTime_F.place(x=390,y=0)
        
        YearTime_F = setYearTime(self)
        YearTime_F.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        YearTime_F.place(x=0,y=0)
        YearTime_F.after(1000,updateTimer)
        

        
        
        


app = App()
app.mainloop()