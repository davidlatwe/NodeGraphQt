#!/usr/bin/python
from PySide2 import QtWidgets, QtCore, QtGui

from NodeGraphQt.constants import (PROPERTY_LABEL,
                                   PROPERTY_TEXT,
                                   PROPERTY_LIST,
                                   PROPERTY_CHECKBOX,
                                   PROPERTY_COLOR,
                                   PROPERTY_SLIDER,
                                   PROPERTY_FLOAT_SLIDER)


class BaseProperty(QtWidgets.QWidget):

    value_changed = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(BaseProperty, self).__init__(parent)
        self.block_signal = False
        self.name = ''


class ColorSolid(QtWidgets.QWidget):

    def __init__(self, parent=None, color=None):
        super(ColorSolid, self).__init__(parent)
        self._color = color or (0, 0, 0, 255)
        self.setToolTip('rgba{}'.format(self._color))
        self.setMinimumSize(15, 15)
        self.setMaximumSize(15, 15)

    def paintEvent(self, event):
        size = self.geometry()
        rect = QtCore.QRect(1, 1, size.width() - 2, size.height() - 2)
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(*self._color))
        painter.drawRoundedRect(rect, 4, 4)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.setToolTip('rgba{}'.format(self._color))
        self.update()


class PropWidgetColorPicker(BaseProperty):

    def __init__(self, parent=None):
        super(PropWidgetColorPicker, self).__init__(parent)
        self._solid = ColorSolid(self)
        self._solid.setMaximumHeight(15)
        self._label = QtWidgets.QLabel()
        button = QtWidgets.QPushButton('select color')
        button.clicked.connect(self._on_select_color)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.setSpacing(2)
        layout.addWidget(button)
        layout.addWidget(self._solid)
        layout.addWidget(self._label)

    def _on_select_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.set_value(color.getRgb())

    def value(self):
        return self._solid.color

    def set_value(self, value):
        self._label.setText(self.hex_color())
        self._label.setStyleSheet(
            'QLabel {{color: rgba({}, {}, {}, 255);}}'
            .format(*self._solid.color))
        self._solid.color = value
        if not self.block_signal:
            self.value_changed.emit(value)

    def hex_color(self):
        return '#{0:02x}{1:02x}{2:02x}'.format(*self._solid.color)


class PropWidgetSlider(BaseProperty):

    def __init__(self, parent=None):
        super(PropWidgetSlider, self).__init__(parent)
        self._block = False
        self._slider = QtWidgets.QSlider()
        self._spnbox = QtWidgets.QSpinBox()
        self._init()
        self.set_min(0)
        self.set_max(100)

    def _init(self):
        self._slider.setOrientation(QtCore.Qt.Horizontal)
        self._slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self._slider.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Preferred)
        self._spnbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self._spnbox)
        layout.addWidget(self._slider)
        self._spnbox.valueChanged.connect(self._on_spnbox_changed)
        self._slider.valueChanged.connect(self._on_slider_changed)
        self._slider.mouseReleaseEvent = self.sliderMouseReleaseEvent

    def sliderMouseReleaseEvent(self, event):
        self._block = False
        self.set_value(self.value())

    def _on_slider_changed(self, value):
        self._block = True
        self._spnbox.setValue(value)

    def _on_spnbox_changed(self, value):
        self._slider.setValue(value)
        if not self._block:
            self.set_value(value)
        self._block = False

    def set_min(self, value):
        self._spnbox.setMinimum(value)
        self._slider.setMinimum(value)

    def set_max(self, value):
        self._spnbox.setMaximum(value)
        self._slider.setMaximum(value)

    def value(self):
        return self._spnbox.value()

    def set_value(self, value):
        if not self._block:
            self.value_changed.emit(value)


class PropWidgetFloatSlider(PropWidgetSlider):

    def __init__(self, parent=None):
        super(PropWidgetSlider, self).__init__(parent)
        self._block = False
        self._slider = QtWidgets.QSlider()
        self._spnbox = QtWidgets.QDoubleSpinBox()
        self._init()
        self.set_min(0.0)
        self.set_max(100.0)


class PropWidgetLabel(QtWidgets.QLabel):

    value_changed = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(PropWidgetLabel, self).__init__(parent)
        self.name = ''

    def value(self):
        return self.text()

    def set_value(self, value):
        self.setText(value)
        self.value_changed.emit(value)


class PropWidgetText(QtWidgets.QLineEdit):

    value_changed = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(PropWidgetText, self).__init__(parent)
        self.name = ''
        self.returnPressed.connect(self._on_return_pressed)

    def _on_return_pressed(self):
        self.value_changed.emit(self.value())

    def value(self):
        return self.text()

    def set_value(self, value):
        self.setText(value)
        self.value_changed.emit(value)


class PropWidgetList(QtWidgets.QComboBox):
    value_changed = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(PropWidgetList, self).__init__(parent)
        self.name = ''
        self.currentIndexChanged.connect(self._on_index_changed)

    def _on_index_changed(self):
        self.value_changed.emit(self.value())

    def value(self):
        return self.currentText()

    def set_value(self, value):
        self.setText(value)
        self.value_changed.emit(value)


class PropWidgetCheckBox(QtWidgets.QCheckBox):

    value_changed = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(PropWidgetCheckBox, self).__init__(parent)
        self.name = ''
        self.clicked.connect(self._on_clicked)

    def _on_clicked(self):
        self.value_changed.emit(self.value())

    def value(self):
        return self.isChecked()

    def set_value(self, value):
        self.setChecked(value)
        self.value_changed.emit(value)


class PropertyWidgetFactory(object):

    @staticmethod
    def get_widget_instance(property_type):
        """
        Args:
            property_type (int): property type

        Returns:
            QtWidgets.QWidget: property widget instance.
        """
        widget_map = {
            PROPERTY_LABEL: PropWidgetLabel,
            PROPERTY_TEXT: PropWidgetText,
            PROPERTY_LIST: PropWidgetList,
            PROPERTY_CHECKBOX: PropWidgetCheckBox,
            PROPERTY_COLOR: PropWidgetColorPicker,
            PROPERTY_SLIDER: PropWidgetSlider,
            PROPERTY_FLOAT_SLIDER: PropWidgetFloatSlider
        }
        return widget_map.get(property_type)


class PropertiesWidget(QtWidgets.QWidget):

    property_changed = QtCore.Signal(str, object)

    def __init__(self, parent=None, graph=None, node=None):
        """
        Args:
            parent:
            graph (NodeGraphQt.NodeGraph):
            node (NodeGraphQt.Node):
        """
        super(PropertiesWidget, self).__init__(parent)
        self._graph = graph
        self._node = node
        self._widgets = {}
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setSpacing(2)

        # TODO: must read the node widgets.


    @property
    def node(self):
        return self._node

    def add_property(self, widget):
        self._widgets[widget.name] = widget
        self.layout.addWidget(widget)

    def get_property(self, name):
        return self._widgets.get(name)

    def hide_property(self, name, visible=False):
        widget = self._widgets.get(name)
        if widget:
            widget.setVisible(visible)

    def remove_property(self, name):
        widget = self._widgets.pop(name)
        widget.deleteLater()


class PropertyBin(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(PropertyBin, self).__init__(parent)
        self._property_widgets = []
        self._layout = QtWidgets.QVBoxLayout(self)

    def add_property_widget(self, widget):
        self._property_widgets.append(widget)
        self._layout.addWidget(widget)

    def remove_property_widget(self, widget):
        self._layout.takeAt(self._property_widgets.index(widget))
        widget.deleteLater()

    def loaded_widgets(self):
        return self._property_widgets

    def clear(self):
        for i in reversed(range(self._layout.count())):
            widget = self._layout.takeAt(i)
            self._property_widgets.remove(widget)
            widget.deleteLater()


if __name__ == '__main__':
    import sys
    from NodeGraphQt import Node

    class TestNode(Node):

        NODE_NAME = 'test node'

        def __init__(self):
            super(TestNode, self).__init__()
            self.create_property('label_test', 'foo bar')
            self.create_property('text_edit', 'hello')
            self.create_property('color_picker', (0, 0, 255), PROPERTY_COLOR)
            self.create_property('integer', 10)
            self.create_property('float', 1.25)
            self.create_property('list', 'foo', items=['foo', 'bar'])
            self.add_combo_menu('fruits', 'fruits', ['apples', 'bananas', 'pears'])



    app = QtWidgets.QApplication(sys.argv)

    test_node = TestNode()
    button = PropertiesWidget(node=test_node)
    # button.show()

    cp = PropWidgetText()
    cp.show()

    app.exec_()
