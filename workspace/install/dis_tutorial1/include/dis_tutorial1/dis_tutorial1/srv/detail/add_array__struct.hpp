// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dis_tutorial1:srv/AddArray.idl
// generated code does not contain a copyright notice

#ifndef DIS_TUTORIAL1__SRV__DETAIL__ADD_ARRAY__STRUCT_HPP_
#define DIS_TUTORIAL1__SRV__DETAIL__ADD_ARRAY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dis_tutorial1__srv__AddArray_Request __attribute__((deprecated))
#else
# define DEPRECATED__dis_tutorial1__srv__AddArray_Request __declspec(deprecated)
#endif

namespace dis_tutorial1
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct AddArray_Request_
{
  using Type = AddArray_Request_<ContainerAllocator>;

  explicit AddArray_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->description = "";
    }
  }

  explicit AddArray_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : description(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->description = "";
    }
  }

  // field types and members
  using _description_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _description_type description;
  using _numbers_type =
    std::vector<int64_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int64_t>>;
  _numbers_type numbers;

  // setters for named parameter idiom
  Type & set__description(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->description = _arg;
    return *this;
  }
  Type & set__numbers(
    const std::vector<int64_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int64_t>> & _arg)
  {
    this->numbers = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dis_tutorial1::srv::AddArray_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const dis_tutorial1::srv::AddArray_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dis_tutorial1::srv::AddArray_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dis_tutorial1::srv::AddArray_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dis_tutorial1::srv::AddArray_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dis_tutorial1::srv::AddArray_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dis_tutorial1::srv::AddArray_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dis_tutorial1::srv::AddArray_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dis_tutorial1::srv::AddArray_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dis_tutorial1::srv::AddArray_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dis_tutorial1__srv__AddArray_Request
    std::shared_ptr<dis_tutorial1::srv::AddArray_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dis_tutorial1__srv__AddArray_Request
    std::shared_ptr<dis_tutorial1::srv::AddArray_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const AddArray_Request_ & other) const
  {
    if (this->description != other.description) {
      return false;
    }
    if (this->numbers != other.numbers) {
      return false;
    }
    return true;
  }
  bool operator!=(const AddArray_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct AddArray_Request_

// alias to use template instance with default allocator
using AddArray_Request =
  dis_tutorial1::srv::AddArray_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace dis_tutorial1


#ifndef _WIN32
# define DEPRECATED__dis_tutorial1__srv__AddArray_Response __attribute__((deprecated))
#else
# define DEPRECATED__dis_tutorial1__srv__AddArray_Response __declspec(deprecated)
#endif

namespace dis_tutorial1
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct AddArray_Response_
{
  using Type = AddArray_Response_<ContainerAllocator>;

  explicit AddArray_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->type = "";
      this->sum = 0ll;
    }
  }

  explicit AddArray_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : type(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->type = "";
      this->sum = 0ll;
    }
  }

  // field types and members
  using _type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _type_type type;
  using _sum_type =
    int64_t;
  _sum_type sum;

  // setters for named parameter idiom
  Type & set__type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->type = _arg;
    return *this;
  }
  Type & set__sum(
    const int64_t & _arg)
  {
    this->sum = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dis_tutorial1::srv::AddArray_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const dis_tutorial1::srv::AddArray_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dis_tutorial1::srv::AddArray_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dis_tutorial1::srv::AddArray_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dis_tutorial1::srv::AddArray_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dis_tutorial1::srv::AddArray_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dis_tutorial1::srv::AddArray_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dis_tutorial1::srv::AddArray_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dis_tutorial1::srv::AddArray_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dis_tutorial1::srv::AddArray_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dis_tutorial1__srv__AddArray_Response
    std::shared_ptr<dis_tutorial1::srv::AddArray_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dis_tutorial1__srv__AddArray_Response
    std::shared_ptr<dis_tutorial1::srv::AddArray_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const AddArray_Response_ & other) const
  {
    if (this->type != other.type) {
      return false;
    }
    if (this->sum != other.sum) {
      return false;
    }
    return true;
  }
  bool operator!=(const AddArray_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct AddArray_Response_

// alias to use template instance with default allocator
using AddArray_Response =
  dis_tutorial1::srv::AddArray_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace dis_tutorial1

namespace dis_tutorial1
{

namespace srv
{

struct AddArray
{
  using Request = dis_tutorial1::srv::AddArray_Request;
  using Response = dis_tutorial1::srv::AddArray_Response;
};

}  // namespace srv

}  // namespace dis_tutorial1

#endif  // DIS_TUTORIAL1__SRV__DETAIL__ADD_ARRAY__STRUCT_HPP_
