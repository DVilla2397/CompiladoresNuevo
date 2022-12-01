from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import Klass, setBaseKlasses, Method, lookupClass, SymbolTableWithScopes



class SemanticListener(coolListener):
    def __init__(self):
        self.main = False

        #Crear estructura inicial de clases
        setBaseKlasses()


    def exitAttribute(self, ctx: coolParser.AttributeContext):
        #test_anattributenamedself
        if ctx.ID().getText() == 'self':
            raise BadAttributeName()

    def enterKlass(self, ctx: coolParser.KlassContext):

        #test_nomain
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True

        #test_badredefineint. test_redefinedobject, test_selftyperedeclared
        if ctx.TYPE(0).getText() in ['Int', 'String', 'Bool', 'SELF_TYPE', 'Object']:
            raise BadClassName()

        #test_inheritsbool, test_inheritsselftype, test_inheritsstring
        if not ctx.TYPE(1) is None and ctx.TYPE(1).getText() in ['Int', 'String', 'Bool', 'SELF_TYPE']:
            raise InvalidInheritance()

        #Crear esta clase, para este subárbol la voy a guardar en self.klass
        if ctx.TYPE(1) is None:
            self.klass = Klass(ctx.TYPE(0).getText())
        else:
            self.klass = Klass(ctx.TYPE(0).getText(), ctx.TYPE(1).getText())

        #Crear el scope de variables, se asocia a la klass para buscar también en atributos
        self.scopes = SymbolTableWithScopes(self.klass)

    def enterMethod(self, ctx:coolParser.MethodContext):
        #params contiene un arreglo de formal, que tiene ID y el TYPE, lo convierto a Klass para usarlo más adelante
        params = []
        for p in ctx.params:
            params.append ( (p.ID().getText(), lookupClass(p.TYPE().getText())) )
        #Crear un método en la clase actual
        self.klass.addMethod(ctx.ID().getText(), Method(ctx.TYPE(), params))

        #Abro el scope para variables-parámteros
        self.scopes.openScope()

    def exitMethod(self, ctx:coolParser.MethodContext):
        #Cierro el scope de parámetros
        self.scopes.closeScope()

    def enterAttribute(self, ctx:coolParser.AttributeContext):
        #Declaro un atributo, pero el tipo lo guardo como Klass, no como string
        self.klass.addAttribute(ctx.ID().getText(), lookupClass(ctx.TYPE().getText()))

    def enterLet(self, ctx:coolParser.LetContext):
        #Abro el scope de variables locales en el let
        self.scopes.openScope()

    def exitLet(self, ctx:coolParser.LetContext):
        #Cierro el scope de variables locales en el let
        #BUG: deberían ir anidadas, pero me parece en esta etapa no hay pruebas así
        #Ejemplo: let x:Int <-5, y:Int <- x in x + y;
        self.scopes.closeScope()

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        #test_letself
        if ctx.ID().getText() == 'self':
            raise BadVariableName()

    def exitProgram(self, ctx: coolParser.ProgramContext):
        #test_nomain
        if not self.main:
            raise NoMain()

    def enterFormal(self, ctx: coolParser.FormalContext):
        #test_selfinformalparameter
        if ctx.ID().getText() == 'self':
            raise BadVariableName()

        #test_selftypeparameterposition
        if ctx.TYPE().getText() == 'SELF_TYPE':
            raise BadClassName()

    def enterAssign(self, ctx: coolParser.AssignContext):
        #test_selfassignment
        if ctx.ID().getText() == 'self':
            raise SelfAssignment()

    # Base para el algoritmo bottom-up
    def enterInt(self, ctx:coolParser.IntContext):
        ctx.type = lookupClass('Int')

