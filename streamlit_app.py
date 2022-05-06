# https://docs.streamlit.io/knowledge-base/tutorials/databases/private-gsheet
import time
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
from gsheetsdb import connect
from PIL import Image

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive  

import base64
import helper as help
# help.set_bg_hack()





# 加入進度條, 增加一個空白元件，等等要放文字
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
	latest_iteration.text(f"目前進度: {i+1} %")
	bar.progress(i + 1)
	time.sleep(0.1)

db = firestore.Client.from_service_account_json("firestore-key.json")



# 網頁配置設定
# st.set_page_config(page_title="Anita")

st.set_page_config(
	page_title="Anita Mui 出道 40 週年應援活動", 
	page_icon="random", 
	layout="wide",  
	initial_sidebar_state="collapsed")


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('20211230mui_0.png')

# st.image("./img/anita_test.jpeg", width=300)


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

image_file = st.file_uploader("放張你最喜歡的 Anita 或是為今天留下一個紀念吧！", type=['png','jpeg'])

if image_file is not None:
	# To View Uploaded Image
	st.image(load_image(image_file), width=300)

# https://github.com/soft-nougat/streamlitwebcam/tree/main/final_model