from os.path import expanduser
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from xbase import ButtonEx
from notification import XNotification, XConfirmation, XError, XMessage, XProgress
from form import XSlider, XTextInput, XNotes, XAuthorization
from file import XFileOpen, XFileSave, XFolder

__author__ = 'ophermit'


class XPopupDemo(BoxLayout):
    def __init__(self, **kwargs):
        super(XPopupDemo, self).__init__(padding=20, spacing=15, orientation='vertical', **kwargs)

        pnl1 = BoxLayout(spacing=15)
        pnl1.add_widget(ButtonEx(id='msgbox', text='XMessage demo', on_release=self._on_click))
        pnl1.add_widget(ButtonEx(id='confirm', text='XConfirmation demo', on_release=self._on_click))
        pnl1.add_widget(ButtonEx(id='error', text='XError demo', on_release=self._on_click))
        pnl1.add_widget(ButtonEx(id='progress', text='XProgress demo', on_release=self._on_click))
        self.add_widget(pnl1)

        pnl1 = BoxLayout(spacing=15)
        pnl1.add_widget(ButtonEx(id='input', text='XTextInput demo', on_release=self._on_click))
        pnl1.add_widget(ButtonEx(id='notes', text='XNotes demo', on_release=self._on_click))
        pnl1.add_widget(ButtonEx(id='slider', text='XSlider demo', on_release=self._on_click))
        pnl1.add_widget(ButtonEx(id='login', text='XAuthorization demo', on_release=self._on_click))
        self.add_widget(pnl1)

        pnl1 = BoxLayout(spacing=15)
        pnl1.add_widget(ButtonEx(text='XOpenFile demo', on_release=self._open_dialog_demo))
        pnl1.add_widget(ButtonEx(text='XSaveFile demo', on_release=self._save_dialog_demo))
        pnl1.add_widget(ButtonEx(text='XFolder demo', on_release=self._folder_dialog_demo))
        self.add_widget(pnl1)

    def _on_click(self, instance):
        s_id = instance.id
        if s_id == 'msgbox':
            XMessage(text='It could be your Ad', title='XMessage demo')
        elif s_id == 'error':
            XError(text='Don`t panic! Its just the XError demo.')
        elif s_id == 'confirm':
            XConfirmation(text='Do you see a confirmation?', on_dismiss=self._callback)
        elif s_id == 'progress':
            self._o_popup = XProgress(title='PopupProgress demo', text='Processing...', max=200)
            Clock.schedule_once(self._progress_test, .1)
        elif s_id == 'input':
            XTextInput(title='Edit text', text='I\'m a text', on_dismiss=self._callback)
        elif s_id == 'notes':
            XNotes(title='Edit notes', text='Text\nToo many text...\nYet another row.', on_dismiss=self._callback)
        elif s_id == 'slider':
            self._o_popup = XSlider(min=.4, max=.9, value=.5, title='Slider test', size_hint=(.6, .5),
                                    buttons=['Horizontal', 'Vertical', 'Close'],
                                    on_change=self._slider_value, on_dismiss=self._slider_click)
        elif s_id == 'login':
            XAuthorization(on_dismiss=self._callback, login='login', password='password')

    @staticmethod
    def _callback(instance):
        if instance.is_canceled():
            return

        s_message = 'Pressed button: %s\n\n' % instance.button_pressed

        try:
            values = instance.values
            for kw in values:
                s_message += ('<' + kw + '> : ' + str(values[kw]) + '\n')
        except AttributeError:
            pass

        XNotification(text=s_message, show_time=3, size_hint=(0.8, 0.4),
                      title='Results of the popup ( will disappear after 3 seconds ):')

    def _progress_test(self, pdt=None):
        if self._o_popup.is_canceled():
            return

        self._o_popup.inc()
        self._o_popup.text = 'Processing (%d / %d)' % (self._o_popup.value, self._o_popup.max)
        if self._o_popup.value < self._o_popup.max:
            Clock.schedule_once(self._progress_test, .01)
        else:
            self._o_popup.complete()

    @staticmethod
    def _slider_value(instance, value):
        if instance.orientation == 'vertical':
            instance.size_hint_x = value
        else:
            instance.size_hint_y = value

    @staticmethod
    def _slider_click(instance):
        if instance.button_pressed == 'Horizontal':
            instance.orientation = 'horizontal'
            instance.size_hint = (.6, .5)
            instance.min = .4
            instance.max = .9
            instance.value = .5
            return True
        elif instance.button_pressed == 'Vertical':
            instance.orientation = 'vertical'
            instance.size_hint = (.5, .6)
            instance.min = .4
            instance.max = .9
            instance.value = .5
            return True

    def _filepopup_callback(self, instance):
            if instance.is_canceled():
                return
            s = 'Path: %s' % instance.path
            if instance.__class__.__name__ == 'XFileSave':
                s += ('\nFilename: %s\nFull name: %s' % (instance.filename, instance.get_full_name()))
            else:
                s += ('\nSelection: %s' % instance.selection)
            XNotification(title='Pressed button: ' + instance.button_pressed, text=s, show_time=5)

    def _open_dialog_demo(self, instance):
        XFileOpen(on_dismiss=self._filepopup_callback, path=expanduser(u'~'), multiselect=True)

    def _save_dialog_demo(self, instance):
        XFileSave(on_dismiss=self._filepopup_callback, path=expanduser(u'~'))

    def _folder_dialog_demo(self, instance):
        XFolder(on_dismiss=self._filepopup_callback, path=expanduser(u'~'))


if __name__ == '__main__':
    import kivy
    kivy.require('1.9.1')
    from kivy.base import runTouchApp
    runTouchApp(XPopupDemo())
