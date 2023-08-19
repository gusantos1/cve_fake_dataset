import random as rd
import json
import pandas as pd
from queue import Queue
from ranges import (
    range_name,
    range_cve,
    manufacturer_equipament,
    range_os,
    range_region,
)
from functions import gen_hostname, gen_cve, gen_ipv4, create_host
from directory import create_directories

# ----------------- CRIAÇÃO DOS DIRETÓRIOS ---------------------
sub_dirs = create_directories()

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

# ----------------- ESCREVENDO ARQUIVOS NOS SUBDIRETÓRIOS ---------------------
for directory in sub_dirs[1]:
    max_files = rd.randint(10, 20)
    for i in range(1, max_files + 1):
        possible_extension = ["json", "csv"]
        extension = rd.choice(possible_extension)
        file_name = f"{directory / str(i).zfill(3)}.{extension}"
        with open(file_name, "w") as file:
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
            match extension:
                case "json":
                    data = json.dumps(fact, indent=4)
                    file.write(data)
                case "csv":
                    data = pd.DataFrame.from_dict(fact, orient="index").T
                    data.to_csv(file_name, index=False, sep=";")
                case _:
                    raise ValueError(
                        f"Extensão de arquivo '{extension}' não suportada."
                    )
