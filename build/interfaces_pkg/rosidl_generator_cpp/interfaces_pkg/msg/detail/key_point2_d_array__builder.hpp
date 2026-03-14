// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces_pkg:msg/KeyPoint2DArray.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__KEY_POINT2_D_ARRAY__BUILDER_HPP_
#define INTERFACES_PKG__MSG__DETAIL__KEY_POINT2_D_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces_pkg/msg/detail/key_point2_d_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces_pkg
{

namespace msg
{

namespace builder
{

class Init_KeyPoint2DArray_data
{
public:
  Init_KeyPoint2DArray_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interfaces_pkg::msg::KeyPoint2DArray data(::interfaces_pkg::msg::KeyPoint2DArray::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::msg::KeyPoint2DArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::msg::KeyPoint2DArray>()
{
  return interfaces_pkg::msg::builder::Init_KeyPoint2DArray_data();
}

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__MSG__DETAIL__KEY_POINT2_D_ARRAY__BUILDER_HPP_
