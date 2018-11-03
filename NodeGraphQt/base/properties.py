#!/usr/bin/python
# -*- coding: utf-8 -*-
from PySide2 import QtWidgets
from NodeGraphQt.constants import (PROPERTY_HIDDEN,
                                   PROPERTY_LABEL,
                                   PROPERTY_TEXT,
                                   PROPERTY_LIST,
                                   PROPERTY_CHECKBOX,
                                   PROPERTY_COLOR,
                                   PROPERTY_SLIDER,
                                   PROPERTY_FLOAT_SLIDER)


class PropertyFactory(object):

    @staticmethod
    def get_instance(property_type):
        """
        Args:
            property_type (int): property type

        Returns:
            NodeProperty: Node property instance
        """
        property_types = {
            PROPERTY_HIDDEN: NodeProperty,
            PROPERTY_LABEL: LabelProperty,
            PROPERTY_TEXT: TextProperty,
            PROPERTY_LIST: ListProperty,
            PROPERTY_CHECKBOX: CheckboxProperty,
            PROPERTY_COLOR: ColorProperty,
            PROPERTY_SLIDER: SliderProperty,
            PROPERTY_FLOAT_SLIDER: FloatSliderProperty
        }
        return property_types.get(property_type)


class NodeProperty(object):

    def __init__(self, node=None, name=None):
        """
        Args:
            node (NodeGraphQt.Node): node controller.
            name (str): property name.
        """
        self._node = node
        self._name = name
        self._value = None

    def type(self):
        return PROPERTY_HIDDEN

    def node(self):
        return self._node

    def name(self):
        return self._name

    def value(self):
        if self._node:
            return self._node.get_property(self._name)
        return self._value

    def set_value(self, value):
        if self._node:
            self._node.set_property(self._name, value)
            return
        self._value = value


class ListProperty(NodeProperty):

    def __init__(self, node=None, name=None):
        super(ListProperty, self).__init__(node, name)
        self._items = []

    def type(self):
        return PROPERTY_LIST

    def items(self):
        return self._items

    def set_items(self, items=None):
        self._items = items


class CheckboxProperty(NodeProperty):

    def type(self):
        return PROPERTY_CHECKBOX


class ColorProperty(NodeProperty):

    def type(self):
        return PROPERTY_COLOR

    def color(self):
        r, g, b, a = self.value()
        '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)

    def set_color(self, color):
        if isinstance(color, str):
            color = color[1:] if color[0] is '#' else color
            color = [(int(color[i:i + 2], 16) for i in (0, 2, 4))]
        if len(color) == 3:
            color.append(255)
        self.set_value(color)


class TextProperty(NodeProperty):

    def type(self):
        return PROPERTY_TEXT


class LabelProperty(NodeProperty):

    def type(self):
        return PROPERTY_LABEL


class SliderProperty(NodeProperty):

    def __init__(self, node=None, name=None, widget=None):
        super(SliderProperty, self).__init__(node, name, widget)
        self._min = 0.0
        self._max = 1.0

    def type(self):
        return PROPERTY_SLIDER

    def min(self):
        return self._min

    def set_min(self, value=0.0):
        self._min = value

    def max(self):
        return self._max

    def set_max(self, value=1.0):
        self._max = value


class FloatSliderProperty(NodeProperty):

    def __init__(self, node=None, name=None, widget=None):
        super(FloatSliderProperty, self).__init__(node, name, widget)
        self._min = 0.0
        self._max = 1.0

    def type(self):
        return PROPERTY_FLOAT_SLIDER

    def min(self):
        return self._min

    def set_min(self, value=0.0):
        self._min = value

    def max(self):
        return self._max

    def set_max(self, value=1.0):
        self._max = value
