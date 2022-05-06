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
st.markdown("<img src='data:image/jpeg;base64,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'>", unsafe_allow_html=True)


place = st.text_input("1. 你是來自哪裡的粉絲:")
years = st.text_input("2. 喜歡 Anita 已經有幾年了")
sentence = st.text_input("3. 你想對 Anita 說")

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

image_file = st.file_uploader("放張你最喜歡的 Anita 或是為今天留下一個紀念吧！（只接收照片唷）", type=['png','jpeg'])

if image_file is not None:
	# To View Uploaded Image
	st.image(load_image(image_file), width=300)


st.video("https://www.youtube.com/watch?v=EoTMlRISRuQ", start_time=0)


st.markdown("<h2 style='text-align: center; color: black;'>謝謝今天的拜訪，你填寫的小卡之後會製作成驚喜，敬請期待 😆</h2>", unsafe_allow_html=True)
# https://github.com/soft-nougat/streamlitwebcam/tree/main/final_model
# https://discuss.streamlit.io/t/how-do-i-use-a-background-image-on-streamlit/5067/9
# https://vocus.cc/article/60ea6520fd89780001771fcd