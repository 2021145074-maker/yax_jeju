// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces_pkg:msg/KeyPoint3D.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__KEY_POINT3_D__STRUCT_H_
#define INTERFACES_PKG__MSG__DETAIL__KEY_POINT3_D__STRUCT_H_

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
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in msg/KeyPoint3D in the package interfaces_pkg.
/**
  * one keypoint for human pose estimation
 */
typedef struct interfaces_pkg__msg__KeyPoint3D
{
  /// id of the keypoint
  int32_t id;
  /// 3D point in meters
  geometry_msgs__msg__Point point;
  /// conf of the keypoint
  double score;
} interfaces_pkg__msg__KeyPoint3D;

// Struct for a sequence of interfaces_pkg__msg__KeyPoint3D.
typedef struct interfaces_pkg__msg__KeyPoint3D__Sequence
{
  interfaces_pkg__msg__KeyPoint3D * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__msg__KeyPoint3D__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES_PKG__MSG__DETAIL__KEY_POINT3_D__STRUCT_H_
