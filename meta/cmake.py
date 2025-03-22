from IO import *

cmake = Dir('cmake')

x86 = File('x86_64-linux-gnu.cmake');cmake/x86


lists = File('CMakeLists.txt')

(lists
 / r'cmake_minimum_required(VERSION 3.22)'
 / r'get_filename_component(CMAKE_PROJECT_NAME ${CMAKE_SOURCE_DIR} NAME_WE)'
 / r'project(${CMAKE_PROJECT_NAME} LANGUAGES C CXX ASM)'
 / ''
 / r'message("-- |")'
 / r'message("-- | toolchain: " ${CMAKE_CXX_COMPILER} " @ " ${CMAKE_TOOLCHAIN_FILE})'
 / r'message("-- |      host: " ${CMAKE_HOST_SYSTEM_NAME}-${CMAKE_HOST_SYSTEM_VERSION})'
 / r'message("-- |    target: " "hw:" ${HW} " cpu:" ${CPU} " arch:" ${ARCH} " os:" ${OS})'
 / r'message("-- |   startup: " "${S}")'
 / r'message("-- |    binary: " ${CMAKE_INSTALL_PREFIX}/${BIN_OUTPUT_NAME}${CMAKE_EXECUTABLE_SUFFIX})'
 / r'message("-- |")'

 )

cmake.sync()
lists.sync()
