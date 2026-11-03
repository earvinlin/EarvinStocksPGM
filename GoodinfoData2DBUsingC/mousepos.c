/**
 * clang -framework ApplicationServices -o mousepos mousepos.c
 */
#include <ApplicationServices/ApplicationServices.h>
#include <stdio.h>
#include <unistd.h>

int main() {
    while (1) {
        CGEventRef event = CGEventCreate(NULL);
        CGPoint cursor = CGEventGetLocation(event);
        CFRelease(event);

        printf("Mouse position: x=%d, y=%d\n", (int)cursor.x, (int)cursor.y);
        fflush(stdout);

        usleep(500000); // 每 0.5 秒更新一次
    }
    return 0;
}
