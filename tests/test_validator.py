from io import BytesIO
from pathlib import Path

import pytest
from pandera.errors import SchemaError

from io_file_validator.validator import ValidatorDataframe


def test_validator():
    validator = ValidatorDataframe(
        url="https://raw.githubusercontent.com/resilientinfrastructure/standards/main/panderas_schema.yml",
        file_format="csv",
    )
    parent_path = Path(__file__).parent
    sample_file_path = parent_path.resolve() / "data" / "sample_prices.csv"

    with open(sample_file_path, "rb") as sample_file:
        file_contents = sample_file.read()
        sample_file_bytesio = BytesIO(file_contents)
        yaml_content = validator.get_yaml_content(validator.url)
        validated_df = validator.load_and_validate_file(my_upload=sample_file_bytesio, yaml_content=yaml_content)
    assert len(validated_df.columns) == 3 and "store" in validated_df.columns


def test_validator_error():
    parent_path = Path(__file__).parent
    sample_file_path = parent_path.resolve() / "data" / "sample_prices_raise_error.csv"
    validator = ValidatorDataframe(
        url="https://raw.githubusercontent.com/resilientinfrastructure/standards/main/panderas_schema.yml",
        file_format="csv",
    )
    with open(sample_file_path, "rb") as sample_file:
        with pytest.raises(SchemaError):
            file_contents = sample_file.read()
            sample_file_bytesio = BytesIO(file_contents)
            yaml_content = validator.get_yaml_content(validator.url)
            validator.load_and_validate_file(my_upload=sample_file_bytesio, yaml_content=yaml_content)
