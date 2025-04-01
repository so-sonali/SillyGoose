
import streamlit as st
import pandas as pd

def render_plate_layout_tab():
    import streamlit as st
    st.subheader("🧪 Plate Layout Helper")
   
    st.write("Design your experiment layout for any plate format (6 to 384 wells).")

    plate_type = st.selectbox("Choose plate type", options=["6", "12", "24", "48", "96", "384"])
    rows_dict = {"6": 2, "12": 3, "24": 4, "48": 6, "96": 8, "384": 16}
    cols_dict = {"6": 3, "12": 4, "24": 6, "48": 8, "96": 12, "384": 24}

    rows = rows_dict[plate_type]
    cols = cols_dict[plate_type]

    layout = pd.DataFrame("", index=[chr(65+i) for i in range(rows)], columns=[str(j+1) for j in range(cols)])

    st.write("👆 Click any cell to label it (e.g., control, treatment A, etc.)")

    edited = st.data_editor(layout, key="plate_layout_editor")

    st.write("🧾 Final Layout:")
    st.dataframe(edited)

    st.download_button("📥 Download Layout as CSV", data=edited.to_csv(index=True).encode("utf-8"),
                       file_name=f"{plate_type}_well_plate_layout.csv", mime="text/csv")
