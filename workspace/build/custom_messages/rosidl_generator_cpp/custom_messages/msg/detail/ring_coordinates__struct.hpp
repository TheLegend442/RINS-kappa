// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_messages:msg/RingCoordinates.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__MSG__DETAIL__RING_COORDINATES__STRUCT_HPP_
#define CUSTOM_MESSAGES__MSG__DETAIL__RING_COORDINATES__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'center'
#include "visualization_msgs/msg/detail/marker__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__custom_messages__msg__RingCoordinates __attribute__((deprecated))
#else
# define DEPRECATED__custom_messages__msg__RingCoordinates __declspec(deprecated)
#endif

namespace custom_messages
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct RingCoordinates_
{
  using Type = RingCoordinates_<ContainerAllocator>;

  explicit RingCoordinates_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : center(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->color = "";
    }
  }

  explicit RingCoordinates_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : center(_alloc, _init),
    color(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->color = "";
    }
  }

  // field types and members
  using _center_type =
    visualization_msgs::msg::Marker_<ContainerAllocator>;
  _center_type center;
  using _color_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _color_type color;

  // setters for named parameter idiom
  Type & set__center(
    const visualization_msgs::msg::Marker_<ContainerAllocator> & _arg)
  {
    this->center = _arg;
    return *this;
  }
  Type & set__color(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->color = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_messages::msg::RingCoordinates_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_messages::msg::RingCoordinates_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_messages::msg::RingCoordinates_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_messages::msg::RingCoordinates_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_messages::msg::RingCoordinates_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_messages::msg::RingCoordinates_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_messages::msg::RingCoordinates_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_messages::msg::RingCoordinates_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_messages::msg::RingCoordinates_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_messages::msg::RingCoordinates_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_messages__msg__RingCoordinates
    std::shared_ptr<custom_messages::msg::RingCoordinates_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_messages__msg__RingCoordinates
    std::shared_ptr<custom_messages::msg::RingCoordinates_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RingCoordinates_ & other) const
  {
    if (this->center != other.center) {
      return false;
    }
    if (this->color != other.color) {
      return false;
    }
    return true;
  }
  bool operator!=(const RingCoordinates_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RingCoordinates_

// alias to use template instance with default allocator
using RingCoordinates =
  custom_messages::msg::RingCoordinates_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_messages

#endif  // CUSTOM_MESSAGES__MSG__DETAIL__RING_COORDINATES__STRUCT_HPP_
