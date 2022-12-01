grammar Mistery;

prog:	class *;

// Para el siguiente ejemplo se desea reconocer los parámetros a un método, por ejemplo:
// main (x, y, z) {}
// donde los parámetros son IDs separados por coma, completa la regla params para reconocer esa sintaxis

class:	ID '(' params ')' '{' '}'
    ;

params:
    ;



PUBLIC: 'public';
STATIC: 'static';
VOID: 'void';
ID: Letter LetterOrDigit*;
INTEGER     : [0-9]+ ;

// fragment es para crear segmentos de token que solamente serán usados en este archivo, pero que no
// generan un token. Son como definiciones "locales" a este archivo.

fragment LetterOrDigit
    : Letter
    | [0-9]
    ;

fragment Letter : [a-zA-Z$_] ;