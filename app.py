import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

st.title("📈 Online Function Plotter")

st.write("Enter one or more functions in terms of `x`. Example: `sin(x)`, `x**2 + 3*x`, `exp(x)`")

# Store multiple functions
if "functions" not in st.session_state:
    st.session_state.functions = []

# Input for new function
func_text = st.text_input("Enter a new function f(x):", "sin(x)")
color = st.color_picker("Pick a color", "#0000FF")

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Add function"):
        if func_text:
            st.session_state.functions.append((func_text, color))

with col2:
    if st.button("🗑 Clear all"):
        st.session_state.functions = []

# Show list of added functions
if st.session_state.functions:
    st.subheader("Functions added:")
    for f, c in st.session_state.functions:
        st.markdown(f"- <span style='color:{c}'>{f}</span>", unsafe_allow_html=True)

# Domain inputs
x_min = st.number_input("X min", value=-10)
x_max = st.number_input("X max", value=10)

# Plotting
if st.button("📊 Plot"):
    fig, ax = plt.subplots()
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True)

    x = sp.symbols('x')

    for func_text, color in st.session_state.functions:
        try:
            expr = sp.sympify(func_text)
            f = sp.lambdify(x, expr, modules=['numpy'])
            X = np.linspace(x_min, x_max, 500)
            Y = f(X)
            ax.plot(X, Y, label=func_text, color=color)
        except Exception as e:
            st.error(f"❌ Error in {func_text}: {e}")

    ax.legend()
    st.pyplot(fig)
