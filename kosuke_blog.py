import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pytube import YouTube
import datetime

st.title('こうすけブログ分析')

df = pd.read_csv('kosuke_blog.csv')
df = df[['日付',  'タイトル', '本文']]
df_title = df[['タイトル']]

st.write(len(df), '投稿')

selected_title = st.selectbox(
    '表示するタイトルを選択：',
    df_title
)

df1 = df.loc[df['タイトル'] == selected_title, 'タイトル'].item()
st.title(df1)

df2 = df.loc[df['タイトル'] == selected_title, '日付'].item()
st.write(df2)

df3 = df.loc[df['タイトル'] == selected_title, '本文'].item()
st.write(df3)

st.write(len(df3), '文字')


def g_nlp(text):
#     text = '吾輩は猫である。名前まだない。'
    key = 'AIzaSyCcZgdyGYIqzsgVIHHy8poswq2NS4mQ_qg'
    url = f'https://language.googleapis.com/v1/documents:analyzeSentiment?key={key}'
    header = {'Content-Type': 'application/json'}
    body = {
        "document": {
            "type": "PLAIN_TEXT",
            "language": "JA",
            "content": text
        }
    }
    res = requests.post(url, headers=header, json=body)
    result = res.json()
    return result

js = g_nlp(df3)

st.title('感情分析')
"""
magnitud : 感情の強さ  
score : 感情の点数(-はネガティブ / +はポジティブ)
"""
st.write(js['documentSentiment'])

st.title("Youtube Video Donwloader")
st.subheader("Enter the URL:")
url = st.text_input(label='URL')
#print(yt.streams)
#print(caption.generate_srt_captions())
if url != '':
    yt = YouTube(url)
    st.image(yt.thumbnail_url, width=300)
    c = yt.length
    td = datetime.timedelta(seconds=(c))
    st.title(td)
    st.subheader(yt.title )
    video = yt.streams
    if len(video) > 0:
        downloaded , download_audio = False , False
        download_video = st.button("ダウンロード ビデオ")
        if yt.streams.filter(only_audio=True):
            download_audio = st.button("ダウンロード　音声のみ")
        if download_video:
            video.get_lowest_resolution().download(r'C:\video')
            downloaded = True
        if download_audio:
            video.filter(only_audio=True).first().download(r'C:\music')
            downloaded = True
        if downloaded:
            st.subheader("ダウンロード完了しました")
            
    else:
        st.subheader("ダウンロードできませんでした")
    audio_file = st.file_uploader('File uploader')
    st.text("再生する")    
    st.audio(audio_file)