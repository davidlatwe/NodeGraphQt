#!/usr/bin/python
# -*- coding: utf-8 -*-
from NodeGraphQt.constants import (PROPERTY_HIDDEN,
                                   PROPERTY_LABEL,
                                   PROPERTY_TEXT,
                                   PROPERTY_LIST,
                                   PROPERTY_CHECKBOX,
                                   PROPERTY_COLOR,
                                   PROPERTY_SLIDER,
                                   PROPERTY_FLOAT_SLIDER)
from NodeGraphQt.base.commands import PropertyChangedCmd


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
    """
    Base property controller.
    """

    _type = PROPERTY_HIDDEN

    def __init__(self, graph=None, node_id=None, prop_name=None):
        """
        Args:
            graph (NodeGraphQt.NodeGraph): node graph.
            node_id (str): node id.
            prop_name (str): property name.
        """
        self._graph = graph
        self._node_id = node_id
        self._name = prop_name
        self._value = None

    def type(self):
        return self._type

    def node(self):
        if self._graph:
            return self._graph.get_node_by_id(self._node_id)

    def name(self):
        return self._name

    def value(self):
        if self._graph is None:
            return self._value
        node = self.node()
        if node is None:
            raise AssertionError('Node deleted!, can\'t get value.')
        node.model.get_property(self._name)

    def set_value(self, value):
        if self._graph is None:
            self._value = value
        node = self.node()
        if node is None:
            raise AssertionError('Node deleted!, can\'t set value.')

        if self._graph and self.name() == 'name':
            value = self._graph.get_unique_name(value)
            node.NODE_NAME = value

        exists = any([self.name() in node.model.properties.keys(),
                      self.name() in node.model.custom_properties.keys()])
        if not exists:
            raise KeyError('No property "{}"'.format(self.name()))

        if self._graph:
            block_widget_signal = node.model.block_widget_signal
            undo_stack = self._graph.undo_stack()

            undo_stack.push(PropertyChangedCmd(self,
                                               self.name(),
                                               value,
                                               block_widget_signal))
        else:
            setattr(node.view, node.name(), value)
            node.model.set_property(self.name(), value)


class ListProperty(NodeProperty):

    _type = PROPERTY_LIST

    def __init__(self, *args, **kwargs):
        super(ListProperty, self).__init__(*args, **kwargs)
        self._items = []

    def items(self):
        return self._items

    def set_items(self, items=None):
        self._items = items


class CheckboxProperty(NodeProperty):

    _type = PROPERTY_CHECKBOX


class ColorProperty(NodeProperty):

    _type = PROPERTY_COLOR

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

    _type = PROPERTY_TEXT


class LabelProperty(NodeProperty):

    _type = PROPERTY_LABEL


class SliderProperty(NodeProperty):

    _type = PROPERTY_SLIDER

    def __init__(self, *args, **kwargs):
        super(SliderProperty, self).__init__(*args, **kwargs)
        self._min = 0.0
        self._max = 1.0

    def min(self):
        return self._min

    def set_min(self, value=0.0):
        self._min = value

    def max(self):
        return self._max

    def set_max(self, value=1.0):
        self._max = value


class FloatSliderProperty(NodeProperty):

    _type = PROPERTY_FLOAT_SLIDER

    def __init__(self,  *args, **kwargs):
        super(FloatSliderProperty, self).__init__(*args, **kwargs)
        self._min = 0.0
        self._max = 1.0

    def min(self):
        return self._min

    def set_min(self, value=0.0):
        self._min = value

    def max(self):
        return self._max

    def set_max(self, value=1.0):
        self._max = value
