#!/bin/bash
set -e

TARGET_SOC="rv110x"

if [ -z $RK_RV110X_TOOLCHAIN ]; then
  echo "Please set the RK_RV110X_TOOLCHAIN environment variable!"
  echo "example:"
  echo "  export RK_RV110X_TOOLCHAIN=<path-to-your-dir/arm-rockchip830-linux-uclibcgnueabihf>"
  exit
fi

# for arm
GCC_COMPILER=$RK_RV110X_TOOLCHAIN

ROOT_PWD=$( cd "$( dirname $0 )" && cd -P "$( dirname "$SOURCE" )" && pwd )

# build
BUILD_DIR=${ROOT_PWD}/build/build_linux_arm

if [[ ! -d "${BUILD_DIR}" ]]; then
  mkdir -p ${BUILD_DIR}
fi

cd ${BUILD_DIR}
cmake ../.. \
    -DTARGET_SOC=${TARGET_SOC} \
    -DCMAKE_C_COMPILER=${GCC_COMPILER}-gcc \
    -DCMAKE_CXX_COMPILER=${GCC_COMPILER}-g++
make -j4
make install
cd -
