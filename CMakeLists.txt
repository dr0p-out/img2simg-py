cmake_minimum_required()

add_library(base
  libbase/stringprintf.cpp
  libbase/mapped_file.cpp)
target_include_directories(base PUBLIC
  libbase/include)

find_package(ZLIB REQUIRED)

add_library(sparse
  core/libsparse/sparse_read.cpp
  core/libsparse/sparse.cpp
  core/libsparse/sparse_err.cpp
  core/libsparse/sparse_crc32.cpp
  core/libsparse/output_file.cpp
  core/libsparse/backed_block.cpp)
target_include_directories(sparse PUBLIC
  core/libsparse/include)
target_link_libraries(sparse
  ZLIB::ZLIB
  base)

add_executable(img2simg
  core/libsparse/img2simg.cpp)
target_link_libraries(img2simg sparse)
