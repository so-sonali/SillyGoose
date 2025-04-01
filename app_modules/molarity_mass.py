from app_modules.unit_converter import convert_to_base, convert_from_base
from app_modules.logger import save_log

valid_units = ["M", "mM", "uM", "nM", "L", "mL", "uL"]

def calculate_mass(concentration, conc_unit, volume, vol_unit, mw):
    if conc_unit not in valid_units or vol_unit not in valid_units:
        raise ValueError("Invalid unit. Use M, mM, uM, nM for concentration and L, mL, uL for volume.")

    conc_base = convert_to_base(concentration, conc_unit)
    vol_base = convert_to_base(volume, vol_unit)

    moles = conc_base * vol_base
    mass_g = moles * mw
    mass_mg = mass_g * 1000

    result = (
        f"⚖️ Molarity ➜ Mass\n"
        f"📌 Desired concentration: {concentration} {conc_unit}\n"
        f"📌 Final volume: {volume} {vol_unit}\n"
        f"📌 Molecular weight: {mw} g/mol\n\n"
        f"🧪 Required mass: {mass_mg:.4f} mg"
    )

    save_log("Molarity-to-Mass", result)
    return result

def calculate_concentration(mass_mg, volume, vol_unit, mw, output_unit):
    if vol_unit not in valid_units or output_unit not in valid_units:
        raise ValueError("Invalid unit.")

    vol_base = convert_to_base(volume, vol_unit)
    mass_g = mass_mg / 1000
    moles = mass_g / mw
    conc_base = moles / vol_base
    conc_converted = convert_from_base(conc_base, output_unit)

    result = (
        f"⚖️ Mass ➜ Molarity\n"
        f"📌 Mass: {mass_mg} mg\n"
        f"📌 Final volume: {volume} {vol_unit}\n"
        f"📌 Molecular weight: {mw} g/mol\n\n"
        f"🧪 Final concentration: {conc_converted:.4f} {output_unit}"
    )

    save_log("Mass-to-Molarity", result)
    return result
