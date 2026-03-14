// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces_pkg:msg/TargetPoint.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__TARGET_POINT__STRUCT_HPP_
#define INTERFACES_PKG__MSG__DETAIL__TARGET_POINT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__interfaces_pkg__msg__TargetPoint __attribute__((deprecated))
#else
# define DEPRECATED__interfaces_pkg__msg__TargetPoint __declspec(deprecated)
#endif

namespace interfaces_pkg
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TargetPoint_
{
  using Type = TargetPoint_<ContainerAllocator>;

  explicit TargetPoint_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->target_x = 0ll;
      this->target_y = 0ll;
    }
  }

  explicit TargetPoint_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->target_x = 0ll;
      this->target_y = 0ll;
    }
  }

  // field types and members
  using _target_x_type =
    int64_t;
  _target_x_type target_x;
  using _target_y_type =
    int64_t;
  _target_y_type target_y;

  // setters for named parameter idiom
  Type & set__target_x(
    const int64_t & _arg)
  {
    this->target_x = _arg;
    return *this;
  }
  Type & set__target_y(
    const int64_t & _arg)
  {
    this->target_y = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces_pkg::msg::TargetPoint_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces_pkg::msg::TargetPoint_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces_pkg::msg::TargetPoint_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces_pkg::msg::TargetPoint_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::msg::TargetPoint_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::msg::TargetPoint_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::msg::TargetPoint_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::msg::TargetPoint_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces_pkg::msg::TargetPoint_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces_pkg::msg::TargetPoint_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces_pkg__msg__TargetPoint
    std::shared_ptr<interfaces_pkg::msg::TargetPoint_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces_pkg__msg__TargetPoint
    std::shared_ptr<interfaces_pkg::msg::TargetPoint_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TargetPoint_ & other) const
  {
    if (this->target_x != other.target_x) {
      return false;
    }
    if (this->target_y != other.target_y) {
      return false;
    }
    return true;
  }
  bool operator!=(const TargetPoint_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TargetPoint_

// alias to use template instance with default allocator
using TargetPoint =
  interfaces_pkg::msg::TargetPoint_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__MSG__DETAIL__TARGET_POINT__STRUCT_HPP_
