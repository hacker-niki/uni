cmake_minimum_required(VERSION 3.14)
project(lab2)

#Set C++ language version
set(CMAKE_CXX_STANDARD 17)
#Enable ASM provided by NASM
enable_language(ASM_NASM)

if (APPLE)
    #Add leading underscore when building macho64 object files
    string(APPEND CMAKE_ASM_NASM_FLAGS "--prefix _")
endif (APPLE)

if (WIN32)
    string(APPEND CMAKE_ASM_NASM_FLAGS "-dWIN32=1")
endif (WIN32)


add_executable(lab2 main.cpp calcS.asm calcY.asm)

add_executable(lab2_gpu main_gpu.cpp calcS.asm calcY.asm)
add_executable(lab2_only_gpu main_only_gpu.cpp calcS.asm calcY.asm)
target_link_libraries(lab2_gpu PRIVATE OpenCL)
target_link_libraries(lab2_only_gpu PRIVATE OpenCL)