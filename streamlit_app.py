# https://docs.streamlit.io/knowledge-base/tutorials/databases/private-gsheet
# streamlit_app.py

import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
from gsheetsdb import connect
from PIL import Image

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()           
drive = GoogleDrive(gauth)  


db = firestore.Client.from_service_account_json("firestore-key.json")
# # Create a connection object.
# credentials = service_account.Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"],
#     scopes=[
#         "https://www.googleapis.com/auth/spreadsheets",
#     ],
# )
# conn = connect(credentials=credentials)

# 網頁配置設定
st.set_page_config(
    page_title="Anita Mui 出道 40 週年應援活動",
    page_icon="random",
    layout="wide", # 網頁中佈局寬度，預設是"centered"，還可以使用"wide"
    initial_sidebar_state="collapsed", # 側邊欄顯示狀態，"expanded"打開或"collapsed"隱藏，預設是"auto"，代表在手機尺寸的設備上是隱藏，否則是打開顯示。
)


# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
st.title('輸入你想對梅姐說的話：')



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

# And then render each post, using some light Markdown
posts_ref = db.collection("posts")
for doc in posts_ref.stream():
	post = doc.to_dict()
	title = post["title"]
	url = post["url"]

	st.subheader(f"Post: {title}")
	st.write(f":link: [{url}]({url})")


# @st.cache(ttl=600)
# def run_query(query):
#     rows = conn.execute(query, headers=1)
#     rows = rows.fetchall()
#     return rows

# sheet_url = st.secrets["private_gsheets_url"]
# rows = run_query(f'SELECT * FROM "{sheet_url}"')

# # Print results.
# for row in rows:
# 	st.text(row)
# 	st.write(f"拜訪時間: {row.時間戳記}\n  我想說: {row.留下一句話你最想跟_Anita_說的話吧_}")

	# st.image("https://drive.google.com/open?id=14456bhRmjPaxYPWmKw4DfjLCQ4MAQZDz") # Manually Adjust the width of the image as per requirement
    # st.write(f"{row._3}")
	# st.write(f"{row.留下一句話你最想跟_Anita_說的話吧_}")

def load_image(image_file):
	img = Image.open(image_file)
	return img

# image_file = st.file_uploader("Upload Files", type=['png','jpeg'], accept_multiple_files = True)
image_file = st.file_uploader("Upload Files", type=['png','jpeg'])

if image_file is not None:
	# To View Uploaded Image
	st.image(load_image(image_file), width=300)

	#Saving upload
	with open(image_file.name,"wb") as f:
		f.write((image_file).getbuffer())
			  
	st.success("File Saved")

	folder_id = '17ltL5jMFTiQr23tVlacN6Q_4NLMBGrx7NpSOi3xYQxBi2ApBffOE1FbHgAzvHkKwk88oQJDF'
	gfile = drive.CreateFile({'parents': [{'id': folder_id}]})
	# Read file and set it as the content of this instance.
	gfile.SetContentFile(image_file)
	gfile.Upload() # Upload the file.

	

	# file_details = {"FileName":image_file.name,"FileType":image_file.type,"FileSize":image_file.size}
    # st.text(file_details)
	
	


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