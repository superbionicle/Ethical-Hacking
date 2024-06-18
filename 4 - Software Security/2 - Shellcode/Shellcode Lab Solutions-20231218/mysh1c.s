section .text
  global _start
    _start:
      ; Store the argument string on stack
      xor  eax, eax 
      push eax          ; Use 0 to terminate the string
      push "//sh"
      push "/bin"
      mov  ebx, esp     ; Get the string address
      
      push eax
      mov ecx, "la##" 	; argv[2] = "ls -la"
      shl ecx, 16
      shr ecx, 16
      push ecx
      push "ls -"
      mov  ecx, esp     ; Get the string address
      
      push eax
      mov edx, "-c##" 	; argv[1] = "-c"
      shl edx, 16
      shr edx, 16
      push edx
      mov  edx, esp     ; Get the string address
      
      ; Construct the argument array argv[]
      push eax          ; argv[3] = 0
      push ecx		; argv[2] = "ls -la"
      push edx		; argv[1] = "-c"
      push ebx          ; argv[0] = "/bin//sh"
      mov  ecx, esp     ; Get the address of argv[]
   
      ; For environment variable 
      xor  edx, edx     ; No env variables 

      ; Invoke execve()
      xor  eax, eax     ; eax = 0x00000000
      mov   al, 0x0b    ; eax = 0x0000000b
      int 0x80
