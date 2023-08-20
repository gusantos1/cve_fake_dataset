import random as rd

"""
gen_ids: Concatena 3 números sorteados aleatoriamente de 0 a 10 e. 
    Ex: [3,5,9] -> '359'

range_cwe: Valores gerados pelo gen_ids representando os grupos de cve. `Um grupo contém N* cves` 
    Ex: ['310', '590', '230', ...]

range_cve: Pega aleatoriamente um valor em `range_cwe` e sorteia aleatoriamente um valor de 4 caractéres para representar uma `cve`. 
    Ex: [(CVE, CWE), (CVE, CWE), ...] -> [('9611','217'), ('2594','217'), ('8451','361')]
"""

gen_ids = lambda n: "".join(rd.choices([str(i) for i in range(0, 10)], k=n))
range_name = [i for i in range(100, 210)]
range_region = ["BR", "EU", "US"]
range_os = [
    ("Ubuntu Server", ["20.04", "18.04", "16.04"]),
    ("Windows Server", ["2022", "2019", "2016"]),
    ("Debian GNU/Linux", ["11", "10", "9"]),
    ("Red Hat Enterprise Linux", ["8", "7", "6"]),
    ("CentOS", ["8", "7", "6"]),
]
manufacturer_equipament = [
    ("Arista Networks", ["Switch Arista"]),
    ("Cisco", ["Switch Access", "Router", "Switch IOS", "ISE"]),
    ("Dell Computer", ["Switch Dell"]),
    ("F5 Networks", ["F5"]),
]
range_cwe = list({gen_ids(3) for _ in range(0, 20)})
range_cve = sorted(
    list({(gen_ids(4), rd.choice(range_cwe)) for _ in range(0, 100)}),
    key=lambda i: (i[1], i[0]),
)