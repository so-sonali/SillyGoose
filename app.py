
import streamlit as st
from src.cell_seeding_calculator import calculate_seeding
from app_modules import pcr_planner
from app_modules.rna_cdna_dilution import render_rna_cdna_tab
from app_modules.dilution import dilution_calc
from app_modules.molarity_mass import calculate_mass, calculate_concentration

st.set_page_config(page_title="Silly Goose Lab Assistant", layout="centered")

st.title("🧪 Silly Goose Lab Assistant")

tabs = st.tabs([
    "⚖️ Molarity ⇌ Mass",
    "🔁 Dilution Calculator",
    "🧫 Cell Seeding",
    "🧬 RNA → cDNA Dilution",
    "🧪 PCR Mix Planner"
])

# ------------------------- MOLARITY MASS ------------------------
with tabs[0]:
    st.subheader("⚖️ Molarity ⇌ Mass Converter")
    units = ["M", "mM", "uM", "nM", "L", "mL", "uL"]

    with st.form("molarity_mass_form"):
        mode = st.radio("Choose mode", ["Molarity ➜ Mass", "Mass ➜ Molarity"])
        if mode == "Molarity ➜ Mass":
            conc = st.number_input("Desired concentration", value=1.0)
            conc_unit = st.selectbox("Concentration unit", units[:4], index=2)
            vol = st.number_input("Final volume", value=1.0)
            vol_unit = st.selectbox("Volume unit", units[4:], index=1)
            mw = st.number_input("Molecular weight (g/mol)", value=180.16)
        else:
            mass = st.number_input("Mass (mg)", value=1.0)
            vol = st.number_input("Final volume", value=1.0)
            vol_unit = st.selectbox("Volume unit", units[4:], index=1)
            mw = st.number_input("Molecular weight (g/mol)", value=180.16)
            output_unit = st.selectbox("Desired concentration unit", units[:4], index=1)
        submit_molar = st.form_submit_button("Convert")

    if submit_molar:
        try:
            if mode == "Molarity ➜ Mass":
                result = calculate_mass(conc, conc_unit, vol, vol_unit, mw)
            else:
                result = calculate_concentration(mass, vol, vol_unit, mw, output_unit)
            st.success(result)
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ------------------------- DILUTION CALCULATOR ------------------
with tabs[1]:
    st.subheader("🔁 Dilution Calculator")
    units = ["M", "mM", "uM", "nM", "L", "mL", "uL"]
    with st.form("dilution_form"):
        C1 = st.number_input("Stock concentration (C1)", value=10.0)
        C1_unit = st.selectbox("Unit for C1", units, index=1)
        C2 = st.number_input("Desired concentration (C2)", value=1.0)
        C2_unit = st.selectbox("Unit for C2", units, index=2)
        V2 = st.number_input("Final volume (V2)", value=1.0)
        V2_unit = st.selectbox("Unit for V2", units, index=5)
        output_unit = st.selectbox("Output unit for volumes", units, index=5)
        submit_dil = st.form_submit_button("Calculate Dilution")

    if submit_dil:
        try:
            result = dilution_calc(C1, C1_unit, C2, C2_unit, V2, V2_unit, output_unit)
            st.success(result)
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ------------------------- CELL SEEDING --------------------------
with tabs[2]:
    plate_specs = {
        "4": (500, 800),
        "6": (2000, 5000),
        "12": (1000, 3500),
        "24": (500, 1000),
        "48": (200, 500),
        "96": (100, 200),
        "384": (20, 50),
        "4-chamber": (200, 400),
        "8-chamber": (100, 200),
        "100mm": (5000, 12000),
        "T25": (3000, 7000),
        "T75": (7000, 15000)
    }

    with st.form("cell_seeding_form"):
        cells_per_well = st.number_input("Desired cells per well", min_value=1.0, value=5000.0, step=100.0)
        plate_type = st.selectbox("Vessel type", list(plate_specs.keys()), index=5)
        num_wells = st.number_input("Number of wells/flasks", min_value=1, value=40, step=1)
        cell_concentration = st.number_input("Cell suspension concentration (cells/mL)", min_value=1.0, value=1500.0, step=100.0)

        vol_min, vol_max = plate_specs[plate_type]
        user_volume_per_well = st.slider(
            f"Volume per well (choose between {vol_min}–{vol_max} µL)",
            min_value=vol_min,
            max_value=vol_max,
            value=vol_min,
            step=10
        )

        overage_percent = st.slider("Extra volume (safety buffer %)", min_value=0, max_value=50, value=10, step=1)
        submitted = st.form_submit_button("Calculate Seeding Volume")

    if submitted:
        try:
            result = calculate_seeding(
                cells_per_well=cells_per_well,
                plate_type=plate_type,
                num_wells=num_wells,
                cell_concentration=cell_concentration,
                user_volume_per_well=user_volume_per_well,
                overage_percent=overage_percent
            )
            st.success(result)
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ------------------------- RNA TO CDNA --------------------------
with tabs[3]:
    render_rna_cdna_tab()

# ------------------------- PCR PLANNER --------------------------
with tabs[4]:
    pcr_planner.render_pcr_tab()
