#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
void check(int depth) {
    char c;
    char *ptr = malloc(1);
    printf("stack at %p, heap at %p\n", &c, ptr);
	void f() {
		printf ("called\n");
	}
    if (depth <= 0) return;
    check(depth-1);
}

int main() {
	int x = 5;
    check(10);
	f();
    return 0;
}
