// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_messages:msg/FaceCoordinates.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__MSG__DETAIL__FACE_COORDINATES__BUILDER_HPP_
#define CUSTOM_MESSAGES__MSG__DETAIL__FACE_COORDINATES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_messages/msg/detail/face_coordinates__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_messages
{

namespace msg
{

namespace builder
{

class Init_FaceCoordinates_upper_left
{
public:
  explicit Init_FaceCoordinates_upper_left(::custom_messages::msg::FaceCoordinates & msg)
  : msg_(msg)
  {}
  ::custom_messages::msg::FaceCoordinates upper_left(::custom_messages::msg::FaceCoordinates::_upper_left_type arg)
  {
    msg_.upper_left = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_messages::msg::FaceCoordinates msg_;
};

class Init_FaceCoordinates_bottom_right
{
public:
  explicit Init_FaceCoordinates_bottom_right(::custom_messages::msg::FaceCoordinates & msg)
  : msg_(msg)
  {}
  Init_FaceCoordinates_upper_left bottom_right(::custom_messages::msg::FaceCoordinates::_bottom_right_type arg)
  {
    msg_.bottom_right = std::move(arg);
    return Init_FaceCoordinates_upper_left(msg_);
  }

private:
  ::custom_messages::msg::FaceCoordinates msg_;
};

class Init_FaceCoordinates_center
{
public:
  Init_FaceCoordinates_center()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FaceCoordinates_bottom_right center(::custom_messages::msg::FaceCoordinates::_center_type arg)
  {
    msg_.center = std::move(arg);
    return Init_FaceCoordinates_bottom_right(msg_);
  }

private:
  ::custom_messages::msg::FaceCoordinates msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_messages::msg::FaceCoordinates>()
{
  return custom_messages::msg::builder::Init_FaceCoordinates_center();
}

}  // namespace custom_messages

#endif  // CUSTOM_MESSAGES__MSG__DETAIL__FACE_COORDINATES__BUILDER_HPP_
