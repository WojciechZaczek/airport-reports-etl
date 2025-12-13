
# import gus_a1_cargo_utils

REPORTS_COLUMNS = ["TABLE",
                   "COUNTRY",
                   "YEAR",
                   "PERIOD",
                   "RAIRPORT",
                   "PAIRPORT",
                   "AD",
                   "SCHEDNS",
                   "PASSFREIGH",
                   "AIRLINEC",
                   "AIRCRAFTTY",
                   "PAX ON BOARD",
                   "FREIGHT ON BOARD",
                   "FLIGHT",
                   "SEATAV",
                   ]





REPORTS_ROWS = [
                    'Rejsowy',
                    'Przekierowany do GDN',
                    'Czarterowy',
                    'Czarterowy NREG',
                    'Cargo',
                    'Cargo/Regularny'
                ]

REPORT_MAPPINGS = {

        "Port ICAO": "PAIRPORT",
        "Operacja": "AD",
        "Przewoźnik ICAO": "AIRLINEC",
        "Model samolotu": "AIRCRAFTTY",
        "PAX Capacity": "SEATAV"
    }

FLIGHT_TYPES = {
    "PASSFREIGH": {
        'Rejsowy': 1,
        'Przekierowany do GDN': 1,
        'Czarterowy': 1,
        'Czarterowy NREG': 1,
        'Cargo': 2,
        'Cargo/Regularny': 2
    },
    "SCHEDNS": {
        'Rejsowy': 1,
        'Przekierowany do GDN': 2,
        'Czarterowy': 1,
        'Czarterowy NREG': 2,
        'Cargo': 1,
        'Cargo/Regularny': 1
    }
}
