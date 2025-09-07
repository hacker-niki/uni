cmake_minimum_required(VERSION 3.29)
project(LAB5)

set(CMAKE_CXX_STANDARD 14)

set(CMAKE_CXX_STANDARD_LIBRARIES "-static-libgcc -static-libstdc++ -lwsock32 -lws2_32 ${CMAKE_CSS_STANDARD_LIBRARIES}")
set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-Bstatic,--whole-archive -lwinpthread -Wl,--no-whole-archive")

include_directories(.)

add_executable(LAB5_client Client.cpp)
add_executable(LAB5_server Server.cpp)

if(WIN32)
    target_link_libraries(LAB5_client wsock32 ws2_32)
    target_link_libraries(LAB5_server wsock32 ws2_32)
endif()