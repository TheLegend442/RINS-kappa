// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dis_tutorial1:srv/AddArray.idl
// generated code does not contain a copyright notice

#ifndef DIS_TUTORIAL1__SRV__DETAIL__ADD_ARRAY__STRUCT_H_
#define DIS_TUTORIAL1__SRV__DETAIL__ADD_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'description'
#include "rosidl_runtime_c/string.h"
// Member 'numbers'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in srv/AddArray in the package dis_tutorial1.
typedef struct dis_tutorial1__srv__AddArray_Request
{
  rosidl_runtime_c__String description;
  rosidl_runtime_c__int64__Sequence numbers;
} dis_tutorial1__srv__AddArray_Request;

// Struct for a sequence of dis_tutorial1__srv__AddArray_Request.
typedef struct dis_tutorial1__srv__AddArray_Request__Sequence
{
  dis_tutorial1__srv__AddArray_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dis_tutorial1__srv__AddArray_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'type'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/AddArray in the package dis_tutorial1.
typedef struct dis_tutorial1__srv__AddArray_Response
{
  rosidl_runtime_c__String type;
  int64_t sum;
} dis_tutorial1__srv__AddArray_Response;

// Struct for a sequence of dis_tutorial1__srv__AddArray_Response.
typedef struct dis_tutorial1__srv__AddArray_Response__Sequence
{
  dis_tutorial1__srv__AddArray_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dis_tutorial1__srv__AddArray_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DIS_TUTORIAL1__SRV__DETAIL__ADD_ARRAY__STRUCT_H_
