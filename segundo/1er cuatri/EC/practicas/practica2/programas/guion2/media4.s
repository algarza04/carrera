.section .data

#ifndef TEST
#define TEST 20
#endif
    # doble macro: lista definida por una linea0 y 3 lineas normales
    # mayoría ejemplos linea0 = linea => lista tiene 4 lineas normales
    .macro linea        # Media / Resto - Comentario

#if TEST==1     //1 / 8
    .int 1, 2, 1, 2
#elif TEST==2   //-1 /-8
    .int -1,-2,-1,-2
#elif TEST==3   //
    .int 0x7fffffff,0x7fffffff,0x7fffffff,0x7fffffff
#elif TEST==4   //
    .int 0x80000000,0x80000000,0x80000000,0x80000000
#elif TEST==5   //
    .int 0xffffffff,0xffffffff,0xffffffff,0xffffffff
#elif TEST==6   //
    .int 2000000000,2000000000,2000000000,2000000000
#elif TEST==7   //
    .int 3000000000,3000000000,3000000000,3000000000
#elif TEST==8   //
    .int -2000000000,-2000000000,-2000000000,-2000000000
#elif TEST==9   //
    .int -3000000000,-3000000000,-3000000000,-3000000000
#elif TEST>=10 && TEST<=14
    .int 1, 1, 1, 1     # linea0 + 3lineas, casi todo a 1
#elif TEST>=15 && TEST<=19
    .int -1,-1,-1,-1        # linea0 + 3lineas, casi todo -1
#else
    .error "Definir TEST entre 1..19"
#endif
    .endm

    # mayoría ejemplos linea0 = linea => lista tiene 4 lineas normales
    
    .macro linea0   # Media / Resto - Comentario
#if TEST>=1 && TEST<=9
    linea       # casi siempre 4 lineas iguales
#elif TEST==10      //1 / 0 - equiv toda lista 1
    .int 0, 2, 1, 1
#elif TEST==11  //
    .int 1, 2, 1, 1
#elif TEST==12  //
    .int 8, 2, 1, 1
#elif TEST==13  //  //
    .int 15,2,1,1
#elif TEST==14  //  //  //
    .int 16,2,1,1
#elif TEST==15  // -1 / 0 - equiv TEST05
    .int 0,-2,-1,-1
#elif TEST==16  //
    .int -1,-2,-1,-1
#elif TEST==17  //
    .int -8,-2,-1,-1
#elif TEST==18  //
    .int -15,-2,-1,-1
#elif TEST==19 //? / ?
    .int -16,-2,-1,-1
#else  
    .error "Definir TEST entre 1..19"
#endif
    .endm
# mayoría ejemplos linea0 = linea => lista tiene 4 lineas normales
lista:  linea0
    .irpc i,123
        linea
    .endr

longlista:	.int   (.-lista)/4
media:	.int   0
resto:	.int   0

formato: .ascii "media \t = %11d \t resto \t = %11d \n"
.asciz "\t = 0x %08x \t \t = 0x %08x\n"

# gcc media4.s -o media4 -no-pie -nostartfiles
# for i in $(seq 1 19); do gcc -x assembler-with-cpp -D TEST=$i -no-pie -nostartfiles media4.s -o media4; printf "__TEST%02d__%35s\n" $i "" | tr " " "-" ; ./media4 ; done

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
	mov  %eax, media
    mov  %edx, resto
	ret

suma:
	mov  $0, %eax
	mov  $0, %rsi
	mov  $0, %edx
    mov  $0, %r8d
    mov  $0, %r9d
	
bucle:
	mov  (%rbx,%rsi,4), %eax
    cltd
	add %eax, %r8d
    adc %edx, %r9d
    inc %rsi
    cmp %rsi,%rcx
	jne bucle
    mov %r8d, %eax
    mov %r9d, %edx
    idiv %ecx
    ret

imprim_C:			# requiere libC
	mov   $formato, %rdi
	mov   media,%rsi
	mov   resto,%rdx
    mov media, %rcx
    mov resto, %r8
	mov          $0,%eax	# varargin sin xmm
	call  printf		# == printf(formato, res, res);
	ret

acabar_C:			# requiere libC
	mov  media, %edi
	call _exit		# ==  exit(resultado)
	ret

