// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_messages:msg/FaceCoordinates.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__MSG__DETAIL__FACE_COORDINATES__STRUCT_HPP_
#define CUSTOM_MESSAGES__MSG__DETAIL__FACE_COORDINATES__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'center'
// Member 'bottom_right'
// Member 'upper_left'
#include "visualization_msgs/msg/detail/marker__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__custom_messages__msg__FaceCoordinates __attribute__((deprecated))
#else
# define DEPRECATED__custom_messages__msg__FaceCoordinates __declspec(deprecated)
#endif

namespace custom_messages
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct FaceCoordinates_
{
  using Type = FaceCoordinates_<ContainerAllocator>;

  explicit FaceCoordinates_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : center(_init),
    bottom_right(_init),
    upper_left(_init)
  {
    (void)_init;
  }

  explicit FaceCoordinates_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : center(_alloc, _init),
    bottom_right(_alloc, _init),
    upper_left(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _center_type =
    visualization_msgs::msg::Marker_<ContainerAllocator>;
  _center_type center;
  using _bottom_right_type =
    visualization_msgs::msg::Marker_<ContainerAllocator>;
  _bottom_right_type bottom_right;
  using _upper_left_type =
    visualization_msgs::msg::Marker_<ContainerAllocator>;
  _upper_left_type upper_left;

  // setters for named parameter idiom
  Type & set__center(
    const visualization_msgs::msg::Marker_<ContainerAllocator> & _arg)
  {
    this->center = _arg;
    return *this;
  }
  Type & set__bottom_right(
    const visualization_msgs::msg::Marker_<ContainerAllocator> & _arg)
  {
    this->bottom_right = _arg;
    return *this;
  }
  Type & set__upper_left(
    const visualization_msgs::msg::Marker_<ContainerAllocator> & _arg)
  {
    this->upper_left = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_messages::msg::FaceCoordinates_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_messages::msg::FaceCoordinates_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_messages::msg::FaceCoordinates_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_messages::msg::FaceCoordinates_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_messages::msg::FaceCoordinates_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_messages::msg::FaceCoordinates_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_messages::msg::FaceCoordinates_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_messages::msg::FaceCoordinates_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_messages::msg::FaceCoordinates_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_messages::msg::FaceCoordinates_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_messages__msg__FaceCoordinates
    std::shared_ptr<custom_messages::msg::FaceCoordinates_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_messages__msg__FaceCoordinates
    std::shared_ptr<custom_messages::msg::FaceCoordinates_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FaceCoordinates_ & other) const
  {
    if (this->center != other.center) {
      return false;
    }
    if (this->bottom_right != other.bottom_right) {
      return false;
    }
    if (this->upper_left != other.upper_left) {
      return false;
    }
    return true;
  }
  bool operator!=(const FaceCoordinates_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FaceCoordinates_

// alias to use template instance with default allocator
using FaceCoordinates =
  custom_messages::msg::FaceCoordinates_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_messages

#endif  // CUSTOM_MESSAGES__MSG__DETAIL__FACE_COORDINATES__STRUCT_HPP_
