# generated from rosidl_generator_py/resource/_idl.py.em
# with input from custom_messages:srv/Shape.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Shape_Request(type):
    """Metaclass of message 'Shape_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('custom_messages')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'custom_messages.srv.Shape_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__shape__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__shape__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__shape__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__shape__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__shape__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Shape_Request(metaclass=Metaclass_Shape_Request):
    """Message class 'Shape_Request'."""

    __slots__ = [
        '_shape',
        '_duration',
    ]

    _fields_and_field_types = {
        'shape': 'string',
        'duration': 'int32',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.shape = kwargs.get('shape', str())
        self.duration = kwargs.get('duration', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.shape != other.shape:
            return False
        if self.duration != other.duration:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def shape(self):
        """Message field 'shape'."""
        return self._shape

    @shape.setter
    def shape(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'shape' field must be of type 'str'"
        self._shape = value

    @builtins.property
    def duration(self):
        """Message field 'duration'."""
        return self._duration

    @duration.setter
    def duration(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'duration' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'duration' field must be an integer in [-2147483648, 2147483647]"
        self._duration = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_Shape_Response(type):
    """Metaclass of message 'Shape_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('custom_messages')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'custom_messages.srv.Shape_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__shape__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__shape__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__shape__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__shape__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__shape__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Shape_Response(metaclass=Metaclass_Shape_Response):
    """Message class 'Shape_Response'."""

    __slots__ = [
        '_shape',
    ]

    _fields_and_field_types = {
        'shape': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.shape = kwargs.get('shape', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.shape != other.shape:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def shape(self):
        """Message field 'shape'."""
        return self._shape

    @shape.setter
    def shape(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'shape' field must be of type 'str'"
        self._shape = value


class Metaclass_Shape(type):
    """Metaclass of service 'Shape'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('custom_messages')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'custom_messages.srv.Shape')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__shape

            from custom_messages.srv import _shape
            if _shape.Metaclass_Shape_Request._TYPE_SUPPORT is None:
                _shape.Metaclass_Shape_Request.__import_type_support__()
            if _shape.Metaclass_Shape_Response._TYPE_SUPPORT is None:
                _shape.Metaclass_Shape_Response.__import_type_support__()


class Shape(metaclass=Metaclass_Shape):
    from custom_messages.srv._shape import Shape_Request as Request
    from custom_messages.srv._shape import Shape_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
