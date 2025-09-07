cmake_minimum_required(VERSION 3.28)
project(Traceroute)

set(CMAKE_CXX_STANDARD 17)

include(FetchContent)
FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
FetchContent_MakeAvailable(googletest)

enable_testing()

add_executable(Traceroute main.cpp
        Traceroute.cpp
        Traceroute.h)


add_executable(TracerouteTests
        tests/TracerouteTests.cpp
        Traceroute.cpp
)

target_link_libraries(TracerouteTests gtest gtest_main)

include(GoogleTest)
gtest_discover_tests(TracerouteTests)