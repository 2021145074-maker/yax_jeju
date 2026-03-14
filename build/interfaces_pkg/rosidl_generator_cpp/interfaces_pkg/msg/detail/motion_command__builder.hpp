// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces_pkg:msg/MotionCommand.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__MOTION_COMMAND__BUILDER_HPP_
#define INTERFACES_PKG__MSG__DETAIL__MOTION_COMMAND__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces_pkg/msg/detail/motion_command__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces_pkg
{

namespace msg
{

namespace builder
{

class Init_MotionCommand_right_speed
{
public:
  explicit Init_MotionCommand_right_speed(::interfaces_pkg::msg::MotionCommand & msg)
  : msg_(msg)
  {}
  ::interfaces_pkg::msg::MotionCommand right_speed(::interfaces_pkg::msg::MotionCommand::_right_speed_type arg)
  {
    msg_.right_speed = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces_pkg::msg::MotionCommand msg_;
};

class Init_MotionCommand_left_speed
{
public:
  explicit Init_MotionCommand_left_speed(::interfaces_pkg::msg::MotionCommand & msg)
  : msg_(msg)
  {}
  Init_MotionCommand_right_speed left_speed(::interfaces_pkg::msg::MotionCommand::_left_speed_type arg)
  {
    msg_.left_speed = std::move(arg);
    return Init_MotionCommand_right_speed(msg_);
  }

private:
  ::interfaces_pkg::msg::MotionCommand msg_;
};

class Init_MotionCommand_steering
{
public:
  Init_MotionCommand_steering()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotionCommand_left_speed steering(::interfaces_pkg::msg::MotionCommand::_steering_type arg)
  {
    msg_.steering = std::move(arg);
    return Init_MotionCommand_left_speed(msg_);
  }

private:
  ::interfaces_pkg::msg::MotionCommand msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces_pkg::msg::MotionCommand>()
{
  return interfaces_pkg::msg::builder::Init_MotionCommand_steering();
}

}  // namespace interfaces_pkg

#endif  // INTERFACES_PKG__MSG__DETAIL__MOTION_COMMAND__BUILDER_HPP_
