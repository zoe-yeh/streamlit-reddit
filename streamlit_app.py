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

db = firestore.Client.from_service_account_json("firestore-key.json")

# 網頁配置設定
st.set_page_config(
	page_title="Anita Mui 出道 40 週年應援活動", 
	page_icon="random", 
	layout="wide",  
	initial_sidebar_state="collapsed")


# # 加入進度條, 增加一個空白元件，等等要放文字
# latest_iteration = st.empty()
# bar = st.progress(0)
# for i in range(100):
# 	latest_iteration.text(f"目前進度: {i+1} %")
# 	bar.progress(i + 1)
# 	time.sleep(0.1)


st.markdown("<h1 style='text-align: center; color: black;'>梅艷芳出道四十週年紀念晝展</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>未變情懷40載, 流年似水如一夢</h2>", unsafe_allow_html=True)

# 背景圖
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

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.




# Streamlit widgets to let a user create a new post
nickname = st.text_input("暱稱:")
st.markdown("<h1 style='text-align: center; color: black;'>梅艷芳出道四十週年紀念晝展</h1>", unsafe_allow_html=True)
place = st.text_input("你是來自哪裡的粉絲:")
years = st.text_input("喜歡 Anita 已經有幾年了")
sentence = st.text_input("你想對 Anita 說")

submit = st.button("Submit")

# Once the user has submitted, upload it to the database
if place and years and nickname and submit:
	doc_ref = db.collection("anita").document("anita40anniversary")
	doc_ref.set({
		"nickname": nickname,
		"place": place,
		"year": years,
		"sentence": sentence
	})

# And then render each post, using some light Markdown
anita_ref = db.collection("anita")
for doc in anita_ref.stream():
	fans_profile = doc.to_dict()
	nickname = fans_profile["nickname"]
	place = fans_profile["place"]
	years = fans_profile["year"]
	sentence = fans_profile["sentence"]

	st.subheader(f"來自{place} 的 {nickname} 已經喜歡Anita 已經有 {years} 年了，他最想跟 Anita 說: {sentence}")
	

def load_image(image_file):
	img = Image.open(image_file)
	return img

image_file = st.file_uploader("放張你最喜歡的 Anita 或是為今天留下一個紀念吧！", type=['png','jpeg'])

if image_file is not None:
	# To View Uploaded Image
	st.image(load_image(image_file), width=300)


st.video("https://www.youtube.com/watch?v=EoTMlRISRuQ", start_time=0)
# https://github.com/soft-nougat/streamlitwebcam/tree/main/final_model
# https://discuss.streamlit.io/t/how-do-i-use-a-background-image-on-streamlit/5067/9
# https://vocus.cc/article/60ea6520fd89780001771fcd