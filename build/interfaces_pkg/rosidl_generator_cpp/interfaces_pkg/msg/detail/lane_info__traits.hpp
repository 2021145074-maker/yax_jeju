// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interfaces_pkg:msg/LaneInfo.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__LANE_INFO__TRAITS_HPP_
#define INTERFACES_PKG__MSG__DETAIL__LANE_INFO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "interfaces_pkg/msg/detail/lane_info__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'target_points'
#include "interfaces_pkg/msg/detail/target_point__traits.hpp"

namespace interfaces_pkg
{

namespace msg
{

inline void to_flow_style_yaml(
  const LaneInfo & msg,
  std::ostream & out)
{
  out << "{";
  // member: slope
  {
    out << "slope: ";
    rosidl_generator_traits::value_to_yaml(msg.slope, out);
    out << ", ";
  }

  // member: target_points
  {
    if (msg.target_points.size() == 0) {
      out << "target_points: []";
    } else {
      out << "target_points: [";
      size_t pending_items = msg.target_points.size();
      for (auto item : msg.target_points) {
        to_flow_style_yaml(item, out);
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
  const LaneInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: slope
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "slope: ";
    rosidl_generator_traits::value_to_yaml(msg.slope, out);
    out << "\n";
  }

  // member: target_points
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.target_points.size() == 0) {
      out << "target_points: []\n";
    } else {
      out << "target_points:\n";
      for (auto item : msg.target_points) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LaneInfo & msg, bool use_flow_style = false)
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
  const interfaces_pkg::msg::LaneInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  interfaces_pkg::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interfaces_pkg::msg::to_yaml() instead")]]
inline std::string to_yaml(const interfaces_pkg::msg::LaneInfo & msg)
{
  return interfaces_pkg::msg::to_yaml(msg);
}

template<>
inline const char * data_type<interfaces_pkg::msg::LaneInfo>()
{
  return "interfaces_pkg::msg::LaneInfo";
}

template<>
inline const char * name<interfaces_pkg::msg::LaneInfo>()
{
  return "interfaces_pkg/msg/LaneInfo";
}

template<>
struct has_fixed_size<interfaces_pkg::msg::LaneInfo>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<interfaces_pkg::msg::LaneInfo>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<interfaces_pkg::msg::LaneInfo>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // INTERFACES_PKG__MSG__DETAIL__LANE_INFO__TRAITS_HPP_
