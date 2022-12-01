grammar Mistery;

prog:	class ;

// El esqueleto para declaración de método en Java acepta "public static void main () {}"
// solamente en ese orden, ¿cómo harías para que lo acepte los modificadores en cualquier orden?
// Nota: está bien si se permite 'public public main () {}'

class:	(PUBLIC | STATIC | VOID)* ID '(' ')' '{' '}'
    ;


PUBLIC: 'public';
STATIC: 'static';
VOID: 'void';
ID: Letter LetterOrDigit*;
INTEGER     : [0-9]+ ;
SPACE   : [ ]+ -> skip;

// fragment es para crear segmentos de token que solamente serán usados en este archivo, pero que no
// generan un token. Son como definiciones "locales" a este archivo.

fragment LetterOrDigit
    : Letter
    | [0-9]
    ;

fragment Letter : [a-zA-Z$_] ;