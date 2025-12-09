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
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGLOGON, name='dlgLogon', parent=prnt,
              pos=wx.Point(499, 300), size=wx.Size(313, 217),
              style=wx.DEFAULT_DIALOG_STYLE,
              title='NeoRouter Network Explorer')
        self.SetClientSize(wx.Size(305, 183))
        self.SetToolTip('')
        self.SetWindowVariant(wx.WINDOW_VARIANT_NORMAL)

        self.sbSignIn = wx.StaticBox(id=wxID_DLGLOGONSBSIGNIN, label='Sign In',
              name='sbSignIn', parent=self, pos=wx.Point(8, 8),
              size=wx.Size(288, 128), style=0)

        self.lblUserName = wx.StaticText(id=wxID_DLGLOGONLBLUSERNAME,
              label='User name:', name='lblUserName', parent=self,
              pos=wx.Point(24, 32), size=wx.Size(55, 13), style=0)

        self.lblPassword = wx.StaticText(id=wxID_DLGLOGONLBLPASSWORD,
              label='Password:', name='lblPassword', parent=self,
              pos=wx.Point(24, 64), size=wx.Size(50, 13), style=0)

        self.lblLogonto = wx.StaticText(id=wxID_DLGLOGONLBLLOGONTO,
              label='Log on to:', name='lblLogonto', parent=self,
              pos=wx.Point(24, 96), size=wx.Size(49, 13), style=0)

        self.txtUserName = wx.TextCtrl(id=wxID_DLGLOGONTXTUSERNAME,
              name='txtUserName', parent=self, pos=wx.Point(96, 32),
              size=wx.Size(184, 21), style=0, value='')
        self.txtUserName.SetToolTip('User Name')

        self.txtPassword = wx.TextCtrl(id=wxID_DLGLOGONTXTPASSWORD,
              name='txtPassword', parent=self, pos=wx.Point(96, 64),
              size=wx.Size(184, 21), style=wx.TE_PASSWORD, value='')
        self.txtPassword.SetToolTip('Password')

        self.txtLogonto = wx.TextCtrl(id=wxID_DLGLOGONTXTLOGONTO,
              name='txtLogonto', parent=self, pos=wx.Point(96, 96),
              size=wx.Size(184, 21), style=0, value='')
        self.txtLogonto.SetToolTip('Domain Name')

        self.btnSignIn = wx.Button(id=wxID_DLGLOGONBTNSIGNIN, label='Sign In',
              name='btnSignIn', parent=self, pos=wx.Point(64, 152),
              size=wx.Size(75, 23), style=0)
        self.btnSignIn.SetDefault()
        self.btnSignIn.Bind(wx.EVT_BUTTON, self.OnBtnSignInButton,
              id=wxID_DLGLOGONBTNSIGNIN)

        self.btnCancel = wx.Button(id=wxID_DLGLOGONBTNCANCEL, label='Cancel',
              name='btnCancel', parent=self, pos=wx.Point(176, 152),
              size=wx.Size(75, 23), style=0)
        self.btnCancel.Bind(wx.EVT_BUTTON, self.OnBtnCancelButton,
              id=wxID_DLGLOGONBTNCANCEL)

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
