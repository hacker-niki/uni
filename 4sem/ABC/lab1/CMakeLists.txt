cmake_minimum_required(VERSION 3.14)
project (lab1)

#Set C++ language version
set(CMAKE_CXX_STANDARD 17)
#Enable ASM provided by NASM
enable_language(ASM_NASM)

if(APPLE)
	#Add leading underscore when building macho64 object files
	string(APPEND CMAKE_ASM_NASM_FLAGS "--prefix _")
endif(APPLE)

if(WIN32)
	string(APPEND CMAKE_ASM_NASM_FLAGS "-dWIN32=1")
endif(WIN32)


add_executable(lab1_HT main.cpp calcS.asm calcY.asm)

