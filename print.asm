

;These functions call sys_write in the linux kernel and writes to stdout
;The parameters must be pushed onto the stack prior to the call, in the case
;of print_text, the length of the string must be pushed too

SECTION .data
True: db "True",10
TrueLen: equ $-True
False: db "False",10
FalseLen: equ $-False

SECTION .text
GLOBAL print_number, print_text, print_boolean


negative:
	neg 	eax				; convert to positive
	push 	eax				; save the register
	mov 	eax,  0x2D		; 2d is '-' in ASCII
	push 	eax				; push to get its address
	mov		eax,  esp		; get the address in eax
	call 	print_digit		; print '-'
	add		esp,  4			; pop the '-' from the stack
	pop		eax				; restore the value of eax
	jmp divide_loop			; now go on to print the value
	
print_number:
	push	ebp				; save the previous frame pointer
	mov 	ebp, esp        ; set up the activation record
	mov		eax,  [ebp+8]	; get the parameter to print into eax
    mov     ecx,  0         ; counter of how many bytes we need to print
	test 	eax, eax		; test if value is negative
	js		negative		; jump if signed
 
divide_loop:
    inc     ecx             ; increase counter
    mov     ebx,  0xA       ; move 10 to edx to divide
    mov		edx,  0			; clear edx before the division
    div     ebx	            ; divide eax by ebx
    add     edx,  0x30		; add 30 to the remainder for ASCII
    push    edx             ; push into the stack for later printing
    cmp     eax,  0         ; check if there are more digits
    jnz     divide_loop     ; if we are not done, keep dividing
 
print_loop:
    dec     ecx             ; count down each byte that we put on the stack
    mov     eax,  esp       ; mov the stack pointer into eax for printing
    call    print_digit     ; print this digit
    pop     eax             ; get the next digit to print
    cmp     ecx,  0         ; check if we are done printing
    jnz     print_loop      ; jump if not, keep printing
	mov		eax,  0xA		; add EOL
	push 	eax				; push it to get its address
	lea		eax,  [esp]		; get the address
	call	print_digit		; print the new line
	add		esp,  4			; pop eax
	pop 	ebp				; restore the base pointer
    ret
	
print_digit:
	push 	ecx					; save the value of ecx as it will be overwritten
	mov		ecx,  eax			; get the digit to print into ecx
	mov 	eax,  4				; sys_write
	mov 	ebx,  1				; stdout is fd 1
	mov 	edx,  1 			; print just one byte
	int 	0x80				; call the kernel
	pop		ecx					; restore ecx
	ret
	
print_text:
    push 	ebp
	mov 	ebp,  esp
	mov 	ecx,  [ebp+12]			;get the address of the text to print
	mov 	eax,  4					;sys_write
	mov 	ebx,  1					;1 is fd for stdout
	mov 	edx,  [ebp+8]			;length of the string was pushed last before print was called
	int 	0x80
	pop 	ebp
	ret

print_boolean:
    push    ebp
    mov     ebp,  esp
    mov     eax,  [esp+8]		; get the parameter
	cmp		eax,  0				; check the parameter's value
	je		print_false
	mov 	ecx,  True			; load the address to print
	mov 	eax,  4				; 4 for sys_write
	mov 	ebx,  1				; 1 for stdout
	mov		edx,  TrueLen		; the length in bytes to be printed
	int		0x80
	pop		ebp
	ret

print_false:
	mov 	ecx,  False			; Load the address of the "False" string
	mov 	eax,  4				; 4 for sys_write
	mov 	ebx,  1				; 1 for stdout
	mov 	edx,  FalseLen		; load the length of the "False" string"
	int 	0x80
	pop 	ebp
	ret
    
