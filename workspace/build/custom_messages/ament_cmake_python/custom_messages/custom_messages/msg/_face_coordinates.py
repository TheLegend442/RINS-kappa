# generated from rosidl_generator_py/resource/_idl.py.em
# with input from custom_messages:msg/FaceCoordinates.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_FaceCoordinates(type):
    """Metaclass of message 'FaceCoordinates'."""

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
                'custom_messages.msg.FaceCoordinates')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__face_coordinates
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__face_coordinates
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__face_coordinates
            cls._TYPE_SUPPORT = module.type_support_msg__msg__face_coordinates
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__face_coordinates

            from visualization_msgs.msg import Marker
            if Marker.__class__._TYPE_SUPPORT is None:
                Marker.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class FaceCoordinates(metaclass=Metaclass_FaceCoordinates):
    """Message class 'FaceCoordinates'."""

    __slots__ = [
        '_center',
        '_bottom_left',
        '_bottom_right',
        '_upper_left',
        '_upper_right',
    ]

    _fields_and_field_types = {
        'center': 'visualization_msgs/Marker',
        'bottom_left': 'visualization_msgs/Marker',
        'bottom_right': 'visualization_msgs/Marker',
        'upper_left': 'visualization_msgs/Marker',
        'upper_right': 'visualization_msgs/Marker',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['visualization_msgs', 'msg'], 'Marker'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['visualization_msgs', 'msg'], 'Marker'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['visualization_msgs', 'msg'], 'Marker'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['visualization_msgs', 'msg'], 'Marker'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['visualization_msgs', 'msg'], 'Marker'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from visualization_msgs.msg import Marker
        self.center = kwargs.get('center', Marker())
        from visualization_msgs.msg import Marker
        self.bottom_left = kwargs.get('bottom_left', Marker())
        from visualization_msgs.msg import Marker
        self.bottom_right = kwargs.get('bottom_right', Marker())
        from visualization_msgs.msg import Marker
        self.upper_left = kwargs.get('upper_left', Marker())
        from visualization_msgs.msg import Marker
        self.upper_right = kwargs.get('upper_right', Marker())

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
        if self.center != other.center:
            return False
        if self.bottom_left != other.bottom_left:
            return False
        if self.bottom_right != other.bottom_right:
            return False
        if self.upper_left != other.upper_left:
            return False
        if self.upper_right != other.upper_right:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def center(self):
        """Message field 'center'."""
        return self._center

    @center.setter
    def center(self, value):
        if __debug__:
            from visualization_msgs.msg import Marker
            assert \
                isinstance(value, Marker), \
                "The 'center' field must be a sub message of type 'Marker'"
        self._center = value

    @builtins.property
    def bottom_left(self):
        """Message field 'bottom_left'."""
        return self._bottom_left

    @bottom_left.setter
    def bottom_left(self, value):
        if __debug__:
            from visualization_msgs.msg import Marker
            assert \
                isinstance(value, Marker), \
                "The 'bottom_left' field must be a sub message of type 'Marker'"
        self._bottom_left = value

    @builtins.property
    def bottom_right(self):
        """Message field 'bottom_right'."""
        return self._bottom_right

    @bottom_right.setter
    def bottom_right(self, value):
        if __debug__:
            from visualization_msgs.msg import Marker
            assert \
                isinstance(value, Marker), \
                "The 'bottom_right' field must be a sub message of type 'Marker'"
        self._bottom_right = value

    @builtins.property
    def upper_left(self):
        """Message field 'upper_left'."""
        return self._upper_left

    @upper_left.setter
    def upper_left(self, value):
        if __debug__:
            from visualization_msgs.msg import Marker
            assert \
                isinstance(value, Marker), \
                "The 'upper_left' field must be a sub message of type 'Marker'"
        self._upper_left = value

    @builtins.property
    def upper_right(self):
        """Message field 'upper_right'."""
        return self._upper_right

    @upper_right.setter
    def upper_right(self, value):
        if __debug__:
            from visualization_msgs.msg import Marker
            assert \
                isinstance(value, Marker), \
                "The 'upper_right' field must be a sub message of type 'Marker'"
        self._upper_right = value
