// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_messages:srv/Shape.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__SRV__DETAIL__SHAPE__BUILDER_HPP_
#define CUSTOM_MESSAGES__SRV__DETAIL__SHAPE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_messages/srv/detail/shape__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_messages
{

namespace srv
{

namespace builder
{

class Init_Shape_Request_duration
{
public:
  explicit Init_Shape_Request_duration(::custom_messages::srv::Shape_Request & msg)
  : msg_(msg)
  {}
  ::custom_messages::srv::Shape_Request duration(::custom_messages::srv::Shape_Request::_duration_type arg)
  {
    msg_.duration = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_messages::srv::Shape_Request msg_;
};

class Init_Shape_Request_shape
{
public:
  Init_Shape_Request_shape()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Shape_Request_duration shape(::custom_messages::srv::Shape_Request::_shape_type arg)
  {
    msg_.shape = std::move(arg);
    return Init_Shape_Request_duration(msg_);
  }

private:
  ::custom_messages::srv::Shape_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_messages::srv::Shape_Request>()
{
  return custom_messages::srv::builder::Init_Shape_Request_shape();
}

}  // namespace custom_messages


namespace custom_messages
{

namespace srv
{

namespace builder
{

class Init_Shape_Response_shape
{
public:
  Init_Shape_Response_shape()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_messages::srv::Shape_Response shape(::custom_messages::srv::Shape_Response::_shape_type arg)
  {
    msg_.shape = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_messages::srv::Shape_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_messages::srv::Shape_Response>()
{
  return custom_messages::srv::builder::Init_Shape_Response_shape();
}

}  // namespace custom_messages


namespace custom_messages
{

namespace srv
{

namespace builder
{

class Init_Shape_Event_response
{
public:
  explicit Init_Shape_Event_response(::custom_messages::srv::Shape_Event & msg)
  : msg_(msg)
  {}
  ::custom_messages::srv::Shape_Event response(::custom_messages::srv::Shape_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_messages::srv::Shape_Event msg_;
};

class Init_Shape_Event_request
{
public:
  explicit Init_Shape_Event_request(::custom_messages::srv::Shape_Event & msg)
  : msg_(msg)
  {}
  Init_Shape_Event_response request(::custom_messages::srv::Shape_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_Shape_Event_response(msg_);
  }

private:
  ::custom_messages::srv::Shape_Event msg_;
};

class Init_Shape_Event_info
{
public:
  Init_Shape_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Shape_Event_request info(::custom_messages::srv::Shape_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_Shape_Event_request(msg_);
  }

private:
  ::custom_messages::srv::Shape_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_messages::srv::Shape_Event>()
{
  return custom_messages::srv::builder::Init_Shape_Event_info();
}

}  // namespace custom_messages

#endif  // CUSTOM_MESSAGES__SRV__DETAIL__SHAPE__BUILDER_HPP_
