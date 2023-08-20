import random as rd
import json
import pandas as pd
from typing import *
from queue import Queue
from ranges import (
    range_name,
    range_cve,
    manufacturer_equipament,
    range_os,
    range_region,
)
from functions import gen_hostname, gen_cve, gen_ipv4, create_host
from directory import create_directories, Path

# ----------------- CRIAÇÃO DOS DIRETÓRIOS ---------------------
base_dir, sub_dir = create_directories()

# ----------------- FILAS ---------------------
queue_hostname = Queue(maxsize=len(range_name))
queue_ipv4 = Queue(maxsize=len(range_name))
queue_cve = Queue(maxsize=len(range_cve))

# ----------------- ALIMENTANDO AS FILAS ---------------------
put_hostname = {queue_hostname.put(gen_hostname(n, range_region)) for n in range_name}
put_ipv4 = {queue_ipv4.put(gen_ipv4()) for _ in range_name}
put_cve = {queue_cve.put(cve) for cve in range_cve}

# ----------------- ESTRUTURAS DE DADOS ---------------------
cve_list = []
dimension_host = []

# ----------------- ADICIONANDO OBJETOS NAS ESTRUTURAS DE DADOS ---------------------
# Enquanto a fila {queue} estiver cheia, faça `FIFO` e adicione na lista {list}.
while not queue_hostname.empty():
    dimension_host.append(
        create_host(
            queue_hostname, queue_ipv4, manufacturer_equipament, range_os, range_region
        )
    )
while not queue_cve.empty():
    cve_list.append(gen_cve(queue_cve))


# ----------------- FUNÇÕES DE ESCRITA PARA CADA EXTENSÃO ---------------------
def template_fact_json(full_file_path: str, data: dict, **kwargs) -> str:
    with open(full_file_path, "w") as file:
        data = json.dumps(data, **kwargs)
        file.write(data)
    return full_file_path


def template_fact_csv(full_file_path: str, data: dict, **kwargs) -> str:
    df = pd.DataFrame.from_dict(data, orient="index").T
    df.to_csv(full_file_path, **kwargs)
    return full_file_path


# ----------------- CLASSE RESPONSÁVEL POR ESCREVER ---------------------
class Writer:
    def __init__(self, directories: List[Path], max_files: int = 50):
        self.directories = directories
        self.max_files = rd.randint(10, max_files) + 1
        self.sucess = set()
        self.__possible_extension = []
        self.__mode_writer = {}

    def write(self) -> Tuple[bool, str]:
        for directory in self.directories:
            for i in range(1, self.max_files):
                extension = rd.choice(self.__possible_extension)
                full_path = f"{directory / str(i).zfill(3)}.{extension}"
                host_id = rd.choice(dimension_host).hostname_id
                cve = rd.choice(cve_list)
                fact = {
                    "hostname_id": host_id,
                    "cve_id": cve.cve_id,
                    "cve_name": cve.cve_name,
                    "cve_severity": cve.cve_severity,
                    "cve_created": cve.cve_created.strftime("%Y-%m-%d"),
                    "cve_publish": cve.cve_publish.strftime("%Y-%m-%d"),
                    "cwe_id": cve.cwe_id,
                    "cwe_name": cve.cwe_name,
                }
                func, kwargs = self.__mode_writer.get(extension)
                result_path = func(full_path, fact, **kwargs)
                self.sucess.add(result_path)

    def learn_to_write(self, extension, template, **kwargs) -> Dict[str, callable]:
        """
        Open-close
        """
        self.__possible_extension.append(extension)
        self.__mode_writer[extension] = template, kwargs
        return self.__mode_writer


# ----------------- ESCREVENDO DIMENSÃO NO DIRETÓRIO PRINCIPAL ---------------------
df_dimensao = pd.DataFrame(dimension_host).to_csv(
    f"{base_dir}/dim.csv", index=False, sep="|"
)

# ----------------- ESCREVENDO FATOS NOS SUBDIRETÓRIOS ---------------------
writer = Writer(sub_dir)
writer.learn_to_write("csv", template_fact_csv, index=False, sep=";")
writer.learn_to_write("json", template_fact_json, indent=4)
writer.write()
