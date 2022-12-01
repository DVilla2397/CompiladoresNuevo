import pytest

from main import compile
from util.exceptions import *

RES_PATH = '../../resources/semantic/input/{}'


def c(file): compile(RES_PATH.format(file))


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
    with pytest.raises(SelfAssignment):
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