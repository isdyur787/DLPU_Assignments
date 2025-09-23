#include <stdio.h>

int main() {
    int a = 100;
    float b = 3.14;
    char c = 'ABC';
    string str = "C语言文件测试";
    
    if (a >= 50) {
        printf("a 大于等于 50");
        a = a + 1;
    } else {
        a = a - 1;
    }
    
    while (a < 20) {
        a = a * 2;
        if (a == 16) break;
    }
}