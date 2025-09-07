cmake_minimum_required(VERSION 3.29)
project(LAB1)

set(CMAKE_CXX_STANDARD 20)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libgcc -static-libstdc++ -static")

add_executable(LAB1 main.cpp)

add_executable(test main2.cpp)
