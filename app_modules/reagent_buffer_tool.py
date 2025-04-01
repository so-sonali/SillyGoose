import streamlit as st

BUFFER_DB = {
    "NaCl": 58.44,
    "Tris": 121.14,
    "EDTA": 292.24,
    "EGTA": 380.4,
    "Glycine": 75.07,
    "HEPES": 238.3,
    "MES": 195.2,
    "Urea": 60.06,
    "NaOH": 40.00,
    "Tricine": 179.2,
    "KCl": 74.56,
    "K2HPO4": 174.18,
    "KH2PO4": 136.09,
    "MgCl2": 95.21,
    "MOPS": 209.27,
    "DTT": 154.3,
}

unit_factors = {
    "M": 1,
    "mM": 1e-3,
    "uM": 1e-6,
    "nM": 1e-9,
}

def render_reagent_buffer_tab():
    st.subheader("🧪 Reagent & Buffer Preparation")
    mode = st.radio("Choose a tool:", ["Calculate mass needed", "Dilute from stock", "Universal Buffer Calculator"])

    if mode == "Calculate mass needed":
        reagent = st.selectbox("Choose a reagent (or type your own):", options=[""] + list(BUFFER_DB.keys()))
        custom_name = ""
        if reagent == "":
            custom_name = st.text_input("Custom reagent name")

        mw = BUFFER_DB.get(reagent, None)
        if not mw:
            mw = st.number_input("Enter molecular weight (g/mol)", value=0.0, min_value=0.0)
        else:
            st.info(f"Molecular weight of {reagent}: **{mw:.2f} g/mol**")

        conc = st.number_input("Desired concentration", value=1.0, min_value=0.0)
        unit = st.selectbox("Concentration unit", list(unit_factors.keys()))
        vol = st.number_input("Final volume to prepare (mL)", value=100.0, min_value=0.0)

        if st.button("📦 Calculate Mass"):
            mol = conc * unit_factors[unit]
            L = vol / 1000
            mass = mol * L * mw
            name = reagent if reagent else custom_name
            if name:
                st.success(f"Add **{mass:.3f} g** of **{name}** and adjust to **{vol:.2f} mL** with distilled water.")
            else:
                st.warning("Please enter a valid reagent name.")

    elif mode == "Dilute from stock":
        stock_conc = st.number_input("Stock concentration", min_value=0.0, value=10.0)
        final_conc = st.number_input("Desired final concentration", min_value=0.0, value=1.0)
        final_vol = st.number_input("Final volume to prepare (mL)", min_value=0.0, value=100.0)

        if st.button("🧪 Calculate volume to use from stock"):
            if final_conc > stock_conc:
                st.error("Final concentration cannot be greater than stock concentration.")
            else:
                v1 = (final_conc * final_vol) / stock_conc
                diluent = final_vol - v1
                st.success(f"Use {v1:.2f} mL of stock and add {diluent:.2f} mL of diluent.")

    elif mode == "Universal Buffer Calculator":
        st.markdown("### 🔢 Universal Buffer Calculator")
        col1, col2 = st.columns(2)
        with col1:
            mw = st.number_input("Molecular Weight (g/mol)", min_value=0.0, value=0.0)
        with col2:
            reagent = st.selectbox("Or choose from common reagents:", [""] + [f"{r} ({mw:.2f})" for r, mw in BUFFER_DB.items()])
            if reagent:
                name = reagent.split(" ")[0]
                mw = BUFFER_DB[name]

        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Weight (g)", value=0.0)
            volume = st.number_input("Volume (mL)", value=0.0)
        with col2:
            conc = st.number_input("Concentration", value=0.0)
            unit = st.selectbox("Unit", list(unit_factors.keys()), index=1)

        calc_type = st.radio("What do you want to calculate?", ["Mass", "Volume", "Concentration"])
        if st.button("🔍 Calculate"):
            mol_factor = unit_factors[unit]
            if calc_type == "Mass":
                try:
                    L = volume / 1000
                    mol = conc * mol_factor
                    result = mol * L * mw
                    st.success(f"Required mass: **{result:.3f} g**")
                except:
                    st.error("Please enter valid volume and concentration.")
            elif calc_type == "Volume":
                try:
                    mol = conc * mol_factor
                    result = weight / (mol * mw) * 1000
                    st.success(f"Required volume: **{result:.2f} mL**")
                except:
                    st.error("Please enter valid weight and concentration.")
            elif calc_type == "Concentration":
                try:
                    L = volume / 1000
                    mol = weight / (mw * L)
                    result = mol / mol_factor
                    st.success(f"Resulting concentration: **{result:.3f} {unit}**")
                except:
                    st.error("Please enter valid weight and volume.")
