// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces_pkg:msg/Mask.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__MASK__BUILDER_HPP_
#define INTERFACES_PKG__MSG__DETAIL__MASK__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces_pkg/msg/detail/mask__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces_pkg
{

namespace msg
{

namespace builder
{

class Init_Mask_data
{
public:
  explicit Init_Mask_data(::interfaces_pkg::msg::Mask & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::msg::Mask data(::interfaces_pkg::msg::Mask::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::msg::Mask msg_;
};

class Init_Mask_width
{
public:
  explicit Init_Mask_width(::interfaces_pkg::msg::Mask & msg)
  : msg_(msg)
  {}
  Init_Mask_data width(::interfaces_pkg::msg::Mask::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_Mask_data(msg_);
  }

private:
  ::interfaces_pkg::msg::Mask msg_;
};

class Init_Mask_height
{
public:
  Init_Mask_height()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Mask_width height(::interfaces_pkg::msg::Mask::_height_type arg)
  {
    msg_.height = std::move(arg);
    return Init_Mask_width(msg_);
  }

private:
  ::interfaces_pkg::msg::Mask msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::msg::Mask>()
{
  return interfaces_pkg::msg::builder::Init_Mask_height();
}

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__MSG__DETAIL__MASK__BUILDER_HPP_
