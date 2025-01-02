import streamlit as st
import langchain_helper

st.title("Restaurant Name Generator")

cuisine = st.sidebar.selectbox("Pick a Cuisine", ("Indian", "Italian", "Mexican", "Arabic", "American"))

if cuisine:
    response = langchain_helper.generate_restaurant_name_and_items(cuisine)
    if response and 'restaurant_name' in response and 'menu_items' in response:
        st.header(response['restaurant_name'].strip())
        menu_items = response['menu_items'].strip().split(",")
        st.write("**Menu Items**")
        for item in menu_items:
            st.write("-", item)
    else:
        st.error("Sorry, something went wrong. Unable to generate the restaurant name or menu items.")