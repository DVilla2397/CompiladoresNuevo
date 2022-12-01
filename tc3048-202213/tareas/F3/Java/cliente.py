# En esta tarea comenzaremos a trabajar con el API de ANTLR para Python3. Toma como modelo el ejemplo de HTML.

# 1. Descarga la gramática de Java del repositorio público de ANTLR, son dos archivos y guárdalos en el
#    directorio antlr
#    https://github.com/antlr/grammars-v4
# 2. Configura la generación de código.
# 3. Prueba un programa sencillo de Java usando el ANTLR preview.

# 4. Resuelve las siguientes tareas:
#     1. Imprimir los nombres de todas las clases
#     2. Imprimir los nombres y tipos de todos los métodos
#     3. Imprimir todos los strings

# Puedes hacer 1 solo listener e ir guardando en una lista lo que vayas encontrando, para al final imprimirlo,
# o bien hacer 3 listeners y mandarlos llamar uno tras otro con el objeto walker.

from antlr4 import *
from antlr.JavaParserListener import JavaParserListener
from antlr.JavaLexer import JavaLexer
from antlr.JavaParser import JavaParser
import sys

from antlr4 import *
from antlr.JavaParserListener import JavaParserListener
from antlr.JavaLexer import JavaLexer
from antlr.JavaParser import JavaParser
import sys


class TreePrinter(JavaParserListener):
    def enterClass(self, ctx:JavaParser.ClassDeclarationContext):

        print(ctx.identifier().getText())

class TreePrinter2(JavaParserListener):
    def enterMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):
        print("Tipo: " + ctx.typeTypeOrVoid().getText() + "Identificador: " + ctx.identifier().getText())

class TreePrinter3(JavaParserListener):
    def enterStrL(self, ctx: JavaParser.StrLContext):
        print("Todos los Strings:" + ctx.getText())
def main(argv):
    parser = JavaParser(CommonTokenStream(JavaLexer(FileStream("test.java"))))
    tree = parser.compilationUnit()

    print(tree)

    walker = ParseTreeWalker()
    walker.walk(TreePrinter(), tree)

    walker2 = ParseTreeWalker()
    walker2.walk(TreePrinter2(), tree)

    walker3 = ParseTreeWalker()
    walker3.walk(TreePrinter3(), tree)


if __name__ == '__main__':
    main("test.java")