// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_messages:msg/FaceCoordinates.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__MSG__DETAIL__FACE_COORDINATES__STRUCT_H_
#define CUSTOM_MESSAGES__MSG__DETAIL__FACE_COORDINATES__STRUCT_H_

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
// Member 'bottom_right'
// Member 'upper_left'
#include "visualization_msgs/msg/detail/marker__struct.h"

/// Struct defined in msg/FaceCoordinates in the package custom_messages.
typedef struct custom_messages__msg__FaceCoordinates
{
  visualization_msgs__msg__Marker center;
  visualization_msgs__msg__Marker bottom_right;
  visualization_msgs__msg__Marker upper_left;
} custom_messages__msg__FaceCoordinates;

// Struct for a sequence of custom_messages__msg__FaceCoordinates.
typedef struct custom_messages__msg__FaceCoordinates__Sequence
{
  custom_messages__msg__FaceCoordinates * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_messages__msg__FaceCoordinates__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MESSAGES__MSG__DETAIL__FACE_COORDINATES__STRUCT_H_
