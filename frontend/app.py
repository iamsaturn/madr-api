from http import HTTPStatus

import streamlit as st
from api import (
    create_book,
    create_novelist,
    get_books,
    get_novelists,
    get_profile,
    login,
    register,
)

st.set_page_config(page_title="MADR", page_icon="📚")

st.title("MADR")
st.caption("Modern Archive for Digital Romance")

logged_in = "token" in st.session_state

if logged_in:
    token = st.session_state["token"]
else:
    token = None


books_tab, novelists_tab, account_tab = st.tabs(
    ["📚 Books", "✍️ Novelists", "👤 Account"]
)


with books_tab:
    st.subheader("Books")

    page = st.number_input("Page", min_value=1, value=1, step=1, key="book_page")
    offset = (page - 1) * 6

    response = get_books(offset=offset, limit=6)

    if response.status_code == HTTPStatus.OK:
        books = response.json()

        if books:
            for book in books:
                with st.container(border=True):
                    st.markdown(f"### {book['title'].title()}")
                    st.write(f"**Novelist:** {book['novelist']['name'].title()}")
                    st.write(f"**Year:** {book['year']}")
        else:
            st.info("No books on this page.")
    else:
        st.error("Could not load books.")

    if logged_in:
        with st.expander("Add book"):
            response = get_novelists(offset=0, limit=100)

            if response.status_code == HTTPStatus.OK:
                novelists = response.json()

                if not novelists:
                    st.info("Create a novelist before adding a book.")
                else:
                    title = st.text_input("Book title")
                    year = st.number_input("Publication year", min_value=0, step=1)

                    novelist_options = {
                        novelist["name"].title(): novelist["id"]
                        for novelist in novelists
                    }

                    selected_novelist = st.selectbox(
                        "Novelist", list(novelist_options.keys())
                    )

                    if st.button("Create book"):
                        response = create_book(
                            title,
                            int(year),
                            novelist_options[selected_novelist],
                            token,
                        )

                        if response.status_code == HTTPStatus.OK:
                            st.success("Book created!")
                            st.rerun()
                        else:
                            data = response.json()
                            st.error(data.get("detail", "Could not create book."))


with novelists_tab:
    st.subheader("Novelists")

    page = st.number_input("Page", min_value=1, value=1, step=1, key="novelist_page")
    offset = (page - 1) * 6

    response = get_novelists(offset=offset, limit=6)

    if response.status_code == HTTPStatus.OK:
        novelists = response.json()

        if novelists:
            for novelist in novelists:
                with st.container(border=True):
                    st.markdown(f"### {novelist['name'].title()}")
        else:
            st.info("No novelists on this page.")
    else:
        st.error("Could not load novelists.")

    if logged_in:
        with st.expander("Add novelist"):
            novelist_name = st.text_input("Novelist name")

            if st.button("Create novelist"):
                response = create_novelist(novelist_name, token)

                if response.status_code == HTTPStatus.OK:
                    st.success("Novelist created!")
                    st.rerun()
                else:
                    data = response.json()
                    st.error(data.get("detail", "Could not create novelist."))


with account_tab:
    if not logged_in:
        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            response = login(email, password)

            if response.status_code == HTTPStatus.OK:
                data = response.json()
                st.session_state["token"] = data["access_token"]
                st.rerun()
            else:
                st.error("Invalid email or password.")

        with st.expander("Create account"):
            username = st.text_input("Username")
            new_email = st.text_input("New email")
            new_password = st.text_input("New password", type="password")

            if st.button("Create my account"):
                response = register(
                    username,
                    new_email,
                    new_password,
                )

                if response.status_code == HTTPStatus.OK:
                    st.success("Account created! You can login now.")
                else:
                    data = response.json()
                    st.error(
                        data.get(
                            "detail",
                            "Could not create account.",
                        )
                    )

    else:
        st.subheader("Account")

        response = get_profile(token)

        if response.status_code == HTTPStatus.OK:
            user = response.json()

            with st.container(border=True):
                st.write(f"**Username:** {user['username']}")
                st.write(f"**Email:** {user['email']}")
        else:
            st.error("Could not load profile.")

        if st.button("Logout", use_container_width=True):
            del st.session_state["token"]
            st.rerun()
