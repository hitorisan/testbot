import pytest
import setting
from setting import *


def test_for_exchange():
    req1 = Exchange(['10', 'USD', 'to', 'EUR'])
    req2 = Exchange(['200', 'Usd', 'to', 'EuR'])
    req3 = Exchange(['UH'])
    req4 = Exchange(['14', 'uah', 'to', 'usd'])

    assert req1.check_for_exchange() == True
    assert req2.check_for_exchange() == True
    assert req3.check_for_exchange() == None
    assert req4.check_for_exchange() == None

    assert req1.convert() == 8.19
    assert req2.convert() == 163.88


def test_for_history():
    req1 = History(['USD/EUR', 'for', '7', 'days'], ['USD', 'EUR'])
    req2 = History(['UsD/EuR', 'for', '8', 'days'], ['UsD', 'EuR'])
    req3 = History(['USD', 'for', '7', 'days'], ['USD', ''])
    req4 = History(['USD/EUR', 'for', '7', 'days'], ['', ''])
    req5 = History(['uah/EuR', 'for', '12', 'days'], ['Uah', 'EuR'])
    req6 = History(['eur/Cad', 'for', '15', 'years'], ['eur', 'Cad'])

    assert req1.check_for_history() == True
    assert req2.check_for_history() == True
    assert req3.check_for_history() == None
    assert req4.check_for_history() == None
    assert req5.check_for_history() == True
    assert req6.check_for_history() == None

    val1 = req1.history()
    val2 = req2.history()
    val5 = req5.history()

    assert len(val1) == 7
    assert len(val2) == 8
    assert len(val5) == 12