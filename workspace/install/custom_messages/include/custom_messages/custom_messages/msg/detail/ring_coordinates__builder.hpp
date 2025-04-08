// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_messages:msg/RingCoordinates.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__MSG__DETAIL__RING_COORDINATES__BUILDER_HPP_
#define CUSTOM_MESSAGES__MSG__DETAIL__RING_COORDINATES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_messages/msg/detail/ring_coordinates__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_messages
{

namespace msg
{

namespace builder
{

class Init_RingCoordinates_center
{
public:
  Init_RingCoordinates_center()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_messages::msg::RingCoordinates center(::custom_messages::msg::RingCoordinates::_center_type arg)
  {
    msg_.center = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_messages::msg::RingCoordinates msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_messages::msg::RingCoordinates>()
{
  return custom_messages::msg::builder::Init_RingCoordinates_center();
}

}  // namespace custom_messages

#endif  // CUSTOM_MESSAGES__MSG__DETAIL__RING_COORDINATES__BUILDER_HPP_
