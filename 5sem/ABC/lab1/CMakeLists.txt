cmake_minimum_required(VERSION 3.10)

project(NasmProject)

# Define the assembly source file
set(SOURCE 32bit-main.asm)

# Specify the output binary name
set(OUTPUT_NAME boot_sect_simple.bin)

# Add the NASM compiler flags for binary format
set(NASM_FLAGS "-f bin -I /home/nikita/uni/5sem/ABC/lab1/")

# Add a custom target for the assembly file
add_custom_command(
        OUTPUT ${OUTPUT_NAME}
        COMMAND nasm ${NASM_FLAGS} ${CMAKE_CURRENT_SOURCE_DIR}/${SOURCE} -o ${OUTPUT_NAME}
        DEPENDS ${SOURCE}
        COMMENT "Assembling ${SOURCE} to binary format"
)

# Add a custom target to build the binary
add_custom_target(build_nasm ALL DEPENDS ${OUTPUT_NAME})