# https://docs.streamlit.io/knowledge-base/tutorials/databases/private-gsheet
import time
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
from gsheetsdb import connect
from PIL import Image

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive  

# # 加入進度條, 增加一個空白元件，等等要放文字
# latest_iteration = st.empty()
# bar = st.progress(0)
# for i in range(100):
# 	latest_iteration.text(f"目前進度: {i+1} %")
# 	bar.progress(i + 1)
# 	time.sleep(0.1)

db = firestore.Client.from_service_account_json("firestore-key.json")

# 網頁配置設定
st.set_page_config(
	page_title="Anita Mui 出道 40 週年應援活動", 
	page_icon="random", 
	layout="wide",  
	initial_sidebar_state="collapsed")

# st.image("./img/anita_test.jpeg", width=300)

st.markdown('<style>div {width: 1200px;height: 1200px;background-image: url(img/anita_test.jpeg);background-repeat: no-repeat;}</style>', unsafe_allow_html=True)
# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
st.title('輸入你想對梅姐說的話：')



# Streamlit widgets to let a user create a new post
place = st.text_input("你是來自哪裡的粉絲:")
years = st.text_input("喜歡 Anita 已經有幾年了")
submit = st.button("Submit")

# Once the user has submitted, upload it to the database
if place and years and submit:
	doc_ref = db.collection("anita").document("anita40anniversary")
	doc_ref.set({
		"place": place,
		"year": years
	})

# And then render each post, using some light Markdown
anita_ref = db.collection("anita")
for doc in anita_ref.stream():
	fans_profile = doc.to_dict()
	place = fans_profile["place"]
	years = fans_profile["year"]
    
	# st.subheader(f"Post: {fans_profile}")

	st.subheader(f"Post: {place}")
	st.subheader(f"喜歡 Anita 已經有幾年了: {years}")

def load_image(image_file):
	img = Image.open(image_file)
	return img

# image_file = st.file_uploader("Upload Files", type=['png','jpeg'], accept_multiple_files = True)
image_file = st.file_uploader("放張你最喜歡的 Anita 或是為今天留下一個紀念吧！", type=['png','jpeg'])

if image_file is not None:
	# To View Uploaded Image
	st.image(load_image(image_file), width=300)



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

# 	# st.image("https://drive.google.com/open?id=14456bhRmjPaxYPWmKw4DfjLCQ4MAQZDz") # Manually Adjust the width of the image as per requirement
#     # st.write(f"{row._3}")
# 	# st.write(f"{row.留下一句話你最想跟_Anita_說的話吧_}")



# 	#Saving upload
# 	with open(image_file.name,"wb") as f:
# 		f.write((image_file).getbuffer())
			  
# 	st.success("File Saved")

# 	folder_id = '17ltL5jMFTiQr23tVlacN6Q_4NLMBGrx7NpSOi3xYQxBi2ApBffOE1FbHgAzvHkKwk88oQJDF'
# 	gfile = drive.CreateFile({'parents': [{'id': folder_id}]})
# 	# Read file and set it as the content of this instance.
# 	gfile.SetContentFile(image_file)
# 	gfile.Upload() # Upload the file.

	

# 	# file_details = {"FileName":image_file.name,"FileType":image_file.type,"FileSize":image_file.size}
#     # st.text(file_details)
	
	


# # # https://blog.streamlit.io/streamlit-firestore-continued/

# # import streamlit as st
# # from google.cloud import firestore

# # db = firestore.Client.from_service_account_json("firestore-key.json")
# # # import json
# # # key_dict = json.loads(st.secrets["textkey"])
# # # creds = service_account.Credentials.from_service_account_info(key_dict)
# # # db = firestore.Client(credentials=creds, project="streamlit-reddit")

# # # Streamlit widgets to let a user create a new post
# # title = st.text_input("Post title")
# # url = st.text_input("Post url")
# # submit = st.button("Submit new post")

# # # Once the user has submitted, upload it to the database
# # if title and url and submit:
# # 	doc_ref = db.collection("posts").document(title)
# # 	doc_ref.set({
# # 		"title": title,
# # 		"url": url
# # 	})

# # # And then render each post, using some light Markdown
# # posts_ref = db.collection("posts")
# # for doc in posts_ref.stream():
# # 	post = doc.to_dict()
# # 	title = post["title"]
# # 	url = post["url"]

# # 	st.subheader(f"Post: {title}")
# # 	st.write(f":link: [{url}]({url})")