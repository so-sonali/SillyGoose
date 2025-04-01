from app_modules.unit_converter import convert_to_base, convert_from_base
from app_modules.logger import save_log

valid_units = ["M", "mM", "uM", "nM", "L", "mL", "uL"]

def dilution_calc(C1, C1_unit, C2, C2_unit, V2, V2_unit, output_vol_unit):
    # Unit validation
    for unit in [C1_unit, C2_unit, V2_unit, output_vol_unit]:
        if unit not in valid_units:
            raise ValueError(f"Invalid unit: {unit}. Must be one of: {', '.join(valid_units)}")

    # Convert to base units
    C1_base = convert_to_base(C1, C1_unit)
    C2_base = convert_to_base(C2, C2_unit)
    V2_base = convert_to_base(V2, V2_unit)

    # Validity check
    if C2_base > C1_base:
        raise ValueError("Desired concentration (C2) cannot be greater than stock concentration (C1).")

    V1_base = (C2_base * V2_base) / C1_base
    if V1_base > V2_base:
        raise ValueError("Calculated volume of stock exceeds total final volume (V2).")

    diluent_base = V2_base - V1_base

    # Convert back to desired output units
    V1 = convert_from_base(V1_base, output_vol_unit)
    diluent = convert_from_base(diluent_base, output_vol_unit)

    # Use scientific notation if numbers are tiny
    if V1 < 0.01 or diluent < 0.01:
        result = f"Use {V1:.2e} {output_vol_unit} of stock and add {diluent:.2e} {output_vol_unit} of diluent."
    else:
        result = f"Use {V1:.2f} {output_vol_unit} of stock and add {diluent:.2f} {output_vol_unit} of diluent."

    save_log("Dilution Calculator", result)
    return result


if __name__ == "__main__":
    print("Available units: M, mM, uM, nM, L, mL, uL")

    try:
        C1 = float(input("Enter stock concentration (C1): "))
        C1_unit = input("Enter unit for C1 (e.g., mM): ").strip()

        C2 = float(input("Enter desired concentration (C2): "))
        C2_unit = input("Enter unit for C2 (e.g., uM): ").strip()

        V2 = float(input("Enter final volume (V2): "))
        V2_unit = input("Enter unit for V2 (e.g., uL): ").strip()

        output_vol_unit = input("Enter desired unit for output volumes (e.g., uL): ").strip()

        print("\n🔬 Calculating...\n")
        print(dilution_calc(C1, C1_unit, C2, C2_unit, V2, V2_unit, output_vol_unit))

    except Exception as e:
        print(f"\n⚠️ Error: {e}")
        print("Please make sure you entered valid numbers and units.")
