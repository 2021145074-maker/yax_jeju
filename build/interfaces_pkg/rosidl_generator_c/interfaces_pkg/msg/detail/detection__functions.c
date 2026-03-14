// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from interfaces_pkg:msg/Detection.idl
// generated code does not contain a copyright notice
#include "interfaces_pkg/msg/detail/detection__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `class_name`
// Member `id`
#include "rosidl_runtime_c/string_functions.h"
// Member `bbox`
#include "interfaces_pkg/msg/detail/bounding_box2_d__functions.h"
// Member `bbox3d`
#include "interfaces_pkg/msg/detail/bounding_box3_d__functions.h"
// Member `mask`
#include "interfaces_pkg/msg/detail/mask__functions.h"
// Member `keypoints`
#include "interfaces_pkg/msg/detail/key_point2_d_array__functions.h"
// Member `keypoints3d`
#include "interfaces_pkg/msg/detail/key_point3_d_array__functions.h"

bool
interfaces_pkg__msg__Detection__init(interfaces_pkg__msg__Detection * msg)
{
  if (!msg) {
    return false;
  }
  // class_id
  // class_name
  if (!rosidl_runtime_c__String__init(&msg->class_name)) {
    interfaces_pkg__msg__Detection__fini(msg);
    return false;
  }
  // score
  // id
  if (!rosidl_runtime_c__String__init(&msg->id)) {
    interfaces_pkg__msg__Detection__fini(msg);
    return false;
  }
  // bbox
  if (!interfaces_pkg__msg__BoundingBox2D__init(&msg->bbox)) {
    interfaces_pkg__msg__Detection__fini(msg);
    return false;
  }
  // bbox3d
  if (!interfaces_pkg__msg__BoundingBox3D__init(&msg->bbox3d)) {
    interfaces_pkg__msg__Detection__fini(msg);
    return false;
  }
  // mask
  if (!interfaces_pkg__msg__Mask__init(&msg->mask)) {
    interfaces_pkg__msg__Detection__fini(msg);
    return false;
  }
  // keypoints
  if (!interfaces_pkg__msg__KeyPoint2DArray__init(&msg->keypoints)) {
    interfaces_pkg__msg__Detection__fini(msg);
    return false;
  }
  // keypoints3d
  if (!interfaces_pkg__msg__KeyPoint3DArray__init(&msg->keypoints3d)) {
    interfaces_pkg__msg__Detection__fini(msg);
    return false;
  }
  return true;
}

void
interfaces_pkg__msg__Detection__fini(interfaces_pkg__msg__Detection * msg)
{
  if (!msg) {
    return;
  }
  // class_id
  // class_name
  rosidl_runtime_c__String__fini(&msg->class_name);
  // score
  // id
  rosidl_runtime_c__String__fini(&msg->id);
  // bbox
  interfaces_pkg__msg__BoundingBox2D__fini(&msg->bbox);
  // bbox3d
  interfaces_pkg__msg__BoundingBox3D__fini(&msg->bbox3d);
  // mask
  interfaces_pkg__msg__Mask__fini(&msg->mask);
  // keypoints
  interfaces_pkg__msg__KeyPoint2DArray__fini(&msg->keypoints);
  // keypoints3d
  interfaces_pkg__msg__KeyPoint3DArray__fini(&msg->keypoints3d);
}

bool
interfaces_pkg__msg__Detection__are_equal(const interfaces_pkg__msg__Detection * lhs, const interfaces_pkg__msg__Detection * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // class_id
  if (lhs->class_id != rhs->class_id) {
    return false;
  }
  // class_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->class_name), &(rhs->class_name)))
  {
    return false;
  }
  // score
  if (lhs->score != rhs->score) {
    return false;
  }
  // id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->id), &(rhs->id)))
  {
    return false;
  }
  // bbox
  if (!interfaces_pkg__msg__BoundingBox2D__are_equal(
      &(lhs->bbox), &(rhs->bbox)))
  {
    return false;
  }
  // bbox3d
  if (!interfaces_pkg__msg__BoundingBox3D__are_equal(
      &(lhs->bbox3d), &(rhs->bbox3d)))
  {
    return false;
  }
  // mask
  if (!interfaces_pkg__msg__Mask__are_equal(
      &(lhs->mask), &(rhs->mask)))
  {
    return false;
  }
  // keypoints
  if (!interfaces_pkg__msg__KeyPoint2DArray__are_equal(
      &(lhs->keypoints), &(rhs->keypoints)))
  {
    return false;
  }
  // keypoints3d
  if (!interfaces_pkg__msg__KeyPoint3DArray__are_equal(
      &(lhs->keypoints3d), &(rhs->keypoints3d)))
  {
    return false;
  }
  return true;
}

bool
interfaces_pkg__msg__Detection__copy(
  const interfaces_pkg__msg__Detection * input,
  interfaces_pkg__msg__Detection * output)
{
  if (!input || !output) {
    return false;
  }
  // class_id
  output->class_id = input->class_id;
  // class_name
  if (!rosidl_runtime_c__String__copy(
      &(input->class_name), &(output->class_name)))
  {
    return false;
  }
  // score
  output->score = input->score;
  // id
  if (!rosidl_runtime_c__String__copy(
      &(input->id), &(output->id)))
  {
    return false;
  }
  // bbox
  if (!interfaces_pkg__msg__BoundingBox2D__copy(
      &(input->bbox), &(output->bbox)))
  {
    return false;
  }
  // bbox3d
  if (!interfaces_pkg__msg__BoundingBox3D__copy(
      &(input->bbox3d), &(output->bbox3d)))
  {
    return false;
  }
  // mask
  if (!interfaces_pkg__msg__Mask__copy(
      &(input->mask), &(output->mask)))
  {
    return false;
  }
  // keypoints
  if (!interfaces_pkg__msg__KeyPoint2DArray__copy(
      &(input->keypoints), &(output->keypoints)))
  {
    return false;
  }
  // keypoints3d
  if (!interfaces_pkg__msg__KeyPoint3DArray__copy(
      &(input->keypoints3d), &(output->keypoints3d)))
  {
    return false;
  }
  return true;
}

interfaces_pkg__msg__Detection *
interfaces_pkg__msg__Detection__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces_pkg__msg__Detection * msg = (interfaces_pkg__msg__Detection *)allocator.allocate(sizeof(interfaces_pkg__msg__Detection), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(interfaces_pkg__msg__Detection));
  bool success = interfaces_pkg__msg__Detection__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
interfaces_pkg__msg__Detection__destroy(interfaces_pkg__msg__Detection * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    interfaces_pkg__msg__Detection__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
interfaces_pkg__msg__Detection__Sequence__init(interfaces_pkg__msg__Detection__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces_pkg__msg__Detection * data = NULL;

  if (size) {
    data = (interfaces_pkg__msg__Detection *)allocator.zero_allocate(size, sizeof(interfaces_pkg__msg__Detection), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = interfaces_pkg__msg__Detection__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        interfaces_pkg__msg__Detection__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
interfaces_pkg__msg__Detection__Sequence__fini(interfaces_pkg__msg__Detection__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      interfaces_pkg__msg__Detection__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

interfaces_pkg__msg__Detection__Sequence *
interfaces_pkg__msg__Detection__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces_pkg__msg__Detection__Sequence * array = (interfaces_pkg__msg__Detection__Sequence *)allocator.allocate(sizeof(interfaces_pkg__msg__Detection__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = interfaces_pkg__msg__Detection__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
interfaces_pkg__msg__Detection__Sequence__destroy(interfaces_pkg__msg__Detection__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    interfaces_pkg__msg__Detection__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
interfaces_pkg__msg__Detection__Sequence__are_equal(const interfaces_pkg__msg__Detection__Sequence * lhs, const interfaces_pkg__msg__Detection__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!interfaces_pkg__msg__Detection__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
interfaces_pkg__msg__Detection__Sequence__copy(
  const interfaces_pkg__msg__Detection__Sequence * input,
  interfaces_pkg__msg__Detection__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(interfaces_pkg__msg__Detection);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    interfaces_pkg__msg__Detection * data =
      (interfaces_pkg__msg__Detection *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!interfaces_pkg__msg__Detection__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          interfaces_pkg__msg__Detection__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!interfaces_pkg__msg__Detection__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
