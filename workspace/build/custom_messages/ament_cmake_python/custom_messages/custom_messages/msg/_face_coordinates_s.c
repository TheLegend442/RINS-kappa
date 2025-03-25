// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from custom_messages:msg/FaceCoordinates.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "custom_messages/msg/detail/face_coordinates__struct.h"
#include "custom_messages/msg/detail/face_coordinates__functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool visualization_msgs__msg__marker__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * visualization_msgs__msg__marker__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool visualization_msgs__msg__marker__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * visualization_msgs__msg__marker__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool visualization_msgs__msg__marker__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * visualization_msgs__msg__marker__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool visualization_msgs__msg__marker__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * visualization_msgs__msg__marker__convert_to_py(void * raw_ros_message);
ROSIDL_GENERATOR_C_IMPORT
bool visualization_msgs__msg__marker__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * visualization_msgs__msg__marker__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool custom_messages__msg__face_coordinates__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[54];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("custom_messages.msg._face_coordinates.FaceCoordinates", full_classname_dest, 53) == 0);
  }
  custom_messages__msg__FaceCoordinates * ros_message = _ros_message;
  {  // center
    PyObject * field = PyObject_GetAttrString(_pymsg, "center");
    if (!field) {
      return false;
    }
    if (!visualization_msgs__msg__marker__convert_from_py(field, &ros_message->center)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // bottom_left
    PyObject * field = PyObject_GetAttrString(_pymsg, "bottom_left");
    if (!field) {
      return false;
    }
    if (!visualization_msgs__msg__marker__convert_from_py(field, &ros_message->bottom_left)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // bottom_right
    PyObject * field = PyObject_GetAttrString(_pymsg, "bottom_right");
    if (!field) {
      return false;
    }
    if (!visualization_msgs__msg__marker__convert_from_py(field, &ros_message->bottom_right)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // upper_left
    PyObject * field = PyObject_GetAttrString(_pymsg, "upper_left");
    if (!field) {
      return false;
    }
    if (!visualization_msgs__msg__marker__convert_from_py(field, &ros_message->upper_left)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // upper_right
    PyObject * field = PyObject_GetAttrString(_pymsg, "upper_right");
    if (!field) {
      return false;
    }
    if (!visualization_msgs__msg__marker__convert_from_py(field, &ros_message->upper_right)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * custom_messages__msg__face_coordinates__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of FaceCoordinates */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("custom_messages.msg._face_coordinates");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "FaceCoordinates");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  custom_messages__msg__FaceCoordinates * ros_message = (custom_messages__msg__FaceCoordinates *)raw_ros_message;
  {  // center
    PyObject * field = NULL;
    field = visualization_msgs__msg__marker__convert_to_py(&ros_message->center);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "center", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // bottom_left
    PyObject * field = NULL;
    field = visualization_msgs__msg__marker__convert_to_py(&ros_message->bottom_left);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "bottom_left", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // bottom_right
    PyObject * field = NULL;
    field = visualization_msgs__msg__marker__convert_to_py(&ros_message->bottom_right);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "bottom_right", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // upper_left
    PyObject * field = NULL;
    field = visualization_msgs__msg__marker__convert_to_py(&ros_message->upper_left);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "upper_left", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // upper_right
    PyObject * field = NULL;
    field = visualization_msgs__msg__marker__convert_to_py(&ros_message->upper_right);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "upper_right", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
