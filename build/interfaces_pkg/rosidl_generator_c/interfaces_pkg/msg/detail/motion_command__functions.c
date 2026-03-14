// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from interfaces_pkg:msg/MotionCommand.idl
// generated code does not contain a copyright notice
#include "interfaces_pkg/msg/detail/motion_command__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
interfaces_pkg__msg__MotionCommand__init(interfaces_pkg__msg__MotionCommand * msg)
{
  if (!msg) {
    return false;
  }
  // steering
  // left_speed
  // right_speed
  return true;
}

void
interfaces_pkg__msg__MotionCommand__fini(interfaces_pkg__msg__MotionCommand * msg)
{
  if (!msg) {
    return;
  }
  // steering
  // left_speed
  // right_speed
}

bool
interfaces_pkg__msg__MotionCommand__are_equal(const interfaces_pkg__msg__MotionCommand * lhs, const interfaces_pkg__msg__MotionCommand * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // steering
  if (lhs->steering != rhs->steering) {
    return false;
  }
  // left_speed
  if (lhs->left_speed != rhs->left_speed) {
    return false;
  }
  // right_speed
  if (lhs->right_speed != rhs->right_speed) {
    return false;
  }
  return true;
}

bool
interfaces_pkg__msg__MotionCommand__copy(
  const interfaces_pkg__msg__MotionCommand * input,
  interfaces_pkg__msg__MotionCommand * output)
{
  if (!input || !output) {
    return false;
  }
  // steering
  output->steering = input->steering;
  // left_speed
  output->left_speed = input->left_speed;
  // right_speed
  output->right_speed = input->right_speed;
  return true;
}

interfaces_pkg__msg__MotionCommand *
interfaces_pkg__msg__MotionCommand__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces_pkg__msg__MotionCommand * msg = (interfaces_pkg__msg__MotionCommand *)allocator.allocate(sizeof(interfaces_pkg__msg__MotionCommand), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(interfaces_pkg__msg__MotionCommand));
  bool success = interfaces_pkg__msg__MotionCommand__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
interfaces_pkg__msg__MotionCommand__destroy(interfaces_pkg__msg__MotionCommand * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    interfaces_pkg__msg__MotionCommand__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
interfaces_pkg__msg__MotionCommand__Sequence__init(interfaces_pkg__msg__MotionCommand__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces_pkg__msg__MotionCommand * data = NULL;

  if (size) {
    data = (interfaces_pkg__msg__MotionCommand *)allocator.zero_allocate(size, sizeof(interfaces_pkg__msg__MotionCommand), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = interfaces_pkg__msg__MotionCommand__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        interfaces_pkg__msg__MotionCommand__fini(&data[i - 1]);
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
interfaces_pkg__msg__MotionCommand__Sequence__fini(interfaces_pkg__msg__MotionCommand__Sequence * array)
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
      interfaces_pkg__msg__MotionCommand__fini(&array->data[i]);
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

interfaces_pkg__msg__MotionCommand__Sequence *
interfaces_pkg__msg__MotionCommand__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  interfaces_pkg__msg__MotionCommand__Sequence * array = (interfaces_pkg__msg__MotionCommand__Sequence *)allocator.allocate(sizeof(interfaces_pkg__msg__MotionCommand__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = interfaces_pkg__msg__MotionCommand__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
interfaces_pkg__msg__MotionCommand__Sequence__destroy(interfaces_pkg__msg__MotionCommand__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    interfaces_pkg__msg__MotionCommand__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
interfaces_pkg__msg__MotionCommand__Sequence__are_equal(const interfaces_pkg__msg__MotionCommand__Sequence * lhs, const interfaces_pkg__msg__MotionCommand__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!interfaces_pkg__msg__MotionCommand__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
interfaces_pkg__msg__MotionCommand__Sequence__copy(
  const interfaces_pkg__msg__MotionCommand__Sequence * input,
  interfaces_pkg__msg__MotionCommand__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(interfaces_pkg__msg__MotionCommand);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    interfaces_pkg__msg__MotionCommand * data =
      (interfaces_pkg__msg__MotionCommand *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!interfaces_pkg__msg__MotionCommand__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          interfaces_pkg__msg__MotionCommand__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!interfaces_pkg__msg__MotionCommand__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
