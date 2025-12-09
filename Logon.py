#Boa:Dialog:dlgLogon

import json
from pathlib import Path

import wx

CONFIG_PATH = Path(__file__).with_name("connection.json")

def new_id():
    return wx.Window.NewControlId()

def create(parent):
    return dlgLogon(parent)

wxID_DLGLOGON = wx.ID_ANY
wxID_DLGLOGONBTNCANCEL = wx.ID_CANCEL
wxID_DLGLOGONBTNSIGNIN = wx.ID_OK
wxID_DLGLOGONLBLLOGONTO = wx.ID_ANY
wxID_DLGLOGONLBLPASSWORD = wx.ID_ANY
wxID_DLGLOGONLBLUSERNAME = wx.ID_ANY
wxID_DLGLOGONSBSIGNIN = wx.ID_ANY
wxID_DLGLOGONTXTLOGONTO = wx.ID_ANY
wxID_DLGLOGONTXTPASSWORD = wx.ID_ANY
wxID_DLGLOGONTXTUSERNAME = wx.ID_ANY

class dlgLogon(wx.Dialog):
    def _init_ctrls(self, prnt):
        wx.Dialog.__init__(self, id=wxID_DLGLOGON, name='dlgLogon', parent=prnt,
              pos=wx.DefaultPosition, size=wx.DefaultSize,
              style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
              title='NeoRouter Network Explorer')
        
        # Main Sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.sbSignIn = wx.StaticBox(id=wxID_DLGLOGONSBSIGNIN, label='Sign In',
              name='sbSignIn', parent=self, style=0)
        
        # Static Box Sizer to contain the form inside the StaticBox
        sbSizer = wx.StaticBoxSizer(self.sbSignIn, wx.VERTICAL)
        
        # Grid Sizer for Form (Label + Input pairs)
        gridSizer = wx.FlexGridSizer(rows=3, cols=2, vgap=10, hgap=10)
        gridSizer.AddGrowableCol(1) # Second column (inputs) grows

        # Row 1: User Name
        self.lblUserName = wx.StaticText(id=wxID_DLGLOGONLBLUSERNAME,
              label='User name:', name='lblUserName', parent=self, style=0)
        self.txtUserName = wx.TextCtrl(id=wxID_DLGLOGONTXTUSERNAME,
              name='txtUserName', parent=self, style=0, value='')
        self.txtUserName.SetToolTip('User Name')
        
        gridSizer.Add(self.lblUserName, 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(self.txtUserName, 1, wx.EXPAND)

        # Row 2: Password
        self.lblPassword = wx.StaticText(id=wxID_DLGLOGONLBLPASSWORD,
              label='Password:', name='lblPassword', parent=self, style=0)
        self.txtPassword = wx.TextCtrl(id=wxID_DLGLOGONTXTPASSWORD,
              name='txtPassword', parent=self, style=wx.TE_PASSWORD, value='')
        self.txtPassword.SetToolTip('Password')

        gridSizer.Add(self.lblPassword, 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(self.txtPassword, 1, wx.EXPAND)

        # Row 3: Log on to (Domain)
        self.lblLogonto = wx.StaticText(id=wxID_DLGLOGONLBLLOGONTO,
              label='Log on to:', name='lblLogonto', parent=self, style=0)
        self.txtLogonto = wx.TextCtrl(id=wxID_DLGLOGONTXTLOGONTO,
              name='txtLogonto', parent=self, style=0, value='')
        self.txtLogonto.SetToolTip('Domain Name')

        gridSizer.Add(self.lblLogonto, 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(self.txtLogonto, 1, wx.EXPAND)

        # Add Grid to StaticBoxSizer
        sbSizer.Add(gridSizer, 1, wx.EXPAND | wx.ALL, 10)
        
        # Add StaticBoxSizer to Main Sizer
        mainSizer.Add(sbSizer, 1, wx.EXPAND | wx.ALL, 10)

        # Button Sizer
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.btnSignIn = wx.Button(id=wxID_DLGLOGONBTNSIGNIN, label='Sign In',
              name='btnSignIn', parent=self, style=0)
        self.btnSignIn.SetDefault()
        self.btnSignIn.Bind(wx.EVT_BUTTON, self.OnBtnSignInButton,
              id=wxID_DLGLOGONBTNSIGNIN)

        self.btnCancel = wx.Button(id=wxID_DLGLOGONBTNCANCEL, label='Cancel',
              name='btnCancel', parent=self, style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGLOGONBTNCANCEL)
              
        btnSizer.Add(self.btnSignIn, 0, wx.RIGHT, 10)
        btnSizer.Add(self.btnCancel, 0)

        # Add Button Sizer to Main Sizer
        mainSizer.Add(btnSizer, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 10)

        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()
        self.Center()


    def __init__(self, parent):
        self.userName = ''
        self.password = ''
        self.domainName = ''
        self._init_ctrls(parent)
        self._load_saved_values()

    def getUserName(self):
        return self.userName

    def getPassword(self):
        return self.password

    def getDomainName(self):
        return self.domainName

    def OnBtnSignInButton(self, event):
        self.userName = self.txtUserName.GetValue()
        self.password = self.txtPassword.GetValue()
        self.domainName = self.txtLogonto.GetValue()
        self._persist_values()
        self.EndModal(wx.ID_OK)

    def OnBtnCancelButton(self, event):
        self.EndModal(wx.ID_CANCEL)

    def _load_saved_values(self):
        if CONFIG_PATH.exists():
            try:
                data = json.loads(CONFIG_PATH.read_text())
                self.txtUserName.SetValue(data.get("username", ""))
                self.txtPassword.SetValue(data.get("password", ""))
                self.txtLogonto.SetValue(data.get("domain", ""))
            except Exception:
                pass

    def _persist_values(self):
        data = {
            "username": self.userName,
            "password": self.password,
            "domain": self.domainName,
        }
        try:
            CONFIG_PATH.write_text(json.dumps(data))
        except Exception:
            pass
