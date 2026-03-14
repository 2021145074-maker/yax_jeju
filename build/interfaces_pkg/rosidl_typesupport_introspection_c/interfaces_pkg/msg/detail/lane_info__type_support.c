// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from interfaces_pkg:msg/LaneInfo.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "interfaces_pkg/msg/detail/lane_info__rosidl_typesupport_introspection_c.h"
#include "interfaces_pkg/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "interfaces_pkg/msg/detail/lane_info__functions.h"
#include "interfaces_pkg/msg/detail/lane_info__struct.h"


// Include directives for member types
// Member `target_points`
#include "interfaces_pkg/msg/target_point.h"
// Member `target_points`
#include "interfaces_pkg/msg/detail/target_point__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  interfaces_pkg__msg__LaneInfo__init(message_memory);
}

void interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_fini_function(void * message_memory)
{
  interfaces_pkg__msg__LaneInfo__fini(message_memory);
}

size_t interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__size_function__LaneInfo__target_points(
  const void * untyped_member)
{
  const interfaces_pkg__msg__TargetPoint__Sequence * member =
    (const interfaces_pkg__msg__TargetPoint__Sequence *)(untyped_member);
  return member->size;
}

const void * interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__get_const_function__LaneInfo__target_points(
  const void * untyped_member, size_t index)
{
  const interfaces_pkg__msg__TargetPoint__Sequence * member =
    (const interfaces_pkg__msg__TargetPoint__Sequence *)(untyped_member);
  return &member->data[index];
}

void * interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__get_function__LaneInfo__target_points(
  void * untyped_member, size_t index)
{
  interfaces_pkg__msg__TargetPoint__Sequence * member =
    (interfaces_pkg__msg__TargetPoint__Sequence *)(untyped_member);
  return &member->data[index];
}

void interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__fetch_function__LaneInfo__target_points(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const interfaces_pkg__msg__TargetPoint * item =
    ((const interfaces_pkg__msg__TargetPoint *)
    interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__get_const_function__LaneInfo__target_points(untyped_member, index));
  interfaces_pkg__msg__TargetPoint * value =
    (interfaces_pkg__msg__TargetPoint *)(untyped_value);
  *value = *item;
}

void interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__assign_function__LaneInfo__target_points(
  void * untyped_member, size_t index, const void * untyped_value)
{
  interfaces_pkg__msg__TargetPoint * item =
    ((interfaces_pkg__msg__TargetPoint *)
    interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__get_function__LaneInfo__target_points(untyped_member, index));
  const interfaces_pkg__msg__TargetPoint * value =
    (const interfaces_pkg__msg__TargetPoint *)(untyped_value);
  *item = *value;
}

bool interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__resize_function__LaneInfo__target_points(
  void * untyped_member, size_t size)
{
  interfaces_pkg__msg__TargetPoint__Sequence * member =
    (interfaces_pkg__msg__TargetPoint__Sequence *)(untyped_member);
  interfaces_pkg__msg__TargetPoint__Sequence__fini(member);
  return interfaces_pkg__msg__TargetPoint__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_member_array[2] = {
  {
    "slope",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(interfaces_pkg__msg__LaneInfo, slope),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "target_points",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(interfaces_pkg__msg__LaneInfo, target_points),  // bytes offset in struct
    NULL,  // default value
    interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__size_function__LaneInfo__target_points,  // size() function pointer
    interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__get_const_function__LaneInfo__target_points,  // get_const(index) function pointer
    interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__get_function__LaneInfo__target_points,  // get(index) function pointer
    interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__fetch_function__LaneInfo__target_points,  // fetch(index, &value) function pointer
    interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__assign_function__LaneInfo__target_points,  // assign(index, value) function pointer
    interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__resize_function__LaneInfo__target_points  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_members = {
  "interfaces_pkg__msg",  // message namespace
  "LaneInfo",  // message name
  2,  // number of fields
  sizeof(interfaces_pkg__msg__LaneInfo),
  interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_member_array,  // message members
  interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_init_function,  // function to initialize message memory (memory has to be allocated)
  interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_type_support_handle = {
  0,
  &interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_interfaces_pkg
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, interfaces_pkg, msg, LaneInfo)() {
  interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, interfaces_pkg, msg, TargetPoint)();
  if (!interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_type_support_handle.typesupport_identifier) {
    interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &interfaces_pkg__msg__LaneInfo__rosidl_typesupport_introspection_c__LaneInfo_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
