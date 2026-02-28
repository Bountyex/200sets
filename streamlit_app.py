import streamlit as st
import threading
import time
from generator_core import generate_sets

st.set_page_config(page_title="Pro Grid Generator", layout="wide")

st.title("🔥 Pro Multi Grid Generator")

# ---------------------------
# SESSION STATE
# ---------------------------
if "running" not in st.session_state:
    st.session_state.running = False

if "results" not in st.session_state:
    st.session_state.results = []

cancel_flag = {"stop": False}

# ---------------------------
# UI CONTROLS
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    total_sets = st.number_input("Total Sets", 1, 50000, 2000)

with col2:
    grid_size = st.number_input("Grid Size", 2, 10, 5)

start_btn = st.button("🚀 Start Generation")
cancel_btn = st.button("⛔ Cancel")

progress_bar = st.progress(0)
status_text = st.empty()
preview_box = st.empty()

# ---------------------------
# CALLBACK (LIVE STREAM)
# ---------------------------
def progress_callback(done, eta, latest_grid):

    progress_bar.progress(done / total_sets)

    status_text.write(
        f"Generated: {done}/{total_sets} | ETA: {int(eta)} sec"
    )

    preview_box.code(latest_grid)

# ---------------------------
# THREAD WORKER
# ---------------------------
def worker():
    st.session_state.results = generate_sets(
        total_sets,
        grid_size,
        progress_callback,
        cancel_flag
    )
    st.session_state.running = False


# ---------------------------
# START
# ---------------------------
if start_btn and not st.session_state.running:
    cancel_flag["stop"] = False
    st.session_state.running = True

    thread = threading.Thread(target=worker)
    thread.start()

# ---------------------------
# CANCEL
# ---------------------------
if cancel_btn:
    cancel_flag["stop"] = True
    st.session_state.running = False
    st.warning("Generation cancelled.")

# ---------------------------
# DOWNLOAD
# ---------------------------
if st.session_state.results:
    output_text = "\n\n".join(st.session_state.results)

    st.download_button(
        "⬇ Download Result",
        output_text,
        "generated_sets.txt"
    )
