// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_messages:srv/Shape.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__SRV__DETAIL__SHAPE__TRAITS_HPP_
#define CUSTOM_MESSAGES__SRV__DETAIL__SHAPE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_messages/srv/detail/shape__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace custom_messages
{

namespace srv
{

inline void to_flow_style_yaml(
  const Shape_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: shape
  {
    out << "shape: ";
    rosidl_generator_traits::value_to_yaml(msg.shape, out);
    out << ", ";
  }

  // member: duration
  {
    out << "duration: ";
    rosidl_generator_traits::value_to_yaml(msg.duration, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Shape_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: shape
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "shape: ";
    rosidl_generator_traits::value_to_yaml(msg.shape, out);
    out << "\n";
  }

  // member: duration
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "duration: ";
    rosidl_generator_traits::value_to_yaml(msg.duration, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Shape_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_messages

namespace rosidl_generator_traits
{

[[deprecated("use custom_messages::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_messages::srv::Shape_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_messages::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_messages::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_messages::srv::Shape_Request & msg)
{
  return custom_messages::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_messages::srv::Shape_Request>()
{
  return "custom_messages::srv::Shape_Request";
}

template<>
inline const char * name<custom_messages::srv::Shape_Request>()
{
  return "custom_messages/srv/Shape_Request";
}

template<>
struct has_fixed_size<custom_messages::srv::Shape_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_messages::srv::Shape_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_messages::srv::Shape_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace custom_messages
{

namespace srv
{

inline void to_flow_style_yaml(
  const Shape_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: shape
  {
    out << "shape: ";
    rosidl_generator_traits::value_to_yaml(msg.shape, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Shape_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: shape
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "shape: ";
    rosidl_generator_traits::value_to_yaml(msg.shape, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Shape_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_messages

namespace rosidl_generator_traits
{

[[deprecated("use custom_messages::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_messages::srv::Shape_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_messages::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_messages::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_messages::srv::Shape_Response & msg)
{
  return custom_messages::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_messages::srv::Shape_Response>()
{
  return "custom_messages::srv::Shape_Response";
}

template<>
inline const char * name<custom_messages::srv::Shape_Response>()
{
  return "custom_messages/srv/Shape_Response";
}

template<>
struct has_fixed_size<custom_messages::srv::Shape_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_messages::srv::Shape_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_messages::srv::Shape_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<custom_messages::srv::Shape>()
{
  return "custom_messages::srv::Shape";
}

template<>
inline const char * name<custom_messages::srv::Shape>()
{
  return "custom_messages/srv/Shape";
}

template<>
struct has_fixed_size<custom_messages::srv::Shape>
  : std::integral_constant<
    bool,
    has_fixed_size<custom_messages::srv::Shape_Request>::value &&
    has_fixed_size<custom_messages::srv::Shape_Response>::value
  >
{
};

template<>
struct has_bounded_size<custom_messages::srv::Shape>
  : std::integral_constant<
    bool,
    has_bounded_size<custom_messages::srv::Shape_Request>::value &&
    has_bounded_size<custom_messages::srv::Shape_Response>::value
  >
{
};

template<>
struct is_service<custom_messages::srv::Shape>
  : std::true_type
{
};

template<>
struct is_service_request<custom_messages::srv::Shape_Request>
  : std::true_type
{
};

template<>
struct is_service_response<custom_messages::srv::Shape_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_MESSAGES__SRV__DETAIL__SHAPE__TRAITS_HPP_
