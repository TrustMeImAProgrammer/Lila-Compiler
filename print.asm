

;These functions call sys_write in the linux kernel and writes to stdout
;The parameters must be pushed onto the stack prior to the call, in the case
;of print_text, the length of the string must be pushed too
GLOBAL print_number, print_text

print_number:
	push ebp
	mov ebp,  esp
	mov eax,  [ebp+8]			;get the parameter to print into a temp register
	add eax,  0x30				;add 30H for ASCII
	mov ah,   0xA				;move 10 (EOL) into the second byte to create a new line
	push eax					;save the value to be printed onto the stack
	mov ecx,  esp				;copy the stack buffer into ecx to pass it to sys_write
	mov eax,  4					;sys_write
	mov ebx,  1					;stdout is fd 1
	mov edx,  2					;print two bytes (number plus EOL)
	int 0x80					;call the kernel
	add esp,  4					;pop the stack buffer
	pop ebp
	ret
print_text:
    push ebp
	mov ebp,  esp
	mov ecx,  [ebp+12]			;get the address of the text to print
	mov eax,  4					;sys_write
	mov ebx,  1					;1 is fd for stdout
	mov edx,  [ebp+8]			;length of the string was pushed last before print was called
	int 0x80
	pop ebp
	ret
