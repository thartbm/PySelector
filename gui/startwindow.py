import wx,os
from wx import *
import numpy as np
import collections
import wx.lib.agw.gradientbutton as gbtn


class MyApp(wx.App):
    def OnInit(self):
        self.mainframe = MyFrame(None)
        self.SetTopWindow(self.mainframe)
        self.mainframe.Show()
        return True

class MyFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # Attributes
        self.parent = parent
        self.MainPanel = MainPanel(self)

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.BackgroundColour = wx.BLACK


        all_settings = [x for x in os.listdir('setting/savedsettings') if x.endswith(".npy")]
        self.filepicker = wx.FilePickerCtrl(self, message='select data file')
        self.settingspicker = wx.Choice(self, choices=all_settings)
        self.submit = gbtn.GradientButton(self, label='Submit')

        self.__DoLayout()

        self.submit.Bind(wx.EVT_BUTTON, self.__returndata())


    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(2)
        sizer.Add(self.filepicker, flag=wx.ALIGN_CENTRE)
        sizer.AddStretchSpacer(2)
        sizer.Add(self.settingspicker, flag=wx.ALIGN_CENTER)
        sizer.AddStretchSpacer(2)
        sizer.Add(self.submit, flag=wx.ALIGN_CENTER)
        self.SetSizerAndFit(sizer)

    def __returndata(self):
        self.datafile = self.filepicker.GetPath()
        self.settings = self.settingspicker.GetStringSelection()
        print(self.datafile)
        print(self.settings)

def run():
    app = MyApp(False)
    app.MainLoop()


if __name__ == "__main__":
    run()
