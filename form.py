"""
Module form.py
==============

This module contains the base class for GUI forms. Also
subclasses which implement some simple forms.

Classes:

* XForm: Base class for all the GUI forms.

* XSlider: Represents :class:`~kivy.uix.slider.Slider` in popup.

* XTextInput: Represents a single line TextInput in popup.

* XNotes: Represents a multiline TextInput in popup.

* XAuthorization: Represents simple authorization form.


XForm class
===========

Subclass of :class:`xpopup.XBase`.
The base class for all the GUI forms. Also you can use this class to create
your own forms. To do this you need to implement :meth:`XForm._get_form` in
your subclass::

    class MyForm(XForm):
        def _get_form(self):
            layout = BoxLayout()
            layout.add_widget(Label(text='Show must go'))
            layout.add_widget(Switch(id='main_switch'))
            return layout

    popup = MyForm(title='Party switch')

IMPORTANT: widgets, the values of which must be received after the close of
the form, must have an "id" attribute (see an example above). Current version
supports obtaining values of following widgets: TextInput, Switch, CheckBox,
Slider.

To obtain this values you need just use :meth:`XForm.get_value`::

    def my_callback(instance):
        print('Switch value: ' + str(instance.get_value('main_switch')))

    popup = MyForm(title='Party switch', on_dismiss=my_callback)

If you omit an argument for the :meth:`XForm.get_value`, method returns
a first value from the values dictionary. It is useful if the layout has only
one widget.

Another way to obtain values is :attr:`XForm.values`::

    def my_callback(instance):
        print('Values: ' + str(instance.values))

    popup = MyForm(title='Party switch', on_dismiss=my_callback)

NOTE: The values are available only when the event `on_dismiss` was triggered.


XSlider class
=============

Subclass of :class:`xpopup.XForm`.
Represents :class:`~kivy.uix.slider.Slider` in a popup. Properties
:attr:`XSlider.value`, :attr:`XSlider.min`, :attr:`XSlider.max` and
:attr:`XSlider.orientation` is binded to an appropriate properties of
the :class:`~kivy.uix.progressbar.Slider`.

Also :class:`xpopup.XSlider` has the event 'on_change'. You can bind
your callback to respond on the slider's position change.

Following example will create a :class:`xpopup.XSlider` object::

    def my_callback(instance, value):
        print('Current volume level: %0.2f' % value)

    popup = XSlider(title='Volume', on_change=my_callback)

Another example you can see in the demo app module.


XTextInput and XNotes classes
=============================

Subclasses of :class:`xpopup.XForm`.
Both classes are represents :class:`~kivy.uix.slider.TextInput` in a popup.
The difference is that the class :class:`xpopup.XTextInput` is used to enter
one text line, and the class :class:`xpopup.XNotes` - for multiline text.

Following example will create a :class:`~kivy.uix.slider.TextInput` object
with the specified default text::

    def my_callback(instance):
        print('Your answer: ' + str(instance.get_value()))

    popup = XTextInput(title='What`s your mood?',
                       text='I`m in the excellent mood!',
                       on_dismiss=my_callback)

NOTE: Pressing "Enter" key will simulate pressing "OK" on the popup. Valid for
the :class:`xpopup.XTextInput` ONLY.


XAuthorization class
====================

Subclass of :class:`xpopup.XForm`.
This class is represents a simple authorization form.
Use :attr:`xpopup.XAuthorization.login` and
:attr:`xpopup.XAuthorization.password` to set default values for the login and
password::

    def my_callback(instance):
        print('Auth values: ' + str(instance.values))

    XAuthorization(on_dismiss=my_callback, login='login', password='password')

Also, you can set a default value for the checkbox "Login automatically" via
:attr:`xpopup.XAuthorization.autologin`

To obtain the specific value, use following ids:

* login -  TextInput for the login

* password - TextInput for the password

* autologin - checkbox "Login automatically"

"""


from kivy import metrics
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty, OptionProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
try:
    from ..xtools.tools_ui import XLabel as LabelEx
except:
    from kivy.uix.label import Label as LabelEx
from xbase import XBase

__author__ = 'ophermit'


class XForm(XBase):
    """XForm class. See module documentation for more information.
    """

    buttons = ListProperty([XBase.BUTTON_OK, XBase.BUTTON_CANCEL])
    '''List of button names. Can be used when using custom button sets.

    :attr:`buttons` is a :class:`~kivy.properties.ListProperty` and defaults to
    [Base.BUTTON_OK, Base.BUTTON_CANCEL].
    '''

    values = DictProperty({})
    '''Dict of pairs <widget_id>: <widget_value>. Use it to get the data from
    form fields. Supported widget classes: TextInput, Switch, CheckBox, Slider.

    :attr:`values` is a :class:`~kivy.properties.DictProperty` and defaults to
    {}, read-only.
    '''

    def __init__(self, **kwargs):
        self._ui_form_container = BoxLayout()
        super(XForm, self).__init__(**kwargs)
        self._ui_form_container.add_widget(self._get_form())

    def _get_body(self):
        return self._ui_form_container

    def _on_click(self, instance):
        self.values = {}
        for widget in self._ui_form_container.walk(restrict=True):
            if widget.id is not None:
                if isinstance(widget, TextInput):
                    v_t = widget.text
                elif isinstance(widget, Switch)\
                        or isinstance(widget, CheckBox):
                    v_t = widget.active
                elif isinstance(widget, Slider):
                    v_t = widget.value
                else:
                    v_t = 'Not supported: ' + widget.__class__.__name__

                self.values[widget.id] = v_t

        super(XForm, self)._on_click(instance)

    def _get_form(self):
        raise NotImplementedError

    def get_value(self, ps_id=''):
        """Obtain values from the widgets on the form.

        :param ps_id: widget id (optional)
            If omit, method returns a first value from the values dictionary
        :return: value of widget with specified id
        """
        assert len(self.values) > 0
        if ps_id == '':
            return self.values.get(self.values.keys()[0])
        else:
            return self.values.get(ps_id)


class XSlider(XForm):
    """XSlider class. See module documentation for more information.

    :Events:
        `on_change`:
            Fired when the :attr:`~kivy.uix.slider.Slider.value` is changed.
    """
    __events__ = ('on_change', )

    buttons = ListProperty([XForm.BUTTON_CLOSE])
    '''Default button set for the popup
    '''

    min = NumericProperty(0.)
    max = NumericProperty(1.)
    value = NumericProperty(.5)
    orientation = OptionProperty(
        'horizontal', options=('vertical', 'horizontal'))
    '''Properties that are binded to the same slider properties.
    '''

    def _get_form(self):
        slider = Slider(id='value', min=self.min, max=self.max,
                        value=self.value, orientation=self.orientation)
        slider.bind(value=self.setter('value'))
        bind = self.bind
        bind(min=slider.setter('min'))
        bind(max=slider.setter('max'))
        bind(value=slider.setter('value'))
        bind(orientation=slider.setter('orientation'))
        return slider

    def on_value(self, instance, value):
        self.dispatch('on_change', value)

    def on_change(self, value):
        pass


class XTextInput(XForm):
    """XTextInput class. See module documentation for more information.
    """

    text = StringProperty('')
    '''This property represents default text in the TextInput.

    :attr:`text` is a :class:`~kivy.properties.StringProperty` and defaults to
    '', read-only.
    '''

    def _get_form(self):
        layout = BoxLayout(orientation='vertical', spacing=5)
        text_input = TextInput(id='text', multiline=False, text=self.text,
                               on_text_validate=self._on_text_validate,
                               # DON`T UNCOMMENT OR FOUND AND FIX THE ISSUE
                               # if `focus` set to `True` - TextInput will be
                               # inactive to edit
                               # focus=True,
                               size_hint_y=None, height=metrics.dp(33))
        layout.add_widget(Widget())
        layout.add_widget(text_input)
        layout.add_widget(Widget())
        return layout

    def _on_text_validate(self, instance):
        self._on_click(Button(id=self.BUTTON_OK))


class XNotes(XTextInput):
    """XNotes class. See module documentation for more information.
    """

    size_hint_x = NumericProperty(.9, allownone=True)
    size_hint_y = NumericProperty(.9, allownone=True)
    '''Default size properties for the popup
    '''

    def _get_form(self):
        return TextInput(id='text', text=self.text)


class XAuthorization(XForm):
    """XAuthorization class. See module documentation for more information.
    """
    BUTTON_LOGIN = 'Login'

    login = StringProperty(u'')
    '''This property represents default text in the `login` TextInput.
    For initialization only.

    :attr:`login` is a :class:`~kivy.properties.StringProperty` and defaults to
    ''.
    '''

    password = StringProperty(u'')
    '''This property represents default text in the `password` TextInput.
    For initialization only.

    :attr:`password` is a :class:`~kivy.properties.StringProperty` and defaults
    to ''.
    '''

    autologin = BooleanProperty(False)
    '''This property represents default value for the CheckBox
    "Login automatically". For initialization only.

    :attr:`autologin` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False.
    '''

    title = StringProperty('Authorization')
    '''Default title for the popup
    '''

    buttons = ListProperty([BUTTON_LOGIN, XForm.BUTTON_CANCEL])
    '''Default button set for the popup
    '''

    size_hint_x = NumericProperty(None, allownone=True)
    size_hint_y = NumericProperty(None, allownone=True)
    width = NumericProperty(metrics.dp(350))
    height = NumericProperty(metrics.dp(200))
    '''Default size properties for the popup
    '''

    def _get_form(self):
        layout = BoxLayout(orientation='vertical', spacing=5)
        layout.add_widget(Widget())

        pnl = BoxLayout(size_hint_y=None, height=metrics.dp(28), spacing=5)
        pnl.add_widget(LabelEx(text='Login:', halign='right', size_hint_x=None,
                               width=metrics.dp(80)))
        pnl.add_widget(TextInput(id='login', multiline=False,
                                 font_size=metrics.sp(14), text=self.login))
        layout.add_widget(pnl)

        pnl = BoxLayout(size_hint_y=None, height=metrics.dp(28), spacing=5)
        pnl.add_widget(LabelEx(text='Password:', halign='right',
                               size_hint_x=None, width=metrics.dp(80)))
        pnl.add_widget(TextInput(id='password', multiline=False, font_size=14,
                                 password=True, text=self.password))
        layout.add_widget(pnl)

        pnl = BoxLayout(size_hint_y=None, height=metrics.dp(28), spacing=5)
        pnl.add_widget(CheckBox(id='autologin', size_hint_x=None,
                                width=metrics.dp(80), active=self.autologin))
        pnl.add_widget(LabelEx(text='Login automatically', halign='left'))
        layout.add_widget(pnl)

        layout.add_widget(Widget())
        return layout
