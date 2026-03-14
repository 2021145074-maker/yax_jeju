// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces_pkg:msg/KeyPoint3DArray.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__KEY_POINT3_D_ARRAY__BUILDER_HPP_
#define INTERFACES_PKG__MSG__DETAIL__KEY_POINT3_D_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces_pkg/msg/detail/key_point3_d_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces_pkg
{

namespace msg
{

namespace builder
{

class Init_KeyPoint3DArray_frame_id
{
public:
  explicit Init_KeyPoint3DArray_frame_id(::interfaces_pkg::msg::KeyPoint3DArray & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::msg::KeyPoint3DArray frame_id(::interfaces_pkg::msg::KeyPoint3DArray::_frame_id_type arg)
  {
    msg_.frame_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::msg::KeyPoint3DArray msg_;
};

class Init_KeyPoint3DArray_data
{
public:
  Init_KeyPoint3DArray_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_KeyPoint3DArray_frame_id data(::interfaces_pkg::msg::KeyPoint3DArray::_data_type arg)
  {
    msg_.data = std::move(arg);
    return Init_KeyPoint3DArray_frame_id(msg_);
  }

private:
  ::interfaces_pkg::msg::KeyPoint3DArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::msg::KeyPoint3DArray>()
{
  return interfaces_pkg::msg::builder::Init_KeyPoint3DArray_data();
}

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__MSG__DETAIL__KEY_POINT3_D_ARRAY__BUILDER_HPP_
