/**
 * clang -framework ApplicationServices -o goodinfo_mac goodinfo_mac.c
 */
#include <ApplicationServices/ApplicationServices.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 移動滑鼠
void move_mouse(int x, int y) {
    CGEventRef move = CGEventCreateMouseEvent(NULL, kCGEventMouseMoved,
                                              CGPointMake(x, y),
                                              kCGMouseButtonLeft);
    CGEventPost(kCGHIDEventTap, move);
    CFRelease(move);
    usleep(50000);
}

// 左鍵點擊
void left_click(int x, int y) {
    CGEventRef click_down = CGEventCreateMouseEvent(NULL, kCGEventLeftMouseDown,
                                                    CGPointMake(x, y),
                                                    kCGMouseButtonLeft);
    CGEventRef click_up = CGEventCreateMouseEvent(NULL, kCGEventLeftMouseUp,
                                                  CGPointMake(x, y),
                                                  kCGMouseButtonLeft);
    CGEventPost(kCGHIDEventTap, click_down);
    CGEventPost(kCGHIDEventTap, click_up);
    CFRelease(click_down);
    CFRelease(click_up);
    usleep(50000);
}

// 輸入字元（僅支援 0–9）
void type_char(char c) {
    if (c < '0' || c > '9') return;

    UniChar uc = c;
    CGEventRef key_down = CGEventCreateKeyboardEvent(NULL, 0, true);
    CGEventRef key_up   = CGEventCreateKeyboardEvent(NULL, 0, false);

    // 設定輸入字元
    CGEventKeyboardSetUnicodeString(key_down, 1, &uc);
    CGEventKeyboardSetUnicodeString(key_up, 1, &uc);

    CGEventPost(kCGHIDEventTap, key_down);
    CGEventPost(kCGHIDEventTap, key_up);

    CFRelease(key_down);
    CFRelease(key_up);
    usleep(30000);
}

// 輸入字串
void type_string(const char *s) {
    for (int i = 0; s[i]; i++) {
        type_char(s[i]);
    }
}

// 按 Enter
void press_enter() {
    CGEventRef key_down = CGEventCreateKeyboardEvent(NULL, (CGKeyCode)36, true);
    CGEventRef key_up   = CGEventCreateKeyboardEvent(NULL, (CGKeyCode)36, false);
    CGEventPost(kCGHIDEventTap, key_down);
    CGEventPost(kCGHIDEventTap, key_up);
    CFRelease(key_down);
    CFRelease(key_up);
    usleep(50000);
}

// Goodinfo 自動化流程
void process_stock(const char *stock_code) {
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
    move_mouse(STOCK_INPUT_X, STOCK_INPUT_Y);
    left_click(STOCK_INPUT_X, STOCK_INPUT_Y);

    // 輸入股票代碼
    type_string(stock_code);
    press_enter();
    sleep(3);

    // 點每月營收
    move_mouse(MENU_SALEMON_X, MENU_SALEMON_Y);
    left_click(MENU_SALEMON_X, MENU_SALEMON_Y);
    sleep(3);

    // 點查20年
    move_mouse(BTN_20Y_X, BTN_20Y_Y);
    left_click(BTN_20Y_X, BTN_20Y_Y);
    sleep(2);

    // 點 XLS
    move_mouse(BTN_XLS_X, BTN_XLS_Y);
    left_click(BTN_XLS_X, BTN_XLS_Y);
    sleep(5);
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("用法: %s STOCK_LIST_FILE theDate\n", argv[0]);
        return 1;
    }

    const char *stock_list_file = argv[1];

    // 開啟 Goodinfo
    system("open -a 'Google Chrome' 'https://goodinfo.tw/tw/index.asp'");
    sleep(5);

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
        process_stock(line);
    }

    fclose(fp);
    return 0;
}
