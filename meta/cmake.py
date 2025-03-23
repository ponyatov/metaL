from IO import *

cmake = Dir('cmake')

x86 = File('x86_64-linux-gnu.cmake'); cmake / x86
(x86
 / r'set(CMAKE_SYSTEM_NAME       Linux)'
 / r'set(CMAKE_SYSTEM_PROCESSOR  x86_64)'
 / r'set(TOOLCHAIN_PREFIX        ${ARCH}-${OS}-gnu)'
 / r'set(CMAKE_EXECUTABLE_SUFFIX "")'
 / ''
 / r'add_compile_options("-march=native")'
 / ''
 / r'include(any_toolchain)'
 )

any = File('any_toolchain.cmake'); cmake / any
(any
 / r'set(CMAKE_C_STANDARD   17)'
 / r'set(CMAKE_CXX_STANDARD 17)'
 / ''
 / r'set(CMAKE_C_COMPILER_FORCED   TRUE)'
 / r'set(CMAKE_CXX_COMPILER_FORCED TRUE)'
 / r'set(CMAKE_C_COMPILER_ID       GNU)'
 / r'set(CMAKE_CXX_COMPILER_ID     GNU)'
 / ''
 / r'set(CMAKE_C_COMPILER   ${TOOLCHAIN_PREFIX}-gcc)'
 / r'set(CMAKE_ASM_COMPILER ${CMAKE_C_COMPILER})'
 / r'set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PREFIX}-g++)'
 / r'set(CMAKE_LINKER       ${CMAKE_C_COMPILER})'
 / r'set(CMAKE_OBJCOPY      ${TOOLCHAIN_PREFIX}-objcopy)'
 / r'set(CMAKE_SIZE         ${TOOLCHAIN_PREFIX}-size)'
 / r'set(CMAKE_RC_COMPILER  ${TOOLCHAIN_PREFIX}-windres)'
 / ''
 / r'string(TOUPPER ${HW}   HW_  )'
 / r'string(TOUPPER ${CPU}  CPU_ )'
 / r'string(TOUPPER ${ARCH} ARCH_)'
 / r'string(TOUPPER ${OS}   OS_  )'
 / ''
 / (S(None, 'add_compile_options(', ')')
    / r'-Wall -Wextra -Wpedantic'
    / r'$<$<CONFIG:Debug>:-DDEBUG>')
 / ''
 / (S(None, 'add_compile_definitions(', ')')
    / r'${HW_} ${CPU_} ${ARCH_} ${OS_}')
    / ''
    / (S(None, 'add_link_options(', ')')
       / r'-Wl,--print-memory-usage')
 / ''
 / r'if(CMAKE_BUILD_TYPE MATCHES Debug)'
 / r'    add_compile_options(-O0 -g3)'
 / r'endif()'
 / r'if(CMAKE_BUILD_TYPE MATCHES Release)'
 / r'    add_compile_options(-Os -g0)'
 / r'endif()'
 / ''
 / r'set(CMAKE_EXECUTABLE_SUFFIX_ASM ${CMAKE_EXECUTABLE_SUFFIX})'
 / r'set(CMAKE_EXECUTABLE_SUFFIX_C   ${CMAKE_EXECUTABLE_SUFFIX})'
 / r'set(CMAKE_EXECUTABLE_SUFFIX_CXX ${CMAKE_EXECUTABLE_SUFFIX})'

 )

class P(S):
    def __init__(self, var, cmd):
        super().__init__(None, 'execute_process(', ')')
        self.var = var
        (self
         / f'OUTPUT_VARIABLE {var}'
         / f'COMMAND {cmd}'
         / r'WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}'
         / r'OUTPUT_STRIP_TRAILING_WHITESPACE')

version = File('version.cmake'); cmake / version
(version
 / P('REL', 'git rev-parse --short=4 HEAD') / ''
 / P('BRANCH', 'git rev-parse --abbrev-ref HEAD') / ''
 / P('NOW', 'date +%y%m%d # _%H%M') / ''
 / r'set(BIN_OUTPUT_NAME "${CMAKE_PROJECT_NAME}_${HW}_${BRANCH}_${NOW}")')

src = File('src.cmake'); cmake / src

class GLOB(S):
    def __init__(self, name):
        super().__init__(None, f'file(GLOB {name}', ')')
        self / r'RELATIVE ${CMAKE_SOURCE_DIR}'

(src
 / (GLOB('LD') / r'hw/${HW}/*.ld') / ''
 / (GLOB('S') / r'hw/${HW}/*.s') / ''
 / (GLOB('C') / r'src/*.c*') / ''
 / (GLOB('H') / r'inc/*.h*') / ''
 / (GLOB('INC'))
 / r'include_directories(${INC})' / ''
 / (GLOB('L') / r'src/*.lex') / ''
 / (GLOB('Y') / r'src/*.yacc') / ''
 / (GLOB('R') / r'src/*.ragel')
 )

lists = File('CMakeLists.txt')
(lists
 / r'cmake_minimum_required(VERSION 3.22)'
 / r'get_filename_component(CMAKE_PROJECT_NAME ${CMAKE_SOURCE_DIR} NAME_WE)'
 / r'project(${CMAKE_PROJECT_NAME} LANGUAGES C CXX ASM)'
 / ''
 / r'include(version)'
 / r'include(src)'
 / ''
 / r'message("-- |")'
 / r'message("-- | toolchain: " ${CMAKE_CXX_COMPILER} " @ " ${CMAKE_TOOLCHAIN_FILE})'
 / r'message("-- |      host: " ${CMAKE_HOST_SYSTEM_NAME}-${CMAKE_HOST_SYSTEM_VERSION})'
 / r'message("-- |    target: " "hw:" ${HW} " cpu:" ${CPU} " arch:" ${ARCH} " os:" ${OS})'
 / r'message("-- |   startup: " "${S}")'
 / r'message("-- |    binary: " ${CMAKE_INSTALL_PREFIX}/${BIN_OUTPUT_NAME}${CMAKE_EXECUTABLE_SUFFIX})'
 / r'message("-- |")'

 )

cmake.sync()
lists.sync()
