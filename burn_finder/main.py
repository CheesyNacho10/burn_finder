import wx
import backend

class WholeFrame(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, title='Burn finder')

        self.device_items_ids_base = 1000

        self.SetSizeHints(800, 600)

        # Menu bar
        self.menu_bar = self.get_menu_bar()
        self.SetMenuBar(self.menu_bar)

        self.whole_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.whole_sizer)

        # Left panel
        self.classification_preview = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap())
        self.whole_sizer.Add(self.classification_preview, 1, wx.EXPAND | wx.ALL, 20)

        # Right panel
        self.right_panel = self.get_right_panel()
        self.whole_sizer.Add(self.right_panel, 0, wx.ALL | wx.EXPAND, 5)

    # GUI
    def get_menu_bar(self):
        menu_bar = wx.MenuBar()

        # File menu
        self.file_menu = wx.Menu()

        self.exit_menu_item = self.file_menu.Append(wx.ID_EXIT, 'E&xit', 'Exit application')
        self.Bind(wx.EVT_MENU, self.on_exit, self.exit_menu_item)

        menu_bar.Append(self.file_menu, '&File')

        # Device menu
        self.device_menu = wx.Menu()

        self.device_items = []

        cams = backend.list_cams()
        if (len(cams) == 0):
            self.device_items.append(self.device_menu.Append(self.device_items_ids_base, 'No avaliable cameras'))
            self.device_items[0].Enable(False)
        else:
            for cam_name, cam_index in cams:
                cam_id = self.device_items_ids_base + cam_index
                self.device_items.append(self.device_menu.AppendRadioItem(cam_id, 'Camera ' + str(cam_name)))
                self.Bind(wx.EVT_MENU, self.on_device_selected(cam_index), self.device_items[cam_index], id=cam_id)
                if cam_index == 0:
                    self.device_items[0].Check()

        menu_bar.Append(self.device_menu, '&Device')

        return menu_bar

    def get_right_panel(self):
        right_panel = wx.Panel(self)
        right_panel.SetMinClientSize((150, -1))

        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_panel.SetSizer(self.right_sizer)

        self.start_stop_camera_button = wx.Button(right_panel, label='Start camera')
        self.right_sizer.Add(self.start_stop_camera_button, 0, wx.EXPAND | wx.ALL, 5)

        return right_panel

    # Events
    def on_exit(self, event):
        self.Close()

    def on_device_selected(self, cam_index):
        print('Selected camera: ' + str(cam_index))


if __name__ == '__main__':
    app = wx.App()
    frame = WholeFrame()
    frame.Show()
    app.MainLoop()