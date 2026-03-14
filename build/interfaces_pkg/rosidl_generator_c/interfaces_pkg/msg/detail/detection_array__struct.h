// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces_pkg:msg/DetectionArray.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES_PKG__MSG__DETAIL__DETECTION_ARRAY__STRUCT_H_
#define INTERFACES_PKG__MSG__DETAIL__DETECTION_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'detections'
#include "interfaces_pkg/msg/detail/detection__struct.h"

/// Struct defined in msg/DetectionArray in the package interfaces_pkg.
/**
  * represents all YOLOv8 detections in one frame
 */
typedef struct interfaces_pkg__msg__DetectionArray
{
  std_msgs__msg__Header header;
  interfaces_pkg__msg__Detection__Sequence detections;
} interfaces_pkg__msg__DetectionArray;

// Struct for a sequence of interfaces_pkg__msg__DetectionArray.
typedef struct interfaces_pkg__msg__DetectionArray__Sequence
{
  interfaces_pkg__msg__DetectionArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces_pkg__msg__DetectionArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES_PKG__MSG__DETAIL__DETECTION_ARRAY__STRUCT_H_
