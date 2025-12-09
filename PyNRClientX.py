#!/usr/bin/env python3
#Boa:PyApp:main

import wx
import BuddyList

modules = {'BuddyList': [0, '', 'BuddyList.py'],
 u'CLIWrapper': [0, '', 'CLIWrapper.py'],
 u'Logon': [0, '', 'Logon.py']}

class NRClientXApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        self.main = BuddyList.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True
    
def main():
    application = NRClientXApp(False)
    application.MainLoop()

if __name__ == '__main__':
    main()
