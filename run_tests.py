import unittest
import coverage

coverage_tracker = coverage.Coverage()
coverage_tracker.start()

test_suite = unittest.TestLoader().discover('tests')
unittest.TextTestRunner(verbosity=2).run(test_suite)

coverage_tracker.stop()
coverage_tracker.save()

print(coverage_tracker.report())
coverage_tracker.html_report()
