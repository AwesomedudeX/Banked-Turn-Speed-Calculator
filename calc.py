import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sn

st.set_page_config("Maximum Speed on Banked Turns", layout="wide", initial_sidebar_state="expanded")

def sin(x):
    return np.sin(x/180*np.pi)

def cos(x):
    return np.cos(x/180*np.pi)

def calcv(x, r, f, g=9.81):
    return np.sqrt(r * g * (f * cos(x) + sin(x)) / (cos(x) - (f * sin(x))))

def calcx(v, r, f, g=9.81):
    return np.arctan( ( f - (v**2 / (r*g)) ) / ( -(f * v**2 / (r*g)) - 1 ) )

sidebar = st.sidebar

mode = sidebar.radio("Calculator Mode:", ["Calculate Maximum Speed", "Calculate Minimum Bank Angle", "Graph", "Table"])

if mode == "Calculate Maximum Speed":

    st.title("Maximum Speed Calculator")
    
    unit = sidebar.radio("Speed Unit:", ["M/S", "KM/H", "MPH"])

    x = st.number_input("Bank Angle (degrees):", min_value=0)
    r = st.number_input("Turn Radius (meters):", value=100)
    f = 1.7
    
    cond = st.radio("Road Conditions (with a regular vehicle, except for F1):", ["Formula 1 (F1 racecar and track)", "Dry Road", "Wet Road", "Snowy Road", "Icy Road"])

    if cond == "Formula 1 - Dry Road (F1 racecar and track)":
        f = 1.7

    elif cond == "Dry Road":
        f = 0.75

    elif cond == "Wet Road":
        f = 0.45

    elif cond == "Snowy Road":
        f = 0.25

    elif cond == "Icy Road":
        f = 0.15

    if st.button("Calculate"):
        
        v = calcv(x, r, f)
        v = str(v)

        if v == "nan":

            if str(calcv(0, r, f)) != "nan":
                st.write("This bank angle is too steep to be used for this calculation. Please enter a lower bank angle.")

            else:
                st.write("The result of the given values cannot be obtained. Please enter a valid set of values.")

        else:

            v = float(v)

            if unit == "M/S":
                st.write(f"**Maximum Speed:** *{round(v, 3)} m/s*")

            elif unit == "KM/H":
                st.write(f"**Maximum Speed:** *{round(v * 3.6, 3)} km/h*")

            elif unit == "MPH":
                st.write(f"**Maximum Speed:** *{round(v * 3.6 / 1.609, 3)} mph*")

elif mode == "Calculate Minimum Bank Angle":

    st.title("Minimum Bank Angle Calculator")

    unit = sidebar.radio("Angle Unit:", ["Degrees", "Radians"])

    v = st.number_input("Target Speed:", min_value=0)
    r = st.number_input("Turn Radius (meters):", value=100)
    f = 1.7

    cond = st.radio("Road Conditions (with a regular vehicle, except for F1):", ["Formula 1 (F1 racecar and track)", "Dry Road", "Wet Road", "Snowy Road", "Icy Road"])

    if cond == "Formula 1 - Dry Road (F1 racecar and track)":
        f = 1.7

    elif cond == "Dry Road":
        f = 0.75

    elif cond == "Wet Road":
        f = 0.45

    elif cond == "Snowy Road":
        f = 0.25

    elif cond == "Icy Road":
        f = 0.15

    if st.button("Calculate"):
        
        x = calcx(v, r, f)
        x = str(x)

        if x == "nan":
            st.write("The result of the given values cannot be obtained. Please enter a valid set of values.")

        else:

            x = float(x)

            if x < 0:
                x = 0

            if unit == "Degrees":
                if x != 0:
                    x = x / (2*np.pi) * 180
                st.write(f"**Minimum Bank Angle:** *{round(x, 3)} degrees*")

            else:
                st.write(f"**Minimum Bank Angle:** *{round(x, 3)} rad.*")

else:

    st.title(f"{mode} View")

    cond = sidebar.radio("Road Conditions (with a regular vehicle, except for F1):", ["Formula 1 (F1 racecar and track)", "Dry Road", "Wet Road", "Snowy Road", "Icy Road"])
    f = 1.7

    if cond == "Formula 1 - Dry Road (F1 racecar and track)":
        f = 1.7

    elif cond == "Dry Road":
        f = 0.75

    elif cond == "Wet Road":
        f = 0.45

    elif cond == "Snowy Road":
        f = 0.25

    elif cond == "Icy Road":
        f = 0.15

    unit = sidebar.radio("Speed Unit:", ["M/S", "KM/H", "MPH"])

    r = sidebar.number_input("Turn Radius (meters):", value=100)
    minb = sidebar.number_input("Minimum Bank Angle:", value=-41)
    maxb = sidebar.number_input("Maximum Bank Angle:", value=45)

    if mode == "Graph":

        c1, c2, c3, c4 = st.columns(4)

        p = sidebar.number_input("Distance Between `x` Values (smoothness):", step=0.01, value=1.0)
        x = np.arange(minb, maxb+1, p)

        if unit == "M/S":
            y = [round(calcv(a, r, f), 3) for a in x]

        elif unit == "KM/H":
            y = [round(calcv(a, r, f), 3) * 3.6 for a in x]

        elif unit == "MPH":
            y = [round(calcv(a, r, f), 3) * 3.6 / 1.609 for a in x]

        if c1.checkbox("Dark Graph Theme"):
            plt.style.use("dark_background")
        
        else:
            plt.style.use("default")

        fig, ax = plt.subplots()

        if c2.checkbox("Show Line Plot", True):
            sn.lineplot(x=x, y=y, color="yellow", size_norm=1)

        if c3.checkbox("Show Scatter Plot", True):
            sn.scatterplot(x=x, y=y, size=p, color="blue")
        
        plt.xlabel("Bank Angle (degrees)")
        plt.ylabel("Maximum Speed (m/s)")

        if c4.checkbox("Vertical Line at  `x = 0`", True):
            plt.axvline(0, color="red")

        st.pyplot(fig)

    else:

        x = np.arange(minb, maxb+1, 1)

        if unit == "M/S":
            y = [round(calcv(a, r, f), 3) for a in x]

        elif unit == "KM/H":
            y = [round(calcv(a, r, f), 3) * 3.6 for a in x]

        elif unit == "MPH":
            y = [round(calcv(a, r, f), 3) * 3.6 / 1.609 for a in x]
        
        for i in range(len(y)):
            if str(y[i]) == "nan":
                y[i] = "Cannot Be Calculated"

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
