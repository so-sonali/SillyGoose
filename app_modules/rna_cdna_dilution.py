
import streamlit as st

def render_rna_cdna_tab():
    st.subheader("🧬 RNA to cDNA Dilution Calculator")

    with st.form("rna_cdna_form"):
        stock_conc = st.number_input("RNA stock concentration (ng/µL)", min_value=0.1, value=500.0)
        desired_conc = st.number_input("Desired RNA concentration (ng/µL)", min_value=0.1, value=50.0)
        final_volume = st.number_input("Final RT reaction volume (µL)", min_value=1.0, value=20.0)

        submitted = st.form_submit_button("🧪 Calculate")

    if submitted:
        try:
            vol_rna = (desired_conc * final_volume) / stock_conc
            vol_water = final_volume - vol_rna

            st.success(f"🔬 Add {vol_rna:.2f} µL of RNA stock")
            st.info(f"💧 Add {vol_water:.2f} µL of nuclease-free water")
        except Exception as e:
            st.error(f"❌ Error: {e}")
