.section .data
    .macro linea
        .int 1,1,1,1
        #.int 0x0fffffff,0x0fffffff,0x0fffffff,0x0fffffff
        #.int 0x10000000,0x10000000,0x10000000,0x10000000
        #.int -1, -1, -1, -1
        #.int 0xffffffff,0xffffffff,0xffffffff,0xffffffff
        #.int -100000000, -100000000, -100000000, -100000000
        #.int -200000000, -200000000, -200000000, -200000000
        #.int -300000000, -300000000, -300000000, -300000000
        #.int -2000000000, -2000000000, -2000000000, -2000000000
    .endm
lista: .irpc i,1234
        linea
    .endr
longlista:	.int   (.-lista)/4
resultado:	.quad   0
  formato: 	.asciz	"suma = %ld = 0x%lx hex\n" 

# 3) gcc media3.s -o media3 -no-pie -nostartfiles		6544 B

.section .text

_start: .global _start

main: .global  main
	call trabajar	# subrutina de usuario
	call imprim_C	# printf()  de libC
	call acabar_C	# exit()    de libC
	ret

trabajar:
	mov     $lista, %rbx
	mov  longlista, %ecx
	call suma		# == suma(&lista, longlista);
	mov  %r8d, resultado
	mov %r9d, resultado+4
	ret

suma:
	mov  $0, %eax
	mov  $0, %rsi
	mov  $0, %edx
    mov  $0, %r8d
    mov  $0, %r9d
	
bucle:
	mov  (%rbx,%rsi,4), %eax
    cltd    #Convert Long to Double, sirve para extender el signo de eax a edx:eax
	add %eax, %r8d
    adc %edx, %r9d
    inc %rsi
    cmp %rsi,%rcx
	jne bucle
    ret

imprim_C:			# requiere libC
	mov   $formato, %rdi
	mov   resultado,%rsi
	mov   resultado,%rdx
	mov          $0,%eax	# varargin sin xmm
	call  printf		# == printf(formato, res, res);
	ret

acabar_C:			# requiere libC
	mov  resultado, %edi
	call _exit		# ==  exit(resultado)
	ret

