cmake_minimum_required(VERSION 3.15)

set(CMAKE_TRY_COMPILE_PLATFORM_VARIABLES TAURUS_BOARD TAURUS_TARGET_SOC TAURUS_TARGET_TRIPLET)
set(TAURUS_BOARD "ARIES_V3" CACHE STRING "Target Board")
set(TAURUS_TARGET_SOC "THEJAS32" CACHE STRING "Target SoC")
set(TAURUS_TARGET_TRIPLET "riscv-none-elf" CACHE STRING "Target Triplet")

project(AriesLEDApp C ASM)

find_package(taurus REQUIRED)

add_executable(app.elf main.c)
target_link_libraries(app.elf PRIVATE taurus::taurus)

add_custom_command(TARGET app.elf POST_BUILD
    COMMAND riscv-none-elf-objcopy -O binary app.elf app.bin
)