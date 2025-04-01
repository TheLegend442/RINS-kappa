// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dis_tutorial1:srv/AddArray.idl
// generated code does not contain a copyright notice

#ifndef DIS_TUTORIAL1__SRV__DETAIL__ADD_ARRAY__BUILDER_HPP_
#define DIS_TUTORIAL1__SRV__DETAIL__ADD_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dis_tutorial1/srv/detail/add_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dis_tutorial1
{

namespace srv
{

namespace builder
{

class Init_AddArray_Request_numbers
{
public:
  explicit Init_AddArray_Request_numbers(::dis_tutorial1::srv::AddArray_Request & msg)
  : msg_(msg)
  {}
  ::dis_tutorial1::srv::AddArray_Request numbers(::dis_tutorial1::srv::AddArray_Request::_numbers_type arg)
  {
    msg_.numbers = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dis_tutorial1::srv::AddArray_Request msg_;
};

class Init_AddArray_Request_description
{
public:
  Init_AddArray_Request_description()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AddArray_Request_numbers description(::dis_tutorial1::srv::AddArray_Request::_description_type arg)
  {
    msg_.description = std::move(arg);
    return Init_AddArray_Request_numbers(msg_);
  }

private:
  ::dis_tutorial1::srv::AddArray_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dis_tutorial1::srv::AddArray_Request>()
{
  return dis_tutorial1::srv::builder::Init_AddArray_Request_description();
}

}  // namespace dis_tutorial1


namespace dis_tutorial1
{

namespace srv
{

namespace builder
{

class Init_AddArray_Response_sum
{
public:
  explicit Init_AddArray_Response_sum(::dis_tutorial1::srv::AddArray_Response & msg)
  : msg_(msg)
  {}
  ::dis_tutorial1::srv::AddArray_Response sum(::dis_tutorial1::srv::AddArray_Response::_sum_type arg)
  {
    msg_.sum = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dis_tutorial1::srv::AddArray_Response msg_;
};

class Init_AddArray_Response_type
{
public:
  Init_AddArray_Response_type()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AddArray_Response_sum type(::dis_tutorial1::srv::AddArray_Response::_type_type arg)
  {
    msg_.type = std::move(arg);
    return Init_AddArray_Response_sum(msg_);
  }

private:
  ::dis_tutorial1::srv::AddArray_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dis_tutorial1::srv::AddArray_Response>()
{
  return dis_tutorial1::srv::builder::Init_AddArray_Response_type();
}

}  // namespace dis_tutorial1

#endif  // DIS_TUTORIAL1__SRV__DETAIL__ADD_ARRAY__BUILDER_HPP_
