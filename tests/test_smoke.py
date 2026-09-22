import sirenas
import sirenas.core
import sirenas.model
import sirenas.data
import sirenas.catalogs


def test_import_sirenas_and_subpackages():
    assert sirenas
    assert sirenas.core
    assert sirenas.model
    assert sirenas.data
    assert sirenas.catalogs
