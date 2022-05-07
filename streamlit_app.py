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
	page_icon="🎤", 
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

# to get different images/media in the rows and columns, have a systematic 
# way to label your images/media. For mine, I have used row_{i}_col_0/1
# also note that different media types such as an audio or video file you 
# will need to have that whole column as an audio or video column!

for i in range(1,2): # number of rows in your table! = 2
    cols = st.columns(2) # number of columns in each row! = 2
    # first column of the ith row
    cols[0].image('./img/anita40anniversary_DM1.jpg', width=100, use_column_width=True)
    cols[1].image('./img/anita40anniversary_DM2.jpg', use_column_width=True)



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

# set_background('20211230mui_0.png')

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.




# Streamlit widgets to let a user create a new post
today = st.date_input("今天日期") 
nickname = st.text_input("暱稱:")
place = st.text_input("你是來自哪裡的粉絲:")
years = st.text_input("喜歡 Anita 已經有幾年了")
sentence = st.text_area("你想對 Anita 說", height=100)



# nickname, place  = st.columns([1,1])
# years, sentence  = st.columns([1,1])
# nickname.text_input("暱稱:")
# place.text_input("你是來自哪裡的粉絲:")
# years.text_input("喜歡 Anita 已經有幾年了")
# sentence.text_area("你想對 Anita 說", height=100)

submit = st.button("Submit")

# Once the user has submitted, upload it to the database
if today and nickname and place and years and sentence and submit:
	doc_ref = db.collection("anita").document("anita40anniversary")
	doc_ref.set({
		"date_time": today,
		"nickname": nickname,
		"place": place,
		"year": years,
		"sentence": sentence
	})

# And then render each post, using some light Markdown
anita_ref = db.collection("anita")
for doc in anita_ref.stream():
	fans_profile = doc.to_dict()
	date_time = fans_profile["date_time"]
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


st.markdown("<h2 style='text-align: center; color: black;'>謝謝今天的拜訪，你填寫的小卡之後會製作成驚喜唷！</h2>", unsafe_allow_html=True)
# st.markdown("<h2 style='text-align: center; color: black;'>一切消息都會公佈在小海的 Instagram 帳號敬請期待 😆</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>一切消息都會公佈在小海的 <a href='https://www.instagram.com/paintinglife_0707/'>Instagram 帳號</a>敬請期待 😆</h2>", unsafe_allow_html=True)


# https://github.com/soft-nougat/streamlitwebcam/tree/main/final_model
# https://discuss.streamlit.io/t/how-do-i-use-a-background-image-on-streamlit/5067/9
# https://vocus.cc/article/60ea6520fd89780001771fcd