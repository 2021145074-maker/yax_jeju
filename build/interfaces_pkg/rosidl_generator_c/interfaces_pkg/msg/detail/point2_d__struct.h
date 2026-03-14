// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces_pkg:msg/Point2D.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__POINT2_D__STRUCT_H_
#define INTERFACES_PKG__MSG__DETAIL__POINT2_D__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Point2D in the package interfaces_pkg.
/**
  * 2D point in pixel coordinates
 */
typedef struct interfaces_pkg__msg__Point2D
{
  double x;
  double y;
} interfaces_pkg__msg__Point2D;

// Struct for a sequence of interfaces_pkg__msg__Point2D.
typedef struct interfaces_pkg__msg__Point2D__Sequence
{
  interfaces_pkg__msg__Point2D * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__msg__Point2D__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES_PKG__MSG__DETAIL__POINT2_D__STRUCT_H_
