import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.set_page_config(layout="wide")

# Session State für den Expander-Zustand initialisieren
if "expander_open" not in st.session_state:
    st.session_state.expander_open = False

# CSS: Maximale Gesamtbreite der Seite begrenzen & Eingabefeld-Breite anpassen
st.markdown("""
<style>
    /* Gesamtbreite der Seite auf z. B. 900px deckeln (nicht ganz so breit) */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
    }
    
    /* Eingabefeld und Antwortbox auf 300px begrenzen */
    div[data-testid="stTextInput"], 
    div[data-testid="stAlert"] {
        max-width: 300px;
    }

    /* 1. Zeile: Frage ("Who is the Goat of Basketball?") */
    div[data-testid="stTextInput"] label {
        font-size: 1.4rem !important;
        font-weight: bold !important;
    }

    /* 2. Zeile: Eingabe-Text ("MJ") */
    div[data-testid="stTextInput"] input {
        font-size: 1.2rem !important;
    }
</style>
""", unsafe_allow_html=True)


text = "Mark's first App with streamlit"
colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#FF8333", "#33FFD1", "#FF33A8"]
letters = [f'<span style="color:{colors[i % len(colors)]};">{c}</span>' if c != " " else "&nbsp;" for i, c in enumerate(text)]
st.markdown(f'<h1 style="font-family: serif; font-size: 3.5rem;">{"".join(letters)}</h1>', unsafe_allow_html=True)

# Logik für die Antwort
with st.form("goat_form"):
    user_input = st.text_input("Who is the Goat of Basketball?")
    submitted = st.form_submit_button("Submit")

if submitted and user_input:
    answer = user_input.strip().lower()
    
    if any(goat in answer for goat in ["mj", "jordan", "michael jordan"]):
        st.balloons()
        st.success("That is correct!")
    elif any(lebron in answer for lebron in ["lebron", "james", "king james"]):
        st.image("MJ_lol.gif")  # Passe den Dateinamen deines LeBron-GIFs hier an
        st.error("Nice try! But LeBron is not the GOAT, Michael Jordan is!")
    else:
        st.image("MJ_dunk.gif")
        st.error("That is wrong, it is Michael Jordan!")
        
st.html("<div style='height: 100px;'></div>")  # Abstand anpassen

#=====================================================================================================================================
# mortgage calculator (mit dynamischem Expander-Zustand)
expander = st.expander("Mortgage Repayments Calculator - Just for fun 😊", expanded=st.session_state.expander_open)

with expander:
    # Sobald Interaktionen im Expander stattfinden, bleibt st.session_state.expander_open auf True
    st.session_state.expander_open = True

    st.write("### Input Data")
    col1, col2 = st.columns(2)
    home_value = col1.number_input("Home Value", min_value=0, value=500000, step=10000)
    deposit = col1.number_input("Deposit", min_value=0, value=100000, step=10000)
    interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value=5.5, step=0.5)
    loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)
    
    # Calculate the repayments.
    loan_amount = home_value - deposit
    monthly_interest_rate = (interest_rate / 100) / 12
    number_of_payments = loan_term * 12
    monthly_payment = (
        loan_amount
        * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
        / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    )
    
    # Display the repayments.
    total_payments = monthly_payment * number_of_payments
    total_interest = total_payments - loan_amount
    
    st.write("### Repayments")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
    col2.metric(label="Total Repayments", value=f"${total_payments:,.0f}")
    col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")
    
    # Create a data-frame with the payment schedule.
    schedule = []
    remaining_balance = loan_amount
    
    for i in range(1, number_of_payments + 1):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        year = math.ceil(i / 12)  # Calculate the year into the loan
        schedule.append(
            [
                i,
                monthly_payment,
                principal_payment,
                interest_payment,
                remaining_balance,
                year,
            ]
        )
    
    df = pd.DataFrame(
        schedule,
        columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
    )
    
    # Display the data-frame as a chart.
    st.write("### Payment Schedule")
    payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
    st.line_chart(payments_df)

