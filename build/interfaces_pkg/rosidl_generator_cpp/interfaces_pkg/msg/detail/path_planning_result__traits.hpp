// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interfaces_pkg:msg/PathPlanningResult.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__PATH_PLANNING_RESULT__TRAITS_HPP_
#define INTERFACES_PKG__MSG__DETAIL__PATH_PLANNING_RESULT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "interfaces_pkg/msg/detail/path_planning_result__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace interfaces_pkg
{

namespace msg
{

inline void to_flow_style_yaml(
  const PathPlanningResult & msg,
  std::ostream & out)
{
  out << "{";
  // member: x_points
  {
    if (msg.x_points.size() == 0) {
      out << "x_points: []";
    } else {
      out << "x_points: [";
      size_t pending_items = msg.x_points.size();
      for (auto item : msg.x_points) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: y_points
  {
    if (msg.y_points.size() == 0) {
      out << "y_points: []";
    } else {
      out << "y_points: [";
      size_t pending_items = msg.y_points.size();
      for (auto item : msg.y_points) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PathPlanningResult & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x_points
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.x_points.size() == 0) {
      out << "x_points: []\n";
    } else {
      out << "x_points:\n";
      for (auto item : msg.x_points) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: y_points
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.y_points.size() == 0) {
      out << "y_points: []\n";
    } else {
      out << "y_points:\n";
      for (auto item : msg.y_points) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PathPlanningResult & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace interfaces_pkg

namespace rosidl_generator_traits
{

[[deprecated("use interfaces_pkg::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interfaces_pkg::msg::PathPlanningResult & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces_pkg::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces_pkg::msg::to_yaml() instead")]]
inline std::string to_yaml(const interfaces_pkg::msg::PathPlanningResult & msg)
{
  return interfaces_pkg::msg::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces_pkg::msg::PathPlanningResult>()
{
  return "interfaces_pkg::msg::PathPlanningResult";
}

template<>
inline const char * name<interfaces_pkg::msg::PathPlanningResult>()
{
  return "interfaces_pkg/msg/PathPlanningResult";
}

template<>
struct has_fixed_size<interfaces_pkg::msg::PathPlanningResult>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<interfaces_pkg::msg::PathPlanningResult>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<interfaces_pkg::msg::PathPlanningResult>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // INTERFACES_PKG__MSG__DETAIL__PATH_PLANNING_RESULT__TRAITS_HPP_
