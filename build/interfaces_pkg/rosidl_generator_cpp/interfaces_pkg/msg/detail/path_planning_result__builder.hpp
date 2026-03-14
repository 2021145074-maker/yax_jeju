// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces_pkg:msg/PathPlanningResult.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__PATH_PLANNING_RESULT__BUILDER_HPP_
#define INTERFACES_PKG__MSG__DETAIL__PATH_PLANNING_RESULT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces_pkg/msg/detail/path_planning_result__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces_pkg
{

namespace msg
{

namespace builder
{

class Init_PathPlanningResult_y_points
{
public:
  explicit Init_PathPlanningResult_y_points(::interfaces_pkg::msg::PathPlanningResult & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::msg::PathPlanningResult y_points(::interfaces_pkg::msg::PathPlanningResult::_y_points_type arg)
  {
    msg_.y_points = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::msg::PathPlanningResult msg_;
};

class Init_PathPlanningResult_x_points
{
public:
  Init_PathPlanningResult_x_points()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PathPlanningResult_y_points x_points(::interfaces_pkg::msg::PathPlanningResult::_x_points_type arg)
  {
    msg_.x_points = std::move(arg);
    return Init_PathPlanningResult_y_points(msg_);
  }

private:
  ::interfaces_pkg::msg::PathPlanningResult msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::msg::PathPlanningResult>()
{
  return interfaces_pkg::msg::builder::Init_PathPlanningResult_x_points();
}

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__MSG__DETAIL__PATH_PLANNING_RESULT__BUILDER_HPP_
