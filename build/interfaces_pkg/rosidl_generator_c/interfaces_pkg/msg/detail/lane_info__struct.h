// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces_pkg:msg/LaneInfo.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__LANE_INFO__STRUCT_H_
#define INTERFACES_PKG__MSG__DETAIL__LANE_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'target_points'
#include "interfaces_pkg/msg/detail/target_point__struct.h"

/// Struct defined in msg/LaneInfo in the package interfaces_pkg.
typedef struct interfaces_pkg__msg__LaneInfo
{
  float slope;
  interfaces_pkg__msg__TargetPoint__Sequence target_points;
} interfaces_pkg__msg__LaneInfo;

// Struct for a sequence of interfaces_pkg__msg__LaneInfo.
typedef struct interfaces_pkg__msg__LaneInfo__Sequence
{
  interfaces_pkg__msg__LaneInfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__msg__LaneInfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES_PKG__MSG__DETAIL__LANE_INFO__STRUCT_H_
