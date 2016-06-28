#include <stdlib.h>
#include <stdio.h>
#include<errno.h>
void check(int depth) {
    char c;
    char *ptr = malloc(1);
    printf("stack at %p, heap at %p\n", &c, ptr);
    if (depth <= 0) return;
    check(depth-1);
}

int main() {
    check(10);
	char* p = malloc(1000);
	char v = "helo"; //integer from pointer without a cast
    return 0;
}
