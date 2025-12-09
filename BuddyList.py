#Boa:Frame:fmBuddyList

import platform
import time

import wx

import CLIWrapper
import Logon

menu_titles = ["Delete a Computer"]
menu_title_by_id = {}

addon_menu_items = {}
addon_menu_items_by_id = {}


def new_id():
    return wx.Window.NewControlId()


def create(parent):
    return fmBuddyList(parent)


wxID_FMBUDDYLIST = wx.ID_ANY
wxID_FMBUDDYLISTPNLBUDDYLIST = wx.ID_ANY
wxID_FMBUDDYLISTSBBUDDYLIST = wx.ID_ANY
wxID_FMBUDDYLISTTBBUDDYLIST = wx.ID_ANY
wxID_FMBUDDYLISTTCBUDDYLIST = wx.ID_ANY

wxID_FMBUDDYLISTMNFILEMNEXIT = new_id()
wxID_FMBUDDYLISTMNFILEMNSIGNIN = new_id()
wxID_FMBUDDYLISTMNFILEMNSIGNOUT = new_id()

wxID_FMBUDDYLISTMNCOMPUTERMNADDCOMPUTERS = new_id()
wxID_FMBUDDYLISTMNCOMPUTERMNCREATECATEGORY = new_id()
wxID_FMBUDDYLISTMNCOMPUTERMNDELETECATEGORY = new_id()
wxID_FMBUDDYLISTMNCOMPUTERMNDELETECOMPUTER = new_id()
wxID_FMBUDDYLISTMNCOMPUTERMNEDITCATEGORY = new_id()

wxID_FMBUDDYLISTMENU1MNABOUT = new_id()
wxID_FMBUDDYLISTMENU1MNHELP = new_id()

wxID_FMBUDDYLISTMNHELPMNABOUT = new_id()
wxID_FMBUDDYLISTMNHELPMNHELP = new_id()

wxID_FMBUDDYLISTTOOLBAR1MNADDCATEGORY = new_id()
wxID_FMBUDDYLISTTOOLBAR1MNADDCOMPUTER = new_id()

wxID_FMBUDDYLISTTBBUDDYLISTMNADDCATEGORY = new_id()
wxID_FMBUDDYLISTTBBUDDYLISTMNADDCOMPUTER = new_id()


class fmBuddyList(wx.Frame):

    def _init_coll_bsBuddyList_Items(self, parent):
        parent.Add(self.tcBuddyList, 1, border=0, flag=wx.EXPAND)

    def _init_coll_mnFile_Items(self, parent):
        parent.Append(wxID_FMBUDDYLISTMNFILEMNSIGNIN, 'Sign In', '')
        parent.Append(wxID_FMBUDDYLISTMNFILEMNSIGNOUT, 'Sign Out', '')
        parent.Append(wxID_FMBUDDYLISTMNFILEMNEXIT, 'Exit', '')
        self.Bind(wx.EVT_MENU, self.OnMnFileMnsignoutMenu,
              id=wxID_FMBUDDYLISTMNFILEMNSIGNOUT)
        self.Bind(wx.EVT_MENU, self.OnMnFileMnsigninMenu,
              id=wxID_FMBUDDYLISTMNFILEMNSIGNIN)
        self.Bind(wx.EVT_MENU, self.OnMnFileMnexitMenu,
              id=wxID_FMBUDDYLISTMNFILEMNEXIT)

    def _init_coll_mnComputer_Items(self, parent):
        parent.Append(wxID_FMBUDDYLISTMNCOMPUTERMNADDCOMPUTERS, 'Add computers', '')
        parent.Append(wxID_FMBUDDYLISTMNCOMPUTERMNDELETECOMPUTER, 'Delete a computer', '')
        parent.AppendSeparator()
        parent.Append(wxID_FMBUDDYLISTMNCOMPUTERMNCREATECATEGORY, 'Create a category', '')
        parent.Append(wxID_FMBUDDYLISTMNCOMPUTERMNEDITCATEGORY, 'Edit a category', '')
        parent.Append(wxID_FMBUDDYLISTMNCOMPUTERMNDELETECATEGORY, 'Delete a category', '')

    def _init_coll_mnHelp_Items(self, parent):
        parent.Append(wxID_FMBUDDYLISTMNHELPMNHELP, 'Help', '')
        parent.Append(wxID_FMBUDDYLISTMNHELPMNABOUT, 'About', '')
        self.Bind(wx.EVT_MENU, self.OnMnHelpMnhelpMenu,
              id=wxID_FMBUDDYLISTMNHELPMNHELP)
        self.Bind(wx.EVT_MENU, self.OnMnHelpMnaboutMenu,
              id=wxID_FMBUDDYLISTMNHELPMNABOUT)

    def _init_coll_mbMenu_Menus(self, parent):
        parent.Append(menu=self.mnFile, title='File')
        parent.Append(menu=self.mnComputer, title='Computer')
        parent.Append(menu=self.mnHelp, title='Help')

    def _init_coll_tbBuddyList_Tools(self, parent):
        parent.AddTool(wxID_FMBUDDYLISTTBBUDDYLISTMNADDCOMPUTER,
              'Add computer',
              wx.Bitmap('images/addcomputer.png', wx.BITMAP_TYPE_PNG),
              wx.NullBitmap,
              wx.ITEM_NORMAL, 'Add computer', 'Add computer')
        parent.AddTool(wxID_FMBUDDYLISTTBBUDDYLISTMNADDCATEGORY,
              'Add category',
              wx.Bitmap('images/addcategory.png', wx.BITMAP_TYPE_PNG),
              wx.NullBitmap,
              wx.ITEM_NORMAL, 'Add category', 'Add category')

        parent.Realize()

    def _init_sizers(self):
        self.bsBuddyList = wx.BoxSizer(orient=wx.VERTICAL)
        self._init_coll_bsBuddyList_Items(self.bsBuddyList)
        self.pnlBuddyList.SetSizer(self.bsBuddyList)

    def _init_utils(self):
        self.mbMenu = wx.MenuBar()
        self.mnFile = wx.Menu(title='')
        self.mnComputer = wx.Menu(title='')
        self.mnHelp = wx.Menu(title='')

        self._init_coll_mbMenu_Menus(self.mbMenu)
        self._init_coll_mnFile_Items(self.mnFile)
        self._init_coll_mnComputer_Items(self.mnComputer)
        self._init_coll_mnHelp_Items(self.mnHelp)

    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=wxID_FMBUDDYLIST, name='fmBuddyList',
              parent=prnt, pos=wx.DefaultPosition, size=wx.Size(300, 500),
              style=wx.DEFAULT_FRAME_STYLE, title='NeoRouter Network Explorer')
        self._init_utils()
        
        # Menu Bar
        self.SetMenuBar(self.mbMenu)
        self.SetStatusBarPane(0)
        self.SetIcon(wx.Icon('images/NRLogo.ico', wx.BITMAP_TYPE_ICO))
        self.SetHelpText('')
        self.Bind(wx.EVT_CLOSE, self.OnFmBuddyListClose)

        # Toolbar
        self.tbBuddyList = wx.ToolBar(id=wxID_FMBUDDYLISTTBBUDDYLIST,
              name='tbBuddyList', parent=self,
              style=wx.TB_HORIZONTAL | wx.NO_BORDER)
        self.tbBuddyList.SetToolPacking(1)
        self.tbBuddyList.SetToolTip('')
        self.SetToolBar(self.tbBuddyList)

        # Status Bar
        self.sbBuddyList = wx.StatusBar(id=wxID_FMBUDDYLISTSBBUDDYLIST,
              name='sbBuddyList', parent=self, style=wx.STB_SIZEGRIP)
        self.sbBuddyList.SetToolTip('')
        self.SetStatusBar(self.sbBuddyList)

        # Main Panel
        self.pnlBuddyList = wx.Panel(id=wxID_FMBUDDYLISTPNLBUDDYLIST,
              name='pnlBuddyList', parent=self, pos=wx.DefaultPosition,
              size=wx.DefaultSize, style=wx.TAB_TRAVERSAL)
        self.pnlBuddyList.SetToolTip('')

        # Tree Control
        self.tcBuddyList = wx.TreeCtrl(id=wxID_FMBUDDYLISTTCBUDDYLIST,
              name='tcBuddyList', parent=self.pnlBuddyList, pos=wx.DefaultPosition,
              size=wx.DefaultSize,
              style=wx.TR_HIDE_ROOT | wx.TR_NO_LINES | wx.TR_FULL_ROW_HIGHLIGHT)
        self.tcBuddyList.SetToolTip('')

        self._init_coll_tbBuddyList_Tools(self.tbBuddyList)
        self._init_sizers()
        
        # Ensure Panel fills Frame
        frameSizer = wx.BoxSizer(wx.VERTICAL)
        frameSizer.Add(self.pnlBuddyList, 1, wx.EXPAND)
        self.SetSizer(frameSizer)
        self.Layout()
        self.Center()


    def __init__(self, parent):
        self._init_ctrls(parent)

        self._init_tcBuddyList_()
        self._init_popupmenu_()
        self._init_cliwrapper_()

    def _init_tcBuddyList_(self):
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        self.idxArrayD = il.Add(wx.Bitmap('images/arrow_d.png', wx.BITMAP_TYPE_PNG), wx.GREEN)
        self.idxArrayR = il.Add(wx.Bitmap('images/arrow_r.png', wx.BITMAP_TYPE_PNG), wx.GREEN)
        self.idxWindowsE = il.Add(wx.Bitmap('images/windows_e.png', wx.BITMAP_TYPE_PNG), wx.GREEN)
        self.idxWindowsD = il.Add(wx.Bitmap('images/windows_d.png', wx.BITMAP_TYPE_PNG), wx.GREEN)
        self.idxComputerE = il.Add(wx.Bitmap('images/computer_e.png', wx.BITMAP_TYPE_PNG), wx.GREEN)
        self.idxComputerD = il.Add(wx.Bitmap('images/computer_d.png', wx.BITMAP_TYPE_PNG), wx.GREEN)
        self.idxMacE = il.Add(wx.Bitmap('images/mac_e.png', wx.BITMAP_TYPE_PNG), wx.GREEN)
        self.idxMacD = il.Add(wx.Bitmap('images/mac_d.png', wx.BITMAP_TYPE_PNG), wx.GREEN)
        self.idxLinuxE = il.Add(wx.Bitmap('images/linux_e.png', wx.BITMAP_TYPE_PNG), wx.GREEN)
        self.idxLinuxD = il.Add(wx.Bitmap('images/linux_d.png', wx.BITMAP_TYPE_PNG), wx.GREEN)
        self.tcBuddyList.SetImageList(il)
        self.il = il

        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tcBuddyList)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tcBuddyList)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tcBuddyList)
        self.tcBuddyList.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.tcBuddyList.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.item_selected = None

    def OnItemExpanded(self, event):
        item = event.GetItem()
        if item:
            pass

    def OnItemCollapsed(self, event):
        item = event.GetItem()
        if item:
            pass

    def OnSelChanged(self, event):
        self.item = event.GetItem()
        if self.item:
            pass
        event.Skip()

    def OnRightUp(self, event):
        pt = event.GetPosition()
        item, flags = self.tcBuddyList.HitTest(pt)
        if item and item.IsOk():
            if self._get_item_data(item) is not None:
                self.item_selected = item
                self.doPopupMenu(event.GetPosition())

    def OnRightDown(self, event):
        pt = event.GetPosition()
        item, flags = self.tcBuddyList.HitTest(pt)
        if item and item.IsOk():
            self.tcBuddyList.SelectItem(item)

    def OnFmBuddyListClose(self, event):
        self.doCLISignOut()
        time.sleep(1)
        event.Skip()

    def OnMnFileMnsignoutMenu(self, event):
        self.doCLISignOut()

    def OnMnFileMnsigninMenu(self, event):
        dlgLogon = Logon.create(self)
        result = dlgLogon.ShowModal()
        if result == wx.ID_OK:
            self.doCLISignIn(dlgLogon.getDomainName(), dlgLogon.getUserName(), dlgLogon.getPassword())
        dlgLogon.Destroy()

    def OnMnFileMnexitMenu(self, event):
        self.doCLISignOut()
        self.Close()

    def OnMnHelpMnhelpMenu(self, event):
        event.Skip()

    def OnMnHelpMnaboutMenu(self, event):
        wx.MessageBox("NRClientX \n\nv0.9.10\n\nCopyrigth(C) 2010 huhu.tiger", "About NRClientX", wx.OK | wx.ICON_INFORMATION, self)

    def PopulateBuddyList(self):
        self.tcBuddyList.DeleteAllItems()
        root = self.tcBuddyList.AddRoot("root")
        self.tcBuddyList.SetItemData(root, None)
        pclist = CLIWrapper.getBuddyList()

        groupItems = {}
        for obj in pclist:
            if obj.group not in groupItems:
                groupItems[obj.group] = self.tcBuddyList.AppendItem(root, obj.group)
                self.tcBuddyList.SetItemData(groupItems[obj.group], None)
                self.tcBuddyList.SetItemBold(groupItems[obj.group], True)
                self.tcBuddyList.SetItemImage(groupItems[obj.group], self.idxArrayR, wx.TreeItemIcon_Normal)
                self.tcBuddyList.SetItemImage(groupItems[obj.group], self.idxArrayD, wx.TreeItemIcon_Expanded)
            item = self.tcBuddyList.AppendItem(groupItems[obj.group], obj.ipAddress + ' - ' + obj.computerName)
            if obj.softwareEdition == 'W':
                if obj.ipAddress != '(offline)':
                    self.tcBuddyList.SetItemImage(item, self.idxWindowsE, wx.TreeItemIcon_Normal)
                else:
                    self.tcBuddyList.SetItemImage(item, self.idxWindowsD, wx.TreeItemIcon_Normal)
            elif obj.softwareEdition == 'M':
                if obj.ipAddress != '(offline)':
                    self.tcBuddyList.SetItemImage(item, self.idxMacE, wx.TreeItemIcon_Normal)
                else:
                    self.tcBuddyList.SetItemImage(item, self.idxMacD, wx.TreeItemIcon_Normal)
            elif obj.softwareEdition == 'L':
                if obj.ipAddress != '(offline)':
                    self.tcBuddyList.SetItemImage(item, self.idxLinuxE, wx.TreeItemIcon_Normal)
                else:
                    self.tcBuddyList.SetItemImage(item, self.idxLinuxD, wx.TreeItemIcon_Normal)
            elif obj.softwareEdition == 'O':
                if obj.ipAddress != '(offline)':
                    self.tcBuddyList.SetItemImage(item, self.idxComputerE, wx.TreeItemIcon_Normal)
                else:
                    self.tcBuddyList.SetItemImage(item, self.idxComputerD, wx.TreeItemIcon_Normal)

            self.tcBuddyList.SetItemData(item, obj)

        for (grp, item) in groupItems.items():
            self.tcBuddyList.Expand(item)

        if len(pclist) > 0:
            self.tcBuddyList.ScrollTo(groupItems[pclist[0].group])

        self.SetLabel(CLIWrapper.getLogonInfo())

    def _init_popupmenu_(self):
        for title in menu_titles:
            menu_title_by_id[wx.Window.NewControlId()] = title

        addon_menu_items.clear()
        menufile = "menu.def"
        if platform.system() == 'Windows':
            menufile = "menu_win.def"
        elif platform.system() == 'Linux':
            menufile = "menu_lin.def"
        elif platform.system() == 'Darwin':
            menufile = "menu_mac.def"
        try:
            with open(menufile, "r") as fileIN:
                for line in fileIN:
                    arr = line.split("=")
                    if len(arr) > 1:
                        addon_menu_items[arr[0]] = arr[1]
        except IOError:
            pass

    def doPopupMenu(self, pt):
        menu = wx.Menu()
        addon_menu_items_by_id.clear()

        for (itemid, title) in menu_title_by_id.items():
            item = menu.Append(itemid, title)
            self.Bind(wx.EVT_MENU, self.MenuSelectionCb, item)

        target = self.item_selected
        if target is not None:
            obj = self._get_item_data(target)
            if obj and obj.ipAddress != '(offline)':
                if len(addon_menu_items) > 0:
                    menu.AppendSeparator()
                    for (desc, cmd) in addon_menu_items.items():
                        itemid = wx.Window.NewControlId()
                        addon_menu_items_by_id[itemid] = cmd
                        item = menu.Append(itemid, desc)
                        self.Bind(wx.EVT_MENU, self.MenuSelectionCb, item)

        self.tcBuddyList.PopupMenu(menu, pt)
        menu.Destroy()

    def _get_item_data(self, item):
        data = self.tcBuddyList.GetItemData(item)
        return data

    def MenuSelectionCb(self, event):
        if event.GetId() in menu_title_by_id:
            operation = menu_title_by_id[event.GetId()]
            self.item_selected = None
            wx.MessageBox(operation)
        elif event.GetId() in addon_menu_items_by_id:
            operation = addon_menu_items_by_id[event.GetId()]
            target = self.item_selected
            if target is not None:
                obj = self._get_item_data(target)
                if obj is not None:
                    cmd = operation.strip(' ').strip('\n')
                    cmd = cmd.replace('%NRIPAddress%', obj.ipAddress)
                    self.process = wx.Process(self)
                    wx.Execute(cmd, wx.EXEC_ASYNC | wx.EXEC_NOHIDE, self.process)

    def doCLISignIn(self, domain, userName, password):
        if not self.worker:
            self.worker = CLIWrapper.WorkerThread(self, domain, userName, password)

    def doCLISignOut(self):
        if self.worker:
            self.worker.doSignOut()

    def _init_cliwrapper_(self):
        CLIWrapper.bind_cli_result(self, self.OnResult)
        self.worker = None

    def OnResult(self, event):
        code = event.data
        message = None
        if isinstance(event.data, tuple):
            code, message = event.data

        if code == CLIWrapper.ID_CLI_READY:
            self.PopulateBuddyList()

        if code == CLIWrapper.ID_CLI_ERROR:
            wx.MessageBox(message or "Error occurred while running CLI.")
            self.worker = None

        if code == CLIWrapper.ID_CLI_QUIT:
            self.worker = None
            self.tcBuddyList.DeleteAllItems()
            self.SetLabel("NeoRouter Network Explorer")
