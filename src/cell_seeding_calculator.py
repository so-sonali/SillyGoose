from pathlib import Path

# Save an updated version of cell_seeding_calculator.py without emojis
clean_seeding_code = '''
from app_modules.unit_converter import convert_to_base, convert_from_base
from app_modules.logger import save_log

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

def calculate_seeding(cells_per_well, plate_type, num_wells, cell_concentration, user_volume_per_well=None, overage_percent=0):
    if plate_type not in plate_volumes:
        raise ValueError("Unsupported plate type. Choose from: " + ", ".join(plate_volumes.keys()))

    # Use provided volume or calculate it based on cells/concentration
    if user_volume_per_well:
        volume_per_well = user_volume_per_well / 1000  # µL to mL
    else:
        volume_per_well = cells_per_well / cell_concentration  # in mL

    total_volume = volume_per_well * num_wells
    total_volume *= (1 + overage_percent / 100)  # Add extra overage

    volume_per_well_uL = volume_per_well * 1000
    total_volume_uL = total_volume * 1000

    max_vol = plate_volumes[plate_type]

    result = (
        f"Vessel type: {plate_type}\\n"
        f"Cells per well: {cells_per_well:.2e}\\n"
        f"Cell suspension concentration: {cell_concentration:.2e} cells/mL\\n"
        f"Volume per well: {volume_per_well_uL:.2f} µL\\n"
        f"Total volume needed (with {overage_percent}% overage): {total_volume_uL:.2f} µL\\n"
    )

    if volume_per_well_uL > max_vol:
        result += (
            f"WARNING: {volume_per_well_uL:.2f} µL exceeds typical max for {plate_type} ({max_vol} µL).\\n"
            f"Consider using a larger vessel or concentrating your cells.\\n"
        )

    save_log("Cell Seeding", result)
    return result


if __name__ == "__main__":
    print("Available vessels: " + ", ".join(plate_volumes.keys()))

    try:
        cells_per_well = float(input("Desired cells per well: "))
        plate_type = input("Vessel type: ").strip()
        num_wells = int(input("Number of wells: "))
        cell_concentration = float(input("Cell concentration (cells/mL): "))
        custom_vol = input("Provide custom volume per well in µL (leave blank to auto-calculate): ")
        overage_percent = float(input("Overage %: "))

        user_vol = float(custom_vol) if custom_vol else None

        print("\\nCalculating...\\n")
        print(calculate_seeding(
            cells_per_well,
            plate_type,
            num_wells,
            cell_concentration,
            user_vol,
            overage_percent
        ))

    except Exception as e:
        print(f"\\nError: {e}")
'''

# Save to a downloadable file
file_path = Path("/mnt/data/cell_seeding_calculator.py")
#file_path.write_text(clean_seeding_code.strip())
file_path.name
