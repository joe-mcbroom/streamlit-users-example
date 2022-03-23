# streamlit_app.py

import streamlit as st
import snowflake.connector
import pandas as pd

# Initialize connection.
# Uses st.experimental_singleton to only run once.


@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])


conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.


@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


rows = run_query("SELECT * from users")
columnsData = run_query("show columns in table users;")
columns = [x[2] for x in columnsData]

# Print results.

df = pd.DataFrame(rows, columns=columns)


age_range = st.slider(
    'Select an age range to display',
    1, 100, (1, 100), step=1, format="%d",
)
selected_min_age, max_age = age_range
ages = df["AGE"]

display_values = df[(ages >= selected_min_age) & (ages <= max_age)]
display_values.style.hide_index()

ages = display_values.groupby("AGE")
st.write('Age distribution:')
st.bar_chart(ages.size())

st.write('Users:')
st.write(display_values)
