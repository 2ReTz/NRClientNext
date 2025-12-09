import wx
import json
import os

class ThemeManager:
    def __init__(self):
        self.themes = {
            'light': {
                'bg_color': '#FFFFFF',
                'fg_color': '#000000',
                'panel_bg': '#F0F0F0',
                'tree_bg': '#FFFFFF',
                'status_bg': '#F0F0F0',
                'toolbar_bg': '#F0F0F0',
                'menu_bg': '#F0F0F0',
                'selected_bg': '#0078D4',
                'selected_fg': '#FFFFFF'
            },
            'dark': {
                'bg_color': '#2B2B2B',
                'fg_color': '#FFFFFF',
                'panel_bg': '#1E1E1E',
                'tree_bg': '#2B2B2B',
                'status_bg': '#1E1E1E',
                'toolbar_bg': '#1E1E1E',
                'menu_bg': '#1E1E1E',
                'selected_bg': '#005A9E',
                'selected_fg': '#FFFFFF'
            }
        }
        self.current_theme = 'light'
        self.custom_themes = {}
        self.load_custom_themes()
        self.load_current_theme()

    def load_custom_themes(self):
        try:
            if os.path.exists('themes.json'):
                with open('themes.json', 'r') as f:
                    self.custom_themes = json.load(f)
                    self.themes.update(self.custom_themes)
        except Exception as e:
            print(f"Error loading custom themes: {e}")

    def save_custom_themes(self):
        try:
            with open('themes.json', 'w') as f:
                json.dump(self.custom_themes, f, indent=4)
        except Exception as e:
            print(f"Error saving custom themes: {e}")

    def load_current_theme(self):
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    theme = config.get('current_theme', 'light')
                    if theme in self.themes:
                        self.current_theme = theme
        except Exception as e:
            print(f"Error loading current theme: {e}")

    def save_current_theme(self):
        try:
            config = {}
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
            config['current_theme'] = self.current_theme
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving current theme: {e}")

    def get_theme(self, theme_name=None):
        if theme_name is None:
            theme_name = self.current_theme
        return self.themes.get(theme_name, self.themes['light'])

    def set_current_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.save_current_theme()

    def add_custom_theme(self, name, colors):
        self.custom_themes[name] = colors
        self.themes[name] = colors
        self.save_custom_themes()

    def apply_theme_to_frame(self, frame, theme):
        frame.SetBackgroundColour(wx.Colour(theme['bg_color']))
        frame.SetForegroundColour(wx.Colour(theme['fg_color']))
        frame.Refresh()

    def apply_theme_to_panel(self, panel, theme):
        panel.SetBackgroundColour(wx.Colour(theme['panel_bg']))
        panel.SetForegroundColour(wx.Colour(theme['fg_color']))
        panel.Refresh()

    def apply_theme_to_tree(self, tree, theme):
        tree.SetBackgroundColour(wx.Colour(theme['tree_bg']))
        tree.SetForegroundColour(wx.Colour(theme['fg_color']))
        # For selected item colors, might need to handle differently
        tree.Refresh()

    def apply_theme_to_toolbar(self, toolbar, theme):
        toolbar.SetBackgroundColour(wx.Colour(theme['toolbar_bg']))
        toolbar.SetForegroundColour(wx.Colour(theme['fg_color']))
        toolbar.Refresh()

    def apply_theme_to_statusbar(self, statusbar, theme):
        statusbar.SetBackgroundColour(wx.Colour(theme['status_bg']))
        statusbar.SetForegroundColour(wx.Colour(theme['fg_color']))
        statusbar.Refresh()

# Global instance
theme_manager = ThemeManager()