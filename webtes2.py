import streamlit as s

# Menentukan halaman yang aktif
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Definisi halaman Home
if st.session_state.page == "Home":
    st.title("Home")
    st.write("Ini adalah halaman Home.")
    if st.button("Lanjutkan ke Page 2"):
        st.session_state.page = "Page 2"

# Definisi halaman Page 2
elif st.session_state.page == "Page 2":
    st.title("Page 2")
    st.write("Ini adalah halaman kedua.")
    if st.button("Kembali ke Home"):
        st.session_state.page = "Home"
