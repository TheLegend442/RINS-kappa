// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from custom_messages:msg/FaceCoordinates.idl
// generated code does not contain a copyright notice
#include "custom_messages/msg/detail/face_coordinates__rosidl_typesupport_fastrtps_cpp.hpp"
#include "custom_messages/msg/detail/face_coordinates__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions
namespace visualization_msgs
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const visualization_msgs::msg::Marker &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  visualization_msgs::msg::Marker &);
size_t get_serialized_size(
  const visualization_msgs::msg::Marker &,
  size_t current_alignment);
size_t
max_serialized_size_Marker(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace visualization_msgs

// functions for visualization_msgs::msg::Marker already declared above

// functions for visualization_msgs::msg::Marker already declared above


namespace custom_messages
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_messages
cdr_serialize(
  const custom_messages::msg::FaceCoordinates & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: center
  visualization_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.center,
    cdr);
  // Member: bottom_right
  visualization_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.bottom_right,
    cdr);
  // Member: upper_left
  visualization_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.upper_left,
    cdr);
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_messages
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  custom_messages::msg::FaceCoordinates & ros_message)
{
  // Member: center
  visualization_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.center);

  // Member: bottom_right
  visualization_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.bottom_right);

  // Member: upper_left
  visualization_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.upper_left);

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_messages
get_serialized_size(
  const custom_messages::msg::FaceCoordinates & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: center

  current_alignment +=
    visualization_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.center, current_alignment);
  // Member: bottom_right

  current_alignment +=
    visualization_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.bottom_right, current_alignment);
  // Member: upper_left

  current_alignment +=
    visualization_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.upper_left, current_alignment);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_custom_messages
max_serialized_size_FaceCoordinates(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: center
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        visualization_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_Marker(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: bottom_right
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        visualization_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_Marker(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: upper_left
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        visualization_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_Marker(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = custom_messages::msg::FaceCoordinates;
    is_plain =
      (
      offsetof(DataType, upper_left) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _FaceCoordinates__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const custom_messages::msg::FaceCoordinates *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _FaceCoordinates__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<custom_messages::msg::FaceCoordinates *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _FaceCoordinates__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const custom_messages::msg::FaceCoordinates *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _FaceCoordinates__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_FaceCoordinates(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _FaceCoordinates__callbacks = {
  "custom_messages::msg",
  "FaceCoordinates",
  _FaceCoordinates__cdr_serialize,
  _FaceCoordinates__cdr_deserialize,
  _FaceCoordinates__get_serialized_size,
  _FaceCoordinates__max_serialized_size
};

static rosidl_message_type_support_t _FaceCoordinates__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_FaceCoordinates__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace custom_messages

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_custom_messages
const rosidl_message_type_support_t *
get_message_type_support_handle<custom_messages::msg::FaceCoordinates>()
{
  return &custom_messages::msg::typesupport_fastrtps_cpp::_FaceCoordinates__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, custom_messages, msg, FaceCoordinates)() {
  return &custom_messages::msg::typesupport_fastrtps_cpp::_FaceCoordinates__handle;
}

#ifdef __cplusplus
}
#endif
