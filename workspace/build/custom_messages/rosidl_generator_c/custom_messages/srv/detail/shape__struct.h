// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_messages:srv/Shape.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MESSAGES__SRV__DETAIL__SHAPE__STRUCT_H_
#define CUSTOM_MESSAGES__SRV__DETAIL__SHAPE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'shape'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/Shape in the package custom_messages.
typedef struct custom_messages__srv__Shape_Request
{
  rosidl_runtime_c__String shape;
  int32_t duration;
} custom_messages__srv__Shape_Request;

// Struct for a sequence of custom_messages__srv__Shape_Request.
typedef struct custom_messages__srv__Shape_Request__Sequence
{
  custom_messages__srv__Shape_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_messages__srv__Shape_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'shape'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/Shape in the package custom_messages.
typedef struct custom_messages__srv__Shape_Response
{
  rosidl_runtime_c__String shape;
} custom_messages__srv__Shape_Response;

// Struct for a sequence of custom_messages__srv__Shape_Response.
typedef struct custom_messages__srv__Shape_Response__Sequence
{
  custom_messages__srv__Shape_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_messages__srv__Shape_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  custom_messages__srv__Shape_Event__request__MAX_SIZE = 1
};
// response
enum
{
  custom_messages__srv__Shape_Event__response__MAX_SIZE = 1
};

/// Struct defined in srv/Shape in the package custom_messages.
typedef struct custom_messages__srv__Shape_Event
{
  service_msgs__msg__ServiceEventInfo info;
  custom_messages__srv__Shape_Request__Sequence request;
  custom_messages__srv__Shape_Response__Sequence response;
} custom_messages__srv__Shape_Event;

// Struct for a sequence of custom_messages__srv__Shape_Event.
typedef struct custom_messages__srv__Shape_Event__Sequence
{
  custom_messages__srv__Shape_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_messages__srv__Shape_Event__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MESSAGES__SRV__DETAIL__SHAPE__STRUCT_H_
