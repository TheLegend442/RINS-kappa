// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_messages:msg/RingCoordinates.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__MSG__DETAIL__RING_COORDINATES__STRUCT_H_
#define CUSTOM_MESSAGES__MSG__DETAIL__RING_COORDINATES__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'center'
#include "visualization_msgs/msg/detail/marker__struct.h"
// Member 'color'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/RingCoordinates in the package custom_messages.
typedef struct custom_messages__msg__RingCoordinates
{
  visualization_msgs__msg__Marker center;
  rosidl_runtime_c__String color;
  double strength;
} custom_messages__msg__RingCoordinates;

// Struct for a sequence of custom_messages__msg__RingCoordinates.
typedef struct custom_messages__msg__RingCoordinates__Sequence
{
  custom_messages__msg__RingCoordinates * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_messages__msg__RingCoordinates__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MESSAGES__MSG__DETAIL__RING_COORDINATES__STRUCT_H_
