// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces_pkg:msg/PathPlanningResult.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__PATH_PLANNING_RESULT__STRUCT_HPP_
#define INTERFACES_PKG__MSG__DETAIL__PATH_PLANNING_RESULT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__interfaces_pkg__msg__PathPlanningResult __attribute__((deprecated))
#else
# define DEPRECATED__interfaces_pkg__msg__PathPlanningResult __declspec(deprecated)
#endif

namespace interfaces_pkg
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PathPlanningResult_
{
  using Type = PathPlanningResult_<ContainerAllocator>;

  explicit PathPlanningResult_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit PathPlanningResult_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _x_points_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _x_points_type x_points;
  using _y_points_type =
    std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>>;
  _y_points_type y_points;

  // setters for named parameter idiom
  Type & set__x_points(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->x_points = _arg;
    return *this;
  }
  Type & set__y_points(
    const std::vector<double, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<double>> & _arg)
  {
    this->y_points = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces_pkg::msg::PathPlanningResult_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces_pkg::msg::PathPlanningResult_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces_pkg::msg::PathPlanningResult_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces_pkg::msg::PathPlanningResult_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::msg::PathPlanningResult_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::msg::PathPlanningResult_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces_pkg::msg::PathPlanningResult_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces_pkg::msg::PathPlanningResult_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces_pkg::msg::PathPlanningResult_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces_pkg::msg::PathPlanningResult_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces_pkg__msg__PathPlanningResult
    std::shared_ptr<interfaces_pkg::msg::PathPlanningResult_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces_pkg__msg__PathPlanningResult
    std::shared_ptr<interfaces_pkg::msg::PathPlanningResult_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PathPlanningResult_ & other) const
  {
    if (this->x_points != other.x_points) {
      return false;
    }
    if (this->y_points != other.y_points) {
      return false;
    }
    return true;
  }
  bool operator!=(const PathPlanningResult_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PathPlanningResult_

// alias to use template instance with default allocator
using PathPlanningResult =
  interfaces_pkg::msg::PathPlanningResult_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__MSG__DETAIL__PATH_PLANNING_RESULT__STRUCT_HPP_
