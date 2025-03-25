// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_messages:srv/PosesInFrontOfFaces.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_FACES__STRUCT_H_
#define CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_FACES__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/PosesInFrontOfFaces in the package custom_messages.
typedef struct custom_messages__srv__PosesInFrontOfFaces_Request
{
  uint8_t structure_needs_at_least_one_member;
} custom_messages__srv__PosesInFrontOfFaces_Request;

// Struct for a sequence of custom_messages__srv__PosesInFrontOfFaces_Request.
typedef struct custom_messages__srv__PosesInFrontOfFaces_Request__Sequence
{
  custom_messages__srv__PosesInFrontOfFaces_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_messages__srv__PosesInFrontOfFaces_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'poses'
#include "geometry_msgs/msg/detail/pose__struct.h"

/// Struct defined in srv/PosesInFrontOfFaces in the package custom_messages.
typedef struct custom_messages__srv__PosesInFrontOfFaces_Response
{
  geometry_msgs__msg__Pose__Sequence poses;
} custom_messages__srv__PosesInFrontOfFaces_Response;

// Struct for a sequence of custom_messages__srv__PosesInFrontOfFaces_Response.
typedef struct custom_messages__srv__PosesInFrontOfFaces_Response__Sequence
{
  custom_messages__srv__PosesInFrontOfFaces_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_messages__srv__PosesInFrontOfFaces_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MESSAGES__SRV__DETAIL__POSES_IN_FRONT_OF_FACES__STRUCT_H_
