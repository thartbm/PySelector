import wx,sys,os
from wx import *
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from gui import settingwindow
import wx.lib.agw.gradientbutton as gbtn
from database.database import get_experiment as exp
from database.database import Experiment
from gui import settingwindow

__experiment__ = None


class MyApp(wx.App):
    def OnInit(self):
        self.mainframe = MyFrame(None)
        self.SetTopWindow(self.mainframe)
        self.mainframe.Show()
        return True


class MyFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, -1, "PySelect", size=(1000, 700))

        # Attributes
        self.parent = parent
        self.MainPanel = MainPanel(self)
        self.PopupMenu = PopupMenu(self)


        # Local Variables
        icon_path = './gui/icons/appicon.png'
        icon = wx.Icon(icon_path , wx.BITMAP_TYPE_PNG)


        # Actions
        self.SetMenuBar(self.PopupMenu)
        self.SetIcon(icon)


        #self.SetSizerAndFit(self.MainPanel.Sizer, wx.GROW)

        #wx.CallAfter(self.setframesize)



    def setframesize(self):
        MinSizeX, MinSizeY = self.MainPanel.Sizer.GetMinSize()
        self.MinClientSize = (MinSizeX, MinSizeY)
        self.ClientSize = (MinSizeX, MinSizeY)

    def set_settings(self, exp_name):
        self.MainPanel.set_settings(exp_name)


    def set_exp(self, setting_name):
        self.MainPanel.set_exp(setting_name)

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.BackgroundColour = wx.BLACK
        self.ButtonPanel = ButtonPanel(self)
        self.Fixp1p2 = False
        self.clicknum = 1
        self.warningmsg = wx.MessageDialog(self, 'Please Choose Settings first', caption=MessageBoxCaptionStr,
                                           style=OK | CENTRE, pos=DefaultPosition)

        self.__setpanel()
        self.__dolayout()

        # Event Handlers
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,
                  self.OnItemSelected)

        self.VelocityCanvas.mpl_connect('button_press_event',
                  self.onVelcoityclick)


    def __setpanel(self):
        self.InfoPanel = InfoPanel(self)
        self.__setreachplot()
        self.__setvelocityplot()

    def refresh(self):
        self.__updatereachplot()
        self.__updatevelocityplot()
        self.InfoPanel.update()
        self.Layout()

    def __dolayout(self):
        MainPanelSizer = wx.GridBagSizer(10,10)
        MainPanelSizer.Add(self.ReachCanvas, pos=(0, 1), span=(1, 1), flag=wx.GROW)
        MainPanelSizer.Add(self.VelocityCanvas, pos=(1, 1), span=(1, 1), flag=wx.GROW)
        MainPanelSizer.Add(self.InfoPanel, pos=(0, 0), span=(1,1), flag=wx.ALIGN_CENTRE | wx.GROW)
        MainPanelSizer.Add(self.ButtonPanel, pos=(1, 0), flag=wx.ALIGN_CENTRE | wx.GROW)
        MainPanelSizer.AddGrowableRow(0, 3)
        MainPanelSizer.AddGrowableCol(1, 1)
        MainPanelSizer.AddGrowableRow(1, 1)
        self.SetSizerAndFit(MainPanelSizer)

    def __setreachplot(self):
        fig = plt.figure()
        plt.axis([0, 1, 0, 1])
        self.ReachCanvas = FigureCanvas(self, -1, fig)
        self.ReachCanvas.SetMinSize((100, 100))
        self.ReachCanvas.draw()

    def __setvelocityplot(self):
        fig = plt.figure()
        plt.axis([0, 1, 0, 1])
        self.VelocityCanvas = FigureCanvas(self, -1, fig)
        self.VelocityCanvas.SetMinSize((100, 100))
        self.VelocityCanvas.draw()

    def __updatereachplot(self):
        CurrentTrial = __experiment__.CurrentTrial
        fig = CurrentTrial.reachplot
        self.ReachCanvas.figure = fig
        self.ReachCanvas.draw()

    def __updatevelocityplot(self):
        CurrentTrial = __experiment__.CurrentTrial
        fig = CurrentTrial.VelocityPlot
        self.VelocityCanvas.figure = fig
        self.VelocityCanvas.draw()

    def OnItemSelected(self, event):
        selected_row = event.GetIndex()
        __experiment__.CurrentTrialNum = self.InfoPanel.GetItemText(selected_row)
        self.refresh()

    def onVelcoityclick(self, event):
        if self.Fixp1p2:
            self.fixp1p2(event)
        else:
            __experiment__.CurrentTrial.MaxVelocity = event.xdata
            self.refresh()



    def fixp1p2(self, event):
        if self.clicknum == 1:
            __experiment__.CurrentTrial.p1 = event.xdata
            self.clicknum = 2
        elif self.clicknum == 2:
            __experiment__.CurrentTrial.p2 = event.xdata
            self.Fixp1p2 = False
            self.clicknum = 1
            self.refresh()


    def set_settings(self, setting_name):
        self.InfoPanel.set_settings(setting_name)

    def set_exp(self, exp_name):
        if self.InfoPanel.setting.GetLabel() ==  'None':
            self.warningmsg.ShowModal()

        else:
            self.InfoPanel.set_exp(exp_name)


class InfoPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.BackgroundColour = wx.RED
        self.setting = wx.StaticText(self, -1, 'None')
        self.experiment = wx.StaticText(self, -1, 'None')
        self.trial = wx.StaticText(self, -1, '0/0')


        settinglabel = wx.StaticText(self, -1, "Setting:")
        experimentlabel = wx.StaticText(self, -1, "Experiment:")
        triallabel = wx.StaticText(self, -1, "Trials:")

        sizer = wx.GridSizer(3, 2, 5, 5)
        sizer.AddMany([settinglabel, self.setting, experimentlabel, self.experiment, triallabel, self.trial])
        self.SetSizerAndFit(sizer)

    def update(self):
        if not __experiment__.setting is None:
            self.setting.SetLabel(__experiment__.setting['Name'])
        self.experiment.SetLabel(__experiment__.Address)
        self.trial.SetLabel(str(__experiment__.CurrentTrialNum) + '/' + str(__experiment__.NumTrials))

    def set_settings(self, setting_name):
        self.setting.SetLabel(os.path.splitext(setting_name)[0])  #don't include "json"
        self.parent.Refresh()


    def set_exp(self, experiment_path):
        self.experiment.SetLabel(experiment_path)
        self.parent.Refresh()


class ButtonPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.Unsure = wx.CheckBox(self,  size= (100, 10), label="Unsure")
        self.Save = wx.ToggleButton(self, label="Accept")
        self.SetMax = wx.Button(self, label=" Max Velocity")
        self.Delete = wx.ToggleButton(self, label="Reject ")
        self.FixP1P2 = wx.Button(self, label="Fix P1 P2")
        self.Next = wx.Button(self, label="Next")
        self.Previous = wx.Button(self, label="Previous")
        self.BackgroundColour = wx.BLUE
        self.gridSizer = wx.GridSizer(rows=4, cols=2, hgap=2, vgap=2)
        emptycell = (0, 0)
        self.gridSizer.AddMany([
            (self.FixP1P2, wx.ALIGN_CENTER), (self.SetMax , wx.ALIGN_CENTER),
            emptycell,  (self.Unsure, wx.ALIGN_LEFT),
            (self.Save, wx.ALIGN_CENTER), (self.Delete, wx.ALIGN_CENTER),
            (self.Previous), (self.Next)])

        self.SetSizer(self.gridSizer)

        ##Actions
        self.Bind(wx.EVT_BUTTON, self.nexttrial, self.Next)
        self.Bind(wx.EVT_BUTTON, self.prvstrial, self.Previous)
        self.Bind(wx.EVT_BUTTON, self.fixp1p2, self.FixP1P2)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.unsuretrial, self.Unsure)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.savetrial, self.Save)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.deltrial, self.Delete)


    def nexttrial(self, e):
        __experiment__.CurrentTrialNum += 1
        self.toggleoff()
        self.parent.refresh()

    def fixp1p2(self, e):
        self.parent.Fixp1p2 = True

    def prvstrial(self, e):
        __experiment__.CurrentTrialNum -= 1
        self.toggleoff()
        self.parent.refresh()

    def deltrial(self, e):
        __experiment__.del_trial = 1
        self.parent.refresh()

    def savetrial(self, e):
        __experiment__.save_trial = 1
        self.parent.refresh()

    def unsuretrial(self, e):
        __experiment__.unsure_trial += 1
        self.parent.refresh()

    def toggleoff(self):
        self.Unsure.SetValue(False)
        self.Save.SetValue(False)
        self.Delete.SetValue(False)


#This is the toolbar menu at the top
class PopupMenu(wx.MenuBar):
    def __init__(self, parent): #parent is mainframe
        super().__init__()
        self.parent = parent

        #The two menus
        self.filemenu = wx.Menu()
        self.settingsmenu = wx.Menu()

        self.savedsettings = wx.Menu() #savedsetting is a submenu of settingmenu
        all_settings = [x for x in os.listdir('setting/savedsettings') if x.endswith(".json")]    # setings that already exist

        for item in all_settings:
            self.savedsettings.Append(-1, item)

        #settingmenu buttons
        newsetting = self.settingsmenu.Append(-1, 'New Setting')
        settingchoice = self.settingsmenu.Append(-1, 'Choose Setting...', self.savedsettings)

        #filemenu buttons
        loaddata = self.filemenu.Append(-1, 'load')
        writedata = self.filemenu.Append(-1, 'save')
        #writedata_cs = filemenu.Append(-1, 'save cs')


        self.Append(self.filemenu, 'Files')
        self.Append(self.settingsmenu, 'Settings')

        self.filepicker = wx.FileDialog(self)


        ##Bindings
        self.Bind(EVT_MENU, self.loadsettinggui, newsetting)
        self.Bind(EVT_MENU, self.getdata, loaddata)
        self.Bind(EVT_MENU, self.outputdata, writedata)
        self.savedsettings.Bind(wx.EVT_MENU, self.choosesetting)




    def loadsettinggui(self, e):
        win = settingwindow.SettingFrame(self)
        win.Show(True)
#       all_settings = [x for x in os.listdir('setting/savedsettings') if x.endswith(".json")]    # setings that already exist
#       for item in all_settings:
#           if item not in self.savedsettings:
#               self.savedsettings.Append(-1, item)

    def choosesetting(self, e):
        self.parent.set_settings(self.savedsettings.FindItemById(e.GetId()).GetItemLabel())

    def getdata(self, e):
        global __experiment__
        self.filepicker.ShowModal()
        self.parent.set_exp(self.filepicker.GetPath())

    def outputdata(self):
        __experiment__.output()




def run():
    app = MyApp(False)
    app.MainLoop()


if __name__ == "__main__":
    run()
