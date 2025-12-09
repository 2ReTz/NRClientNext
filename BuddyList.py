#Boa:Frame:fmBuddyList

import platform
import time
import os

import wx
import wx.adv
import json

import CLIWrapper
import Logon
import themes
import ThemeDialog

menu_titles = ["Delete a Computer"]
menu_title_by_id = {}

addon_menu_items = {}
addon_menu_items_by_id = {}


def new_id():
    return wx.Window.NewControlId()


class CustomImagePanel(wx.Panel):
    def __init__(self, parent, theme_manager):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.config = {}
        self.load_config()

        # Create scrolled window for the image
        self.scrolled_win = wx.ScrolledWindow(self, style=wx.VSCROLL | wx.HSCROLL)
        self.scrolled_win.SetScrollRate(10, 10)

        # Static bitmap for images
        self.static_bitmap = wx.StaticBitmap(self.scrolled_win)

        # Animation control for GIFs
        self.animation_ctrl = wx.adv.AnimationCtrl(self.scrolled_win)
        self.animation_ctrl.Hide()

        # Sizer for the scrolled window
        # Sizer for the scrolled window
        scrolled_sizer = wx.BoxSizer(wx.VERTICAL)
        # Add stretchable space before
        scrolled_sizer.AddStretchSpacer(1)
        scrolled_sizer.Add(self.static_bitmap, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        scrolled_sizer.Add(self.animation_ctrl, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        # Add stretchable space after
        scrolled_sizer.AddStretchSpacer(1)
        self.scrolled_win.SetSizer(scrolled_sizer)

        # Main sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.scrolled_win, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # Drag and drop
        self.drop_target = CustomImageDropTarget(self)
        self.scrolled_win.SetDropTarget(self.drop_target)

        # Load initial image
        self.load_image()

        # Bind events
        self.Bind(wx.EVT_SIZE, self.on_size)

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.config = {
                    'enabled': config.get('custom_image_enabled', False),
                    'path': config.get('custom_image_path', ''),
                    'width': config.get('custom_image_width', 300),
                    'height': config.get('custom_image_height', 200),
                    'fit': config.get('custom_image_fit', True)
                }
            print(f"[DEBUG] CustomImagePanel.load_config: Loaded config: {self.config}")
        except Exception as e:
            print(f"Error loading custom image config: {e}")
            self.config = {'enabled': False, 'path': '', 'width': 300, 'height': 200, 'fit': True}
            print(f"[DEBUG] CustomImagePanel.load_config: Using default config: {self.config}")

    def save_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            config.update({
                'custom_image_enabled': self.config['enabled'],
                'custom_image_path': self.config['path'],
                'custom_image_width': self.config['width'],
                'custom_image_height': self.config['height'],
                'custom_image_fit': self.config['fit']
            })
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            print(f"[DEBUG] CustomImagePanel.save_config: Saved config: {self.config}")
        except Exception as e:
            print(f"Error saving custom image config: {e}")
            print(f"[DEBUG] CustomImagePanel.save_config: Failed to save config: {self.config}")

    def get_target_size(self, img):
        if self.config['fit']:
            client_size = self.scrolled_win.GetClientSize()
            available_width = client_size.width - 20
            available_height = client_size.height - 20
            if available_width <= 0 or available_height <= 0:
                return img.GetWidth(), img.GetHeight()
            return available_width, available_height

        width = max(self.config.get('width', img.GetWidth()), 1)
        height = max(self.config.get('height', img.GetHeight()), 1)
        return width, height

    def load_image(self):
        print(f"[DEBUG] CustomImagePanel.load_image: Starting load with config: enabled={self.config['enabled']}, path='{self.config['path']}'")
        
        if not self.config['enabled'] or not self.config['path']:
            print(f"[DEBUG] CustomImagePanel.load_image: Disabled or no path, clearing image")
            self.static_bitmap.SetBitmap(wx.NullBitmap)
            self.animation_ctrl.Stop()
            self.animation_ctrl.Hide()
            self.static_bitmap.Hide()
            return

        # Normalize the path and check existence
        image_path = self.config['path']
        if not os.path.isabs(image_path):
            # If it's a relative path, make it relative to the app directory
            image_path = os.path.join(os.getcwd(), image_path)
            print(f"[DEBUG] CustomImagePanel.load_image: Normalized path: {image_path}")
        
        if not os.path.exists(image_path):
            print(f"[DEBUG] CustomImagePanel.load_image: File not found: {image_path}")
            wx.MessageBox(f"Image not found:\n{self.config['path']}\n\nTried: {image_path}", "Error", wx.OK | wx.ICON_ERROR)
            self.static_bitmap.SetBitmap(wx.NullBitmap)
            self.animation_ctrl.Stop()
            self.animation_ctrl.Hide()
            self.static_bitmap.Hide()
            return

        try:
            _, ext = os.path.splitext(image_path)
            print(f"[DEBUG] CustomImagePanel.load_image: Loading file with extension: {ext}")
            
            if ext.lower() == '.gif':
                animation = wx.adv.Animation(image_path)
                if animation.IsOk():
                    print(f"[DEBUG] CustomImagePanel.load_image: GIF loaded successfully as animation")
                    self.animation_ctrl.SetAnimation(animation)
                    self.animation_ctrl.SetMinSize(animation.GetSize())
                    self.scrolled_win.SetVirtualSize(animation.GetSize())
                    self.animation_ctrl.Play()
                    self.animation_ctrl.Show()
                    self.static_bitmap.Hide()
                else:
                    print(f"[DEBUG] CustomImagePanel.load_image: GIF not animated, falling back to static")
                    # Fallback to static load if GIF isn't animated/parsable
                    img = wx.Image(image_path)
                    if not img.IsOk():
                        raise Exception("Invalid GIF image")
                    target_width, target_height = self.get_target_size(img)
                    if target_width != img.GetWidth() or target_height != img.GetHeight():
                        img = img.Scale(target_width, target_height, wx.IMAGE_QUALITY_HIGH)
                    bitmap = wx.Bitmap(img)
                    self.static_bitmap.SetBitmap(bitmap)
                    self.static_bitmap.Show()
                    self.animation_ctrl.Stop()
                    self.animation_ctrl.Hide()
                    self.scrolled_win.SetVirtualSize(bitmap.GetWidth(), bitmap.GetHeight())
            else:
                # Load as static image
                print(f"[DEBUG] CustomImagePanel.load_image: Loading as static image")
                img = wx.Image(image_path)
                if img.IsOk():
                    target_width, target_height = self.get_target_size(img)
                    print(f"[DEBUG] CustomImagePanel.load_image: Original size: {img.GetWidth()}x{img.GetHeight()}, Target size: {target_width}x{target_height}")
                    if target_width != img.GetWidth() or target_height != img.GetHeight():
                        img = img.Scale(target_width, target_height, wx.IMAGE_QUALITY_HIGH)
                    bitmap = wx.Bitmap(img)
                    self.static_bitmap.SetBitmap(bitmap)
                    self.static_bitmap.Show()
                    self.animation_ctrl.Stop()
                    self.animation_ctrl.Hide()
                    # Set virtual size for scrolling
                    self.scrolled_win.SetVirtualSize(bitmap.GetWidth(), bitmap.GetHeight())
                    print(f"[DEBUG] CustomImagePanel.load_image: Static image loaded and displayed")
                else:
                    raise Exception("Invalid image")
            self.scrolled_win.Layout()
            self.Layout()
            print(f"[DEBUG] CustomImagePanel.load_image: Image loading completed successfully")
        except Exception as e:
            print(f"Error loading image {self.config['path']}: {e}")
            print(f"[DEBUG] CustomImagePanel.load_image: Exception during image loading: {e}")
            wx.MessageBox(f"Failed to load image: {self.config['path']}\n\nError: {e}", "Error", wx.OK | wx.ICON_ERROR)
            self.static_bitmap.SetBitmap(wx.NullBitmap)
            self.animation_ctrl.Stop()
            self.animation_ctrl.Hide()

    def set_image_path(self, path):
        print(f"[DEBUG] CustomImagePanel.set_image_path: Setting path to '{path}'")
        self.config['path'] = path
        self.save_config()
        self.load_image()

    def toggle_enabled(self):
        print(f"[DEBUG] CustomImagePanel.toggle_enabled: Toggling enabled from {self.config['enabled']} to {not self.config['enabled']}")
        self.config['enabled'] = not self.config['enabled']
        self.save_config()
        self.load_image()

    def apply_theme(self):
        theme = self.theme_manager.get_theme()
        self.theme_manager.apply_theme_to_custom_image_panel(self, theme)
        self.theme_manager.apply_theme_to_custom_image_panel(self.scrolled_win, theme)

    def on_size(self, event):
        if self.config['fit']:
            self.load_image()  # Reload to fit new size
        event.Skip()


class CustomImageDropTarget(wx.FileDropTarget):
    def __init__(self, panel):
        super().__init__()
        self.panel = panel

    def OnDropFiles(self, x, y, filenames):
        if filenames:
            path = filenames[0]
            ext = path.lower().split('.')[-1]
            if ext in ['png', 'jpg', 'jpeg', 'bmp', 'gif']:
                self.panel.config['enabled'] = True
                self.panel.set_image_path(path)
            else:
                wx.MessageBox("Unsupported file type. Supported: PNG, JPG, BMP, GIF", "Error", wx.OK | wx.ICON_ERROR)
        return True


class CustomImageDialog(wx.Dialog):
    def __init__(self, parent, custom_panel):
        super().__init__(parent, title="Custom Image Settings", size=(400, 300))
        self.custom_panel = custom_panel
        self.InitUI()
        self.Centre()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Enable checkbox
        self.enable_cb = wx.CheckBox(panel, label="Enable custom image display")
        self.enable_cb.SetValue(self.custom_panel.config['enabled'])
        self.enable_cb.Bind(wx.EVT_CHECKBOX, self.OnEnableChanged)
        vbox.Add(self.enable_cb, 0, wx.ALL, 10)

        # File selection
        file_box = wx.StaticBox(panel, label="Image File")
        file_sizer = wx.StaticBoxSizer(file_box, wx.HORIZONTAL)

        self.file_tc = wx.TextCtrl(panel, value=str(self.custom_panel.config.get('path', '')))
        browse_btn = wx.Button(panel, label="Browse...")
        browse_btn.Bind(wx.EVT_BUTTON, self.OnBrowse)

        file_sizer.Add(self.file_tc, 1, wx.ALL | wx.EXPAND, 5)
        file_sizer.Add(browse_btn, 0, wx.ALL, 5)
        vbox.Add(file_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # Dimensions
        dim_box = wx.StaticBox(panel, label="Dimensions")
        dim_sizer = wx.StaticBoxSizer(dim_box, wx.VERTICAL)

        grid_sizer = wx.FlexGridSizer(2, 2, 5, 5)

        grid_sizer.Add(wx.StaticText(panel, label="Width:"))
        self.width_spin = wx.SpinCtrl(panel, value=str(self.custom_panel.config['width']), min=50, max=2000)
        grid_sizer.Add(self.width_spin)

        grid_sizer.Add(wx.StaticText(panel, label="Height:"))
        self.height_spin = wx.SpinCtrl(panel, value=str(self.custom_panel.config['height']), min=50, max=2000)
        grid_sizer.Add(self.height_spin)

        dim_sizer.Add(grid_sizer, 0, wx.ALL, 5)

        # Fit checkbox
        self.fit_cb = wx.CheckBox(panel, label="Fit to panel size")
        self.fit_cb.SetValue(self.custom_panel.config['fit'])
        dim_sizer.Add(self.fit_cb, 0, wx.ALL, 5)

        vbox.Add(dim_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        apply_btn = wx.Button(panel, id=wx.ID_OK, label="Apply")
        apply_btn.SetDefault()
        apply_btn.Bind(wx.EVT_BUTTON, self.OnApply)
        cancel_btn = wx.Button(panel, id=wx.ID_CANCEL, label="Cancel")
        cancel_btn.Bind(wx.EVT_BUTTON, self.OnCancel)

        btn_sizer.Add(apply_btn, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)

        vbox.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizer(vbox)
        # Initial enable/disable to reflect current state
        self.OnEnableChanged(None)

    def OnEnableChanged(self, event):
        enabled = self.enable_cb.GetValue()
        self.file_tc.Enable(enabled)
        self.width_spin.Enable(enabled)
        self.height_spin.Enable(enabled)
        self.fit_cb.Enable(enabled)

    def apply_changes(self):
        print(f"[DEBUG] CustomImageDialog.apply_changes: Applying changes")
        self.custom_panel.config['enabled'] = self.enable_cb.GetValue()
        self.custom_panel.config['path'] = self.file_tc.GetValue()
        self.custom_panel.config['width'] = self.width_spin.GetValue()
        self.custom_panel.config['height'] = self.height_spin.GetValue()
        self.custom_panel.config['fit'] = self.fit_cb.GetValue()
        print(f"[DEBUG] CustomImageDialog.apply_changes: New config: enabled={self.custom_panel.config['enabled']}, path='{self.custom_panel.config['path']}', width={self.custom_panel.config['width']}, height={self.custom_panel.config['height']}, fit={self.custom_panel.config['fit']}")
        self.custom_panel.save_config()
        self.custom_panel.load_image()
        print(f"[DEBUG] CustomImageDialog.apply_changes: Changes applied successfully")

    def OnBrowse(self, event):
        print(f"[DEBUG] CustomImageDialog.OnBrowse: Opening file dialog")
        with wx.FileDialog(self, "Choose image file", wildcard="Image files (*.png;*.jpg;*.jpeg;*.bmp;*.gif)|*.png;*.jpg;*.jpeg;*.bmp;*.gif",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                print(f"[DEBUG] CustomImageDialog.OnBrowse: File dialog cancelled")
                return
            path = fileDialog.GetPath()
            print(f"[DEBUG] CustomImageDialog.OnBrowse: Selected file (absolute): {path}")
            
            # Convert absolute path to relative path if it's within the application directory
            current_dir = os.getcwd()
            if path.startswith(current_dir):
                # Remove the current directory and leading separator to get relative path
                relative_path = os.path.relpath(path, current_dir)
                print(f"[DEBUG] CustomImageDialog.OnBrowse: Converted to relative path: {relative_path}")
                self.file_tc.SetValue(relative_path)
            else:
                # Keep absolute path if it's outside the application directory
                print(f"[DEBUG] CustomImageDialog.OnBrowse: Keeping absolute path (outside app dir)")
                self.file_tc.SetValue(path)

    def OnApply(self, event):
        print(f"[DEBUG] CustomImageDialog.OnApply: Apply button clicked")
        self.apply_changes()
        
        # Force a refresh of the parent layout
        if self.custom_panel:
            self.custom_panel.Layout()
            self.custom_panel.Refresh()
            self.custom_panel.Update()
            
        if self.IsModal():
            print(f"[DEBUG] CustomImageDialog.OnApply: Ending modal with OK")
            self.EndModal(wx.ID_OK)
        else:
            print(f"[DEBUG] CustomImageDialog.OnApply: Closing dialog")
            self.Close()

    def OnCancel(self, event):
        print(f"[DEBUG] CustomImageDialog.OnCancel: Cancel button clicked")
        self.EndModal(wx.ID_CANCEL)


def create(parent):
    return fmBuddyList(parent)


wxID_FMBUDDYLIST = wx.ID_ANY
wxID_FMBUDDYLISTPNLBUDDYLIST = wx.ID_ANY
wxID_FMBUDDYLISTSBBUDDYLIST = wx.ID_ANY
wxID_FMBUDDYLISTTBBUDDYLIST = wx.ID_ANY
wxID_FMBUDDYLISTTCBUDDYLIST = wx.ID_ANY
wxID_FMBUDDYLISTPNLCUSTOMIMAGE = wx.ID_ANY

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
wxID_FMBUDDYLISTMNHELPMNTHEMES = new_id()
wxID_FMBUDDYLISTMNHELPMNCUSTOMIMAGE = new_id()

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
        parent.Append(wxID_FMBUDDYLISTMNHELPMNTHEMES, 'Themes', '')
        parent.Append(wxID_FMBUDDYLISTMNHELPMNCUSTOMIMAGE, 'Custom Image', '')
        self.Bind(wx.EVT_MENU, self.OnMnHelpMnhelpMenu,
              id=wxID_FMBUDDYLISTMNHELPMNHELP)
        self.Bind(wx.EVT_MENU, self.OnMnHelpMnaboutMenu,
              id=wxID_FMBUDDYLISTMNHELPMNABOUT)
        self.Bind(wx.EVT_MENU, self.OnMnHelpMnthemesMenu,
              id=wxID_FMBUDDYLISTMNHELPMNTHEMES)
        self.Bind(wx.EVT_MENU, self.OnMnHelpMncustomimageMenu,
              id=wxID_FMBUDDYLISTMNHELPMNCUSTOMIMAGE)

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

        # Custom Image Panel
        self.pnlCustomImage = CustomImagePanel(parent=self, theme_manager=themes.theme_manager)
        self.pnlCustomImage.SetMinSize((-1, 200))  # Default height

        self._init_coll_tbBuddyList_Tools(self.tbBuddyList)
        self._init_sizers()
        
        # Ensure Panels fill Frame
        frameSizer = wx.BoxSizer(wx.VERTICAL)
        frameSizer.Add(self.pnlBuddyList, 1, wx.EXPAND)
        frameSizer.Add(self.pnlCustomImage, 0, wx.EXPAND)
        self.SetSizer(frameSizer)
        self.Layout()
        self.Center()


    def __init__(self, parent):
        self._init_ctrls(parent)

        self._init_tcBuddyList_()
        self._init_popupmenu_()
        self._init_cliwrapper_()
        self.ApplyTheme()

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

    def OnMnHelpMnthemesMenu(self, event):
        dlg = ThemeDialog.ThemeDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            self.ApplyTheme()
        dlg.Destroy()

    def OnMnHelpMncustomimageMenu(self, event):
        dlg = CustomImageDialog(self, self.pnlCustomImage)
        if dlg.ShowModal() == wx.ID_OK:
            # Apply theme if needed, but it's already done in load_image
            pass
        dlg.Destroy()

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
        # Don't pre-generate IDs for standard items here
        
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
        
        # 1. Standard Items: Generate fresh IDs every time
        menu_title_by_id.clear()
        for title in menu_titles:
            itemid = wx.Window.NewControlId()
            menu_title_by_id[itemid] = title
            item = menu.Append(itemid, title)
            self.Bind(wx.EVT_MENU, self.MenuSelectionCb, item)

        # 2. Addon Items: Generate fresh IDs every time (already doing this, but ensure consistency)
        addon_menu_items_by_id.clear()
        
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
                    wx.Execute(cmd, wx.EXEC_ASYNC, self.process)

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

    def ApplyTheme(self):
        theme = themes.theme_manager.get_theme()

        # Apply to frame
        themes.theme_manager.apply_theme_to_frame(self, theme)

        # Apply to panel
        themes.theme_manager.apply_theme_to_panel(self.pnlBuddyList, theme)

        # Apply to tree control
        themes.theme_manager.apply_theme_to_tree(self.tcBuddyList, theme)

        # Apply to toolbar
        themes.theme_manager.apply_theme_to_toolbar(self.tbBuddyList, theme)

        # Apply to status bar
        themes.theme_manager.apply_theme_to_statusbar(self.sbBuddyList, theme)

        # Apply to custom image panel
        self.pnlCustomImage.apply_theme()

        # Refresh the entire frame
        self.Refresh()
        self.Layout()
