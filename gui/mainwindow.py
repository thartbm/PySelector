import wx, os
from wx import *
import matplotlib

matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from database.Read_Data import set_data
from database.Plot_Data import velocity_profiler, reach_profiler
from gui import settingwindow


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
        icon = wx.Icon(icon_path, wx.BITMAP_TYPE_PNG)

        # Actions
        self.SetMenuBar(self.PopupMenu)
        self.SetIcon(icon)

        # self.SetSizerAndFit(self.MainPanel.Sizer, wx.GROW)

        # wx.CallAfter(self.setframesize)

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
        self.BackgroundColour = wx.Colour('SALMON')
        self.ButtonPanel = ButtonPanel(self)
        self.Fixp1p2mode = False
        self.clicknum = 1
        self.selected_velocity = 'pyselect'
        self.warningmsg = wx.MessageDialog(self, 'Please Choose Settings first', caption=MessageBoxCaptionStr,
                                           style=OK | CENTRE, pos=DefaultPosition)
        self.__setpanel()
        self.__dolayout()
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)

        # Event Handlers
        # self.Bind(wx.EVT_LIST_ITEM_SELECTED,
        #          self.OnItemSelected)

        self.VelocityCanvas.mpl_connect('button_press_event',
                                        self.onVelcoityclick)

    def __setpanel(self):
        self.InfoPanel = InfoPanel(self)
        self.__setreachplot()
        self.__setvelocityplot()

    def __dolayout(self):
        MainPanelSizer = wx.GridBagSizer(10, 10)
        MainPanelSizer.Add(self.ReachCanvas, pos=(0, 1), span=(1, 1), flag=wx.GROW)
        MainPanelSizer.Add(self.VelocityCanvas, pos=(1, 1), span=(1, 1), flag=wx.GROW)
        MainPanelSizer.Add(self.InfoPanel, pos=(0, 0), span=(1, 1), flag=wx.ALIGN_CENTRE | wx.GROW)
        MainPanelSizer.Add(self.ButtonPanel, pos=(1, 0), flag=wx.ALIGN_CENTRE | wx.GROW)
        MainPanelSizer.AddGrowableRow(0, 3)
        MainPanelSizer.AddGrowableCol(1, 1)
        MainPanelSizer.AddGrowableRow(1, 1)
        self.SetSizerAndFit(MainPanelSizer)

    def __setreachplot(self):
        fig = plt.figure()
        plt.axis([0, 1, 0, 1])
        self.ReachCanvas = FigureCanvas(self, -1, fig)
        self.ReachCanvas.draw()

    def __setvelocityplot(self):
        fig = plt.figure()
        plt.axis([0, 1, 0, 1])
        self.VelocityCanvas = FigureCanvas(self, -1, fig)
        self.VelocityCanvas.SetMinSize((100, 100))

    def __updatereachplot(self):
        # this is somewhat prone to errors, it should be fine as long as the program consistnaly runs velocity plots
        # before reach plots though as it does now.
        fig = reach_profiler(self.trial_data, self.setting, self.max_position, self.trial_data.selectedmaxvelocity, self.experiment['all_targets'])
        fig.gca().set_aspect('auto')

        self.ReachCanvas.figure = fig
        self.ReachCanvas.draw()

    def __updatevelocityplot(self):
        if self.Fixp1p2mode:
            self.Fixp1p2mode = False
            self.selected_velocity = 'pyselect'
            self.VelocityCanvas.figure.get_axes()[0].get_children()[2].set_xdata(self.trial_data.selectedp1)
            self.VelocityCanvas.figure.get_axes()[0].get_children()[3].set_xdata(self.trial_data.selectedp2)
            [c, a, b, d, self.trial_data.selectedmaxvelocity,e] = velocity_profiler(self.trial_data, self.selected_velocity)
            if ~(self.trial_data.selectedp1 <= self.trial_data.selectedmaxvelocity <= self.trial_data.selectedp2):
                    self.trial_data.selectedmaxvelocity = velocity_profiler(self.trial_data, 'update', self.velocity_profile)[0]
                    self.VelocityCanvas.figure.get_axes()[0].get_children()[1].set_xdata(self.trial_data.selectedmaxvelocity)




            #start_idx = self.trial_data.loc[lambda df: df.time_ms > self.trial_data['P1'].max(), :].index.min()
            #end_idx = self.trial_data.loc[lambda df: df.time_ms > self.trial_data['P2'].max(), :].index.min
            self.VelocityCanvas.draw()

        else:
            if self.selected_velocity is 'pyselect':  # will always happen first.
                [fig, self.trial_data.selectedp1, self.trial_data.selectedp2, self.max_position, self.trial_data.selectedmaxvelocity, self.velocity_profile] \
                    = velocity_profiler(self.trial_data, self.selected_velocity)
                self.VelocityCanvas.figure = fig

            elif self.selected_velocity is 'user':
                # maybe do this differently (outsource to a function?) . Consider this later.
                self.VelocityCanvas.figure.get_axes()[0].get_children()[1].set_xdata(self.trial_data.selectedmaxvelocity)
                self.selected_velocity = 'pyselect'

            self.VelocityCanvas.draw()

    # def OnItemSelected(self, event):
    #    selected_row = event.GetIndex()
    #    __experiment__.CurrentTrialNum = self.InfoPanel.GetItemText(selected_row)
    #    self.refresh()

    def onVelcoityclick(self, event):
        if self.Fixp1p2mode:
            self.fixp1p2(event)
            self.selected_velocity = 'pyselect'

        else:
            self.selected_velocity = 'user'
            self.trial_data.selectedmaxvelocity = event.xdata
            self.refresh()

    def fixp1p2(self, event):
        if self.clicknum == 1:
            self.trial_data.selectedp1 = event.xdata
            self.clicknum = 2
        elif self.clicknum == 2:
            self.trial_data.selectedp2 = event.xdata
            self.clicknum = 1
            self.refresh()

    def set_settings(self, setting_name):
        self.InfoPanel.set_settings(setting_name)

    def set_exp(self, exp_name):
        if self.InfoPanel.setting.GetLabel() == 'None':
            self.warningmsg.ShowModal()

        else:
            self.experiment, self.setting = set_data(exp_name, self.InfoPanel.setting.GetLabel())
            self.InfoPanel.set_exp(exp_name, self.experiment)

    def set_trial_data(self, trial):
        self.trial_data = self.experiment['output'].where(self.experiment['output'].trial_no == trial)
        self.trial_data.dropna(inplace= True)
        #self.trial_data = self.experiment['Trial'][trial]
        #self.trial_data.where(self.trial_data.selected == 1, inplace=True)
        self.refresh()

    def refresh(self):
        self.__updatevelocityplot()
        self.__updatereachplot()
        self.InfoPanel.update()
        self.Layout()
        self.Fit()
        self.parent.Fit()

    def updateoutput(self):
        maxvel_idx = next(x[0] for x in enumerate(self.trial_data.time_ms) if x[1] >= self.trial_data.selectedmaxvelocity)
        p1_idx = next(x[0] for x in enumerate(self.trial_data.time_ms) if x[1] >= self.trial_data.selectedp1)
        p2_idx = next(x[0]+1 for x in enumerate(self.trial_data.time_ms) if x[1] >= self.trial_data.selectedp2)
        self.trial_data.selected[p1_idx:p2_idx] = 1
        self.trial_data.max_velocity[maxvel_idx] = 1
        self.experiment['output'].update(self.trial_data)

    def outputdata(self):
        self.experiment['output'].to_csv('test.csv', index=False)

    def onKeyPress(self, e):
        if e == wx.WXK_RIGHT:
            self.MainPanel.ButtonPanel.nexttrial(e)
        elif e == wx.WXK_LEFT:
            self.MainPanel.ButtonPane.prvstrial(e)
        elif e == wx.WXK_DOWN:
            self.MainPanel.ButtonPane.savetrial(e)

class InfoPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.trial_index = 0
        self.BackgroundColour = wx.Colour('SALMON')
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
        self.trial.SetLabel(str(self.current_trial) + '/' + str(self.all_trials.iloc[-1]))

    def set_settings(self, setting_name):
        self.setting.SetLabel(os.path.splitext(setting_name)[0])  # don't include "json"
        self.parent.Refresh()

    def update_trial_index(self, direction):
        if isinstance(direction, int):
            self.trial_index = direction
        elif direction is 'up':
            self.trial_index += 1
        elif direction is 'down':
            self.trial_index -= 1

        self.current_trial = self.all_trials.unique()[self.trial_index]
        self.parent.set_trial_data(self.current_trial)


    def set_exp(self, experiment_path, experiment):
        self.experiment.SetLabel(experiment_path)
        # ====  RECODE maybe? / there has to be a nicer way of handling this
        self.current_trial = experiment['output'].trial_no[self.trial_index]
        self.all_trials = experiment['output'].trial_no
        self.trial.SetLabel(str(self.current_trial) + '/' + str(self.all_trials.iloc[-1]))
        self.parent.set_trial_data(self.current_trial)


class ButtonPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.Unsure = wx.CheckBox(self, size=(100, 10), label="Unsure")
        self.Save = wx.ToggleButton(self, label="Accept")
        self.SetMax = wx.Button(self, label=" Max Velocity")
        self.Delete = wx.ToggleButton(self, label="Reject ")
        self.FixP1P2 = wx.Button(self, label="Fix P1 P2")
        self.Next = wx.Button(self, label="Next")
        self.Previous = wx.Button(self, label="Previous")
        self.BackgroundColour = wx.Colour('SALMON')
        self.gridSizer = wx.GridSizer(rows=4, cols=2, hgap=2, vgap=2)
        emptycell = (0, 0)
        self.gridSizer.AddMany([
            (self.FixP1P2, wx.ALIGN_CENTER), (self.SetMax, wx.ALIGN_CENTER),
            emptycell, (self.Unsure, wx.ALIGN_LEFT),
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


    def nexttrial(self,e):
        if self.parent.trial_data.accept.min():
            self.parent.updateoutput()
            self.parent.InfoPanel.update_trial_index('up')
            self.toggleoff()

    def fixp1p2(self, e):
        self.parent.Fixp1p2mode = True

    def prvstrial(self, e):
        self.parent.InfoPanel.update_trial_index('down')
        self.toggleoff()

    def deltrial(self, e):
        self.parent.trial_data['Reject'] = 1

    def savetrial(self, e):
        self.parent.trial_data['accept'] = 1

    def unsuretrial(self, e):
        self.parent.trial_data['Unsure'] = 1



    def toggleoff(self):
        self.Unsure.SetValue(False)
        self.Save.SetValue(False)
        self.Delete.SetValue(False)


# This is the toolbar menu at the top
class PopupMenu(wx.MenuBar):
    def __init__(self, parent):  # parent is mainframe
        super().__init__()
        self.parent = parent

        # The two menus
        self.filemenu = wx.Menu()
        self.settingsmenu = wx.Menu()
        self.savedsettings = wx.Menu()  # savedsetting is a submenu of settingmenu
        all_settings = [x for x in os.listdir('setting/savedsettings') if
                        x.endswith(".json")]  # setings that already exist

        for item in all_settings:
            self.savedsettings.Append(-1, item)

        # settingmenu buttons
        newsetting = self.settingsmenu.Append(-1, 'New Setting')
        settingchoice = self.settingsmenu.Append(-1, 'Choose Setting...', self.savedsettings)

        # filemenu buttons
        loaddata = self.filemenu.Append(-1, 'load')
        writedata = self.filemenu.Append(-1, 'save')
        # writedata_cs = filemenu.Append(-1, 'save cs')

        self.Append(self.filemenu, 'Files')
        self.Append(self.settingsmenu, 'Settings')

        self.filepicker = wx.FileDialog(self)

        ##Bindings
        self.Bind(EVT_MENU, self.loadsettinggui, newsetting)
        self.Bind(EVT_MENU, self.outputdata, writedata)
        self.Bind(EVT_MENU, self.getdata, loaddata)
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
        self.filepicker.ShowModal()
        self.parent.set_exp(self.filepicker.GetPath())

    def outputdata(self, e):
        self.parent.MainPanel.outputdata()


def run():
    app = MyApp(False)
    app.MainLoop()


if __name__ == "__main__":
    run()
