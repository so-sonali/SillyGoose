unit_factors = {
    "M": 1,
    "mM": 1e-3,
    "uM": 1e-6,
    "nM": 1e-9,
    "L": 1,
    "mL": 1e-3,
    "uL": 1e-6,
}


def convert_to_base(value, unit):
    return value * unit_factors[unit]

def convert_from_base(value, target_unit):
    return value / unit_factors[target_unit]
