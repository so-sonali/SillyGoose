
import streamlit as st
from datetime import datetime
from app_modules.learn_pcr import render_learn_pcr_flashcards

def render_pcr_tab():
    st.subheader("🧪 Advanced PCR/qPCR Mix Planner")

    if st.toggle("📚 Learn PCR / qPCR"):
        render_learn_pcr_flashcards()
        st.markdown("---")

    st.markdown("Add your reagents, enter stock/final concentrations, and get your master mix.")

    with st.form("pcr_mix_form"):
        num_reactions = st.number_input("Number of reactions", min_value=1, value=10)
        reaction_volume = st.number_input("Total volume per reaction (µL)", min_value=1.0, value=20.0)
        overage_percent = st.slider("Extra % overage", 0, 100, 10)

        reagent_count = st.number_input("How many reagents do you want to add?", min_value=1, value=5, step=1)

        reagent_data = []
        for i in range(reagent_count):
            col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
            with col1:
                name = st.text_input(f"Reagent {i+1} name", value=f"Reagent{i+1}", key=f"name_{i}")
            with col2:
                stock = st.number_input("Stock Conc", min_value=0.0, value=10.0, key=f"stock_{i}")
            with col3:
                final = st.number_input("Final Conc", min_value=0.0, value=1.0, key=f"final_{i}")
            with col4:
                note = st.text_input("Note (optional)", value="", key=f"note_{i}")
            reagent_data.append((name, stock, final, note))

        submitted = st.form_submit_button("🧪 Calculate Mix")

    if submitted:
        try:
            total_reactions = num_reactions * (1 + overage_percent / 100)
            total_volume = reaction_volume * total_reactions
            result_lines = []
            water_volume = total_volume

            result_lines.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            result_lines.append(f"Total reactions (with overage): {total_reactions:.1f}")
            result_lines.append(f"Final mix volume: {total_volume:.2f} µL\n")

            for name, stock, final, note in reagent_data:
                if stock == 0:
                    vol = 0
                else:
                    vol = (final / stock) * reaction_volume
                total = vol * total_reactions
                water_volume -= total
                line = f"🧪 {name}: {total:.2f} µL ({vol:.2f} µL/reaction)"
                if note:
                    line += f" — {note}"
                result_lines.append(line)

            result_lines.append(f"💧 Nuclease-Free Water: {water_volume:.2f} µL")
            result_lines.append("\n✅ Ready to prepare your master mix.")

            result = "\n".join(result_lines)
            st.success(result)

            with open("logs/calculation_history.txt", "a", encoding="utf-8") as log:
                log.write(result + "\n\n")

        except Exception as e:
            st.error(f"❌ Error: {e}")
