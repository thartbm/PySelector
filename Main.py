#!/usr/bin/ipython

from gui import mainwindow,startwindow,settingwindow
from database import database


##
# import sys,os
# cd PySelect
# sys.path.append(os.getcwd())


def main():

    #[setting,data] = startwindow.run()

    #print('     ****       Reading Data           ****        ')
    #rawdata = database.DataSet('Baselinenocursor_p33.txt', '')  # Handles fullpaths.
    #rawdata.autoprocess('')  # Analysis an be performed at lower levels.
    #myexp = rawdata.prepare('')

    #print('     ****       Preparing Display      ****        ')
    mainwindow.run()
    #settingwindow.run()


if __name__ == "__main__":
    main()
