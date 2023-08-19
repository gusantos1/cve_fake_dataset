from collections import namedtuple

Host = namedtuple(
    "Host",
    [
        "hostname_id",
        "hostname",
        "ipv4",
        "deployment",
        "os",
        "os_version",
        "region",
        "network_provider",
        "network_equipament",
        "created_date",
    ],
)
Cve = namedtuple(
    "Cve",
    [
        "cve_id",
        "cve_name",
        "cve_severity",
        "cve_created",
        "cve_publish",
        "cwe_id",
        "cwe_name",
    ],
)
