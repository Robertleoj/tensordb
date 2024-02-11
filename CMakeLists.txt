cmake_minimum_required(VERSION 3.22)
project(project)
set(CMAKE_CXX_STANDARD 20)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Python 3.10 COMPONENTS Interpreter Development.Module REQUIRED)
if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

add_subdirectory(external/fmt)
add_subdirectory(external/spdlog)
add_subdirectory(external/nanobind)

# Set to ON for profiling.
# Off by default because this consumes a lot of memory.
option(TRACY_ENABLE "" OFF)
add_subdirectory(external/tracy)

add_subdirectory(src)
