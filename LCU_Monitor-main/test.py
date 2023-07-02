import ACUbackend

class TEST(ACUbackend.AsyncedClass):
    def Async(self):
        print(self.ACUmonitor.FrontEnd.COM_F.combbox.get())
        self.sleep()
    def __init__(self,acu=None):
        super().__init__(acu)



