import wx
#from wx import *
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
#from database.database import get_experiment as exp
#from database.database import  ExperimentDesign

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="The Main Frame")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="",
    pos=wx.DefaultPosition, size=wx.DefaultSize,
    style=wx.DEFAULT_FRAME_STYLE,
    name="MyFrame"):
        super(MyFrame, self).__init__(parent, id, title,
        pos, size, style, name)
        # Attributes
        self.panel = wx.Panel(self)

if __name__ == "__main__":
    app = MyApp(False)
