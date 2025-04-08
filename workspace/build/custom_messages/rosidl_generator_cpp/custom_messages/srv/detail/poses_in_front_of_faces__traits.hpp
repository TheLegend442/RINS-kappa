// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_messages:srv/PosesInFrontOfFaces.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_FACES__TRAITS_HPP_
#define CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_FACES__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_messages/srv/detail/poses_in_front_of_faces__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace custom_messages
{

namespace srv
{

inline void to_flow_style_yaml(
  const PosesInFrontOfFaces_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PosesInFrontOfFaces_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PosesInFrontOfFaces_Request & msg, bool use_flow_style = false)
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
  const custom_messages::srv::PosesInFrontOfFaces_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_messages::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_messages::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_messages::srv::PosesInFrontOfFaces_Request & msg)
{
  return custom_messages::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_messages::srv::PosesInFrontOfFaces_Request>()
{
  return "custom_messages::srv::PosesInFrontOfFaces_Request";
}

template<>
inline const char * name<custom_messages::srv::PosesInFrontOfFaces_Request>()
{
  return "custom_messages/srv/PosesInFrontOfFaces_Request";
}

template<>
struct has_fixed_size<custom_messages::srv::PosesInFrontOfFaces_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<custom_messages::srv::PosesInFrontOfFaces_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<custom_messages::srv::PosesInFrontOfFaces_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'poses'
#include "geometry_msgs/msg/detail/pose__traits.hpp"

namespace custom_messages
{

namespace srv
{

inline void to_flow_style_yaml(
  const PosesInFrontOfFaces_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: poses
  {
    if (msg.poses.size() == 0) {
      out << "poses: []";
    } else {
      out << "poses: [";
      size_t pending_items = msg.poses.size();
      for (auto item : msg.poses) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PosesInFrontOfFaces_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: poses
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.poses.size() == 0) {
      out << "poses: []\n";
    } else {
      out << "poses:\n";
      for (auto item : msg.poses) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PosesInFrontOfFaces_Response & msg, bool use_flow_style = false)
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
  const custom_messages::srv::PosesInFrontOfFaces_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_messages::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_messages::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_messages::srv::PosesInFrontOfFaces_Response & msg)
{
  return custom_messages::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_messages::srv::PosesInFrontOfFaces_Response>()
{
  return "custom_messages::srv::PosesInFrontOfFaces_Response";
}

template<>
inline const char * name<custom_messages::srv::PosesInFrontOfFaces_Response>()
{
  return "custom_messages/srv/PosesInFrontOfFaces_Response";
}

template<>
struct has_fixed_size<custom_messages::srv::PosesInFrontOfFaces_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_messages::srv::PosesInFrontOfFaces_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_messages::srv::PosesInFrontOfFaces_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<custom_messages::srv::PosesInFrontOfFaces>()
{
  return "custom_messages::srv::PosesInFrontOfFaces";
}

template<>
inline const char * name<custom_messages::srv::PosesInFrontOfFaces>()
{
  return "custom_messages/srv/PosesInFrontOfFaces";
}

template<>
struct has_fixed_size<custom_messages::srv::PosesInFrontOfFaces>
  : std::integral_constant<
    bool,
    has_fixed_size<custom_messages::srv::PosesInFrontOfFaces_Request>::value &&
    has_fixed_size<custom_messages::srv::PosesInFrontOfFaces_Response>::value
  >
{
};

template<>
struct has_bounded_size<custom_messages::srv::PosesInFrontOfFaces>
  : std::integral_constant<
    bool,
    has_bounded_size<custom_messages::srv::PosesInFrontOfFaces_Request>::value &&
    has_bounded_size<custom_messages::srv::PosesInFrontOfFaces_Response>::value
  >
{
};

template<>
struct is_service<custom_messages::srv::PosesInFrontOfFaces>
  : std::true_type
{
};

template<>
struct is_service_request<custom_messages::srv::PosesInFrontOfFaces_Request>
  : std::true_type
{
};

template<>
struct is_service_response<custom_messages::srv::PosesInFrontOfFaces_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_FACES__TRAITS_HPP_
