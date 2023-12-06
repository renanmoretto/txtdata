from pathlib import Path
from typing import Literal


class TxtData:
    def __init__(
        self,
        path: Path,
        delimiter: str = ';',
        fixed_columns: bool = True,
    ):
        if not fixed_columns:
            raise NotImplementedError(f'dynamic columns are not implemented yet.')

        path = self._parse_path(path)
        self._ensure_file(path)

        self.path: Path = path
        self.items: dict = self._load_txt(path)
        self._type: Literal['fixed', 'dynamic'] = 'fixed' if fixed_columns else 'dynamic'

    def _parse_path(self, path: Path) -> Path:
        # if path is None:
        #     # Create file on the relative .py file directory which is
        #     # initializing the TxtData object.
        #     return Path(__file__) / 'data.txt'

        if path.suffix != '.txt':
            raise ValueError('Path suffix must be .txt')

        return path

    def _ensure_file(self, file_path: Path):
        """Create file if not exists"""
        if not file_path.is_file():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch(exist_ok=True)

    @staticmethod
    def _load_txt(file_path: Path) -> dict:
        # TODO
        ...

    def insert(self):
        # TODO
        ...

    def loc(self) -> dict:
        # TODO
        ...

    def delete(self):
        # TODO
        ...

    def save(self):
        # TODO
        ...
