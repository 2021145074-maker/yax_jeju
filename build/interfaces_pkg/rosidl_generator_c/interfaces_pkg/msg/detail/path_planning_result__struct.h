// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces_pkg:msg/PathPlanningResult.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__PATH_PLANNING_RESULT__STRUCT_H_
#define INTERFACES_PKG__MSG__DETAIL__PATH_PLANNING_RESULT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'x_points'
// Member 'y_points'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/PathPlanningResult in the package interfaces_pkg.
/**
  * PathPlanningResult.msg
 */
typedef struct interfaces_pkg__msg__PathPlanningResult
{
  /// 경로의 각 점들의 x 좌표
  rosidl_runtime_c__double__Sequence x_points;
  /// 경로의 각 점들의 y 좌표
  rosidl_runtime_c__double__Sequence y_points;
} interfaces_pkg__msg__PathPlanningResult;

// Struct for a sequence of interfaces_pkg__msg__PathPlanningResult.
typedef struct interfaces_pkg__msg__PathPlanningResult__Sequence
{
  interfaces_pkg__msg__PathPlanningResult * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__msg__PathPlanningResult__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES_PKG__MSG__DETAIL__PATH_PLANNING_RESULT__STRUCT_H_
