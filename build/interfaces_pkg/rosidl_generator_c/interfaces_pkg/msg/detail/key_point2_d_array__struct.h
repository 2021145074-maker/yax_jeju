// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces_pkg:msg/KeyPoint2DArray.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__KEY_POINT2_D_ARRAY__STRUCT_H_
#define INTERFACES_PKG__MSG__DETAIL__KEY_POINT2_D_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'data'
#include "interfaces_pkg/msg/detail/key_point2_d__struct.h"

/// Struct defined in msg/KeyPoint2DArray in the package interfaces_pkg.
/**
  * represents all the keypoints for human pose estimation
 */
typedef struct interfaces_pkg__msg__KeyPoint2DArray
{
  interfaces_pkg__msg__KeyPoint2D__Sequence data;
} interfaces_pkg__msg__KeyPoint2DArray;

// Struct for a sequence of interfaces_pkg__msg__KeyPoint2DArray.
typedef struct interfaces_pkg__msg__KeyPoint2DArray__Sequence
{
  interfaces_pkg__msg__KeyPoint2DArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__msg__KeyPoint2DArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES_PKG__MSG__DETAIL__KEY_POINT2_D_ARRAY__STRUCT_H_
