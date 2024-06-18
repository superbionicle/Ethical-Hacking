section .text
  global _start
    _start:
      ; Store the argument string on stack
      xor  eax, eax 
      push eax          ; Use 0 to terminate the string
      push "/env"
      push "/bin"
      push "/usr"
      mov  ebx, esp     ; Get the string address

      ; Construct the argument array argv[]
      push eax          ; argv[1] = 0
      push ebx          ; argv[0] = "/usr/bin/env"
      mov  ecx, esp     ; Get the address of argv[]
   
      ; For environment variable 
      push eax
      push "1234"
      push "aaa="
      mov  edx, esp     ; Get the string address
      
      push eax
      push "5678"
      push "bbb="
      mov  esi, esp     ; Get the string address
      
      push eax
      mov edi, "4###"
      shl edi, 24
      shr edi, 24
      push edi
      push "=123"
      push "cccc"
      mov edi, esp
      
      ; Construct the argument array env[]
      push eax          ; env[3] = 0
      push edx		; env[2] = "aaa=1234"
      push esi		; env[1] = "bbb=5678"
      push edi          ; env[0] = "cccc=1234"
      mov  edx, esp     ; Get the address of env[]

      ; Invoke execve()
      xor  eax, eax     ; eax = 0x00000000
      mov   al, 0x0b    ; eax = 0x0000000b
      int 0x80
