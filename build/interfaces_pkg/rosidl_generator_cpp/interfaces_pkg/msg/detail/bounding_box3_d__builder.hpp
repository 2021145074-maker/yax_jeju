// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces_pkg:msg/BoundingBox3D.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__BOUNDING_BOX3_D__BUILDER_HPP_
#define INTERFACES_PKG__MSG__DETAIL__BOUNDING_BOX3_D__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces_pkg/msg/detail/bounding_box3_d__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces_pkg
{

namespace msg
{

namespace builder
{

class Init_BoundingBox3D_frame_id
{
public:
  explicit Init_BoundingBox3D_frame_id(::interfaces_pkg::msg::BoundingBox3D & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::msg::BoundingBox3D frame_id(::interfaces_pkg::msg::BoundingBox3D::_frame_id_type arg)
  {
    msg_.frame_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::msg::BoundingBox3D msg_;
};

class Init_BoundingBox3D_size
{
public:
  explicit Init_BoundingBox3D_size(::interfaces_pkg::msg::BoundingBox3D & msg)
  : msg_(msg)
  {}
  Init_BoundingBox3D_frame_id size(::interfaces_pkg::msg::BoundingBox3D::_size_type arg)
  {
    msg_.size = std::move(arg);
    return Init_BoundingBox3D_frame_id(msg_);
  }

private:
  ::interfaces_pkg::msg::BoundingBox3D msg_;
};

class Init_BoundingBox3D_center
{
public:
  Init_BoundingBox3D_center()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_BoundingBox3D_size center(::interfaces_pkg::msg::BoundingBox3D::_center_type arg)
  {
    msg_.center = std::move(arg);
    return Init_BoundingBox3D_size(msg_);
  }

private:
  ::interfaces_pkg::msg::BoundingBox3D msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::msg::BoundingBox3D>()
{
  return interfaces_pkg::msg::builder::Init_BoundingBox3D_center();
}

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__MSG__DETAIL__BOUNDING_BOX3_D__BUILDER_HPP_
