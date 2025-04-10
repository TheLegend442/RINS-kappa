// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from custom_messages:msg/RingCoordinates.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "custom_messages/msg/detail/ring_coordinates__rosidl_typesupport_introspection_c.h"
#include "custom_messages/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "custom_messages/msg/detail/ring_coordinates__functions.h"
#include "custom_messages/msg/detail/ring_coordinates__struct.h"


// Include directives for member types
// Member `center`
#include "visualization_msgs/msg/marker.h"
// Member `center`
#include "visualization_msgs/msg/detail/marker__rosidl_typesupport_introspection_c.h"
// Member `color`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  custom_messages__msg__RingCoordinates__init(message_memory);
}

void custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_fini_function(void * message_memory)
{
  custom_messages__msg__RingCoordinates__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_message_member_array[2] = {
  {
    "center",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_messages__msg__RingCoordinates, center),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "color",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_messages__msg__RingCoordinates, color),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_message_members = {
  "custom_messages__msg",  // message namespace
  "RingCoordinates",  // message name
  2,  // number of fields
  sizeof(custom_messages__msg__RingCoordinates),
  custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_message_member_array,  // message members
  custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_init_function,  // function to initialize message memory (memory has to be allocated)
  custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_message_type_support_handle = {
  0,
  &custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_custom_messages
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_messages, msg, RingCoordinates)() {
  custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, visualization_msgs, msg, Marker)();
  if (!custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_message_type_support_handle.typesupport_identifier) {
    custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &custom_messages__msg__RingCoordinates__rosidl_typesupport_introspection_c__RingCoordinates_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
