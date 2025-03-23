#include "metaL.hpp"

int main(int argc, char *argv[]) {
    arg(0, argv[0]);
    for (int i = 1; i < argc; i++) {  //
        arg(i, argv[i]);
    }
}

void arg(int argc, char *argv) {  //
    fprintf(stderr, "argv[%i] = <%s>\n", argc, argv);
}

/// <class:Object>
Object *Object::pool = nullptr;
Object::Object() {  //
    ref = 0;
    prev = pool;
    pool = this;
}
Object::~Object() {  //

}

/// <class:Primitive>
Primitive::Primitive():Object() {  //
}

/// <class:Int>
Int::Int():Primitive() {  //
}

/// <class:Hex>
Hex::Hex():Int() {  //
}

/// <class:Oct>
Oct::Oct():Int() {  //
}

/// <class:Bin>
Bin::Bin():Int() {  //
}

/// <class:Num>
Num::Num():Primitive() {  //
}
