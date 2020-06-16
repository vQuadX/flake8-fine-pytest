import pathlib
from typing import List, Optional, Union

from flake8_fine_pytest.watchers.base import BaseWatcher


def get_stem(filepath: Union[str, pathlib.Path]) -> str:
    return pathlib.PurePath(filepath).stem


def get_file_directory(filepath: str) -> str:
    directory = pathlib.Path(filepath).parent

    return get_stem(directory)


def is_test_file(filename: str) -> bool:
    return filename.startswith('test_')


def get_allowed_directories_display(allowed_test_directories: List[str]) -> str:
    return ','.join(allowed_test_directories)


def get_error_message(template: str, allowed_directories: List[str], filepath: str) -> str:
    allowed_directories_display = get_allowed_directories_display(allowed_directories)
    return template.format(
        filepath=filepath, allowed_directories=allowed_directories_display,
    )


class ModulesStructureWatcher(BaseWatcher):
    error_template = (
        'FP003 File {filepath} is in the wrong directory. Allowed directories: {allowed_directories}'
    )

    def run(self) -> None:
        allowed_test_directories = self.options.allowed_test_directories

        if self._should_check(allowed_test_directories) is False:
            return None

        file_directory = get_file_directory(self.filename)

        if file_directory not in allowed_test_directories:
            error_message = get_error_message(self.error_template, allowed_test_directories, self.filename)

            self.add_error((0, 0, error_message))

    def _should_check(self, allowed_test_directories: Optional[List[str]]) -> bool:
        stem = get_stem(self.filename)

        return is_test_file(stem) and allowed_test_directories is not None