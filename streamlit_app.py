import streamlit as st
from google.cloud import firestore

db = firestore.Client.from_service_account_json("firestore-key.json")

# Streamlit widgets to let a user create a new post
title = st.text_input("Post title")
url = st.text_input("Post url")
submit = st.button("Submit new post")

# Once the user has submitted, upload it to the database
if title and url and submit:
	doc_ref = db.collection("posts").document(title)
	doc_ref.set({
		"title": title,
		"url": url
	})

st.subheader(f"我們收到囉")
