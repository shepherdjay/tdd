import inspect

def pytest_namespace():
    """Make unittest assert methods available.
    This is useful for things such floating point checks with assertAlmostEqual.
    """

    from django.test import TestCase

    class Dummy(TestCase):
        def dummy(self):
            pass

    obj = Dummy('dummy')

    names = {name: member
             for name, member in inspect.getmembers(obj)
             if name.startswith('assert') and '_' not in name}

    return names
