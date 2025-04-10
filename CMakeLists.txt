#
# core/libsparse/Android.bp
#

cmake_minimum_required()

if(CYGWIN)
# https://www.cygwin.com/ml/cygwin/2007-10/msg00594.html
# XXX: upstream does same for macOS, consider applying:
#      https://github.com/nmeum/android-tools/commit/21f1e58
add_compile_definitions(
  off64_t=off_t
  lseek64=lseek
  ftruncate64=ftruncate
)
endif()

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

add_executable(simg2img
  core/libsparse/simg2img.cpp)
target_link_libraries(simg2img sparse)
