import wx
import string

########################################################################
class CharValidator(wx.PyValidator):
    ''' Validates data as it is entered into the text controls. '''

    #----------------------------------------------------------------------
    def __init__(self, flag):
        wx.PyValidator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)

    #----------------------------------------------------------------------
    def Clone(self):
        '''Required Validator method'''
        return CharValidator(self.flag)

    #----------------------------------------------------------------------
    def Validate(self, win):
        return True

    #----------------------------------------------------------------------
    def TransferToWindow(self):
        return True

    #----------------------------------------------------------------------
    def TransferFromWindow(self):
        return True

    #----------------------------------------------------------------------
    def OnChar(self, event):
        keycode = int(event.GetKeyCode())
        if keycode < 256:
            #print keycode
            key = chr(keycode)
            #print key
            if self.flag == 'no-alpha' and key in string.letters:
                return
            if self.flag == 'no-digit' and key in string.digits:
                return
        event.Skip()

########################################################################
class ValidationDemo(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, 
                          "Text Validation Tutorial")

        panel = wx.Panel(self)
        textOne = wx.TextCtrl(panel, validator=CharValidator('no-alpha'))
        textTwo = wx.TextCtrl(panel, validator=CharValidator('no-digit'))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(textOne, 0, wx.ALL, 5)
        sizer.Add(textTwo, 0, wx.ALL, 5)
        panel.SetSizer(sizer)

# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = ValidationDemo()
    frame.Show()
    app.MainLoop()
