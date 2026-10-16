import unittest

from robot.api.types import Secret
from robot.libraries import Process
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.libraries.DateTime import Date
from robot.libraries.Process import ProcessConfiguration
from robot.utils.asserts import (
    assert_equal, assert_false, assert_raises_with_msg, assert_true
)


class TestBuiltInWhenRobotNotRunning(unittest.TestCase):

    def test_using_namespace(self):
        assert_raises_with_msg(
            RobotNotRunningError,
            "Cannot access execution context",
            BuiltIn().get_variables,
        )

    def test_using_namespace_backwards_compatibility(self):
        assert_raises_with_msg(
            AttributeError,
            "Cannot access execution context",
            BuiltIn().get_variables,
        )

    def test_suite_doc_and_metadata(self):
        assert_raises_with_msg(
            RobotNotRunningError,
            "Cannot access execution context",
            BuiltIn().set_suite_documentation,
            "value",
        )
        assert_raises_with_msg(
            RobotNotRunningError,
            "Cannot access execution context",
            BuiltIn().set_suite_metadata,
            "name",
            "value",
        )


class TestBuiltInPropertys(unittest.TestCase):

    def test_robot_running(self):
        assert_equal(BuiltIn().robot_running, False)

    def test_dry_run_active(self):
        assert_equal(BuiltIn().dry_run_active, False)


class TestDateTime(unittest.TestCase):

    def test_date_seconds(self):
        secs = 1234567890
        assert_equal(Date(secs).seconds, secs)


class TestProcessSecretEnvOnWindows(unittest.TestCase):

    def setUp(self):
        self.windows = Process.WINDOWS
        Process.WINDOWS = True  # Env var names are upper-cased on Windows.

    def tearDown(self):
        Process.WINDOWS = self.windows

    def test_lowercase_secret_env_name(self):
        config = ProcessConfiguration(**{"env:v2": Secret("This is secret!")})
        assert_equal(config.env["V2"], "This is secret!")
        assert_false("This is secret!" in str(config))
        assert_true("'V2': '<secret>'" in str(config))

    def test_lowercase_secret_env_name_in_env_dict(self):
        config = ProcessConfiguration(env={"v1": Secret("This is secret!")})
        assert_equal(config.env, {"V1": "This is secret!"})
        assert_false("This is secret!" in str(config))
        assert_true("'V1': '<secret>'" in str(config))


if __name__ == "__main__":
    unittest.main()
