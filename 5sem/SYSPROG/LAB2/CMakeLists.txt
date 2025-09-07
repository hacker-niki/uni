cmake_minimum_required(VERSION 3.29)
project(LAB2)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libgcc -static-libstdc++ -static")

add_executable(LAB2 main.cpp)

add_executable(LAB2_create create.cpp)