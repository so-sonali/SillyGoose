from app_modules.unit_converter import convert_to_base, convert_from_base
from app_modules.logger import save_log

valid_units = ["M", "mM", "uM", "nM", "L", "mL", "uL"]

def dilution_calc(C1, C1_unit, C2, C2_unit, V2, V2_unit, output_vol_unit):
    if any(unit not in valid_units for unit in [C1_unit, C2_unit, V2_unit, output_vol_unit]):
        raise ValueError("Invalid unit provided.")

    C1_base = convert_to_base(C1, C1_unit)
    C2_base = convert_to_base(C2, C2_unit)
    V2_base = convert_to_base(V2, V2_unit)

    if C2_base > C1_base:
        raise ValueError("Desired concentration (C2) cannot be greater than stock concentration (C1).")

    V1_base = (C2_base * V2_base) / C1_base
    diluent_volume_base = V2_base - V1_base

    V1_final = convert_from_base(V1_base, output_vol_unit)
    diluent_final = convert_from_base(diluent_volume_base, output_vol_unit)

    result = (
        f"🔬 Dilution Calculation\n"
        f"📌 Stock concentration (C1): {C1} {C1_unit}\n"
        f"📌 Desired concentration (C2): {C2} {C2_unit}\n"
        f"📌 Final volume (V2): {V2} {V2_unit}\n\n"
        f"🧪 Volume of stock to use (V1): {V1_final:.2f} {output_vol_unit}\n"
        f"💧 Volume of diluent to add: {diluent_final:.2f} {output_vol_unit}"
    )

    save_log("Dilution", result)
    return result
