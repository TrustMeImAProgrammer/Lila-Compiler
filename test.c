#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
void check(int depth) {
    char c;
    char *ptr = malloc(1);
    printf("stack at %p, heap at %p\n", &c, ptr);
    if (depth <= 0) return;
    check(depth-1);
}

int func(){
	return 1;
}
int main() {
	double x = 5.3;
//    check(10);
	printf ("%f\n", x);
	x++;
	printf ("%f\n", x);
    return 0;
}

int t{
	return 4;
}













