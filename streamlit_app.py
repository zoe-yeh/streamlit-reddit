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

st.markdown('<style>div {width: 600px;height: 600px;background-image: url(data:image/jpeg;base64,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);background-repeat: no-repeat;}</style>', unsafe_allow_html=True)
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