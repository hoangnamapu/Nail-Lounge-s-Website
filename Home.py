import streamlit as st
from database import init_connection, get_client, signup

# ---------------Settings -----------------

page_title = "Posh Lounge | Home"
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

# ----- HIDE Streamlit Style --------------

hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        h1 {text-align:center;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

with st.container(border=True):
    rows = get_client("6027238354")
    st.write(rows)
    # st.page_link(
    #     "pages/1_Check_In.py", label="Go to Check In", use_container_width=True
    # )
    # st.page_link(
    #     "pages/2_Dashboard.py", label="Go to Dashboard", use_container_width=True
    # )
    st.link_button(
        label="Go to Check In",
        url="/Check_In",
        use_container_width=True,
        type="primary",
    )
    st.link_button(
        label="Go to Dashboard",
        url="/Dashboard",
        use_container_width=True,
        type="primary",
    )
