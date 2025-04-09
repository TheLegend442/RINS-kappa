// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_messages:msg/FaceCoordinates.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__MSG__DETAIL__FACE_COORDINATES__TRAITS_HPP_
#define CUSTOM_MESSAGES__MSG__DETAIL__FACE_COORDINATES__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_messages/msg/detail/face_coordinates__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'center'
// Member 'bottom_right'
// Member 'upper_left'
#include "visualization_msgs/msg/detail/marker__traits.hpp"

namespace custom_messages
{

namespace msg
{

inline void to_flow_style_yaml(
  const FaceCoordinates & msg,
  std::ostream & out)
{
  out << "{";
  // member: center
  {
    out << "center: ";
    to_flow_style_yaml(msg.center, out);
    out << ", ";
  }

  // member: bottom_right
  {
    out << "bottom_right: ";
    to_flow_style_yaml(msg.bottom_right, out);
    out << ", ";
  }

  // member: upper_left
  {
    out << "upper_left: ";
    to_flow_style_yaml(msg.upper_left, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const FaceCoordinates & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: center
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center:\n";
    to_block_style_yaml(msg.center, out, indentation + 2);
  }

  // member: bottom_right
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "bottom_right:\n";
    to_block_style_yaml(msg.bottom_right, out, indentation + 2);
  }

  // member: upper_left
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "upper_left:\n";
    to_block_style_yaml(msg.upper_left, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const FaceCoordinates & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace custom_messages

namespace rosidl_generator_traits
{

[[deprecated("use custom_messages::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_messages::msg::FaceCoordinates & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_messages::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_messages::msg::to_yaml() instead")]]
inline std::string to_yaml(const custom_messages::msg::FaceCoordinates & msg)
{
  return custom_messages::msg::to_yaml(msg);
}

template<>
inline const char * data_type<custom_messages::msg::FaceCoordinates>()
{
  return "custom_messages::msg::FaceCoordinates";
}

template<>
inline const char * name<custom_messages::msg::FaceCoordinates>()
{
  return "custom_messages/msg/FaceCoordinates";
}

template<>
struct has_fixed_size<custom_messages::msg::FaceCoordinates>
  : std::integral_constant<bool, has_fixed_size<visualization_msgs::msg::Marker>::value> {};

template<>
struct has_bounded_size<custom_messages::msg::FaceCoordinates>
  : std::integral_constant<bool, has_bounded_size<visualization_msgs::msg::Marker>::value> {};

template<>
struct is_message<custom_messages::msg::FaceCoordinates>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_MESSAGES__MSG__DETAIL__FACE_COORDINATES__TRAITS_HPP_
