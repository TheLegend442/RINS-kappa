// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from custom_messages:msg/FaceCoordinates.idl
// generated code does not contain a copyright notice
#include "custom_messages/msg/detail/face_coordinates__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `center`
// Member `bottom_right`
// Member `upper_left`
#include "visualization_msgs/msg/detail/marker__functions.h"

bool
custom_messages__msg__FaceCoordinates__init(custom_messages__msg__FaceCoordinates * msg)
{
  if (!msg) {
    return false;
  }
  // center
  if (!visualization_msgs__msg__Marker__init(&msg->center)) {
    custom_messages__msg__FaceCoordinates__fini(msg);
    return false;
  }
  // bottom_right
  if (!visualization_msgs__msg__Marker__init(&msg->bottom_right)) {
    custom_messages__msg__FaceCoordinates__fini(msg);
    return false;
  }
  // upper_left
  if (!visualization_msgs__msg__Marker__init(&msg->upper_left)) {
    custom_messages__msg__FaceCoordinates__fini(msg);
    return false;
  }
  return true;
}

void
custom_messages__msg__FaceCoordinates__fini(custom_messages__msg__FaceCoordinates * msg)
{
  if (!msg) {
    return;
  }
  // center
  visualization_msgs__msg__Marker__fini(&msg->center);
  // bottom_right
  visualization_msgs__msg__Marker__fini(&msg->bottom_right);
  // upper_left
  visualization_msgs__msg__Marker__fini(&msg->upper_left);
}

bool
custom_messages__msg__FaceCoordinates__are_equal(const custom_messages__msg__FaceCoordinates * lhs, const custom_messages__msg__FaceCoordinates * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // center
  if (!visualization_msgs__msg__Marker__are_equal(
      &(lhs->center), &(rhs->center)))
  {
    return false;
  }
  // bottom_right
  if (!visualization_msgs__msg__Marker__are_equal(
      &(lhs->bottom_right), &(rhs->bottom_right)))
  {
    return false;
  }
  // upper_left
  if (!visualization_msgs__msg__Marker__are_equal(
      &(lhs->upper_left), &(rhs->upper_left)))
  {
    return false;
  }
  return true;
}

bool
custom_messages__msg__FaceCoordinates__copy(
  const custom_messages__msg__FaceCoordinates * input,
  custom_messages__msg__FaceCoordinates * output)
{
  if (!input || !output) {
    return false;
  }
  // center
  if (!visualization_msgs__msg__Marker__copy(
      &(input->center), &(output->center)))
  {
    return false;
  }
  // bottom_right
  if (!visualization_msgs__msg__Marker__copy(
      &(input->bottom_right), &(output->bottom_right)))
  {
    return false;
  }
  // upper_left
  if (!visualization_msgs__msg__Marker__copy(
      &(input->upper_left), &(output->upper_left)))
  {
    return false;
  }
  return true;
}

custom_messages__msg__FaceCoordinates *
custom_messages__msg__FaceCoordinates__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_messages__msg__FaceCoordinates * msg = (custom_messages__msg__FaceCoordinates *)allocator.allocate(sizeof(custom_messages__msg__FaceCoordinates), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(custom_messages__msg__FaceCoordinates));
  bool success = custom_messages__msg__FaceCoordinates__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
custom_messages__msg__FaceCoordinates__destroy(custom_messages__msg__FaceCoordinates * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    custom_messages__msg__FaceCoordinates__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
custom_messages__msg__FaceCoordinates__Sequence__init(custom_messages__msg__FaceCoordinates__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_messages__msg__FaceCoordinates * data = NULL;

  if (size) {
    data = (custom_messages__msg__FaceCoordinates *)allocator.zero_allocate(size, sizeof(custom_messages__msg__FaceCoordinates), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = custom_messages__msg__FaceCoordinates__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        custom_messages__msg__FaceCoordinates__fini(&data[i - 1]);
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
custom_messages__msg__FaceCoordinates__Sequence__fini(custom_messages__msg__FaceCoordinates__Sequence * array)
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
      custom_messages__msg__FaceCoordinates__fini(&array->data[i]);
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

custom_messages__msg__FaceCoordinates__Sequence *
custom_messages__msg__FaceCoordinates__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_messages__msg__FaceCoordinates__Sequence * array = (custom_messages__msg__FaceCoordinates__Sequence *)allocator.allocate(sizeof(custom_messages__msg__FaceCoordinates__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = custom_messages__msg__FaceCoordinates__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
custom_messages__msg__FaceCoordinates__Sequence__destroy(custom_messages__msg__FaceCoordinates__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    custom_messages__msg__FaceCoordinates__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
custom_messages__msg__FaceCoordinates__Sequence__are_equal(const custom_messages__msg__FaceCoordinates__Sequence * lhs, const custom_messages__msg__FaceCoordinates__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!custom_messages__msg__FaceCoordinates__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
custom_messages__msg__FaceCoordinates__Sequence__copy(
  const custom_messages__msg__FaceCoordinates__Sequence * input,
  custom_messages__msg__FaceCoordinates__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(custom_messages__msg__FaceCoordinates);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    custom_messages__msg__FaceCoordinates * data =
      (custom_messages__msg__FaceCoordinates *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!custom_messages__msg__FaceCoordinates__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          custom_messages__msg__FaceCoordinates__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!custom_messages__msg__FaceCoordinates__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
