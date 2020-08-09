import unittest
import warnings

# local file imports
from PythonHelpers.custom_exceptions import TooDirtyException, NotImplementedException
from PythonHelpers.method_decorators import overrides, deprecated, needs_refactoring, dirty, timer, count_calls, \
    unimplemented, validate_args, require_not_none, require_not_empty_strings


class TestSmallDecoratorMethods(unittest.TestCase):

    def test_overrides(self):
        """Problem here: parent has no such method"""
        class A:
            pass

        with self.assertRaises(expected_exception=AssertionError):
            class B(A):
                @overrides(A)
                def operation(self):
                    return 42

    def test_overrides_corrected(self):
        class A:
            def operation(self):
                pass

        class B(A):
            @overrides(A)
            def operation(self):
                return 42

        b = B()
        b.operation()

    def test_overrides_static_method(self):
        """Problem here: Static methods cannot be overwritten"""

        class A:
            @staticmethod
            def operation():
                pass

        with self.assertRaises(expected_exception=AssertionError):
            class B(A):

                @staticmethod
                @overrides(A)
                def operation():
                    return 42

    def test_deprecated_1(self):
        @deprecated
        def old_method(i: int) -> str:
            return str(i)

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            old_method(42)
            # Verify some things
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "deprecated" in str(w[-1].message)

    def test_deprecated_2(self):
        def old_method(i: int) -> str:
            return str(i)

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            old_method(42)
            # Verify some things
            assert not len(w) == 1

    def test_needs_refactoring_1(self):
        @needs_refactoring
        def old_method(i: int) -> str:
            return str(i)

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            old_method(42)
            # Verify some things
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "refactoring" in str(w[-1].message)

    def test_needs_refactoring_2(self):
        def old_method(i: int) -> str:
            return str(i)

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            old_method(42)
            # Verify some things
            assert not len(w) == 1

    def test_dirty(self):
        @dirty
        def dirt(i: int) -> str:
            return str(i)

        with self.assertRaises(expected_exception=TooDirtyException):
            dirt(42)

    def test_unimplemented(self):
        @unimplemented
        def dirt(i: int) -> str:
            return str(i)

        with self.assertRaises(expected_exception=NotImplementedException):
            dirt(42)

    def test_timer(self):
        @timer
        def operation(i: int) -> str:
            return str(i)

        operation(42)

    def test_count_calls(self):
        @count_calls
        def operation(i: int) -> str:
            return str(i)

        operation(42)

    def test_validate_args(self):
        @validate_args(lambda x: (x > 42, f'Each arg should be > 42, but it was {x}.'))
        def some_calculation(a, b, c):
            return a + b + c

        some_calculation(43, 45, 50)
        with self.assertRaises(expected_exception=AssertionError):
            some_calculation(30, 40, 50)
        with self.assertRaises(expected_exception=AssertionError):
            some_calculation(c=30, a=40, b=50)

    def test_require_not_none(self):
        @require_not_none
        def some_calculation(a, b, c):
            return a + b + c

        some_calculation(43, 0, -50)
        with self.assertRaises(expected_exception=AssertionError):
            some_calculation(30, None, 50)

    def test_require_not_empty_strings(self):
        @require_not_empty_strings
        def some_calculation(a, b, c):
            return a + b + c

        some_calculation('Hello ', 'W', 'orld   !')
        with self.assertRaises(expected_exception=AssertionError):
            some_calculation('Hello', '   ', 'World')
        with self.assertRaises(expected_exception=AssertionError):
            some_calculation('Hello', 4, 'World')
        with self.assertRaises(expected_exception=AssertionError):
            some_calculation('Hello', '4', None)

