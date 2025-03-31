import streamlit as st
from app_modules.dilution import dilution_calc
from app_modules.molarity_mass import calculate_mass, calculate_concentration
from app_modules.cell_seeding import calculate_seeding

st.set_page_config(page_title="Silly Goose 🧪", layout="centered")

st.title("🧪 Silly Goose - Bio Lab Assistant")
st.markdown("A handy toolkit for scientists doing common calculations 🧬")

# Sidebar navigation
tool = st.sidebar.radio("Choose a tool:", [
    "Dilution Calculator",
    "Molarity ↔ Mass Converter",
    "Cell Seeding Calculator"
])

# ------------------------- DILUTION TOOL -------------------------
if tool == "Dilution Calculator":
    st.header("🔁 Dilution Calculator")

    C1 = st.number_input("Stock concentration (C1)", min_value=0.0, step=0.01)
    C1_unit = st.selectbox("C1 Unit", ["M", "mM", "uM", "nM"])

    C2 = st.number_input("Desired concentration (C2)", min_value=0.0, step=0.01)
    C2_unit = st.selectbox("C2 Unit", ["M", "mM", "uM", "nM"])

    V2 = st.number_input("Final volume (V2)", min_value=0.0, step=0.01)
    V2_unit = st.selectbox("V2 Unit", ["L", "mL", "uL"])

    output_unit = st.selectbox("Output volume unit", ["L", "mL", "uL"])

    if st.button("Calculate Dilution"):
        try:
            result = dilution_calc(C1, C1_unit, C2, C2_unit, V2, V2_unit, output_unit)
            st.success(result)
        except Exception as e:
            st.error(f"Error: {e}")

# ---------------------- MOLARITY ↔ MASS -------------------------
elif tool == "Molarity ↔ Mass Converter":
    st.header("⚖️ Molarity ↔ Mass Converter")

    mode = st.radio("Choose conversion mode", ["Molarity ➜ Mass", "Mass ➜ Molarity"])

    if mode == "Molarity ➜ Mass":
        conc = st.number_input("Desired concentration", min_value=0.0, step=0.01)
        conc_unit = st.selectbox("Concentration unit", ["M", "mM", "uM", "nM"])
        volume = st.number_input("Final volume", min_value=0.0, step=0.01)
        vol_unit = st.selectbox("Volume unit", ["L", "mL", "uL"])
        mw = st.number_input("Molecular weight (g/mol)", min_value=0.0, step=0.01)

        if st.button("Calculate Mass"):
            try:
                result = calculate_mass(conc, conc_unit, volume, vol_unit, mw)
                st.success(result)
            except Exception as e:
                st.error(f"Error: {e}")

    else:
        mass = st.number_input("Mass (mg)", min_value=0.0, step=0.01)
        volume = st.number_input("Final volume", min_value=0.0, step=0.01)
        vol_unit = st.selectbox("Volume unit", ["L", "mL", "uL"])
        mw = st.number_input("Molecular weight (g/mol)", min_value=0.0, step=0.01)
        conc_unit = st.selectbox("Desired concentration unit", ["M", "mM", "uM", "nM"])

        if st.button("Calculate Molarity"):
            try:
                result = calculate_concentration(mass, volume, vol_unit, mw, conc_unit)
                st.success(result)
            except Exception as e:
                st.error(f"Error: {e}")

# ---------------------- CELL SEEDING TOOL -------------------------
elif tool == "Cell Seeding Calculator":
    st.header("🧫 Cell Seeding Calculator")

    cells_per_well = st.number_input("Desired cells per well", min_value=0.0, step=100.0)
    vessel_type = st.selectbox("Vessel type", [
        "4", "6", "12", "24", "48", "96", "384", "4-chamber", "8-chamber", "100mm", "T25", "T75"
    ])
    num_wells = st.number_input("Number of wells/flasks", min_value=1, step=1)
    concentration = st.number_input("Cell suspension concentration (cells/mL)", min_value=1.0, step=100.0)
    overage = st.slider("Extra volume (safety buffer)", 0, 50, 10)

    if st.button("Calculate Seeding Volume"):
        try:
            result = calculate_seeding(cells_per_well, vessel_type, num_wells, concentration, overage)
            st.success(result)
        except Exception as e:
            st.error(f"Error: {e}")
