;These functions call sys_write in the linux kernel and writes to stdout

PrintNumber:
	push ebp
	mov ebp,  esp
	mov ecx,  [ebp+8]			;get the parameter to print into ecx
	add ecx,  0x30				;add 30H for ASCII
	mov ch,   0xA				;move 10 (EOL) into the second byte to create a new line
	mov eax,  4					;sys_write
	mov ebx,  1					;stdout is fd 1
	mov edx,  2					;print two bytes (number plus EOL)
	int 0x80					;call the kernel
	pop ebp
	ret

PrintText:
	push ebp
	mov ebp,  esp
	mov ecx,  [ebp+12]			;get the address of the text to print
	mov eax,  4					;sys_write
	mov ebx,  1					;1 is fd for stdout
	mov edx,  [ebp+8]			;length of the string was pushed last before print was called
	int 0x80
	pop ebp
	ret
