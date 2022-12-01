import pytest

from main import compile
from main import PATH
from util.exceptions import *
from util.structure import clearAllClasses

RES_PATH = '../../resources/semantic/input/{}'


def c(file): compile(RES_PATH.format(file))

def setup_function():
    clearAllClasses()

def test_anattributenamedself():
    with pytest.raises(BadAttributeName):
        c('anattributenamedself.cool')


def test_badredefineint():
    with pytest.raises(BadClassName):
        c('badredefineint.cool')


def test_inheritsbool():
    with pytest.raises(InvalidInheritance):
        c('inheritsbool.cool')


def test_inheritsselftype():
    with pytest.raises(InvalidInheritance):
        c('inheritsselftype.cool')


def test_inheritsstring():
    with pytest.raises(InvalidInheritance):
        c('inheritsstring.cool')


def test_letself():
    with pytest.raises(BadVariableName):
        c('letself.cool')


def test_nomain():
    with pytest.raises(NoMain):
        c('nomain.cool')


def test_redefinedobject():
    with pytest.raises(BadClassName):
        c('redefinedobject.cool')


def test_selfassignment():
    with pytest.raises(BadVariableName):
        c('self-assignment.cool')


def test_selfinformalparameter():
    with pytest.raises(BadVariableName):
        c('selfinformalparameter.cool')


def test_selftypeparameterposition():
    with pytest.raises(BadClassName):
        c('selftypeparameterposition.cool')


def test_selftyperedeclared():
    with pytest.raises(BadClassName):
        c('selftyperedeclared.cool')


def test_badarith():
    with pytest.raises(BadOperands):
        c('badarith.cool')

def test_baddispatch():
    with pytest.raises(MethodDoesNotExist):
        c('baddispatch.cool')

def test_badequalitytest():
    with pytest.raises(BadOperands):
        c('badequalitytest.cool')

def test_badequalitytest2():
    with pytest.raises(BadOperands):
        c('badequalitytest2.cool')

def test_badwhilebody():
    with pytest.raises(MethodDoesNotExist):
        c('badwhilebody.cool')

def test_badwhilecond():
    with pytest.raises(BadType):
        c('badwhilecond.cool')

def test_caseidenticalbranch():
    with pytest.raises(CaseIdenticalBranch):
        c('caseidenticalbranch.cool')

def test_missingclass():
    with pytest.raises(BadClassName):
        c('missingclass.cool')

def test_outofscope():
    with pytest.raises(BadVariableName):
        c('outofscope.cool')

def test_redefinedclass():
    with pytest.raises(BadClassName):
        c('redefinedclass.cool')

def test_returntypenoexist():
    with pytest.raises(BadClassName):
        c('returntypenoexist.cool')

def test_selftypebadreturn():
    with pytest.raises(SelftypeBadReturn):
        c('selftypebadreturn.cool')

def test_assignnoconform():
    with pytest.raises(BadType):
        c('assignnoconform.cool')

def test_attrbadinit():
    with pytest.raises(BadVariableName):
        c('attrbadinit.cool')

def test_attroverride():
    with pytest.raises(InvalidOverride):
        c('attroverride.cool')

def test_badargs1():
    with pytest.raises(BadType):
        c('badargs1.cool')

def test_badmethodcallsitself():
    with pytest.raises(BadType):
        c('badmethodcallsitself.cool')

def test_badstaticdispatch():
    with pytest.raises(InvalidDispatch):
        c('badstaticdispatch.cool')

def test_dupformals():
    with pytest.raises(BadVariableName):
        c('dupformals.cool')

def test_letbadinit():
    with pytest.raises(BadType):
        c('letbadinit.cool')

def test_lubtest():
    with pytest.raises(BadType):
        c('lubtest.cool')

def test_overridingmethod4():
    with pytest.raises(InvalidOverride):
        c('overridingmethod4.cool')

def test_signaturechange():
    with pytest.raises(InvalidOverride):
        c('signaturechange.cool')

def test_trickyatdispatch2():
    with pytest.raises(MethodDoesNotExist):
        c('trickyatdispatch2.cool')
