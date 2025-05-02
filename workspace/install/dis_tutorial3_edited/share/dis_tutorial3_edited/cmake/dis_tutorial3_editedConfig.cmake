# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_dis_tutorial3_edited_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED dis_tutorial3_edited_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(dis_tutorial3_edited_FOUND FALSE)
  elseif(NOT dis_tutorial3_edited_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(dis_tutorial3_edited_FOUND FALSE)
  endif()
  return()
endif()
set(_dis_tutorial3_edited_CONFIG_INCLUDED TRUE)

# output package information
if(NOT dis_tutorial3_edited_FIND_QUIETLY)
  message(STATUS "Found dis_tutorial3_edited: 0.0.1 (${dis_tutorial3_edited_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'dis_tutorial3_edited' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${dis_tutorial3_edited_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(dis_tutorial3_edited_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${dis_tutorial3_edited_DIR}/${_extra}")
endforeach()
