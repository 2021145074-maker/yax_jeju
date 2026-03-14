// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces_pkg:msg/LaneInfo.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__LANE_INFO__BUILDER_HPP_
#define INTERFACES_PKG__MSG__DETAIL__LANE_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces_pkg/msg/detail/lane_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces_pkg
{

namespace msg
{

namespace builder
{

class Init_LaneInfo_target_points
{
public:
  explicit Init_LaneInfo_target_points(::interfaces_pkg::msg::LaneInfo & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::msg::LaneInfo target_points(::interfaces_pkg::msg::LaneInfo::_target_points_type arg)
  {
    msg_.target_points = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::msg::LaneInfo msg_;
};

class Init_LaneInfo_slope
{
public:
  Init_LaneInfo_slope()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LaneInfo_target_points slope(::interfaces_pkg::msg::LaneInfo::_slope_type arg)
  {
    msg_.slope = std::move(arg);
    return Init_LaneInfo_target_points(msg_);
  }

private:
  ::interfaces_pkg::msg::LaneInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::msg::LaneInfo>()
{
  return interfaces_pkg::msg::builder::Init_LaneInfo_slope();
}

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__MSG__DETAIL__LANE_INFO__BUILDER_HPP_
