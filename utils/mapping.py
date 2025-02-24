
REPORTS_COLUMNS = {
    "A1": [
        "PAIRPORT",
        "AD",
        "SCHEDNS",
        "PASSFREIGH",
        "AIRLINEC",
        "PAX ON BOARD",
        "FREIGHT_ON_BOARD",
        "FLIGHT",
        "SEATAV",
        "TABLE",
        "COUNTRY",
        "RAIRPORT"
    ],
    "B1": [
        "PAIRPORT",
        "AD",
        "SCHEDNS",
        "PASSFREIGH",
        "AIRLINEC",
        "PAX_CARRIED",
        "TABLE",
        "COUNTRY",
        "RAIRPORT"
    ],
    "C1": [
        "PAIRPORT",
        "AD",
        "SCHEDNS",
        "FLIGHT_COUNT",
        "TABLE",
        "COUNTRY",
        "RAIRPORT"
    ]
}

REPORTS_ROWS = {"A1": [
                    'Rejsowy',
                    'Przekierowanych do GDN',
                    'Czarterowy',
                    'Czarterowy NREG',
                    'Cargo',
                    'Cargo/Regularny'
                ]
}

REPORT_MAPPINGS = {
    "A1": {
        "Port ICAO": "PAIRPORT",
        "Operacja": "AD",
        "Przewoźnik ICAO": "AIRLINEC",
        "Model samolotu": "AIRCRAFTTY",
        "PAX Capacity": "SEATAV"
    },
    "B1": {
        "PAIRPORT": "PAIRPORT",
        "AD": "AD",
        "SCHEDNS": "SCHEDNS",
        "PASSFREIGH": "PASSFREIGH",
        "AIRLINEC": "AIRLINEC",
        "PAX_CARRIED": "PAX_ON_BOARD",
        "TABLE": "B1",
        "COUNTRY": "EP",
        "RAIRPORT": "EPGD"
    },
    "C1": {
        "PAIRPORT": "PAIRPORT",
        "AD": "AD",
        "SCHEDNS": "SCHEDNS",
        "FLIGHT_COUNT": "FLIGHT",
        "TABLE": "C1",
        "COUNTRY": "EP",
        "RAIRPORT": "EPGD"
    }
}

FLIGHT_TYPES = {
    "PASSFREIGH": {
        'Rejsowy': 1,
        'Przekierowanych do GDN': 1,
        'Czarterowy': 1,
        'Czarterowy NREG': 1,
        'Cargo': 2,
        'Cargo/Regularny': 2
    },
    "SCHEDNS": {
        'Rejsowy': 1,
        'Przekierowanych do GDN': 2,
        'Czarterowy': 1,
        'Czarterowy NREG': 2,
        'Cargo': 1,
        'Cargo/Regularny': 1
    }
}
