from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser


class SemanticListener(coolListener):
    def __init__(self):
        self.main = False

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
