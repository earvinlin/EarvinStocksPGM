#include <X11/Xlib.h>
#include <X11/extensions/XTest.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 移動滑鼠
void move_mouse(Display *d, int x, int y) {
    XWarpPointer(d, None, DefaultRootWindow(d), 0, 0, 0, 0, x, y);
    XFlush(d);
    usleep(50000);
}

// 左鍵點擊
void left_click(Display *d) {
    XTestFakeButtonEvent(d, 1, True, 0);
    XTestFakeButtonEvent(d, 1, False, 0);
    XFlush(d);
    usleep(50000);
}

// 輸入字元（僅支援 0–9）
void type_char(Display *d, char c) {
    if (c < '0' || c > '9') return;

    int keycode = c - '0' + 10; // X11: 0→10, 1→11, ...
    XTestFakeKeyEvent(d, keycode, True, 0);
    XTestFakeKeyEvent(d, keycode, False, 0);
    XFlush(d);
    usleep(30000);
}

// 輸入字串
void type_string(Display *d, const char *s) {
    for (int i = 0; s[i]; i++) {
        type_char(d, s[i]);
    }
}

// 按 Enter
void press_enter(Display *d) {
    int keycode = 36; // Enter
    XTestFakeKeyEvent(d, keycode, True, 0);
    XTestFakeKeyEvent(d, keycode, False, 0);
    XFlush(d);
    usleep(50000);
}

// Goodinfo 自動化流程
void process_stock(Display *d, const char *stock_code) {
    // 你要自己量這些座標
    int STOCK_INPUT_X = 400;
    int STOCK_INPUT_Y = 200;

    int MENU_SALEMON_X = 150;
    int MENU_SALEMON_Y = 400;

    int BTN_20Y_X = 600;
    int BTN_20Y_Y = 250;

    int BTN_XLS_X = 700;
    int BTN_XLS_Y = 250;

    // 點輸入框
    move_mouse(d, STOCK_INPUT_X, STOCK_INPUT_Y);
    left_click(d);

    // 輸入股票代碼
    type_string(d, stock_code);
    press_enter(d);
    sleep(3);

    // 點每月營收
    move_mouse(d, MENU_SALEMON_X, MENU_SALEMON_Y);
    left_click(d);
    sleep(3);

    // 點查20年
    move_mouse(d, BTN_20Y_X, BTN_20Y_Y);
    left_click(d);
    sleep(2);

    // 點 XLS
    move_mouse(d, BTN_XLS_X, BTN_XLS_Y);
    left_click(d);
    sleep(5);
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("用法: %s STOCK_LIST_FILE theDate\n", argv[0]);
        return 1;
    }

    const char *stock_list_file = argv[1];

    // 開啟 Goodinfo
    system("google-chrome 'https://goodinfo.tw/tw/index.asp' &");
    sleep(5);

    Display *d = XOpenDisplay(NULL);
    if (!d) {
        printf("無法開啟 X11 Display\n");
        return 1;
    }

    FILE *fp = fopen(stock_list_file, "r");
    if (!fp) {
        perror("無法開啟股票清單");
        return 1;
    }

    char line[64];
    while (fgets(line, sizeof(line), fp)) {
        line[strcspn(line, "\n")] = 0;
        if (line[0] == '\0') continue;

        printf("處理股票：%s\n", line);
        process_stock(d, line);
    }

    fclose(fp);
    XCloseDisplay(d);
    return 0;
}