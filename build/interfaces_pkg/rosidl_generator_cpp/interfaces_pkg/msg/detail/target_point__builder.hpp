// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces_pkg:msg/TargetPoint.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__TARGET_POINT__BUILDER_HPP_
#define INTERFACES_PKG__MSG__DETAIL__TARGET_POINT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces_pkg/msg/detail/target_point__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces_pkg
{

namespace msg
{

namespace builder
{

class Init_TargetPoint_target_y
{
public:
  explicit Init_TargetPoint_target_y(::interfaces_pkg::msg::TargetPoint & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::msg::TargetPoint target_y(::interfaces_pkg::msg::TargetPoint::_target_y_type arg)
  {
    msg_.target_y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::msg::TargetPoint msg_;
};

class Init_TargetPoint_target_x
{
public:
  Init_TargetPoint_target_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TargetPoint_target_y target_x(::interfaces_pkg::msg::TargetPoint::_target_x_type arg)
  {
    msg_.target_x = std::move(arg);
    return Init_TargetPoint_target_y(msg_);
  }

private:
  ::interfaces_pkg::msg::TargetPoint msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::msg::TargetPoint>()
{
  return interfaces_pkg::msg::builder::Init_TargetPoint_target_x();
}

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__MSG__DETAIL__TARGET_POINT__BUILDER_HPP_
