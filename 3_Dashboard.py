import streamlit as st
from database import *
import pandas as pd
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh

# ---------------Settings -----------------

page_title = "Posh Lounge | Dashboard"
page_icon = "amd"
layout = "centered"


# -----------------------------------------

st.set_page_config(
    page_title=page_title,
    page_icon=page_icon,
    layout=layout,
    initial_sidebar_state="collapsed",
)
st.title("Posh Nail Lounge | Dashboard")

# ----- HIDE Streamlit Style --------------

hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)


# ------- Functions -------------------------
def redeem(edited_rows, df):
    rows = edited_rows.keys()
    points = []
    phones = []
    for row in rows:
        if not edited_rows[row]["select"]:
            continue
        if df.at[row, "points"] < 10:
            st.error(f"{df.at[row, 'name']} does not have enough points.", icon="⚠️")
            continue
        points.append(df.at[row, "points"] - 10)
        phones.append(df.at[row, "phoneNumber"])

    return redeemDB(points=points, phones=phones)


selected = option_menu(
    None,
    ["Active Session", "History Logs"],
    icons=["c-circle", "clock-history"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)
if selected == "History Logs":
    # ------ Listing Check In Logs -----------------
    st.header("History Log")

    with st.expander("Select date range for log"):
        st.session_state.expanderHelper = "Choose range to retrieve data"
        col1, col2 = st.columns(2)
        col1.date_input(
            label="Start date", value="today", format="YYYY-MM-DD", key="sdate"
        )
        col2.date_input(
            label="End date", value="today", format="YYYY-MM-DD", key="edate"
        )
        submitted = st.button("Retrieve", use_container_width=True, type="primary")

        if submitted:
            clients = checkin(st.session_state["sdate"], st.session_state["edate"])
            if clients == -1:
                st.error("Database Error. Try again.")
            elif len(clients) == 0:
                st.warning("No Data. Choose different range.")
            else:
                column_config = {
                    "name": "Name",
                    "birthdate": "DoB",
                    "points": st.column_config.NumberColumn(
                        label="Points", format="%d ⭐️"
                    ),
                    "phoneNumber": "Phone",
                    "services": st.column_config.ListColumn(label="Services"),
                    "dateTime": st.column_config.DatetimeColumn(
                        label="Date Time", format="ddd, MMM DD, hh:mm A", timezone="MST"
                    ),
                }
                title = column_config.keys()
                clients = pd.DataFrame(list(clients), columns=title)
                st.dataframe(
                    clients, use_container_width=True, column_config=column_config
                )

    # ------ Listing Clients -----------------------
    st.header("Client Info")
    with st.expander("Search or edit clients' info"):

        column_config = {
            "phoneNumber": "Phone Number",
            "firstName": "First Name",
            "lastName": "Last Name",
            "birthdate": st.column_config.DateColumn(label="DoB", format="MMM DD"),
            "points": st.column_config.NumberColumn(label="Points", format="%d ⭐️"),
        }
        titles = column_config.keys()
        clients = get_client()
        if clients != -1:
            disabled = True
            clients = pd.DataFrame(list(clients), columns=titles)
            st.data_editor(
                clients,
                use_container_width=True,
                column_config=column_config,
                key="clientlist",
            )
            if len(st.session_state.clientlist["edited_rows"]) != 0:
                disabled = False
            st.button(
                "Save Change",
                on_click=updateClientInfo,
                args=(st.session_state.clientlist["edited_rows"], clients),
                type="primary",
                disabled=disabled,
                key="saveChange",
            )

if selected == "Active Session":
    # ------  Active Session ------------------------
    _count = st_autorefresh(interval=10000, limit=None, key="ActiveSession")
    st.header("Active Session")
    with st.container():
        today = datetime.now() - timedelta(hours=7)
        entries = checkin(today, today)
        column_config = {
            "select": st.column_config.CheckboxColumn(label="Select"),
            "name": "Name",
            "birthdate": st.column_config.DateColumn(label="DoB", format="MMM DD"),
            "points": st.column_config.NumberColumn(label="Points", format="%d ⭐️"),
            "phoneNumber": "Phone",
            "services": st.column_config.ListColumn(label="Services"),
            "dateTime": st.column_config.DatetimeColumn(
                label="Check In", format="hh:mm A", timezone="MST"
            ),
        }
        titles = list(column_config.keys())[1:]
        entries = pd.DataFrame(list(entries), columns=titles)
        entries.insert(0, "select", False)
        st.data_editor(
            entries,
            use_container_width=True,
            column_config=column_config,
            hide_index=True,
            disabled=titles,
            key="activeList",
        )
        disabled = True
        if len(st.session_state.activeList["edited_rows"]) != 0:
            disabled = False

        redeem = st.button(
            "Redeem",
            on_click=redeem,
            args=(st.session_state.activeList["edited_rows"], entries),
            disabled=disabled,
            use_container_width=True,
        )
        # TODO: Implement checkout to remove completed clients
