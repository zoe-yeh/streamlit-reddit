# https://docs.streamlit.io/knowledge-base/tutorials/databases/private-gsheet
# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
from PIL import Image
# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
for row in rows:
	st.text(row)
	st.write(f"拜訪時間: {row.時間戳記}\n  我想說: {row.留下一句話你最想跟_Anita_說的話吧_}")
	st.image("https://drive.google.com/open?id=14456bhRmjPaxYPWmKw4DfjLCQ4MAQZDz") # Manually Adjust the width of the image as per requirement
    # st.write(f"{row._3}")
	# st.write(f"{row.留下一句話你最想跟_Anita_說的話吧_}")

# def load_image(image_file):
# 	img = Image.open(image_file)
# 	return img

uploaded_file = st.file_uploader("Upload Files",type=['png','jpeg'])
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    st.write(file_details)

# # https://blog.streamlit.io/streamlit-firestore-continued/

# import streamlit as st
# from google.cloud import firestore

# db = firestore.Client.from_service_account_json("firestore-key.json")
# # import json
# # key_dict = json.loads(st.secrets["textkey"])
# # creds = service_account.Credentials.from_service_account_info(key_dict)
# # db = firestore.Client(credentials=creds, project="streamlit-reddit")

# # Streamlit widgets to let a user create a new post
# title = st.text_input("Post title")
# url = st.text_input("Post url")
# submit = st.button("Submit new post")

# # Once the user has submitted, upload it to the database
# if title and url and submit:
# 	doc_ref = db.collection("posts").document(title)
# 	doc_ref.set({
# 		"title": title,
# 		"url": url
# 	})

# # And then render each post, using some light Markdown
# posts_ref = db.collection("posts")
# for doc in posts_ref.stream():
# 	post = doc.to_dict()
# 	title = post["title"]
# 	url = post["url"]

# 	st.subheader(f"Post: {title}")
# 	st.write(f":link: [{url}]({url})")