from pathlib import Path
from typing import Tuple
from datetime import datetime as dt


def create_directories() -> Tuple[Path, Path]:
    """
    Cria um diretório principal com base no ano atual e 12 subdiretórios representando os meses do ano em %MM.
    Ex:
        - 2023
        |- 01 (Janeiro)
        |- 02 (Fevereiro)
        |- 03 (Março)
        |- 04 (Abril)
        |- 05 (Maio)
        |- 06 (Junho)
        |- 07 (Julho)
        |- 08 (Agosto)
        |- 09 (Setembro)
        |- 10 (Outubro)
        |- 11 (Novembro)
        |- 12 (Dezembro)
    """
    try:
        source = Path('dataset')
        source.mkdir(exist_ok=True)
        current_year = str(dt.now().year)
        base_directory = source / Path(current_year)
        base_directory.mkdir(exist_ok=True)
        subdirs = []
        for month in range(1, 13):
            month_name = str(month).zfill(2)
            month_directory = base_directory / month_name
            month_directory.mkdir(exist_ok=True)
            subdirs.append(month_directory)
        return base_directory, subdirs
    except Exception as e:
        raise e
