from logger import save_log

# Vessel → typical max µL volume per well
plate_volumes = {
    "4": 800,
    "6": 5000,
    "12": 3500,
    "24": 1000,
    "48": 500,
    "96": 200,
    "384": 50,
    "4-chamber": 400,
    "8-chamber": 200,
    "100mm": 12000,
    "T25": 7000,
    "T75": 15000
}

def calculate_seeding(cells_per_well, plate_type, num_wells, cell_concentration, overage_percent=0):
    if plate_type not in plate_volumes:
        raise ValueError("Unsupported plate type. Choose from: " + ", ".join(plate_volumes.keys()))

    volume_per_well = cells_per_well / cell_concentration  # in mL
    total_volume = volume_per_well * num_wells

    # Add extra overage if desired
    total_volume *= (1 + overage_percent / 100)

    # Convert to µL
    volume_per_well_uL = volume_per_well * 1000
    total_volume_uL = total_volume * 1000

    max_vol = plate_volumes[plate_type]

    result = (
        f"Vessel type: {plate_type}\n"
        f"Cells per well: {cells_per_well:.2e}\n"
        f"Cell suspension concentration: {cell_concentration:.2e} cells/mL\n"
        f"Volume per well: {volume_per_well_uL:.2f} µL\n"
        f"Total volume needed (with {overage_percent}% overage): {total_volume_uL:.2f} µL\n"
    )

    if volume_per_well_uL > max_vol:
        result += (
            f"WARNING: {volume_per_well_uL:.2f} µL exceeds typical max volume for {plate_type} ({max_vol} µL).\n"
            f"Consider concentrating your cells or using a larger format.\n"
        )

    save_log("Cell Seeding", result)
    return result

if __name__ == "__main__":
    print("Available vessels: 4, 6, 12, 24, 48, 96, 384, 4-chamber, 8-chamber, 100mm, T25, T75")

    try:
        cells_per_well = float(input("Enter desired cells per well: "))
        plate_type = input("Enter vessel type (e.g., 6, 96, T25, 4-chamber): ").strip()
        num_wells = int(input("Enter number of wells/flasks/dishes to plate: "))
        cell_concentration = float(input("Enter cell suspension concentration (cells/mL): "))
        overage_percent = float(input("Add extra volume? Enter % overage (e.g., 10 for 10% extra): "))

        print("\nCalculating...\n")
        print(calculate_seeding(cells_per_well, plate_type, num_wells, cell_concentration, overage_percent))

    except Exception as e:
        print(f"\nError: {e}")
        print("Please make sure all inputs are valid.")
