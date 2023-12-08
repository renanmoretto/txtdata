from pathlib import Path
from typing import Literal


_DEFAULT_DELIMITER = ';'


class _DataFormat(list):
    ...


class TxtData:
    """Basically, it's a list of dicts."""

    def __init__(
        self,
        data: list[dict] | None = None,
        delimiter: str = _DEFAULT_DELIMITER,
        fields: list[str] | None = None,
    ):
        self.data: list[dict] = data.copy() if data else []
        self.delimiter: str = delimiter
        self._original_fields = fields

    @property
    def empty(self) -> bool:
        return bool(self.data)

    @property
    def txt(self) -> list[str]:
        return self._data_to_txt(self.data, self.delimiter)

    @property
    def fields(self) -> list[str]:
        if self.empty:
            return []
        return list(self.data[0].keys())

    def __len__(self):
        return len(self.data)

    @staticmethod
    def _txt_to_dict(txt_lines: list, delimiter: str = _DEFAULT_DELIMITER) -> list[dict]:
        fields = txt_lines[0].strip().split(delimiter)
        data = []
        for line in txt_lines[1:]:
            values = line.strip().split(delimiter)
            row_dict = {}
            for k, v in zip(fields, values):
                row_dict[k] = v
            data.append(row_dict)
        return data

    @staticmethod
    def _data_to_txt(data: list[dict], delimiter: str = _DEFAULT_DELIMITER) -> list[str]:
        fields = list(data[0].keys())
        txt_header = f'{delimiter}'.join(fields) + '\n'
        txt_lines = [txt_header]
        for data_slice in data:
            row_values = [str(v) if v is not None else '' for v in data_slice.values()]
            row = f'{delimiter}'.join(row_values) + '\n'
            txt_lines.append(row)
        return txt_lines

    @classmethod
    def from_path(cls, path: Path, delimiter: str = _DEFAULT_DELIMITER) -> 'TxtData':
        if path.suffix != '.txt':
            raise ValueError('Path suffix must be .txt')

        with open(path, 'r') as file:
            lines = file.readlines()

        data = cls._txt_to_dict(lines, delimiter)
        return cls(data, delimiter)

    def insert(self, data: dict):
        new_data = data.copy()
        data_fields = list(data.keys())
        new_fields = [field for field in data_fields if field not in self.fields]

        has_new_fields = bool(new_fields)

        if has_new_fields:
            # Update old data with new fields
            for i_data in self.data:
                for new_field in new_fields:
                    i_data.update({new_field: None})

        self.data.append(new_data)

    def loc(self) -> dict:
        # TODO
        ...

    def delete(self, irow: int):
        # TODO
        ...

    def save(self, path: Path):
        # TODO
        ...


def _ensure_file(file_path: Path):
    """Create file if not exists"""
    if not file_path.is_file():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch(exist_ok=True)
