import os
import glob
# import pytest


def pytest_sessionfinish(session, exitstatus):
    """ Code to execute after all tests. """

    # dat files are created when using attachements, like cards from Card cog, etc...  # noqa: E501
    print("\n-------------------------\nClean dpytest_*.dat files")
    fileList = glob.glob('./dpytest_*.dat')
    for filePath in fileList:
        try:
            os.remove(filePath)
        except Exception:
            print("Error while deleting file : ", filePath)

    # Delete json log file created by the tests
    print("\n-------------------\nClean test log.json\n")
    log_test_file = "utils/test_log.json"
    try:
        os.remove(log_test_file)
    except FileNotFoundError:
        pass
