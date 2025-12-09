import wx
import themes

class ThemeDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Theme Settings", size=(400, 500))

        self.theme_manager = themes.theme_manager
        self.selected_theme = self.theme_manager.current_theme

        self.InitUI()
        self.LoadThemes()
        self.Centre()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Theme selection
        theme_box = wx.StaticBox(panel, label="Select Theme")
        theme_sizer = wx.StaticBoxSizer(theme_box, wx.VERTICAL)

        self.theme_choice = wx.Choice(panel, choices=[])
        self.theme_choice.Bind(wx.EVT_CHOICE, self.OnThemeChoice)
        theme_sizer.Add(self.theme_choice, 0, wx.ALL | wx.EXPAND, 5)

        # Color settings
        colors_box = wx.StaticBox(panel, label="Customize Colors")
        colors_sizer = wx.StaticBoxSizer(colors_box, wx.VERTICAL)

        self.color_controls = {}
        color_labels = [
            ('bg_color', 'Background Color'),
            ('fg_color', 'Foreground Color'),
            ('panel_bg', 'Panel Background'),
            ('tree_bg', 'Tree Background'),
            ('status_bg', 'Status Bar Background'),
            ('toolbar_bg', 'Toolbar Background'),
            ('menu_bg', 'Menu Background'),
            ('selected_bg', 'Selected Item Background'),
            ('selected_fg', 'Selected Item Foreground')
        ]

        grid_sizer = wx.GridSizer(3, 2, 5, 5)  # 3 columns, but we'll adjust

        for key, label in color_labels:
            lbl = wx.StaticText(panel, label=label)
            btn = wx.Button(panel, label="Choose")
            btn.Bind(wx.EVT_BUTTON, lambda evt, k=key: self.OnChooseColor(evt, k))
            self.color_controls[key] = (lbl, btn)
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(lbl, 1, wx.ALIGN_CENTER_VERTICAL)
            hbox.Add(btn, 0)
            colors_sizer.Add(hbox, 0, wx.ALL | wx.EXPAND, 2)

        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        save_btn = wx.Button(panel, label="Save Custom Theme")
        save_btn.Bind(wx.EVT_BUTTON, self.OnSaveCustom)
        apply_btn = wx.Button(panel, label="Apply")
        apply_btn.Bind(wx.EVT_BUTTON, self.OnApply)
        cancel_btn = wx.Button(panel, label="Cancel")
        cancel_btn.Bind(wx.EVT_BUTTON, self.OnCancel)

        btn_sizer.Add(save_btn, 0, wx.ALL, 5)
        btn_sizer.Add(apply_btn, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)

        vbox.Add(theme_sizer, 0, wx.ALL | wx.EXPAND, 10)
        vbox.Add(colors_sizer, 1, wx.ALL | wx.EXPAND, 10)
        vbox.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizer(vbox)

    def LoadThemes(self):
        self.theme_choice.Clear()
        for theme_name in self.theme_manager.themes.keys():
            self.theme_choice.Append(theme_name)
        if self.selected_theme in self.theme_manager.themes:
            self.theme_choice.SetStringSelection(self.selected_theme)
        self.UpdateColorControls()

    def UpdateColorControls(self):
        theme = self.theme_manager.get_theme(self.selected_theme)
        for key, (lbl, btn) in self.color_controls.items():
            color = theme.get(key, '#FFFFFF')
            btn.SetBackgroundColour(wx.Colour(color))

    def OnThemeChoice(self, event):
        self.selected_theme = self.theme_choice.GetStringSelection()
        self.UpdateColorControls()

    def OnChooseColor(self, event, key):
        theme = self.theme_manager.get_theme(self.selected_theme)
        current_color = wx.Colour(theme.get(key, '#FFFFFF'))
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetColour(current_color)
        if dlg.ShowModal() == wx.ID_OK:
            color = dlg.GetColourData().GetColour()
            hex_color = color.GetAsString(wx.C_ALPHA_HEX)
            # Update the theme temporarily
            self.theme_manager.themes[self.selected_theme][key] = hex_color
            self.UpdateColorControls()
        dlg.Destroy()

    def OnSaveCustom(self, event):
        dlg = wx.TextEntryDialog(self, "Enter theme name:", "Save Custom Theme")
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            if name and name not in self.theme_manager.themes:
                self.theme_manager.add_custom_theme(name, self.theme_manager.themes[self.selected_theme].copy())
                self.LoadThemes()
                self.theme_choice.SetStringSelection(name)
                self.selected_theme = name
        dlg.Destroy()

    def OnApply(self, event):
        self.theme_manager.set_current_theme(self.selected_theme)
        self.EndModal(wx.ID_OK)

    def OnCancel(self, event):
        self.EndModal(wx.ID_CANCEL)