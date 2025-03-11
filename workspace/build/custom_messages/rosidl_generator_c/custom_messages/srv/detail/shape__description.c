// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from custom_messages:srv/Shape.idl
// generated code does not contain a copyright notice

#include "custom_messages/srv/detail/shape__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_custom_messages
const rosidl_type_hash_t *
custom_messages__srv__Shape__get_type_hash(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x39, 0xf9, 0xab, 0xb5, 0xdd, 0x40, 0xbf, 0xbe,
      0xd3, 0x87, 0xea, 0xf0, 0xdb, 0x76, 0xcb, 0x9d,
      0x80, 0x30, 0xbd, 0x74, 0x75, 0x51, 0xf3, 0x39,
      0xdd, 0x0a, 0xe8, 0x8b, 0x77, 0x34, 0xd4, 0xea,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_custom_messages
const rosidl_type_hash_t *
custom_messages__srv__Shape_Request__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xbd, 0x0c, 0x81, 0x25, 0x87, 0xa5, 0x66, 0x6e,
      0xd9, 0xa7, 0x5e, 0xda, 0xb1, 0x94, 0xd4, 0xe4,
      0xa3, 0xc1, 0x95, 0x82, 0x35, 0x43, 0xb2, 0x85,
      0xb8, 0x91, 0x34, 0xc7, 0x9e, 0x32, 0xa0, 0xa9,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_custom_messages
const rosidl_type_hash_t *
custom_messages__srv__Shape_Response__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xfa, 0x37, 0x2e, 0x8f, 0x99, 0xbe, 0x4e, 0x91,
      0xd9, 0x6b, 0x30, 0xf7, 0x56, 0x23, 0xaf, 0x0f,
      0x9f, 0xbb, 0xbe, 0xc8, 0xcb, 0x94, 0xc9, 0x56,
      0x96, 0x1f, 0x0e, 0x97, 0x61, 0x1a, 0xd4, 0xe4,
    }};
  return &hash;
}

ROSIDL_GENERATOR_C_PUBLIC_custom_messages
const rosidl_type_hash_t *
custom_messages__srv__Shape_Event__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x5f, 0x44, 0x51, 0x85, 0x04, 0xbc, 0xab, 0xf9,
      0xe3, 0xda, 0xed, 0xa4, 0x5b, 0x4b, 0x34, 0x29,
      0x26, 0xb0, 0x9b, 0x45, 0x52, 0x35, 0x8f, 0x37,
      0xde, 0x0f, 0x5e, 0x89, 0xe8, 0x73, 0xc9, 0x0d,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "service_msgs/msg/detail/service_event_info__functions.h"
#include "builtin_interfaces/msg/detail/time__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t service_msgs__msg__ServiceEventInfo__EXPECTED_HASH = {1, {
    0x41, 0xbc, 0xbb, 0xe0, 0x7a, 0x75, 0xc9, 0xb5,
    0x2b, 0xc9, 0x6b, 0xfd, 0x5c, 0x24, 0xd7, 0xf0,
    0xfc, 0x0a, 0x08, 0xc0, 0xcb, 0x79, 0x21, 0xb3,
    0x37, 0x3c, 0x57, 0x32, 0x34, 0x5a, 0x6f, 0x45,
  }};
#endif

static char custom_messages__srv__Shape__TYPE_NAME[] = "custom_messages/srv/Shape";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char custom_messages__srv__Shape_Event__TYPE_NAME[] = "custom_messages/srv/Shape_Event";
static char custom_messages__srv__Shape_Request__TYPE_NAME[] = "custom_messages/srv/Shape_Request";
static char custom_messages__srv__Shape_Response__TYPE_NAME[] = "custom_messages/srv/Shape_Response";
static char service_msgs__msg__ServiceEventInfo__TYPE_NAME[] = "service_msgs/msg/ServiceEventInfo";

// Define type names, field names, and default values
static char custom_messages__srv__Shape__FIELD_NAME__request_message[] = "request_message";
static char custom_messages__srv__Shape__FIELD_NAME__response_message[] = "response_message";
static char custom_messages__srv__Shape__FIELD_NAME__event_message[] = "event_message";

static rosidl_runtime_c__type_description__Field custom_messages__srv__Shape__FIELDS[] = {
  {
    {custom_messages__srv__Shape__FIELD_NAME__request_message, 15, 15},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {custom_messages__srv__Shape_Request__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {custom_messages__srv__Shape__FIELD_NAME__response_message, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {custom_messages__srv__Shape_Response__TYPE_NAME, 34, 34},
    },
    {NULL, 0, 0},
  },
  {
    {custom_messages__srv__Shape__FIELD_NAME__event_message, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {custom_messages__srv__Shape_Event__TYPE_NAME, 31, 31},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription custom_messages__srv__Shape__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {custom_messages__srv__Shape_Event__TYPE_NAME, 31, 31},
    {NULL, 0, 0},
  },
  {
    {custom_messages__srv__Shape_Request__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
  {
    {custom_messages__srv__Shape_Response__TYPE_NAME, 34, 34},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
custom_messages__srv__Shape__get_type_description(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {custom_messages__srv__Shape__TYPE_NAME, 25, 25},
      {custom_messages__srv__Shape__FIELDS, 3, 3},
    },
    {custom_messages__srv__Shape__REFERENCED_TYPE_DESCRIPTIONS, 5, 5},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = custom_messages__srv__Shape_Event__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = custom_messages__srv__Shape_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[3].fields = custom_messages__srv__Shape_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char custom_messages__srv__Shape_Request__FIELD_NAME__shape[] = "shape";
static char custom_messages__srv__Shape_Request__FIELD_NAME__duration[] = "duration";

static rosidl_runtime_c__type_description__Field custom_messages__srv__Shape_Request__FIELDS[] = {
  {
    {custom_messages__srv__Shape_Request__FIELD_NAME__shape, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {custom_messages__srv__Shape_Request__FIELD_NAME__duration, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
custom_messages__srv__Shape_Request__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {custom_messages__srv__Shape_Request__TYPE_NAME, 33, 33},
      {custom_messages__srv__Shape_Request__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char custom_messages__srv__Shape_Response__FIELD_NAME__shape[] = "shape";

static rosidl_runtime_c__type_description__Field custom_messages__srv__Shape_Response__FIELDS[] = {
  {
    {custom_messages__srv__Shape_Response__FIELD_NAME__shape, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
custom_messages__srv__Shape_Response__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {custom_messages__srv__Shape_Response__TYPE_NAME, 34, 34},
      {custom_messages__srv__Shape_Response__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}
// Define type names, field names, and default values
static char custom_messages__srv__Shape_Event__FIELD_NAME__info[] = "info";
static char custom_messages__srv__Shape_Event__FIELD_NAME__request[] = "request";
static char custom_messages__srv__Shape_Event__FIELD_NAME__response[] = "response";

static rosidl_runtime_c__type_description__Field custom_messages__srv__Shape_Event__FIELDS[] = {
  {
    {custom_messages__srv__Shape_Event__FIELD_NAME__info, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {custom_messages__srv__Shape_Event__FIELD_NAME__request, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {custom_messages__srv__Shape_Request__TYPE_NAME, 33, 33},
    },
    {NULL, 0, 0},
  },
  {
    {custom_messages__srv__Shape_Event__FIELD_NAME__response, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_BOUNDED_SEQUENCE,
      1,
      0,
      {custom_messages__srv__Shape_Response__TYPE_NAME, 34, 34},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription custom_messages__srv__Shape_Event__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {custom_messages__srv__Shape_Request__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
  {
    {custom_messages__srv__Shape_Response__TYPE_NAME, 34, 34},
    {NULL, 0, 0},
  },
  {
    {service_msgs__msg__ServiceEventInfo__TYPE_NAME, 33, 33},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
custom_messages__srv__Shape_Event__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {custom_messages__srv__Shape_Event__TYPE_NAME, 31, 31},
      {custom_messages__srv__Shape_Event__FIELDS, 3, 3},
    },
    {custom_messages__srv__Shape_Event__REFERENCED_TYPE_DESCRIPTIONS, 4, 4},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[1].fields = custom_messages__srv__Shape_Request__get_type_description(NULL)->type_description.fields;
    description.referenced_type_descriptions.data[2].fields = custom_messages__srv__Shape_Response__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&service_msgs__msg__ServiceEventInfo__EXPECTED_HASH, service_msgs__msg__ServiceEventInfo__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = service_msgs__msg__ServiceEventInfo__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string shape\n"
  "int32 duration\n"
  "---\n"
  "string shape";

static char srv_encoding[] = "srv";
static char implicit_encoding[] = "implicit";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
custom_messages__srv__Shape__get_individual_type_description_source(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {custom_messages__srv__Shape__TYPE_NAME, 25, 25},
    {srv_encoding, 3, 3},
    {toplevel_type_raw_source, 44, 44},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
custom_messages__srv__Shape_Request__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {custom_messages__srv__Shape_Request__TYPE_NAME, 33, 33},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
custom_messages__srv__Shape_Response__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {custom_messages__srv__Shape_Response__TYPE_NAME, 34, 34},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource *
custom_messages__srv__Shape_Event__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {custom_messages__srv__Shape_Event__TYPE_NAME, 31, 31},
    {implicit_encoding, 8, 8},
    {NULL, 0, 0},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
custom_messages__srv__Shape__get_type_description_sources(
  const rosidl_service_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[6];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 6, 6};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *custom_messages__srv__Shape__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *custom_messages__srv__Shape_Event__get_individual_type_description_source(NULL);
    sources[3] = *custom_messages__srv__Shape_Request__get_individual_type_description_source(NULL);
    sources[4] = *custom_messages__srv__Shape_Response__get_individual_type_description_source(NULL);
    sources[5] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
custom_messages__srv__Shape_Request__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *custom_messages__srv__Shape_Request__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
custom_messages__srv__Shape_Response__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *custom_messages__srv__Shape_Response__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
custom_messages__srv__Shape_Event__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[5];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 5, 5};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *custom_messages__srv__Shape_Event__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *custom_messages__srv__Shape_Request__get_individual_type_description_source(NULL);
    sources[3] = *custom_messages__srv__Shape_Response__get_individual_type_description_source(NULL);
    sources[4] = *service_msgs__msg__ServiceEventInfo__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
