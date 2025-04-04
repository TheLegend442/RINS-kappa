// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_messages:srv/PosesInFrontOfFaces.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_FACES__STRUCT_HPP_
#define CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_FACES__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_messages__srv__PosesInFrontOfFaces_Request __attribute__((deprecated))
#else
# define DEPRECATED__custom_messages__srv__PosesInFrontOfFaces_Request __declspec(deprecated)
#endif

namespace custom_messages
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct PosesInFrontOfFaces_Request_
{
  using Type = PosesInFrontOfFaces_Request_<ContainerAllocator>;

  explicit PosesInFrontOfFaces_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit PosesInFrontOfFaces_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    custom_messages::srv::PosesInFrontOfFaces_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_messages::srv::PosesInFrontOfFaces_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_messages::srv::PosesInFrontOfFaces_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_messages::srv::PosesInFrontOfFaces_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::PosesInFrontOfFaces_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::PosesInFrontOfFaces_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::PosesInFrontOfFaces_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::PosesInFrontOfFaces_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_messages::srv::PosesInFrontOfFaces_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_messages::srv::PosesInFrontOfFaces_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_messages__srv__PosesInFrontOfFaces_Request
    std::shared_ptr<custom_messages::srv::PosesInFrontOfFaces_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_messages__srv__PosesInFrontOfFaces_Request
    std::shared_ptr<custom_messages::srv::PosesInFrontOfFaces_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PosesInFrontOfFaces_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const PosesInFrontOfFaces_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PosesInFrontOfFaces_Request_

// alias to use template instance with default allocator
using PosesInFrontOfFaces_Request =
  custom_messages::srv::PosesInFrontOfFaces_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_messages


// Include directives for member types
// Member 'poses'
#include "geometry_msgs/msg/detail/pose__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__custom_messages__srv__PosesInFrontOfFaces_Response __attribute__((deprecated))
#else
# define DEPRECATED__custom_messages__srv__PosesInFrontOfFaces_Response __declspec(deprecated)
#endif

namespace custom_messages
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct PosesInFrontOfFaces_Response_
{
  using Type = PosesInFrontOfFaces_Response_<ContainerAllocator>;

  explicit PosesInFrontOfFaces_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit PosesInFrontOfFaces_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _poses_type =
    std::vector<geometry_msgs::msg::Pose_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Pose_<ContainerAllocator>>>;
  _poses_type poses;

  // setters for named parameter idiom
  Type & set__poses(
    const std::vector<geometry_msgs::msg::Pose_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Pose_<ContainerAllocator>>> & _arg)
  {
    this->poses = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_messages::srv::PosesInFrontOfFaces_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_messages::srv::PosesInFrontOfFaces_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_messages::srv::PosesInFrontOfFaces_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_messages::srv::PosesInFrontOfFaces_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::PosesInFrontOfFaces_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::PosesInFrontOfFaces_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_messages::srv::PosesInFrontOfFaces_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_messages::srv::PosesInFrontOfFaces_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_messages::srv::PosesInFrontOfFaces_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_messages::srv::PosesInFrontOfFaces_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_messages__srv__PosesInFrontOfFaces_Response
    std::shared_ptr<custom_messages::srv::PosesInFrontOfFaces_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_messages__srv__PosesInFrontOfFaces_Response
    std::shared_ptr<custom_messages::srv::PosesInFrontOfFaces_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PosesInFrontOfFaces_Response_ & other) const
  {
    if (this->poses != other.poses) {
      return false;
    }
    return true;
  }
  bool operator!=(const PosesInFrontOfFaces_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PosesInFrontOfFaces_Response_

// alias to use template instance with default allocator
using PosesInFrontOfFaces_Response =
  custom_messages::srv::PosesInFrontOfFaces_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_messages

namespace custom_messages
{

namespace srv
{

struct PosesInFrontOfFaces
{
  using Request = custom_messages::srv::PosesInFrontOfFaces_Request;
  using Response = custom_messages::srv::PosesInFrontOfFaces_Response;
};

}  // namespace srv

}  // namespace custom_messages

#endif  // CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_FACES__STRUCT_HPP_
