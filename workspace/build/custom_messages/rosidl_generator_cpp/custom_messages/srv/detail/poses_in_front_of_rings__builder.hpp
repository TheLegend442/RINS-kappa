// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_messages:srv/PosesInFrontOfRings.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_RINGS__BUILDER_HPP_
#define CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_RINGS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_messages/srv/detail/poses_in_front_of_rings__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_messages
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_messages::srv::PosesInFrontOfRings_Request>()
{
  return ::custom_messages::srv::PosesInFrontOfRings_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace custom_messages


namespace custom_messages
{

namespace srv
{

namespace builder
{

class Init_PosesInFrontOfRings_Response_colors
{
public:
  explicit Init_PosesInFrontOfRings_Response_colors(::custom_messages::srv::PosesInFrontOfRings_Response & msg)
  : msg_(msg)
  {}
  ::custom_messages::srv::PosesInFrontOfRings_Response colors(::custom_messages::srv::PosesInFrontOfRings_Response::_colors_type arg)
  {
    msg_.colors = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_messages::srv::PosesInFrontOfRings_Response msg_;
};

class Init_PosesInFrontOfRings_Response_poses
{
public:
  Init_PosesInFrontOfRings_Response_poses()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PosesInFrontOfRings_Response_colors poses(::custom_messages::srv::PosesInFrontOfRings_Response::_poses_type arg)
  {
    msg_.poses = std::move(arg);
    return Init_PosesInFrontOfRings_Response_colors(msg_);
  }

private:
  ::custom_messages::srv::PosesInFrontOfRings_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_messages::srv::PosesInFrontOfRings_Response>()
{
  return custom_messages::srv::builder::Init_PosesInFrontOfRings_Response_poses();
}

}  // namespace custom_messages

#endif  // CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_RINGS__BUILDER_HPP_
