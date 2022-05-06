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