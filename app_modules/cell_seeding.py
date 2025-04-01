
from app_modules.logger import save_log

plate_specs = {
    "4": {"max_vol": 800, "range": (500, 800)},
    "6": {"max_vol": 5000, "range": (2000, 5000)},
    "12": {"max_vol": 3500, "range": (1000, 3500)},
    "24": {"max_vol": 1000, "range": (500, 1000)},
    "48": {"max_vol": 500, "range": (200, 500)},
    "96": {"max_vol": 200, "range": (100, 200)},
    "384": {"max_vol": 50, "range": (20, 50)},
    "4-chamber": {"max_vol": 400, "range": (200, 400)},
    "8-chamber": {"max_vol": 200, "range": (100, 200)},
    "100mm": {"max_vol": 12000, "range": (5000, 12000)},
    "T25": {"max_vol": 7000, "range": (3000, 7000)},
    "T75": {"max_vol": 15000, "range": (7000, 15000)}
}

def format_volume(vol_uL):
    if vol_uL >= 1000:
        return f"{vol_uL / 1000:.2f} mL"
    else:
        return f"{vol_uL:.2f} µL"

def calculate_smart_seeding(cells_per_well, plate_type, num_wells, cell_concentration, user_volume_per_well, overage_percent=0):
    if plate_type not in plate_specs:
        raise ValueError("Unsupported plate type.")

    total_volume_uL = user_volume_per_well * num_wells * (1 + overage_percent / 100)

    total_cells_needed = cells_per_well * num_wells
    volume_of_cells_uL = (total_cells_needed / cell_concentration) * 1000

    media_volume_uL = total_volume_uL - volume_of_cells_uL
    max_vol = plate_specs[plate_type]["max_vol"]

    result = (
        f"🧫 Vessel type: {plate_type}-well\n"
        f"🧬 Cells per well: {cells_per_well:,.0f}\n"
        f"📦 Cell concentration: {cell_concentration:,.2f} cells/mL\n"
        f"🧪 Volume per well: {user_volume_per_well:.0f} µL\n"
        f"🔢 Number of wells: {num_wells}\n"
        f"🧪 Total volume needed (with {overage_percent}% overage): {format_volume(total_volume_uL)}\n\n"
        f"🔬 Add {format_volume(volume_of_cells_uL)} of cell suspension\n"
        f"➕ Mix with {format_volume(media_volume_uL)} of fresh media\n"
    )

    if user_volume_per_well > max_vol:
        result += (
            f"\n⚠️ WARNING: {user_volume_per_well:.0f} µL exceeds recommended max per well ({max_vol} µL)\n"
            f"👉 Consider reducing volume or switching to a larger format."
        )

    save_log("Smart Cell Seeding", result)
    return result
