cmake_minimum_required(VERSION 3.10)
project(NetworkSecurityLab)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Boost REQUIRED COMPONENTS system)

add_executable(server server.cpp)
add_executable(client client.cpp)
add_executable(attack attack.cpp)

target_link_libraries(server Boost::system)
target_link_libraries(client Boost::system)
target_link_libraries(attack Boost::system)

target_link_libraries(server pthread)
target_link_libraries(client pthread)
target_link_libraries(attack pthread)