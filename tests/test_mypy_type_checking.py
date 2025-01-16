import glob
import logging
import os

import allure
import pytest
from mypy.api import run as mypy_api_run

logger = logging.getLogger(__name__)


def get_files_in_directories(directories: list[str]) -> list[str]:
    files: list[str] = []
    for dir in directories:
        if not os.path.isdir(dir):
            raise ValueError(f"Directory {dir} does not exist.")
        else:
            current_dir = os.path.abspath(dir)
            files.extend(
                glob.glob(os.path.join(current_dir, "**", "*.py"), recursive=True)
            )
    return files


@allure.feature("Static type checking")
@allure.story("Mypy")
@pytest.mark.parametrize("folders", [(["pages"]), (["tests"])])
def test_mypy_type_checking(folders: list[str]) -> None:
    """Run mypy static type checking on the target folders."""
    files_paths = get_files_in_directories(folders)
    logger.info(f"Running mypy static type checking on folder(s): {folders}")
    normal_report, error_report, exit_status = mypy_api_run(
        [
            "--ignore-missing-imports",
            "--strict",
            "--allow-untyped-decorators",
            *files_paths,
        ]
    )
    assert exit_status == 0, normal_report + error_report
