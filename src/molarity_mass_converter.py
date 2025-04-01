from app_modules.unit_converter import convert_to_base, convert_from_base
from app_modules.logger import save_log

valid_units = ["M", "mM", "uM", "nM", "L", "mL", "uL"]

def calculate_mass(concentration, conc_unit, volume, vol_unit, mw):
    # Validate units
    if conc_unit not in valid_units or vol_unit not in valid_units:
        raise ValueError("Invalid unit. Use M, mM, uM, nM for concentration and L, mL, uL for volume.")

    # Convert inputs to base units
    conc_base = convert_to_base(concentration, conc_unit)  # M
    vol_base = convert_to_base(volume, vol_unit)           # L

    # Calculate moles and mass
    moles = conc_base * vol_base
    mass_g = moles * mw
    mass_mg = mass_g * 1000

    # Format result
    result = f"You need {mass_mg:.4f} mg of compound."
    save_log("Molarity-to-Mass", result)
    return result

def calculate_concentration(mass_mg, volume, vol_unit, mw, output_unit):
    if vol_unit not in valid_units or output_unit not in valid_units:
        raise ValueError("Invalid unit. Use L, mL, uL for volume; M, mM, uM, nM for output.")

    vol_base = convert_to_base(volume, vol_unit)
    mass_g = mass_mg / 1000
    moles = mass_g / mw
    conc_base = moles / vol_base
    conc_converted = convert_from_base(conc_base, output_unit)

    result = f"Final concentration is {conc_converted:.4f} {output_unit}."
    save_log("Mass-to-Molarity", result)
    return result

if __name__ == "__main__":
    print("Choose mode:")
    print("1: Calculate mass from molarity")
    print("2: Calculate molarity from mass")

    mode = input("Enter 1 or 2: ").strip()

    try:
        if mode == "1":
            concentration = float(input("Enter desired concentration: "))
            conc_unit = input("Enter concentration unit (e.g., mM): ").strip()
            volume = float(input("Enter final volume: "))
            vol_unit = input("Enter volume unit (e.g., mL): ").strip()
            mw = float(input("Enter molecular weight (g/mol): "))

            print("\n🔬 Calculating...\n")
            print(calculate_mass(concentration, conc_unit, volume, vol_unit, mw))

        elif mode == "2":
            mass = float(input("Enter mass of compound (mg): "))
            volume = float(input("Enter final volume: "))
            vol_unit = input("Enter volume unit (e.g., mL): ").strip()
            mw = float(input("Enter molecular weight (g/mol): "))
            output_unit = input("Enter desired concentration unit (e.g., uM): ").strip()

            print("\n🔬 Calculating...\n")
            print(calculate_concentration(mass, volume, vol_unit, mw, output_unit))

        else:
            print("Invalid option. Please choose 1 or 2.")

    except Exception as e:
        print(f"\n⚠️ Error: {e}")
        print("Please make sure all inputs are valid.")
