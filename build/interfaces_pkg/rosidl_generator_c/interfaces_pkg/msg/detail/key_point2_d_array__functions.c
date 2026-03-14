// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from interfaces_pkg:msg/KeyPoint2DArray.idl
// generated code does not contain a copyright notice
#include "interfaces_pkg/msg/detail/key_point2_d_array__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `data`
#include "interfaces_pkg/msg/detail/key_point2_d__functions.h"

bool
interfaces_pkg__msg__KeyPoint2DArray__init(interfaces_pkg__msg__KeyPoint2DArray * msg)
{
  if (!msg) {
    return false;
  }
  // data
  if (!interfaces_pkg__msg__KeyPoint2D__Sequence__init(&msg->data, 0)) {
    interfaces_pkg__msg__KeyPoint2DArray__fini(msg);
    return false;
  }
  return true;
}

void
interfaces_pkg__msg__KeyPoint2DArray__fini(interfaces_pkg__msg__KeyPoint2DArray * msg)
{
  if (!msg) {
    return;
  }
  // data
  interfaces_pkg__msg__KeyPoint2D__Sequence__fini(&msg->data);
}

bool
interfaces_pkg__msg__KeyPoint2DArray__are_equal(const interfaces_pkg__msg__KeyPoint2DArray * lhs, const interfaces_pkg__msg__KeyPoint2DArray * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // data
  if (!interfaces_pkg__msg__KeyPoint2D__Sequence__are_equal(
      &(lhs->data), &(rhs->data)))
  {
    return false;
  }
  return true;
}

bool
interfaces_pkg__msg__KeyPoint2DArray__copy(
  const interfaces_pkg__msg__KeyPoint2DArray * input,
  interfaces_pkg__msg__KeyPoint2DArray * output)
{
  if (!input || !output) {
    return false;
  }
  // data
  if (!interfaces_pkg__msg__KeyPoint2D__Sequence__copy(
      &(input->data), &(output->data)))
  {
    return false;
  }
  return true;
}

interfaces_pkg__msg__KeyPoint2DArray *
interfaces_pkg__msg__KeyPoint2DArray__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces_pkg__msg__KeyPoint2DArray * msg = (interfaces_pkg__msg__KeyPoint2DArray *)allocator.allocate(sizeof(interfaces_pkg__msg__KeyPoint2DArray), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(interfaces_pkg__msg__KeyPoint2DArray));
  bool success = interfaces_pkg__msg__KeyPoint2DArray__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
interfaces_pkg__msg__KeyPoint2DArray__destroy(interfaces_pkg__msg__KeyPoint2DArray * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    interfaces_pkg__msg__KeyPoint2DArray__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
interfaces_pkg__msg__KeyPoint2DArray__Sequence__init(interfaces_pkg__msg__KeyPoint2DArray__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces_pkg__msg__KeyPoint2DArray * data = NULL;

  if (size) {
    data = (interfaces_pkg__msg__KeyPoint2DArray *)allocator.zero_allocate(size, sizeof(interfaces_pkg__msg__KeyPoint2DArray), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = interfaces_pkg__msg__KeyPoint2DArray__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        interfaces_pkg__msg__KeyPoint2DArray__fini(&data[i - 1]);
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
interfaces_pkg__msg__KeyPoint2DArray__Sequence__fini(interfaces_pkg__msg__KeyPoint2DArray__Sequence * array)
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
      interfaces_pkg__msg__KeyPoint2DArray__fini(&array->data[i]);
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

interfaces_pkg__msg__KeyPoint2DArray__Sequence *
interfaces_pkg__msg__KeyPoint2DArray__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces_pkg__msg__KeyPoint2DArray__Sequence * array = (interfaces_pkg__msg__KeyPoint2DArray__Sequence *)allocator.allocate(sizeof(interfaces_pkg__msg__KeyPoint2DArray__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = interfaces_pkg__msg__KeyPoint2DArray__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
interfaces_pkg__msg__KeyPoint2DArray__Sequence__destroy(interfaces_pkg__msg__KeyPoint2DArray__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    interfaces_pkg__msg__KeyPoint2DArray__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
interfaces_pkg__msg__KeyPoint2DArray__Sequence__are_equal(const interfaces_pkg__msg__KeyPoint2DArray__Sequence * lhs, const interfaces_pkg__msg__KeyPoint2DArray__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!interfaces_pkg__msg__KeyPoint2DArray__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
interfaces_pkg__msg__KeyPoint2DArray__Sequence__copy(
  const interfaces_pkg__msg__KeyPoint2DArray__Sequence * input,
  interfaces_pkg__msg__KeyPoint2DArray__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(interfaces_pkg__msg__KeyPoint2DArray);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    interfaces_pkg__msg__KeyPoint2DArray * data =
      (interfaces_pkg__msg__KeyPoint2DArray *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!interfaces_pkg__msg__KeyPoint2DArray__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          interfaces_pkg__msg__KeyPoint2DArray__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!interfaces_pkg__msg__KeyPoint2DArray__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
