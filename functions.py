import random as rd
from faker import Faker
from queue import Queue
from typing import *
from structure import Host, Cve
from dateutil.relativedelta import relativedelta

fake = Faker()
ComplexRange = List[Tuple[str, List[str]]]


def gen_hostname(number: int, range_region: List[str]) -> str:
    """
    Gera o nome de um servidor no formato: SVR-{região}-{int}
    Ex: gen_hostname(number) -> 'SVR-US-136'
    """
    get_region = rd.choice(range_region)
    hostname = f"SVR-{get_region}-{number}"
    return hostname


def gen_ipv4() -> str:
    """
    Gera um ipv4 aleatório para o hostname.
    EX: gen_ipv4() -> '111.47.91.20'
    """
    range_ip = [10] + [rd.randint(12, 127) for _ in range(2)]
    range_ip.append(rd.randint(0, 255))
    ip = ".".join(map(str, range_ip))
    return ip


def gen_cve(queue: Queue) -> Cve:
    """
    Gera um CVE (vulnerabilidade) aleatório.
    Ex: gen_cve() ->
    """
    cve_date = fake.date_time_between(start_date="-2y", end_date="-1y").date()
    cve_end_date = cve_date + relativedelta(days=90)
    cve_pubish_date = fake.date_time_between(
        start_date=cve_date, end_date=cve_end_date
    ).date()
    cve_cwe_id = queue.get()  # cve = i[0], cwe = i[1]
    cve_id = cve_cwe_id[0]
    cve_name = f"CVE-{cve_date.year}-{cve_id}"
    cwe_id = cve_cwe_id[1]
    cwe_name = f"CWE-{cwe_id}"
    severity = rd.choice(["Low", "Medium", "High", "Critical"])
    return Cve(
        int(cve_id),
        cve_name,
        severity,
        cve_date,
        cve_pubish_date,
        int(cwe_id),
        cwe_name,
    )


def create_host(
    queue_hostname: Queue,
    queue_ipv4: Queue,
    equipament: ComplexRange,
    range_os: ComplexRange,
    range_region: ComplexRange,
) -> Host:
    """
    Cria um host com dados fictícios obtendo alguns elementos das filas.
    """

    hostname = queue_hostname.get()  # get and deleted in queue
    hostname_id = int(hostname[-3:])
    ipv4 = queue_ipv4.get()  # get and deleted in queue
    deployment = rd.choice(["Cloud", "On-Premise"])
    _os = rd.choice(range_os)
    os, os_version = _os[0], rd.choice(_os[1])
    region = rd.choice(range_region)
    _hardware = rd.choice(equipament)
    network_provider, network_equipament = _hardware[0], rd.choice(_hardware[1])
    created_date = fake.date_time_between(start_date="-2y", end_date="-180d")
    return Host(
        hostname_id,
        hostname,
        ipv4,
        deployment,
        os,
        os_version,
        region,
        network_provider,
        network_equipament,
        created_date,
    )
