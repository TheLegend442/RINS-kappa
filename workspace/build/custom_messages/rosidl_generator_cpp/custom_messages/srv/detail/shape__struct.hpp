// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_messages:srv/Shape.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__SRV__DETAIL__SHAPE__STRUCT_HPP_
#define CUSTOM_MESSAGES__SRV__DETAIL__SHAPE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_messages__srv__Shape_Request __attribute__((deprecated))
#else
# define DEPRECATED__custom_messages__srv__Shape_Request __declspec(deprecated)
#endif

namespace custom_messages
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Shape_Request_
{
  using Type = Shape_Request_<ContainerAllocator>;

  explicit Shape_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->shape = "";
      this->duration = 0l;
    }
  }

  explicit Shape_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : shape(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->shape = "";
      this->duration = 0l;
    }
  }

  // field types and members
  using _shape_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _shape_type shape;
  using _duration_type =
    int32_t;
  _duration_type duration;

  // setters for named parameter idiom
  Type & set__shape(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->shape = _arg;
    return *this;
  }
  Type & set__duration(
    const int32_t & _arg)
  {
    this->duration = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_messages::srv::Shape_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_messages::srv::Shape_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_messages::srv::Shape_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_messages::srv::Shape_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::Shape_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::Shape_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::Shape_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::Shape_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_messages::srv::Shape_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_messages::srv::Shape_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_messages__srv__Shape_Request
    std::shared_ptr<custom_messages::srv::Shape_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_messages__srv__Shape_Request
    std::shared_ptr<custom_messages::srv::Shape_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Shape_Request_ & other) const
  {
    if (this->shape != other.shape) {
      return false;
    }
    if (this->duration != other.duration) {
      return false;
    }
    return true;
  }
  bool operator!=(const Shape_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Shape_Request_

// alias to use template instance with default allocator
using Shape_Request =
  custom_messages::srv::Shape_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_messages


#ifndef _WIN32
# define DEPRECATED__custom_messages__srv__Shape_Response __attribute__((deprecated))
#else
# define DEPRECATED__custom_messages__srv__Shape_Response __declspec(deprecated)
#endif

namespace custom_messages
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Shape_Response_
{
  using Type = Shape_Response_<ContainerAllocator>;

  explicit Shape_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->shape = "";
    }
  }

  explicit Shape_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : shape(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->shape = "";
    }
  }

  // field types and members
  using _shape_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _shape_type shape;

  // setters for named parameter idiom
  Type & set__shape(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->shape = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_messages::srv::Shape_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_messages::srv::Shape_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_messages::srv::Shape_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_messages::srv::Shape_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::Shape_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::Shape_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::Shape_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::Shape_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_messages::srv::Shape_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_messages::srv::Shape_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_messages__srv__Shape_Response
    std::shared_ptr<custom_messages::srv::Shape_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_messages__srv__Shape_Response
    std::shared_ptr<custom_messages::srv::Shape_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Shape_Response_ & other) const
  {
    if (this->shape != other.shape) {
      return false;
    }
    return true;
  }
  bool operator!=(const Shape_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Shape_Response_

// alias to use template instance with default allocator
using Shape_Response =
  custom_messages::srv::Shape_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_messages


// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__custom_messages__srv__Shape_Event __attribute__((deprecated))
#else
# define DEPRECATED__custom_messages__srv__Shape_Event __declspec(deprecated)
#endif

namespace custom_messages
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Shape_Event_
{
  using Type = Shape_Event_<ContainerAllocator>;

  explicit Shape_Event_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_init)
  {
    (void)_init;
  }

  explicit Shape_Event_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : info(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _info_type =
    service_msgs::msg::ServiceEventInfo_<ContainerAllocator>;
  _info_type info;
  using _request_type =
    rosidl_runtime_cpp::BoundedVector<custom_messages::srv::Shape_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<custom_messages::srv::Shape_Request_<ContainerAllocator>>>;
  _request_type request;
  using _response_type =
    rosidl_runtime_cpp::BoundedVector<custom_messages::srv::Shape_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<custom_messages::srv::Shape_Response_<ContainerAllocator>>>;
  _response_type response;

  // setters for named parameter idiom
  Type & set__info(
    const service_msgs::msg::ServiceEventInfo_<ContainerAllocator> & _arg)
  {
    this->info = _arg;
    return *this;
  }
  Type & set__request(
    const rosidl_runtime_cpp::BoundedVector<custom_messages::srv::Shape_Request_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<custom_messages::srv::Shape_Request_<ContainerAllocator>>> & _arg)
  {
    this->request = _arg;
    return *this;
  }
  Type & set__response(
    const rosidl_runtime_cpp::BoundedVector<custom_messages::srv::Shape_Response_<ContainerAllocator>, 1, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<custom_messages::srv::Shape_Response_<ContainerAllocator>>> & _arg)
  {
    this->response = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_messages::srv::Shape_Event_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_messages::srv::Shape_Event_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_messages::srv::Shape_Event_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_messages::srv::Shape_Event_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::Shape_Event_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::Shape_Event_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::Shape_Event_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::Shape_Event_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_messages::srv::Shape_Event_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_messages::srv::Shape_Event_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_messages__srv__Shape_Event
    std::shared_ptr<custom_messages::srv::Shape_Event_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_messages__srv__Shape_Event
    std::shared_ptr<custom_messages::srv::Shape_Event_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Shape_Event_ & other) const
  {
    if (this->info != other.info) {
      return false;
    }
    if (this->request != other.request) {
      return false;
    }
    if (this->response != other.response) {
      return false;
    }
    return true;
  }
  bool operator!=(const Shape_Event_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Shape_Event_

// alias to use template instance with default allocator
using Shape_Event =
  custom_messages::srv::Shape_Event_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_messages

namespace custom_messages
{

namespace srv
{

struct Shape
{
  using Request = custom_messages::srv::Shape_Request;
  using Response = custom_messages::srv::Shape_Response;
  using Event = custom_messages::srv::Shape_Event;
};

}  // namespace srv

}  // namespace custom_messages

#endif  // CUSTOM_MESSAGES__SRV__DETAIL__SHAPE__STRUCT_HPP_
