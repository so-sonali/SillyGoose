
import streamlit as st
import time

import streamlit as st

def render_timer_tab():
    st.subheader("⏱️ Experiment Timer")
   

    minutes = st.number_input("Set timer (minutes)", min_value=1, value=10, step=1)
    start = st.button("▶️ Start Timer")

    if start:
        total_seconds = int(minutes * 60)
        st.success(f"⏳ Timer started for {minutes} minute(s)")

        progress_bar = st.progress(0)
        status = st.empty()

        for remaining in range(total_seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            time_str = f"{mins:02}:{secs:02}"
            status.info(f"Time left: {time_str}")
            progress_bar.progress((total_seconds - remaining) / total_seconds)
            time.sleep(1)

        status.success("✅ Time's up!")
        progress_bar.empty()
