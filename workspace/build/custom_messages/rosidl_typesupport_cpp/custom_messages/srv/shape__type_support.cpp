// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from custom_messages:srv/Shape.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "custom_messages/srv/detail/shape__functions.h"
#include "custom_messages/srv/detail/shape__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace custom_messages
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _Shape_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Shape_Request_type_support_ids_t;

static const _Shape_Request_type_support_ids_t _Shape_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Shape_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Shape_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Shape_Request_type_support_symbol_names_t _Shape_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, custom_messages, srv, Shape_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, custom_messages, srv, Shape_Request)),
  }
};

typedef struct _Shape_Request_type_support_data_t
{
  void * data[2];
} _Shape_Request_type_support_data_t;

static _Shape_Request_type_support_data_t _Shape_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Shape_Request_message_typesupport_map = {
  2,
  "custom_messages",
  &_Shape_Request_message_typesupport_ids.typesupport_identifier[0],
  &_Shape_Request_message_typesupport_symbol_names.symbol_name[0],
  &_Shape_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Shape_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Shape_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &custom_messages__srv__Shape_Request__get_type_hash,
  &custom_messages__srv__Shape_Request__get_type_description,
  &custom_messages__srv__Shape_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace custom_messages

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<custom_messages::srv::Shape_Request>()
{
  return &::custom_messages::srv::rosidl_typesupport_cpp::Shape_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, custom_messages, srv, Shape_Request)() {
  return get_message_type_support_handle<custom_messages::srv::Shape_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_messages/srv/detail/shape__functions.h"
// already included above
// #include "custom_messages/srv/detail/shape__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_messages
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _Shape_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Shape_Response_type_support_ids_t;

static const _Shape_Response_type_support_ids_t _Shape_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Shape_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Shape_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Shape_Response_type_support_symbol_names_t _Shape_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, custom_messages, srv, Shape_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, custom_messages, srv, Shape_Response)),
  }
};

typedef struct _Shape_Response_type_support_data_t
{
  void * data[2];
} _Shape_Response_type_support_data_t;

static _Shape_Response_type_support_data_t _Shape_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Shape_Response_message_typesupport_map = {
  2,
  "custom_messages",
  &_Shape_Response_message_typesupport_ids.typesupport_identifier[0],
  &_Shape_Response_message_typesupport_symbol_names.symbol_name[0],
  &_Shape_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Shape_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Shape_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &custom_messages__srv__Shape_Response__get_type_hash,
  &custom_messages__srv__Shape_Response__get_type_description,
  &custom_messages__srv__Shape_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace custom_messages

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<custom_messages::srv::Shape_Response>()
{
  return &::custom_messages::srv::rosidl_typesupport_cpp::Shape_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, custom_messages, srv, Shape_Response)() {
  return get_message_type_support_handle<custom_messages::srv::Shape_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_messages/srv/detail/shape__functions.h"
// already included above
// #include "custom_messages/srv/detail/shape__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_messages
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _Shape_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Shape_Event_type_support_ids_t;

static const _Shape_Event_type_support_ids_t _Shape_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Shape_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Shape_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Shape_Event_type_support_symbol_names_t _Shape_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, custom_messages, srv, Shape_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, custom_messages, srv, Shape_Event)),
  }
};

typedef struct _Shape_Event_type_support_data_t
{
  void * data[2];
} _Shape_Event_type_support_data_t;

static _Shape_Event_type_support_data_t _Shape_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Shape_Event_message_typesupport_map = {
  2,
  "custom_messages",
  &_Shape_Event_message_typesupport_ids.typesupport_identifier[0],
  &_Shape_Event_message_typesupport_symbol_names.symbol_name[0],
  &_Shape_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Shape_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Shape_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &custom_messages__srv__Shape_Event__get_type_hash,
  &custom_messages__srv__Shape_Event__get_type_description,
  &custom_messages__srv__Shape_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace custom_messages

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<custom_messages::srv::Shape_Event>()
{
  return &::custom_messages::srv::rosidl_typesupport_cpp::Shape_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, custom_messages, srv, Shape_Event)() {
  return get_message_type_support_handle<custom_messages::srv::Shape_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "custom_messages/srv/detail/shape__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_messages
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _Shape_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Shape_type_support_ids_t;

static const _Shape_type_support_ids_t _Shape_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _Shape_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Shape_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Shape_type_support_symbol_names_t _Shape_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, custom_messages, srv, Shape)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, custom_messages, srv, Shape)),
  }
};

typedef struct _Shape_type_support_data_t
{
  void * data[2];
} _Shape_type_support_data_t;

static _Shape_type_support_data_t _Shape_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Shape_service_typesupport_map = {
  2,
  "custom_messages",
  &_Shape_service_typesupport_ids.typesupport_identifier[0],
  &_Shape_service_typesupport_symbol_names.symbol_name[0],
  &_Shape_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t Shape_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Shape_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<custom_messages::srv::Shape_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<custom_messages::srv::Shape_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<custom_messages::srv::Shape_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<custom_messages::srv::Shape>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<custom_messages::srv::Shape>,
  &custom_messages__srv__Shape__get_type_hash,
  &custom_messages__srv__Shape__get_type_description,
  &custom_messages__srv__Shape__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace custom_messages

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<custom_messages::srv::Shape>()
{
  return &::custom_messages::srv::rosidl_typesupport_cpp::Shape_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp
