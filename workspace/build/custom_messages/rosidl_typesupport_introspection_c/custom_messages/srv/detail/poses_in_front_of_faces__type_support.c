// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from custom_messages:srv/PosesInFrontOfFaces.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "custom_messages/srv/detail/poses_in_front_of_faces__rosidl_typesupport_introspection_c.h"
#include "custom_messages/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "custom_messages/srv/detail/poses_in_front_of_faces__functions.h"
#include "custom_messages/srv/detail/poses_in_front_of_faces__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void custom_messages__srv__PosesInFrontOfFaces_Request__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  custom_messages__srv__PosesInFrontOfFaces_Request__init(message_memory);
}

void custom_messages__srv__PosesInFrontOfFaces_Request__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_fini_function(void * message_memory)
{
  custom_messages__srv__PosesInFrontOfFaces_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember custom_messages__srv__PosesInFrontOfFaces_Request__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_message_member_array[1] = {
  {
    "structure_needs_at_least_one_member",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_messages__srv__PosesInFrontOfFaces_Request, structure_needs_at_least_one_member),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers custom_messages__srv__PosesInFrontOfFaces_Request__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_message_members = {
  "custom_messages__srv",  // message namespace
  "PosesInFrontOfFaces_Request",  // message name
  1,  // number of fields
  sizeof(custom_messages__srv__PosesInFrontOfFaces_Request),
  custom_messages__srv__PosesInFrontOfFaces_Request__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_message_member_array,  // message members
  custom_messages__srv__PosesInFrontOfFaces_Request__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  custom_messages__srv__PosesInFrontOfFaces_Request__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t custom_messages__srv__PosesInFrontOfFaces_Request__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_message_type_support_handle = {
  0,
  &custom_messages__srv__PosesInFrontOfFaces_Request__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_custom_messages
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_messages, srv, PosesInFrontOfFaces_Request)() {
  if (!custom_messages__srv__PosesInFrontOfFaces_Request__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_message_type_support_handle.typesupport_identifier) {
    custom_messages__srv__PosesInFrontOfFaces_Request__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &custom_messages__srv__PosesInFrontOfFaces_Request__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "custom_messages/srv/detail/poses_in_front_of_faces__rosidl_typesupport_introspection_c.h"
// already included above
// #include "custom_messages/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "custom_messages/srv/detail/poses_in_front_of_faces__functions.h"
// already included above
// #include "custom_messages/srv/detail/poses_in_front_of_faces__struct.h"


// Include directives for member types
// Member `poses`
#include "geometry_msgs/msg/pose.h"
// Member `poses`
#include "geometry_msgs/msg/detail/pose__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  custom_messages__srv__PosesInFrontOfFaces_Response__init(message_memory);
}

void custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_fini_function(void * message_memory)
{
  custom_messages__srv__PosesInFrontOfFaces_Response__fini(message_memory);
}

size_t custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__size_function__PosesInFrontOfFaces_Response__poses(
  const void * untyped_member)
{
  const geometry_msgs__msg__Pose__Sequence * member =
    (const geometry_msgs__msg__Pose__Sequence *)(untyped_member);
  return member->size;
}

const void * custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__get_const_function__PosesInFrontOfFaces_Response__poses(
  const void * untyped_member, size_t index)
{
  const geometry_msgs__msg__Pose__Sequence * member =
    (const geometry_msgs__msg__Pose__Sequence *)(untyped_member);
  return &member->data[index];
}

void * custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__get_function__PosesInFrontOfFaces_Response__poses(
  void * untyped_member, size_t index)
{
  geometry_msgs__msg__Pose__Sequence * member =
    (geometry_msgs__msg__Pose__Sequence *)(untyped_member);
  return &member->data[index];
}

void custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__fetch_function__PosesInFrontOfFaces_Response__poses(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const geometry_msgs__msg__Pose * item =
    ((const geometry_msgs__msg__Pose *)
    custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__get_const_function__PosesInFrontOfFaces_Response__poses(untyped_member, index));
  geometry_msgs__msg__Pose * value =
    (geometry_msgs__msg__Pose *)(untyped_value);
  *value = *item;
}

void custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__assign_function__PosesInFrontOfFaces_Response__poses(
  void * untyped_member, size_t index, const void * untyped_value)
{
  geometry_msgs__msg__Pose * item =
    ((geometry_msgs__msg__Pose *)
    custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__get_function__PosesInFrontOfFaces_Response__poses(untyped_member, index));
  const geometry_msgs__msg__Pose * value =
    (const geometry_msgs__msg__Pose *)(untyped_value);
  *item = *value;
}

bool custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__resize_function__PosesInFrontOfFaces_Response__poses(
  void * untyped_member, size_t size)
{
  geometry_msgs__msg__Pose__Sequence * member =
    (geometry_msgs__msg__Pose__Sequence *)(untyped_member);
  geometry_msgs__msg__Pose__Sequence__fini(member);
  return geometry_msgs__msg__Pose__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_message_member_array[1] = {
  {
    "poses",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(custom_messages__srv__PosesInFrontOfFaces_Response, poses),  // bytes offset in struct
    NULL,  // default value
    custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__size_function__PosesInFrontOfFaces_Response__poses,  // size() function pointer
    custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__get_const_function__PosesInFrontOfFaces_Response__poses,  // get_const(index) function pointer
    custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__get_function__PosesInFrontOfFaces_Response__poses,  // get(index) function pointer
    custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__fetch_function__PosesInFrontOfFaces_Response__poses,  // fetch(index, &value) function pointer
    custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__assign_function__PosesInFrontOfFaces_Response__poses,  // assign(index, value) function pointer
    custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__resize_function__PosesInFrontOfFaces_Response__poses  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_message_members = {
  "custom_messages__srv",  // message namespace
  "PosesInFrontOfFaces_Response",  // message name
  1,  // number of fields
  sizeof(custom_messages__srv__PosesInFrontOfFaces_Response),
  custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_message_member_array,  // message members
  custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_message_type_support_handle = {
  0,
  &custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_custom_messages
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_messages, srv, PosesInFrontOfFaces_Response)() {
  custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Pose)();
  if (!custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_message_type_support_handle.typesupport_identifier) {
    custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &custom_messages__srv__PosesInFrontOfFaces_Response__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "custom_messages/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "custom_messages/srv/detail/poses_in_front_of_faces__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers custom_messages__srv__detail__poses_in_front_of_faces__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_service_members = {
  "custom_messages__srv",  // service namespace
  "PosesInFrontOfFaces",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // custom_messages__srv__detail__poses_in_front_of_faces__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Request_message_type_support_handle,
  NULL  // response message
  // custom_messages__srv__detail__poses_in_front_of_faces__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_Response_message_type_support_handle
};

static rosidl_service_type_support_t custom_messages__srv__detail__poses_in_front_of_faces__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_service_type_support_handle = {
  0,
  &custom_messages__srv__detail__poses_in_front_of_faces__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_messages, srv, PosesInFrontOfFaces_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_messages, srv, PosesInFrontOfFaces_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_custom_messages
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_messages, srv, PosesInFrontOfFaces)() {
  if (!custom_messages__srv__detail__poses_in_front_of_faces__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_service_type_support_handle.typesupport_identifier) {
    custom_messages__srv__detail__poses_in_front_of_faces__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)custom_messages__srv__detail__poses_in_front_of_faces__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_messages, srv, PosesInFrontOfFaces_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_messages, srv, PosesInFrontOfFaces_Response)()->data;
  }

  return &custom_messages__srv__detail__poses_in_front_of_faces__rosidl_typesupport_introspection_c__PosesInFrontOfFaces_service_type_support_handle;
}
