from copy import deepcopy
from pathlib import Path
from typing import Any


_DEFAULT_DELIMITER = ';'

_DataDict = dict[str, Any]
DataLike = dict[str, Any] | list[dict[str, Any]] | dict[str, list[Any]]


class TxtData:
    """
    Properties
    ----------
        data: list[dict[str, Any]]
        delimiter: str
        empty: bool
        fields: list[str]

    """

    def __init__(
        self,
        data: list[_DataDict] | None = None,
        delimiter: str = _DEFAULT_DELIMITER,
    ):
        if data:
            self.data = self._parse_data(data)
        else:
            self.data = []
        self.delimiter: str = delimiter

    @property
    def empty(self) -> bool:
        return not bool(self.data)

    @property
    def fields(self) -> list[str]:
        if self.empty:
            return []
        return list(self.data[0].keys())

    def __len__(self):
        return len(self.data)

    def __str__(self) -> str:
        return self.data.__str__()

    def __repr__(self) -> str:
        return self.data.__repr__()

    @staticmethod
    def _is_simple_dict(obj: Any) -> bool:
        if not isinstance(obj, dict):
            return False
        for key, value in obj.items():  # type: ignore
            if not isinstance(key, str) or isinstance(value, list):
                return False
        return True

    @staticmethod
    def _is_list_of_dicts(obj: Any) -> bool:
        """Verify if obj is list[dict[str, Any]]"""
        if not isinstance(obj, list):
            return False

        for item in obj:  # type: ignore
            if not isinstance(item, dict):
                return False
            if all(isinstance(key, str) for key in item):  # type: ignore
                return True
        return False

    @staticmethod
    def _is_dict_of_lists(obj: Any) -> bool:
        """Verify if obj is dict[str, list[Any]]"""
        if not isinstance(obj, dict):
            return False
        for key, value in obj.items():  # type: ignore
            if not isinstance(key, str) or not isinstance(value, list):
                return False
        return True

    def _parse_data(self, data: DataLike) -> list[_DataDict]:
        """Verify data type and return a copy if valid"""
        if self._is_simple_dict(data):
            return [data].copy()  # type: ignore
        elif self._is_dict_of_lists(data):
            # TODO
            raise NotImplementedError('data as dict os lists not implemented')
        elif self._is_list_of_dicts(data):
            return data.copy()  # type: ignore
        else:
            raise TypeError(
                'data must be a dict, a list of dicts or dict of [str, list[Any]]'
            )

    @staticmethod
    def _txt_to_dict(
        txt_lines: list[str], delimiter: str = _DEFAULT_DELIMITER
    ) -> list[_DataDict]:
        fields = txt_lines[0].strip().split(delimiter)
        data: list[_DataDict] = []
        for line in txt_lines[1:]:
            values = line.strip().split(delimiter)
            row_dict = {}
            for k, v in zip(fields, values):
                row_dict[k] = v
            data.append(row_dict)
        return data

    @staticmethod
    def _data_to_txt(
        data: list[_DataDict], delimiter: str = _DEFAULT_DELIMITER
    ) -> list[str]:
        fields = list(data[0].keys())
        txt_header = f'{delimiter}'.join(fields) + '\n'
        txt_lines = [txt_header]
        for data_slice in data:
            row_values = [
                str(v) if v is not None else '' for v in data_slice.values()
            ]
            row = f'{delimiter}'.join(row_values) + '\n'
            txt_lines.append(row)
        return txt_lines

    @classmethod
    def from_path(
        cls, path: Path, delimiter: str = _DEFAULT_DELIMITER
    ) -> 'TxtData':
        if path.suffix != '.txt':
            raise ValueError('Path suffix must be .txt')

        with open(path, 'r') as file:
            lines = file.readlines()

        data = cls._txt_to_dict(lines, delimiter)
        return cls(data, delimiter)

    def _format_new_data(self, data: _DataDict) -> _DataDict:
        """Adds missing fields (txt fields) in new data."""
        data = data.copy()
        missing_fields = [
            field for field in self.fields if field not in data.keys()
        ]
        for field in missing_fields:
            data.update({field: None})
        return data

    def copy(self) -> 'TxtData':
        return deepcopy(self)

    def _insert_single_data(self, data: _DataDict):
        new_data = self._format_new_data(data)
        data_fields = list(data.keys())
        new_fields = [
            field for field in data_fields if field not in self.fields
        ]

        has_new_fields = bool(new_fields)

        if has_new_fields:
            # Update old data with new fields
            for i_data in self.data:
                for new_field in new_fields:
                    i_data.update({new_field: None})

        self.data.append(new_data)

    def insert(
        self,
        __data: dict[str, Any] | list[dict[str, Any]] | None = None,
        /,
        **kwargs: Any,
    ):
        """Inserts new data into the object by a dict, list of dicts
        or keywords.

        Example
        -------

        """
        if __data is not None:
            if kwargs:
                raise ValueError('keyword data not allowed if data was passed.')
            data = self._parse_data(__data)
        else:
            data = kwargs.copy()

        if isinstance(data, dict):
            self._insert_single_data(data)
        else:
            for single_data in data:
                self._insert_single_data(single_data)

    def filter(self, **kwargs: Any) -> 'TxtData':
        """
        Filter data by keyword arguments passed.
        PS: This is NOT in place.

        Returns
        -------
        TxtData
            A new TxtData instance filtered.

        Examples
        --------
            >>> txt = TxtData([
                {'A': None, 'B': 10, 'C': 50},
                {'A': 150, 'B': 50, 'C': 39},
                {'A': 32, 'B': 50, 'C': 2},
            ])
            >>> txt_filtered = txt.filter(A=150)
            >>> print(txt_filtered)
            [{'A': 150, 'B': 50, 'C': 39}]
        """
        filtered_data: list[_DataDict] = []
        for key, value in kwargs.items():
            filtered_data_by_key: list[_DataDict] = [
                d for d in self.data if d[key] == value
            ]
            filtered_data.extend(filtered_data_by_key)
        return TxtData(data=filtered_data, delimiter=self.delimiter)

    def to_dict(self) -> dict[str, list[Any]]:
        # TODO
        ...

    def to_dicts(self) -> list[dict[str, Any]]:
        return self.data

    def save(self, path: Path):
        """
        Saves the txt file.

        Parameters
        ----------
        path : Path
        """
        if not path.is_file():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)

        txt_data = self._data_to_txt(self.data, self.delimiter)
        with open(path, 'w') as file:
            file.writelines(txt_data)
