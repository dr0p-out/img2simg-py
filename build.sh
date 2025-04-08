#!/bin/sh
#
# compile_commands.json
#

CC=clang CXX=clang++ cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -Wno-dev
cmake --build build --parallel
