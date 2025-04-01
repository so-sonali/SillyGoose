
import streamlit as st

def render_spectro_od_tab():
    import streamlit as st
    st.subheader("📊 Spectrophotometry & OD Tools")
    

    tool = st.radio("Choose tool:", ["Concentration from Absorbance", "Estimate Cell Density (OD600)", "Dilute to Target Absorbance"])

    if tool == "Concentration from Absorbance":
        absorbance = st.number_input("Measured absorbance (A)", min_value=0.0)
        extinction_coeff = st.number_input("Extinction coefficient (ε, M⁻¹cm⁻¹)", min_value=0.0)
        path_length = st.number_input("Path length (cm)", min_value=0.1, value=1.0)

        if st.button("🔬 Calculate concentration"):
            try:
                conc = absorbance / (extinction_coeff * path_length)
                st.success(f"Concentration = {conc:.4e} M")
            except ZeroDivisionError:
                st.error("Extinction coefficient and path length must be greater than zero.")

    elif tool == "Estimate Cell Density (OD600)":
        od600 = st.number_input("OD600 reading", min_value=0.0)
        volume = st.number_input("Culture volume (mL)", min_value=0.0)

        if st.button("🧫 Estimate cell count"):
            est_cells = od600 * 8e8 * volume  # estimate 8×10⁸ cells per mL per unit OD
            st.success(f"Estimated total cells: {est_cells:.2e} cells")

    elif tool == "Dilute to Target Absorbance":
        current_abs = st.number_input("Current absorbance", min_value=0.0)
        target_abs = st.number_input("Target absorbance", min_value=0.0)
        current_vol = st.number_input("Current volume (µL)", min_value=0.0)

        if st.button("🧪 Calculate dilution volume"):
            if current_abs < target_abs:
                st.error("Current absorbance must be higher than target.")
            else:
                new_vol = (current_abs * current_vol) / target_abs
                add_vol = new_vol - current_vol
                st.success(f"Add {add_vol:.2f} µL diluent to reach {target_abs} absorbance.")
