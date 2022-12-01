from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser
from util.structure import lookupClass, SymbolTableWithScopes, SymbolTable


class SemanticListener(coolListener):
    def __init__(self):
        self.main = False

    def exitAttribute(self, ctx: coolParser.AttributeContext):
        #test_anattributenamedself
        if ctx.ID().getText() == 'self':
            raise BadAttributeName()

        #test_assignmentnoconform

    def enterKlass(self, ctx: coolParser.KlassContext):
        #test_nomain
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True

        #test_badredefineint. test_redefinedobject, test_selftyperedeclared
        if ctx.TYPE(0).getText() in ['Int', 'String', 'Bool', 'SELF_TYPE', 'Object']:
            raise BadClassName()

        #En este momento la clase ya debe estar definida, la tomo de la tabla
        self.klass = lookupClass(ctx.TYPE(0).getText())

        #Crear el scope de variables, se asocia a la klass para buscar también en atributos
        self.scopes = SymbolTableWithScopes(self.klass)

    def enterMethod(self, ctx:coolParser.MethodContext):
        #Abro el scope para variables-parámteros
        self.scopes.openScope()

    def exitMethod(self, ctx:coolParser.MethodContext):
        #Cierro el scope de parámetros
        self.scopes.closeScope()

        #test_selftypebadreturn

    def enterFormal(self, ctx: coolParser.FormalContext):
        #test_selfinformalparameter
        if ctx.ID().getText() == 'self':
            raise BadVariableName()

        #test_selftypeparameterposition
        if ctx.TYPE().getText() == 'SELF_TYPE':
            raise BadClassName()

        #test_dupformals
        self.scopes[ctx.ID().getText()] = lookupClass(ctx.TYPE().getText())

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

        self.scopes[ctx.ID().getText()] = lookupClass(ctx.TYPE().getText())

    def exitLet_decl(self, ctx:coolParser.Let_declContext):
        #test_letbadinit
        pass

    def exitProgram(self, ctx: coolParser.ProgramContext):
        #test_nomain
        if not self.main:
            raise NoMain()

    def enterAssign(self, ctx: coolParser.AssignContext):
        #test_selfassignment
        if ctx.ID().getText() == 'self':
            raise SelfAssignment()

    # Base para el algoritmo bottom-up
    def enterInt(self, ctx:coolParser.IntContext):
        ctx.type = lookupClass('Int')

    def enterStr(self, ctx:coolParser.StrContext):
        ctx.type = lookupClass('String')

    def enterBool(self, ctx:coolParser.BoolContext):
        ctx.type = lookupClass('Bool')

    def enterParens(self, ctx:coolParser.ParensContext):
        ctx.type = ctx.expr().type

    def exitPri(self, ctx:coolParser.PriContext):
        #¡Este paso es necesario porque en la gramática hay una regla que consolida todas las literales!
        #Es necesario para darles la misma precedencia
        #Descomentar la siguiente línea una vez que los nodos de la regla primary ya tengan tipo
        ctx.type = ctx.primary().type


    def exitAdd(self, ctx:coolParser.AddContext):
        #test_badarith
        if not (ctx.expr(0).type.name == 'Integer' and ctx.expr(1).type.name == 'Integer'):
            raise BadOperands
        ctx.type = lookupClass('Integer')

    def exitCall(self, ctx:coolParser.CallContext):
        #test_badmethodcallitself
        pass

    def exitCallobj(self, ctx:coolParser.CallobjContext):
        #test_baddispatch, test_badwhilebody, test_badargs1
        try:
            method = ctx.expr(0).type.lookupMethod(ctx.ID().getText())
            ctx.type = method.type
        except KeyError:
            raise MethodDoesNotExist

    def exitCallstat(self, ctx:coolParser.CallstatContext):
        #test_badstaticdispatch, test_tricyatdispatch2
        pass

    def exitEq(self, ctx:coolParser.EqContext):
        #test_badequalitytest, test_badequalitytest2
        if ctx.expr(0).type.name in ['Int', 'Bool', 'String'] and ctx.expr(0).type != ctx.expr(1).type:
            raise BadOperands
        ctx.type = lookupClass('Bool')

    def exitWhile(self, ctx:coolParser.WhileContext):
        #test_badwhilecond
        if ctx.expr(0).type.name != 'Bool':
            raise BadType
        ctx.type = lookupClass('Object')

    def enterCase_stat(self, ctx:coolParser.Case_statContext):
        self.scopes.openScope()
        self.scopes[ctx.ID().getText()] = lookupClass(ctx.TYPE().getText())

    def exitCase_stat(self, ctx:coolParser.Case_statContext):
        self.scopes.closeScope()

    def exitCase(self, ctx:coolParser.CaseContext):
        #test_caseidenticalbranch
        local = SymbolTable()
        try:
            for caso in ctx.case_stat():
                local[caso.TYPE().getText()] = caso.ID().getText()
        except KeyError:
            raise CaseIdenticalBranch

    def exitVar(self, ctx:coolParser.VarContext):
        #test_outofscope
        try:
            ctx.type = self.scopes[ctx.ID().getText()]
        except KeyError:
            raise BadVariableName

    def exitNew(self, ctx:coolParser.NewContext):
        #test_returntypenoexist
        try:
            self.type = lookupClass(ctx.TYPE().getText())
        except KeyError:
            raise BadClassName

    def exitAssign(self, ctx:coolParser.AssignContext):
        #test_assignoconform
        pass

    def exitIf(self, ctx:coolParser.IfContext):
        #test_lubtest
        pass