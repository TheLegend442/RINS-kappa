// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_messages:srv/PosesInFrontOfFaces.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_FACES__BUILDER_HPP_
#define CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_FACES__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_messages/srv/detail/poses_in_front_of_faces__struct.hpp"
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
auto build<::custom_messages::srv::PosesInFrontOfFaces_Request>()
{
  return ::custom_messages::srv::PosesInFrontOfFaces_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace custom_messages


namespace custom_messages
{

namespace srv
{

namespace builder
{

class Init_PosesInFrontOfFaces_Response_poses
{
public:
  Init_PosesInFrontOfFaces_Response_poses()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_messages::srv::PosesInFrontOfFaces_Response poses(::custom_messages::srv::PosesInFrontOfFaces_Response::_poses_type arg)
  {
    msg_.poses = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_messages::srv::PosesInFrontOfFaces_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_messages::srv::PosesInFrontOfFaces_Response>()
{
  return custom_messages::srv::builder::Init_PosesInFrontOfFaces_Response_poses();
}

}  // namespace custom_messages

#endif  // CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_FACES__BUILDER_HPP_
