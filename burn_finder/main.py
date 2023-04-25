import wx
import wx.lib.statbmp as statbmp
import frontend
import backend

class WholeFrame(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, title='Burn finder')
        self.SetIcon(wx.Icon('./resources/icon.png'))
        self.SetSizeHints(800, 600)

        self.selected_file = None

        # Render timer
        self.render_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnRenderTimer, self.render_timer)
        self.render_timer.Start(int(1000 / 30)) # 30 FPS

        # Menu bar
        self.menu_bar = self.GetMenuBar()
        self.SetMenuBar(self.menu_bar)

        self.whole_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.whole_sizer)

        # Left panel
        self.classification_preview = statbmp.GenStaticBitmap(self, wx.ID_ANY, wx.Bitmap(wx.Image('./resources/video_placeholder.jpeg')))
        self.classification_preview.Bind(wx.EVT_SIZE, self.OnPreviewSizeChanged)
        self.whole_sizer.Add(self.classification_preview, 1, wx.EXPAND | wx.ALL, 5)

        # Right panel
        self.right_panel = self.GetRightPanel()
        self.whole_sizer.Add(self.right_panel, 0, wx.ALL | wx.EXPAND, 5)

    # GUI
    def GetMenuBar(self):
        menu_bar = wx.MenuBar()

        # File menu
        self.file_menu = wx.Menu()

        self.exit_menu_item = self.file_menu.Append(wx.ID_EXIT, 'E&xit', 'Exit application')
        self.Bind(wx.EVT_MENU, self.OnExit, self.exit_menu_item)

        menu_bar.Append(self.file_menu, '&File')

        # Device menu
        self.device_menu = wx.Menu()

        self.avaliable_cams = frontend.GetActualListCams()
        self.device_items = []

        if len(self.avaliable_cams) == 0:
            self.device_menu.Append(wx.ID_ANY, 'No cameras found').Enable(False)
        else:
            for i, cam in enumerate(self.avaliable_cams):
                self.device_items.append(DeviceMenuItem(self.device_menu, cam[1], cam[0]))
                self.device_menu.Append(self.device_items[i])
                self.Bind(wx.EVT_MENU, self.OnDeviceSelected, self.device_items[i])
            self.device_items[0].Check()

        menu_bar.Append(self.device_menu, '&Device')

        return menu_bar

    def GetRightPanel(self):
        right_panel = wx.Panel(self)
        right_panel.SetMinClientSize((150, -1))

        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_panel.SetSizer(self.right_sizer)

        self.start_stop_camera_button = wx.Button(right_panel, label='Start camera')
        self.right_sizer.Add(self.start_stop_camera_button, 0, wx.EXPAND | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.OnStartStopCamera, self.start_stop_camera_button)

        if self.GetCameraIndex() == -1:
            self.start_stop_camera_button.Disable()

        self.select_file_button = wx.Button(right_panel, label='Select file')
        self.right_sizer.Add(self.select_file_button, 0, wx.EXPAND | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.OnSelectVideoFile, self.select_file_button)

        return right_panel

    # Events
    def OnExit(self, event):
        print(event)
        self.Close()

    def OnDeviceSelected(self, event):
        print(event)
        for item in self.device_items:
            if item.device_id == event.GetId():
                item.Check()
                self.selected_device_index = item.device_id
            elif item.IsChecked():
                item.Check(False)

    def OnRenderTimer(self, event):
        if self.start_stop_camera_button.GetLabel() == 'Stop camera':
            backend.AnalyzeCam(self.GetCameraIndex(), 5, self.DisplayFrame)
        elif self.select_file_button.GetLabel() == 'Stop file':
            backend.AnalyzeVideo(self.selected_file, 5, self.DisplayFrame)

    def OnPreviewSizeChanged(self, event):
        if self.classification_preview.GetBitmap():
            wx.Bitmap.Rescale(self.classification_preview.GetBitmap(), wx.Size(self.classification_preview.GetSize()[0], self.classification_preview.GetSize()[1]))
            self.classification_preview.Refresh()

    def OnStartStopCamera(self, event):
        if self.start_stop_camera_button.GetLabel() == 'Start camera':
            self.start_stop_camera_button.SetLabel('Stop camera')
            self.select_file_button.Disable()
        else:
            self.start_stop_camera_button.SetLabel('Start camera')
            self.select_file_button.Enable()

    def OnSelectVideoFile(self, event):
        if self.select_file_button.GetLabel() == 'Stop file':
            self.start_stop_camera_button.Enable()
            self.select_file_button.SetLabel('Select file')
        else:
            self.selected_file = wx.FileSelector('Select video file', wildcard='Video files (*.mp4;*.avi;*.mkv)|*.mp4;*.avi;*.mkv')
            if self.selected_file:
                self.start_stop_camera_button.Disable()
                self.select_file_button.SetLabel('Stop file')

    # Helpers
    def GetCameraIndex(self):
        for item in self.device_items:
            if item.IsChecked():
                return item.device_id
        return -1

    def DisplayFrame(self, rgb_frame):
        frame = wx.Bitmap.FromBuffer(rgb_frame.shape[1], rgb_frame.shape[0], rgb_frame)
        frame.SetSize((self.classification_preview.GetSize()))
        self.classification_preview.SetBitmap(frame)
        self.Layout()
        wx.App.Get().Yield() # This is needed to update the GUI
        return self.start_stop_camera_button.GetLabel() == 'Stop camera' or\
            self.select_file_button.GetLabel() == 'Stop video'

class DeviceMenuItem(wx.MenuItem):
    def __init__(self, parent, device_id, text):
        super().__init__(parent, wx.ID_ANY, text, kind=wx.ITEM_CHECK)

        self.device_id = device_id

if __name__ == '__main__':
    app = wx.App()
    frame = WholeFrame()
    frame.Show()
    app.MainLoop()