cmake_minimum_required(VERSION 3.4.1)

project(rknn_yolov5_demo)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wl,--allow-shlib-undefined")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wl,--allow-shlib-undefined")

# install target and libraries
set(CMAKE_INSTALL_PREFIX ${CMAKE_SOURCE_DIR}/install/rknn_yolov5_demo_${CMAKE_SYSTEM_NAME})

set(CMAKE_SKIP_INSTALL_RPATH FALSE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")

# rknn api
if(TARGET_SOC STREQUAL "rk356x")
  set(RKNN_API_PATH ${CMAKE_SOURCE_DIR}/../../runtime/RK356X/${CMAKE_SYSTEM_NAME}/librknn_api)
elseif(TARGET_SOC STREQUAL "rk3588")
  set(RKNN_API_PATH ${CMAKE_SOURCE_DIR}/../../runtime/RK3588/${CMAKE_SYSTEM_NAME}/librknn_api)
  elseif(TARGET_SOC STREQUAL "rv110x")
  set(RKNN_API_PATH ${CMAKE_SOURCE_DIR}/../../runtime/RV110X/${CMAKE_SYSTEM_NAME}/librknn_api)
else()
  message(FATAL_ERROR "TARGET_SOC is not set, ref value: rk356x or rk3588 or rv110x")
endif()

if (CMAKE_SYSTEM_NAME STREQUAL "Android")
  set(RKNN_RT_LIB ${RKNN_API_PATH}/${CMAKE_ANDROID_ARCH_ABI}/librknnrt.so)
else()
  if (CMAKE_C_COMPILER MATCHES "aarch64")
    set(LIB_ARCH aarch64)
  else()
    set(LIB_ARCH armhf)
  endif()
  if(TARGET_SOC STREQUAL "rv110x")
    set(RKNN_RT_LIB ${RKNN_API_PATH}/${LIB_ARCH}/librknnmrt.so)
  else()
    set(RKNN_RT_LIB ${RKNN_API_PATH}/${LIB_ARCH}/librknnrt.so)
  endif()
endif()
include_directories(${RKNN_API_PATH}/include)
include_directories(${CMAKE_SOURCE_DIR}/../3rdparty)

# opencv
if (CMAKE_SYSTEM_NAME STREQUAL "Android")
    set(OpenCV_DIR ${CMAKE_SOURCE_DIR}/../3rdparty/opencv/OpenCV-android-sdk/sdk/native/jni/abi-${CMAKE_ANDROID_ARCH_ABI})
else()
  if(LIB_ARCH STREQUAL "armhf")
    set(OpenCV_DIR ${CMAKE_SOURCE_DIR}/../3rdparty/opencv/opencv-linux-armhf/share/OpenCV)
  else()
    set(OpenCV_DIR ${CMAKE_SOURCE_DIR}/../3rdparty/opencv/opencv-linux-aarch64/share/OpenCV)
  endif()
endif()
find_package(OpenCV REQUIRED)

#rga
if(TARGET_SOC STREQUAL "rk356x")
  set(RGA_PATH ${CMAKE_SOURCE_DIR}/../3rdparty/rga/RK356X)
elseif(TARGET_SOC STREQUAL "rk3588")
  set(RGA_PATH ${CMAKE_SOURCE_DIR}/../3rdparty/rga/RK3588)
elseif(TARGET_SOC STREQUAL "rv110x")
  set(RGA_PATH ${CMAKE_SOURCE_DIR}/../3rdparty/rga/RV110X)
else()
  message(FATAL_ERROR "TARGET_SOC is not set, ref value: rk356x or rk3588 or rv110x")
endif()
if (CMAKE_SYSTEM_NAME STREQUAL "Android")
  set(RGA_LIB ${RGA_PATH}/lib/Android/${CMAKE_ANDROID_ARCH_ABI}/librga.so)
else()
  if (CMAKE_C_COMPILER MATCHES "aarch64")
    set(LIB_ARCH aarch64)
  else()
    set(LIB_ARCH armhf)
  endif()
  set(RGA_LIB ${RGA_PATH}/lib/Linux//${LIB_ARCH}/librga.so)
endif()
include_directories( ${RGA_PATH}/include)

# rknn_yolov5_demo
include_directories( ${CMAKE_SOURCE_DIR}/include)

if(TARGET_SOC STREQUAL "rv110x")
  add_executable(rknn_yolov5_demo_zero_copy
              src/main_zero_copy.cc
              src/postprocess.cc
  )

  target_link_libraries(rknn_yolov5_demo_zero_copy
  ${RKNN_RT_LIB}
  )

  # install target and libraries
  set(CMAKE_INSTALL_PREFIX ${CMAKE_SOURCE_DIR}/install/rknn_yolov5_demo_${CMAKE_SYSTEM_NAME})
  install(TARGETS rknn_yolov5_demo_zero_copy DESTINATION ./)
else()
  add_executable(rknn_yolov5_demo
          src/main.cc
          src/postprocess.cc
  )

  target_link_libraries(rknn_yolov5_demo
    ${RKNN_RT_LIB}
    ${RGA_LIB}
    ${OpenCV_LIBS}
  )
  install(TARGETS rknn_yolov5_demo DESTINATION ./)

  add_executable(rknn_yolov5_demo_zero_copy
              src/main_zero_copy.cc
              src/postprocess.cc
  )

  target_link_libraries(rknn_yolov5_demo_zero_copy
  ${RKNN_RT_LIB}
  )

  # install target and libraries
  set(CMAKE_INSTALL_PREFIX ${CMAKE_SOURCE_DIR}/install/rknn_yolov5_demo_${CMAKE_SYSTEM_NAME})
  install(TARGETS rknn_yolov5_demo_zero_copy DESTINATION ./)

endif()

install(PROGRAMS ${RKNN_RT_LIB} DESTINATION lib)
install(DIRECTORY model DESTINATION ./)
