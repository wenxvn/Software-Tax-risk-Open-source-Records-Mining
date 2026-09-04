"""Small DuckDB facade; no server is required."""
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd


class DatabaseManager:
    def __init__(self, path: str | Path = "data/processed/taxrisk.duckdb") -> None:
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = duckdb.connect(self.path)

    def register(self, name: str, frame: pd.DataFrame) -> None:
        self.connection.register(name, frame)

    def load(self, name: str, path: str | Path) -> None:
        file_path = str(path)
        suffix = Path(file_path).suffix.lower()
        if suffix == ".csv":
            self.connection.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_csv_auto(?)", [file_path])
        elif suffix in {".parquet", ".pq"}:
            self.connection.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_parquet(?)", [file_path])
        else:
            raise ValueError(f"unsupported data file: {suffix}")

    def query(self, sql: str, parameters: list[Any] | None = None) -> pd.DataFrame:
        return self.connection.execute(sql, parameters or []).fetchdf()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "DatabaseManager":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

