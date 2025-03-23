#pragma once

/// @defgroup libc libc
/// @{
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

/// @defgroup main main
/// @{

/// @brief POSIX entry point
extern int main(int argc, char *argv[]);

/// @brief print command line argument
extern void arg(int argc, char *argv);
/// @}
/// @}

/// @defgroup core core
/// @brief executable object graph
/// @{

/// @defgroup gc gc
/// @brief garbage collection
/// @{
/// @}

/// @brief executable object graph root class
class Object {  //
    /// @ingroup gc
    /// @{
    size_t ref;           ///< reference counter
    static Object *pool;  ///< flobal object pool
    Object *prev;         ///< global @ref Object's linked list
    /// @}
};

/// @defgroup prim prim
/// @brief primitive/machine elements
/// @{

/// @brief primitive/machine elements
class Primitive : public Object {  //
};

/// @brief integer
class Int : public Primitive {  //
    int value;
};

/// @brief hexadecimal
class Hex : public Int {  //
};

/// @brief octal
class Oct : public Int {  //
};

/// @brief binary
class Bin : public Int {  //
};

/// @brief floating point
class Num : public Primitive {  //
    float value;
};
/// @}
/// @}
