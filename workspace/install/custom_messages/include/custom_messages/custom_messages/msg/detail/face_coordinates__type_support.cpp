// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from custom_messages:msg/FaceCoordinates.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "custom_messages/msg/detail/face_coordinates__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace custom_messages
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void FaceCoordinates_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) custom_messages::msg::FaceCoordinates(_init);
}

void FaceCoordinates_fini_function(void * message_memory)
{
  auto typed_message = static_cast<custom_messages::msg::FaceCoordinates *>(message_memory);
  typed_message->~FaceCoordinates();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember FaceCoordinates_message_member_array[3] = {
  {
    "center",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<visualization_msgs::msg::Marker>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_messages::msg::FaceCoordinates, center),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "bottom_right",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<visualization_msgs::msg::Marker>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_messages::msg::FaceCoordinates, bottom_right),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "upper_left",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<visualization_msgs::msg::Marker>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_messages::msg::FaceCoordinates, upper_left),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers FaceCoordinates_message_members = {
  "custom_messages::msg",  // message namespace
  "FaceCoordinates",  // message name
  3,  // number of fields
  sizeof(custom_messages::msg::FaceCoordinates),
  FaceCoordinates_message_member_array,  // message members
  FaceCoordinates_init_function,  // function to initialize message memory (memory has to be allocated)
  FaceCoordinates_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t FaceCoordinates_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &FaceCoordinates_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace custom_messages


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<custom_messages::msg::FaceCoordinates>()
{
  return &::custom_messages::msg::rosidl_typesupport_introspection_cpp::FaceCoordinates_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, custom_messages, msg, FaceCoordinates)() {
  return &::custom_messages::msg::rosidl_typesupport_introspection_cpp::FaceCoordinates_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
