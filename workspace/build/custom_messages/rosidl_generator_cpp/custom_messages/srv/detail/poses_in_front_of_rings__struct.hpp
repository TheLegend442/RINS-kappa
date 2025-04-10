// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_messages:srv/PosesInFrontOfRings.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_RINGS__STRUCT_HPP_
#define CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_RINGS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_messages__srv__PosesInFrontOfRings_Request __attribute__((deprecated))
#else
# define DEPRECATED__custom_messages__srv__PosesInFrontOfRings_Request __declspec(deprecated)
#endif

namespace custom_messages
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct PosesInFrontOfRings_Request_
{
  using Type = PosesInFrontOfRings_Request_<ContainerAllocator>;

  explicit PosesInFrontOfRings_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit PosesInFrontOfRings_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    custom_messages::srv::PosesInFrontOfRings_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_messages::srv::PosesInFrontOfRings_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_messages::srv::PosesInFrontOfRings_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_messages::srv::PosesInFrontOfRings_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::PosesInFrontOfRings_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::PosesInFrontOfRings_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::PosesInFrontOfRings_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::PosesInFrontOfRings_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_messages::srv::PosesInFrontOfRings_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_messages::srv::PosesInFrontOfRings_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_messages__srv__PosesInFrontOfRings_Request
    std::shared_ptr<custom_messages::srv::PosesInFrontOfRings_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_messages__srv__PosesInFrontOfRings_Request
    std::shared_ptr<custom_messages::srv::PosesInFrontOfRings_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PosesInFrontOfRings_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const PosesInFrontOfRings_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PosesInFrontOfRings_Request_

// alias to use template instance with default allocator
using PosesInFrontOfRings_Request =
  custom_messages::srv::PosesInFrontOfRings_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_messages


// Include directives for member types
// Member 'poses'
#include "geometry_msgs/msg/detail/pose__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__custom_messages__srv__PosesInFrontOfRings_Response __attribute__((deprecated))
#else
# define DEPRECATED__custom_messages__srv__PosesInFrontOfRings_Response __declspec(deprecated)
#endif

namespace custom_messages
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct PosesInFrontOfRings_Response_
{
  using Type = PosesInFrontOfRings_Response_<ContainerAllocator>;

  explicit PosesInFrontOfRings_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit PosesInFrontOfRings_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _poses_type =
    std::vector<geometry_msgs::msg::Pose_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Pose_<ContainerAllocator>>>;
  _poses_type poses;
  using _colors_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _colors_type colors;

  // setters for named parameter idiom
  Type & set__poses(
    const std::vector<geometry_msgs::msg::Pose_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Pose_<ContainerAllocator>>> & _arg)
  {
    this->poses = _arg;
    return *this;
  }
  Type & set__colors(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->colors = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_messages::srv::PosesInFrontOfRings_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_messages::srv::PosesInFrontOfRings_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_messages::srv::PosesInFrontOfRings_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_messages::srv::PosesInFrontOfRings_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::PosesInFrontOfRings_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::PosesInFrontOfRings_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::PosesInFrontOfRings_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::PosesInFrontOfRings_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_messages::srv::PosesInFrontOfRings_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_messages::srv::PosesInFrontOfRings_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_messages__srv__PosesInFrontOfRings_Response
    std::shared_ptr<custom_messages::srv::PosesInFrontOfRings_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_messages__srv__PosesInFrontOfRings_Response
    std::shared_ptr<custom_messages::srv::PosesInFrontOfRings_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PosesInFrontOfRings_Response_ & other) const
  {
    if (this->poses != other.poses) {
      return false;
    }
    if (this->colors != other.colors) {
      return false;
    }
    return true;
  }
  bool operator!=(const PosesInFrontOfRings_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PosesInFrontOfRings_Response_

// alias to use template instance with default allocator
using PosesInFrontOfRings_Response =
  custom_messages::srv::PosesInFrontOfRings_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_messages

namespace custom_messages
{

namespace srv
{

struct PosesInFrontOfRings
{
  using Request = custom_messages::srv::PosesInFrontOfRings_Request;
  using Response = custom_messages::srv::PosesInFrontOfRings_Response;
};

}  // namespace srv

}  // namespace custom_messages

#endif  // CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_RINGS__STRUCT_HPP_
