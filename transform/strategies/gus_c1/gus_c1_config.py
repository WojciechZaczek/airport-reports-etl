
REPORTS_COLUMNS = [
        "TABLE",
        "COUNTRY",
        "YEAR",
        "PERIOD",
        "RAIRPORT",
        "AIRLINEC",
        "PAX",
        "TRANSITPAX",
        "FREIGHT",
        "AIRCRAFTM",
        "AIRCRAFTMY"

    ]


REPORT_MAPPINGS = {

        "Operacja": "FLIGHT",
        "Przewoźnik ICAO": "AIRLINEC",
        "Tranzyt": "TRANSITPAX",

    }

REPORTS_ROWS = [
                    'Rejsowy',
                    'Przekierowany do GDN',
                    'Czarterowy',
                    'Czarterowy NREG',
                    'Cargo',
                    'Cargo/Regularny',
                    'General Aviation',
                    'General Aviation (kom)',
                    'General Aviation(n-kom)',
                    'Sanitarny',
                    'Szkoleniowy',
                    'Techniczny'

                ]
MAPPING_TMY = [
        "General Aviation (kom)", "General Aviation(n-kom)", "General Aviation",
        "Sanitarny", "Szkoleniowy", "Techniczny"
]

MAPPING_A1_TYPE = [
            "Rejsowy", "Przekierowany do GDN", "Czarterowy",
            "Czarterowy NREG", "Cargo", "Cargo/Regularny"
        ]