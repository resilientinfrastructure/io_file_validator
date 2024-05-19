from pathlib import Path

import pytest
from pydiggs import validator

from io_file_validator.validator import Validator


class PydiggsValidator(Validator):
    def __init__(self, file_format) -> None:
        super().__init__(file_format=file_format)
        self._validation_method = "yaml_url"

    def run_validation(self, file_path):
        # dataframe = pd.read_xml(my_upload)
        pydiggs_validator = validator(file_path)
        pydiggs_validator.schema_check()
        error_log = pydiggs_validator.schema_validation_log
        assert error_log is None


def test_validator():
    validator = PydiggsValidator(
        file_format="xml",
    )
    parent_path = Path(__file__).parent
    sample_file_path = parent_path.resolve() / "data" / "No_Error.xml"
    validator.run_validation(file_path=str(sample_file_path))


def test_validator_error():
    validator = PydiggsValidator(
        file_format="xml",
    )
    parent_path = Path(__file__).parent
    sample_file_path = parent_path.resolve() / "data" / "Schema_Error_1.xml"
    with pytest.raises(Exception):  # Replace 'Exception' with the specific exception you expect to be raised
        validator.run_validation(file_path=str(sample_file_path))
