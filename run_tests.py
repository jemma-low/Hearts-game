# tests/runner.py
import unittest

# import your test modules
import cards.tests/test_card as test_card

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule())
suite.addTests(loader.loadTestsFromModule(scenario))
suite.addTests(loader.loadTestsFromModule(thing))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)