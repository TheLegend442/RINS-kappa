// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from dis_tutorial1:srv/AddArray.idl
// generated code does not contain a copyright notice

#ifndef DIS_TUTORIAL1__SRV__DETAIL__ADD_ARRAY__TRAITS_HPP_
#define DIS_TUTORIAL1__SRV__DETAIL__ADD_ARRAY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "dis_tutorial1/srv/detail/add_array__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace dis_tutorial1
{

namespace srv
{

inline void to_flow_style_yaml(
  const AddArray_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: description
  {
    out << "description: ";
    rosidl_generator_traits::value_to_yaml(msg.description, out);
    out << ", ";
  }

  // member: numbers
  {
    if (msg.numbers.size() == 0) {
      out << "numbers: []";
    } else {
      out << "numbers: [";
      size_t pending_items = msg.numbers.size();
      for (auto item : msg.numbers) {
        rosidl_generator_traits::value_to_yaml(item, out);
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
  const AddArray_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: description
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "description: ";
    rosidl_generator_traits::value_to_yaml(msg.description, out);
    out << "\n";
  }

  // member: numbers
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.numbers.size() == 0) {
      out << "numbers: []\n";
    } else {
      out << "numbers:\n";
      for (auto item : msg.numbers) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const AddArray_Request & msg, bool use_flow_style = false)
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

}  // namespace dis_tutorial1

namespace rosidl_generator_traits
{

[[deprecated("use dis_tutorial1::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dis_tutorial1::srv::AddArray_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  dis_tutorial1::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dis_tutorial1::srv::to_yaml() instead")]]
inline std::string to_yaml(const dis_tutorial1::srv::AddArray_Request & msg)
{
  return dis_tutorial1::srv::to_yaml(msg);
}

template<>
inline const char * data_type<dis_tutorial1::srv::AddArray_Request>()
{
  return "dis_tutorial1::srv::AddArray_Request";
}

template<>
inline const char * name<dis_tutorial1::srv::AddArray_Request>()
{
  return "dis_tutorial1/srv/AddArray_Request";
}

template<>
struct has_fixed_size<dis_tutorial1::srv::AddArray_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<dis_tutorial1::srv::AddArray_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<dis_tutorial1::srv::AddArray_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace dis_tutorial1
{

namespace srv
{

inline void to_flow_style_yaml(
  const AddArray_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: type
  {
    out << "type: ";
    rosidl_generator_traits::value_to_yaml(msg.type, out);
    out << ", ";
  }

  // member: sum
  {
    out << "sum: ";
    rosidl_generator_traits::value_to_yaml(msg.sum, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const AddArray_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "type: ";
    rosidl_generator_traits::value_to_yaml(msg.type, out);
    out << "\n";
  }

  // member: sum
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sum: ";
    rosidl_generator_traits::value_to_yaml(msg.sum, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const AddArray_Response & msg, bool use_flow_style = false)
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

}  // namespace dis_tutorial1

namespace rosidl_generator_traits
{

[[deprecated("use dis_tutorial1::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dis_tutorial1::srv::AddArray_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  dis_tutorial1::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dis_tutorial1::srv::to_yaml() instead")]]
inline std::string to_yaml(const dis_tutorial1::srv::AddArray_Response & msg)
{
  return dis_tutorial1::srv::to_yaml(msg);
}

template<>
inline const char * data_type<dis_tutorial1::srv::AddArray_Response>()
{
  return "dis_tutorial1::srv::AddArray_Response";
}

template<>
inline const char * name<dis_tutorial1::srv::AddArray_Response>()
{
  return "dis_tutorial1/srv/AddArray_Response";
}

template<>
struct has_fixed_size<dis_tutorial1::srv::AddArray_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<dis_tutorial1::srv::AddArray_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<dis_tutorial1::srv::AddArray_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<dis_tutorial1::srv::AddArray>()
{
  return "dis_tutorial1::srv::AddArray";
}

template<>
inline const char * name<dis_tutorial1::srv::AddArray>()
{
  return "dis_tutorial1/srv/AddArray";
}

template<>
struct has_fixed_size<dis_tutorial1::srv::AddArray>
  : std::integral_constant<
    bool,
    has_fixed_size<dis_tutorial1::srv::AddArray_Request>::value &&
    has_fixed_size<dis_tutorial1::srv::AddArray_Response>::value
  >
{
};

template<>
struct has_bounded_size<dis_tutorial1::srv::AddArray>
  : std::integral_constant<
    bool,
    has_bounded_size<dis_tutorial1::srv::AddArray_Request>::value &&
    has_bounded_size<dis_tutorial1::srv::AddArray_Response>::value
  >
{
};

template<>
struct is_service<dis_tutorial1::srv::AddArray>
  : std::true_type
{
};

template<>
struct is_service_request<dis_tutorial1::srv::AddArray_Request>
  : std::true_type
{
};

template<>
struct is_service_response<dis_tutorial1::srv::AddArray_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // DIS_TUTORIAL1__SRV__DETAIL__ADD_ARRAY__TRAITS_HPP_
