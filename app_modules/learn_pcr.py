
import streamlit as st
import time

def render_learn_pcr_flashcards():
    st.markdown("### 📚 Learn PCR / qPCR (Flashcard Mode)")

    flashcards = [
        {
            "question": "🔬 What does PCR stand for?",
            "answer": "Polymerase Chain Reaction – a technique used to amplify DNA."
        },
        {
            "question": "🧬 What are the three main steps of PCR?",
            "answer": "1️⃣ Denaturation (95°C): DNA strands separate\n2️⃣ Annealing (~55°C): Primers bind\n3️⃣ Extension (72°C): DNA polymerase extends new strands"
        },
        {
            "question": "🧪 What enzyme is used in PCR?",
            "answer": "Taq polymerase – a heat-stable DNA polymerase from *Thermus aquaticus*."
        },
        {
            "question": "📏 What is a primer in PCR?",
            "answer": "A short DNA sequence that binds to the target region to guide DNA polymerase."
        },
        {
            "question": "🔁 What is a PCR cycle?",
            "answer": "One repetition of denaturation, annealing, and extension. Typically 25–35 cycles."
        },
        {
            "question": "💡 What is the difference between PCR and qPCR?",
            "answer": "PCR is typically used to amplify DNA for sequencing or other downstream applications. qPCR is typically used to detect and quantify RNA viruses.RT-PCR is a type of PCR that is used to make cDNA from mRNA template molecules."
        },
        {
            "question": "📈 What is Ct value in qPCR?",
            "answer": "Cycle threshold – the cycle at which fluorescence exceeds background and DNA is detected."
        }
    ]

    if "flashcard_index" not in st.session_state:
        st.session_state.flashcard_index = 0
        st.session_state.show_answer = False

    current = st.session_state.flashcard_index

    st.info(flashcards[current]["question"])

    if st.session_state.show_answer:
        st.success(flashcards[current]["answer"])

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("◀️ Previous", key="prev_btn") and current > 0:
            st.session_state.flashcard_index -= 1
            st.session_state.show_answer = False
            st.rerun()
    with col2:
        if st.button("💡 Show Answer", key="toggle_answer"):
            st.session_state.show_answer = not st.session_state.show_answer
            st.rerun()
    with col3:
        if st.button("Next ▶️", key="next_btn") and current < len(flashcards) - 1:
            st.session_state.flashcard_index += 1
            st.session_state.show_answer = False
            st.rerun()


def render_pcr_timeline():
    st.markdown("### 🧬 PCR Cycle Animation")

    steps = [
        ("🔬 Initial Denaturation", "Heating to ~95°C to separate double-stranded DNA."),
        ("🧲 Annealing", "Cooling to ~55°C so primers bind to their target sequences."),
        ("🧪 Extension", "Heating to ~72°C so Taq polymerase synthesizes new DNA strands.")
    ]

    for i, (title, desc) in enumerate(steps):
        st.markdown(f"#### Step {i+1}: {title}")
        with st.spinner("Animating..."):
            time.sleep(1.2)
        st.info(desc)
        st.progress((i+1)/len(steps))
        time.sleep(0.3)

    st.success("🔁 This completes one PCR cycle. Repeat for 25–35 cycles.")
