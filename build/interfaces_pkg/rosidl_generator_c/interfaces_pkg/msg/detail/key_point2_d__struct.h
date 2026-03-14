// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces_pkg:msg/KeyPoint2D.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__KEY_POINT2_D__STRUCT_H_
#define INTERFACES_PKG__MSG__DETAIL__KEY_POINT2_D__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'point'
#include "interfaces_pkg/msg/detail/point2_d__struct.h"

/// Struct defined in msg/KeyPoint2D in the package interfaces_pkg.
/**
  * one keypoint for human pose estimation
 */
typedef struct interfaces_pkg__msg__KeyPoint2D
{
  /// id of the keypoint
  int32_t id;
  /// 2D point in pixels
  interfaces_pkg__msg__Point2D point;
  /// conf of the keypoint
  double score;
} interfaces_pkg__msg__KeyPoint2D;

// Struct for a sequence of interfaces_pkg__msg__KeyPoint2D.
typedef struct interfaces_pkg__msg__KeyPoint2D__Sequence
{
  interfaces_pkg__msg__KeyPoint2D * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__msg__KeyPoint2D__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES_PKG__MSG__DETAIL__KEY_POINT2_D__STRUCT_H_
