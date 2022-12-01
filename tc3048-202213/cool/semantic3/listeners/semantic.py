from cool.semantic3.antlr.coolListener import coolListener
from cool.semantic3.antlr.coolParser import coolParser
from cool.semantic3.util.exceptions import *
from cool.semantic3.util.exceptions import BadClassName, MethodDoesNotExist
from cool.semantic3.util.structure import lookupClass, SymbolTableWithScopes


class SemanticListener(coolListener):
    def _init_(self):
        self.main = False
        self.in_while = False
        self.nested_whiles = 0

    def exitAttribute(self, ctx: coolParser.AttributeContext):
        # test_anattributenamedself
        if ctx.ID().getText() == 'self':
            raise BadAttributeName()

        # test_assignmentnoconform

    def enterKlass(self, ctx: coolParser.KlassContext):
        # test_nomain
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True

        # test_badredefineint. test_redefinedobject, test_selftyperedeclared
        if ctx.TYPE(0).getText() in ['Int', 'String', 'Bool', 'SELF_TYPE', 'Object']:
            raise BadClassName()

        # En este momento la clase ya debe estar definida, la tomo de la tabla
        self.klass = lookupClass(ctx.TYPE(0).getText())

        # Crear el scope de variables, se asocia a la klass para buscar también en atributos
        self.scopes = SymbolTableWithScopes(self.klass)

    def enterMethod(self, ctx: coolParser.MethodContext):
        # Abro el scope para variables-parámteros
        self.scopes.openScope()

    def exitMethod(self, ctx: coolParser.MethodContext):
        # Cierro el scope de parámetros
        # print(self.klass.lookupMethod(ctx.expr[0].getText()).params)
        # if self.klass.lookupMethod(ctx.expr[0].getText()).params != self.klass.lookupMethod(
        #         ctx.expr[1].getText()).params:
        #     raise BadType()
        pass

        # test_selftypebadreturn

    def enterFormal(self, ctx: coolParser.FormalContext):
        # test_selfinformalparameter
        if ctx.ID().getText() == 'self':
            raise BadVariableName()

        # test_selftypeparameterposition
        if ctx.TYPE().getText() == 'SELF_TYPE':
            raise BadClassName()

        # test_dupformals
        self.scopes[ctx.ID().getText()] = lookupClass(ctx.TYPE().getText())

    def enterLet(self, ctx: coolParser.LetContext):
        # Abro el scope de variables locales en el let
        self.scopes.openScope()

    def exitLet(self, ctx: coolParser.LetContext):
        # Cierro el scope de variables locales en el let
        # BUG: deberían ir anidadas, pero me parece en esta etapa no hay pruebas así
        # Ejemplo: let x:Int <-5, y:Int <- x in x + y;
        self.scopes.closeScope()

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        # test_letself
        if ctx.ID().getText() == 'self':
            raise BadVariableName()

        self.scopes[ctx.ID().getText()] = lookupClass(ctx.TYPE().getText())

    def exitLet_decl(self, ctx: coolParser.Let_declContext):
        # test_letbadinit
        pass

    def exitProgram(self, ctx: coolParser.ProgramContext):
        # test_nomain
        if not self.main:
            raise NoMain()

    def enterAssign(self, ctx: coolParser.AssignContext):
        # test_selfassignment
        if ctx.ID().getText() == 'self':
            raise SelfAssignment()

    # Base para el algoritmo bottom-up
    def enterInt(self, ctx: coolParser.IntContext):
        ctx.type = lookupClass('Int')

    def exitPri(self, ctx: coolParser.PriContext):
        # ¡Este paso es necesario porque en la gramática hay una regla que consolida todas las literales!
        # Es necesario para darles la misma precedencia
        # Descomentar la siguiente línea una vez que los nodos de la regla primary ya tengan tipo
        # HolaPrueba
        # ctx.type = ctx.primary().type
        pass

    def exitAdd(self, ctx: coolParser.AddContext):
        # test_badarith
        pass

    def exitCall(self, ctx: coolParser.CallContext):
        # test_badmethodcallitself
        # for x, y in zip(self.klass.lookupMethod(ctx.ID.getText()).params, ctx.params):
        #     if len(method.params) != len(ctx.params):
        #         raise BadAttributeName
        pass

    ### BAD WHILE BODY
    def enterWhile(self, ctx):
        self.nested_whiles += 1
        self.in_while = True

    def exitWhile(self, ctx: coolParser.WhileContext):
        self.nested_whiles -= 1
        self.in_while = False if self.nested_whiles < 1 else True

    def exitCallobj(self, ctx: coolParser.CallobjContext):
        # test_baddispatch, test_badwhilebody, test_badargs1
        try:
            try:
                method = ctx.expr(0).type.lookupMethod(ctx.ID().getText())
                ctx.type = method.type
            except KeyError:
                raise MethodDoesNotExist
        except Exception as e:
            if self.in_while:
                raise MethodDoesNotExist
            else:
                raise e

    ### BAD WHILE BODY

    def exitCallstat(self, ctx: coolParser.CallstatContext):
        # test_badstaticdispatch, test_tricyatdispatch2
        pass

    def exitEq(self, ctx: coolParser.EqContext):
        # test_badequalitytest, test_badequalitytest2
        pass

    def exitCase(self, ctx: coolParser.CaseContext):
        # test_caseidenticalbranch
        pass

    def exitVar(self, ctx: coolParser.VarContext):
        # try:
        #     ctx.type = self.scopes(ctx.ID().getText())
        # except KeyError:
        #     raise BadVariableName
        pass

    ### RETURN TYPE NO EXIST
    def exitNew(self, ctx: coolParser.NewContext):
        try:
            lookupClass(ctx.TYPE().getText())
        except KeyError:
            raise BadClassName()

    ### RETURN TYPE NO EXIST
    def exitAssign(self, ctx: coolParser.AssignContext):
        # test_assignoconform
        pass

    def exitIf(self, ctx: coolParser.IfContext):
        # test_lubtest
        pass

    def exitN(self, ctx: coolParser.NewContext):
        try:
            ctx.type = lookupClass(ctx.TYPE().getText())
        except KeyError:
            raise BadVariableName