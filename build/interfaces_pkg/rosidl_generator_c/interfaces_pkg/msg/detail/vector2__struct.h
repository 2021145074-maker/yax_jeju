// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces_pkg:msg/Vector2.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__VECTOR2__STRUCT_H_
#define INTERFACES_PKG__MSG__DETAIL__VECTOR2__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Vector2 in the package interfaces_pkg.
/**
  * 2D size in pixel
 */
typedef struct interfaces_pkg__msg__Vector2
{
  double x;
  double y;
} interfaces_pkg__msg__Vector2;

// Struct for a sequence of interfaces_pkg__msg__Vector2.
typedef struct interfaces_pkg__msg__Vector2__Sequence
{
  interfaces_pkg__msg__Vector2 * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__msg__Vector2__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES_PKG__MSG__DETAIL__VECTOR2__STRUCT_H_
