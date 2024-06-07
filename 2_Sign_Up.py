import streamlit as st
from streamlit_option_menu import option_menu
import calendar
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from database import *


# ---------------Settings -----------------

page_title = "Posh Lounge | Check In"
page_icon = "💅"
layout = "centered"


# -----------------------------------------

st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout,
    initial_sidebar_state="collapsed",
)
st.title("Welcome to Posh Nail Lounge")

# ----- Drop down for selecting period ----
years = [datetime.today().year - 1, datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])

# ----- HIDE Streamlit Style --------------

# hide_st_style = """
#     <style>
#         #MainMenu {visibility: hidden;}
#         footer {visibility:hidden;}
#         header {visibility:hidden;}
#     </style>
#     """
# st.markdown(hide_st_style, unsafe_allow_html=True)


# ---------Session State Instances --------

# if "InputPhone" not in st.session_state:
#     st.session_state.InputPhone = ""
#     st.session_state.InputServices = None
#     st.session_state.InputFirst = ""
#     st.session_state.InputLast = ""
#     st.session_state.InputBirthdate = None


# --------------- Nav Bar -----------------

selected = option_menu(
    menu_title=None,
    options=["Check In", "Sign Up"],
    icons=["box-arrow-in-left", "plus-square"],
    orientation="horizontal",
)
_count = st_autorefresh(interval=2500, limit=None, key="CheckInRefresh")
# ------- Input & Save periods ----
if selected == "Check In":
    st.header("Check In")
    with st.form("checkin_form", clear_on_submit=True):
        options = (
            "Pedicure",
            "Reg. Manicure",
            "Gel Manicure",
            "Liquiq full set",
            "Liquiq Fill",
            "Full set",
            "Fill",
            "Dip",
            "Wax",
        )
        col1, col2 = st.columns([0.4, 0.6])
        col1.text_input(
            label="Phone Number",
            value="",
            placeholder="000-000-0000",
            max_chars=10,
            key="phone",
        )
        col2.multiselect(
            label="Services",
            options=options,
            placeholder="Choose your service(s)",
            key="services",
        )

        submitted = st.form_submit_button("Enter", type="primary")
        if submitted:
            phone = st.session_state.phone
            services = st.session_state.services
            if not phone.isnumeric() or not len(phone) == 10:
                st.error(
                    f"{phone}: Please enter a valid 10-digit phone number.", icon="⚠️"
                )
            else:
                results = checkin(phone=phone, services=services)
                if results != None and results != -1:
                    st.success(
                        f"Welcome, {results[0]}! You have {results[1]} points.",
                        icon="🥳",
                    )
                if results == None:
                    st.warning(f"{phone}: New Client. Please sign up.", icon="🙏")
                if results == -1:
                    st.error("Update error. Please retry.", icon="⚠️")

# ------- Display periods -----------
if selected == "Sign Up":

    st.header("Sign Up")
    with st.form("signup_form", clear_on_submit=True):
        options = (
            "Pedicure",
            "Reg. Manicure",
            "Gel Manicure",
            "Liquiq full set",
            "Liquiq Fill",
            "Full set",
            "Fill",
            "Dip",
            "Wax",
        )

        col1, col2 = st.columns(2)
        col1.text_input(
            label="First name",
            value="",
            placeholder="Pretty",
            max_chars=20,
            key="fname",
        )
        col2.text_input(
            label="Last Name",
            value="",
            placeholder="Bella",
            max_chars=20,
            key="lname",
        )
        st.text_input(
            label="Phone Number",
            value="",
            placeholder="(480) 590-6703",
            max_chars=10,
            key="phone",
        )
        st.date_input(
            label="Birthdate", value=None, format="YYYY-MM-DD", key="birthdate"
        )
        st.multiselect(
            label="Today Services",
            options=options,
            default=None,
            placeholder="Choose your service(s)",
            key="services",
        )
        submitted = st.form_submit_button("Submit", type="primary")
        if submitted:
            valid = True
            fname = st.session_state["fname"]
            lname = st.session_state["lname"]
            dob = st.session_state["birthdate"]
            phone = st.session_state["phone"]
            client = (
                st.session_state["phone"],
                st.session_state["fname"],
                st.session_state["lname"],
                st.session_state["birthdate"],
                st.session_state["services"],
            )
            if not client[0].isnumeric() or len(client[0]) != 10:
                st.error(
                    f"{client[0]}: Please enter a valid 10-digit phone number.",
                    icon="⚠️",
                )
                valid = False
            if not client[1].isalpha():
                st.error(
                    f"{client[1]}: Please enter your first name. Alphabet only.",
                    icon="⚠️",
                )
                valid = False
            if not client[2].isalpha():
                st.error(
                    f"{client[2]}: Please enter your last name. Alphabet only.",
                    icon="⚠️",
                )
                valid = False
            if not client[3]:
                st.error(f"{client[3]}: Please set your birthdate.", icon="⚠️")
                valid = False

            if valid:
                r, c = signup(fname, lname, dob, phone)
                if r == 1:
                    st.success(f"Welcome, {client[1]}! You have 1 points.", icon="🥳")
                if r == -1:
                    st.error("Update error. Please retry.", icon="⚠️")
                if r == 0:
                    st.success(f"Welcome, {c[0]}! You have {c[1]} points.", icon="🥳")
