import os
import platform
import queue
import shutil
import subprocess
import time
from threading import Thread

import wx

#Messages sent to UI
ID_CLI_READY = wx.Window.NewControlId()
ID_CLI_QUIT = wx.Window.NewControlId()
ID_CLI_ERROR = wx.Window.NewControlId()
#CLI commands
ID_CMD_SIGNOUT = wx.Window.NewControlId()

CLIProcess = None
logon_info = None

class objComputer:
    def __init__(self, group, ipAddress, computerName, softwareEdition):
        self.group = group
        self.ipAddress = ipAddress
        self.computerName = computerName
        self.softwareEdition = softwareEdition


objComputerList = []


def getBuddyList():
    global objComputerList
    return objComputerList


def getLogonInfo():
    global logon_info
    if logon_info is None:
        logon_info = "NeoRouter Network Explorer"
    return logon_info


EVT_RESULT_TYPE = wx.NewEventType()
EVT_RESULT_BINDER = wx.PyEventBinder(EVT_RESULT_TYPE, 1)


def bind_cli_result(win, func):
    win.Bind(EVT_RESULT_BINDER, func)


class ResultEvent(wx.PyCommandEvent):
    def __init__(self, data=None):
        super().__init__(EVT_RESULT_TYPE, -1)
        self.data = data


class WorkerThread(Thread):
    def __init__(self, notify_window, domain, userName, password):
        Thread.__init__(self)
        # private
        self._notify_window = notify_window
        self._want_abort = 0
        self._domain = domain
        self._userName = userName
        self._password = password

        self.task_queue = queue.Queue()
        self.start()

    def run(self):
        global objComputerList
        global CLIProcess

        signin_status = 0
        mode = 0
        count = 0
        title = ''
        item = ''
        tag = ''
        group = ''
        ipAddress = ''
        computerName = ''
        edition = ''

        if platform.system() == 'Darwin':
            nrclientcmdpath = "/Library/NeoRouter/nrclientcmd"
        else:
            nrclientcmdpath = shutil.which("nrclientcmd") or "nrclientcmd"
            if nrclientcmdpath == "nrclientcmd":
                default_paths = [
                    r"C:\Program Files\NeoRouter\nrclientcmd.exe",
                    r"C:\Program Files (x86)\NeoRouter\nrclientcmd.exe",
                    r"C:\Program Files (x86)\ZebraNetworkSystems\NeoRouter\NRClientCmd.exe",
                ]
                for p in default_paths:
                    if shutil.which(p) or os.path.exists(p):
                        nrclientcmdpath = p
                        break
        try:
            CLIProcess = subprocess.Popen(
                [nrclientcmdpath, "-internal", "-d", self._domain, "-u", self._userName, "-p", self._password],
                shell=False,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
            )
        except FileNotFoundError:
            CLIProcess = None
            wx.PostEvent(
                self._notify_window,
                ResultEvent((ID_CLI_ERROR, f"nrclientcmd not found (tried '{nrclientcmdpath}')")),
            )
            return
        while True:
            newline = CLIProcess.stdout.readline()
            if not newline:
                print('====Print all====')
                print('Title:', title)
                for index, obj in enumerate(objComputerList):
                    print(index, '->', obj.group, '|', obj.softwareEdition, '|', obj.ipAddress, '|', obj.computerName)
                # CLIProcess closed
                CLIProcess = None
                wx.PostEvent(self._notify_window, ResultEvent(ID_CLI_QUIT))
                break
            output = newline.replace('\n', '').strip()
            count = count + 1
            # print count, output
            if len(output) > 0:
                if output[0] == '$':
                    # List gets refreshed
                    signin_status = 1
                    wx.PostEvent(self._notify_window, ResultEvent(ID_CLI_READY))
                elif output[0] == '?':
                    CLIProcess.stdin.write('cancel\n')
                    CLIProcess.stdin.flush()
                    wx.PostEvent(self._notify_window, ResultEvent(ID_CLI_ERROR))
                elif output[0] == '#':
                    mode = (mode + 1) % 3
                else:
                    # Parse Title
                    if mode == 1:
                        title = output.replace('\n', '')
                        global logon_info
                        logon_info = title.replace('NeoRouter Network Explorer - ', '')
                        del objComputerList[0:]
                    # Parse list
                    elif mode == 2:
                        item = output.replace('\n', '')
                        tag = item[0:1]
                        if tag[0] == '>':
                            # parse group name
                            group = item[2:].strip()
                        else:
                            # parse computer information
                            edition = item[0]
                            ipAddress = item[2:17].strip()
                            computerName = item[18:].strip()
                            x = objComputer(group, ipAddress, computerName, edition)
                            objComputerList.append(x)
        # not signed in yet
        if signin_status == 0:
            wx.PostEvent(self._notify_window, ResultEvent(ID_CLI_ERROR))

    def abort(self):
        self._want_abort = 1

    def getTask(self):
        try:
            i = self.task_queue.get(True)
        except queue.Empty:
            i = None
        return i

    def doSignOut(self):
        global CLIProcess
        self.task_queue.put('quit')
        task = self.getTask()
        if CLIProcess and CLIProcess.stdin:
            CLIProcess.stdin.write(f'{task}\n')
            CLIProcess.stdin.flush()
