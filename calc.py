import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sn

st.set_page_config("Maximum Speed on Banked Turns", layout="wide", initial_sidebar_state="expanded")

def sin(x):
    return np.sin(x/180*np.pi)

def cos(x):
    return np.cos(x/180*np.pi)

def calc(x, r, f, g=9.81):
    return np.sqrt(r * g * (f * cos(x) + sin(x)) / (cos(x) - (f * sin(x))))

sidebar = st.sidebar

mode = sidebar.radio("Calculator Mode:", ["Single Value", "Graph", "Table"])
unit = sidebar.radio("Speed Unit:", ["M/S", "KM/H", "MPH"])

if mode == "Single Value":

    st.title("Maximum Speed Calculator")

    x = st.number_input("Bank Angle (degrees):", min_value=-45, max_value=45)
    r = st.number_input("Turn Radius (meters):")
    f = st.number_input("Friction Coefficient:")

    if st.button("Calculate"):
        
        v = calc(x, r, f)

        if unit == "M/S":
            st.write(f"**Maximum Speed:** *{round(v, 3)} m/s*")

        elif unit == "KM/H":
            st.write(f"**Maximum Speed:** *{round(v * 3.6, 3)} km/h*")

        elif unit == "MPH":
            st.write(f"**Maximum Speed:** *{round(v * 3.6 / 1.609, 3)} mph*")

else:

    st.write(":grey[Results for angles less than -41 degrees become unusable, and angles higher than 45 degrees become unreasonable, so they have been excluded.]")

    r = sidebar.number_input("Turn Radius (meters):", value=100)
    f = sidebar.number_input("Friction Coefficient:", value=0.9)
    minb = sidebar.number_input("Minimum Bank Angle:", value=-41, min_value=-41)
    maxb = sidebar.number_input("Maximum Bank Angle:", value=45, max_value=45)

    if mode == "Graph":

        st.title("Graph Display")

        c1, c2, c3, c4 = st.columns(4)

        p = sidebar.number_input("Distance Between `x` Values (smoothness):", step=0.01, value=1.0)
        x = np.arange(minb, maxb+1, p)

        if unit == "M/S":
            y = [round(calc(a, r, f), 3) for a in x]

        elif unit == "KM/H":
            y = [round(calc(a, r, f), 3) * 3.6 for a in x]

        elif unit == "MPH":
            y = [round(calc(a, r, f), 3) * 3.6 / 1.609 for a in x]

        if c1.checkbox("Dark Graph Theme"):
            plt.style.use("dark_background")
        
        else:
            plt.style.use("default")

        fig, ax = plt.subplots()

        if c2.checkbox("Show Line Plot"):
            sn.lineplot(x=x, y=y, color="yellow", size_norm=1)

        if c3.checkbox("Show Scatter Plot"):
            sn.scatterplot(x=x, y=y, size=p, color="blue")
        
        plt.xlabel("Bank Angle (degrees)")
        plt.ylabel("Maximum Speed (m/s)")

        if c4.checkbox("Vertical Line at `x=0`"):
            plt.axvline(0, color="red")

        st.pyplot(fig)

    else:

        x = np.arange(minb, maxb+1, 1)

        if unit == "M/S":
            y = [round(calc(a, r, f), 3) for a in x]

        elif unit == "KM/H":
            y = [round(calc(a, r, f), 3) * 3.6 for a in x]

        elif unit == "MPH":
            y = [round(calc(a, r, f), 3) * 3.6 / 1.609 for a in x]

        if unit == "M/S":
            
            data = {
                "Bank Angle (degrees)": x,
                "Max. Speed (M/S)": y
            }

        elif unit == "KM/H":
            
            data = {
                "Bank Angle (degrees)": x,
                "Max. Speed (KM/H)": y
            }

        elif unit == "MPH":
            
            data = {
                "Bank Angle (degrees)": x,
                "Max. Speed (MPH)": y
            }

        st.dataframe(data, use_container_width=True, hide_index=True)
