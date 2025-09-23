// 测试程序 - 编译原理课程设计
// 作者: 邵昱铭 孙智博 王宝飞 肖宇航

int main() {
    int a = 10;
    float b = 3.14;
    char c = 'A';
    string message = "Hello World";
    
    if (a > 5) {
        printf("a is greater than 5");
        a = a + 1;
    } else {
        a = a - 1;
    }
    
    while (a < 20) {
        a = a * 2;
        if (a == 16) break;
    }
    
    return 0;
}
