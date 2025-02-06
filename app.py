import streamlit as st
import tensorflow as tf
import numpy as np
import pickle
import joblib
import json
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 配置加载
with open('config.json', 'r') as f:
    config = json.load(f)
max_len = config['max_len']
max_features = config['max_features']

# 加载预处理资源
with open('char_index.pkl', 'rb') as f:
    char_index = pickle.load(f)
label_encoder = joblib.load('label_encoder.pkl')
model = tf.keras.models.load_model('malicious_url_model.h5')

# 威胁描述配置
threat_descriptions = {
    "benign": {"emoji": "✅", "desc": {"en": "Safe URL", "zh": "安全网址"}},
    "defacement": {"emoji": "💥", "desc": {"en": "Web Defacement", "zh": "网页篡改攻击"}},
    "phishing": {"emoji": "🎣", "desc": {"en": "Phishing Website", "zh": "钓鱼网站"}},
    "malware": {"emoji": "🦠", "desc": {"en": "Malware Distribution", "zh": "恶意软件传播"}}
}

# 预处理函数
def preprocess_url(url):
    url = url.lower().strip()
    seq = [char_index.get(char, 0) for char in url[:max_len]]
    return pad_sequences([seq], maxlen=max_len, padding='post', truncating='post')

# 界面设计
st.set_page_config(page_title="URL Safety Detection", layout="wide")

# 语言选择
language = st.sidebar.selectbox("Language / 语言", ["English", "中文"])

# 系统介绍
if language == "English":
    st.sidebar.markdown("""
    ## Introduction
    The system encodes character-level features of URLs, uses CNN to efficiently extract local features, and applies Transformer to capture global dependencies in long sequences. This hybrid deep learning model combines the strengths of both approaches to provide a more comprehensive analysis of malicious URLs, improving detection accuracy.
    """)
else:
    st.sidebar.markdown("""
    ## 系统介绍
    系统通过对网址的字符级特征进行编码，CNN高效提取URL中的局部特征，Transformer处理长序列数据捕捉全局依赖关系，构建了一个深度学习混合模型进行网址分类。这种混合模型结合了两者的优势，能够更全面地分析恶意网址的特征，提高检测精度。
    """)

# 主界面内容
if language == "English":
    st.title("🛡️ A malicious URL detection system based on Convolutional Neural Networks (CNN) and Transformer models")
    st.markdown("""
    <style>
        .stTextInput input {font-size: 16px !important;}
        .stProgress > div > div {background-color: #28a745 !important;}
    </style>
    """, unsafe_allow_html=True)

    col1 = st.columns([3])[0]

    url = st.text_input("Enter the URL to be detected:", "", 
                      placeholder="www.example.com/...")

    if st.button("Start Detection", use_container_width=True):
        if not url:
            st.warning("Please enter a valid URL")
        else:
            with st.spinner("Analyzing URL..."):
                processed = preprocess_url(url)
                pred = model.predict(processed)
                confidence = np.max(pred)
                label = label_encoder.inverse_transform([np.argmax(pred)])[0]

            # 结果显示
            result = threat_descriptions[label]

            st.subheader("Detection Result")
            st.markdown(f"""
            <div style="border-left:4px solid #28a745; padding-left:1rem;">
                <h3 style='margin:0;color:#28a745;'>
                    {result['emoji']} {result['desc']['en']}
                    <small style='font-size:0.8em;'>({label})</small>
                </h3>
                <p>Confidence: <strong>{confidence:.2%}</strong></p>
            </div>
            """, unsafe_allow_html=True)

    # 侧边栏说明
    st.sidebar.markdown("""
    ## Instructions
    1. **Paste URL:** Paste the URL you want to detect in the input box (e.g., www.example.com). Ensure the URL format is correct.
    2. **Click 'Start Detection' button:** After clicking the button, the system will automatically analyze the URL you entered and determine its safety.
    3. **Wait for the analysis result:** The detection process may take a few seconds, depending on the complexity of the URL. Please be patient.
    4. **View the detection result:** The system will display the security level of the URL and its confidence level, helping you assess the risk of the website.

    ## Detection Type Description
    - ✅ **Safe URL:** Indicates that the URL is trustworthy and safe to visit.
    - 💥 **Web Defacement:** The URL may have been maliciously modified, and its content may be tampered with, potentially leading to unsafe pages.
    - 🎣 **Phishing Website:** This is a fake website, usually designed to steal your personal information (e.g., passwords, bank accounts), so be cautious.
    - 🦠 **Malware:** The website may contain viruses or malware that could harm or infect your device upon visiting.
    """)
else:
    st.title("🛡️ 基于卷积神经网络（CNN）与Transformer模型的恶意网址智能检测系统")
    st.markdown("""
    <style>
        .stTextInput input {font-size: 16px !important;}
        .stProgress > div > div {background-color: #28a745 !important;}
    </style>
    """, unsafe_allow_html=True)

    col1 = st.columns([3])[0]

    url = st.text_input("输入需要检测的URL地址：", "", 
                      placeholder="www.example.com/...")

    if st.button("开始检测", use_container_width=True):
        if not url:
            st.warning("请输入有效的URL地址")
        else:
            with st.spinner("正在分析URL..."):
                processed = preprocess_url(url)
                pred = model.predict(processed)
                confidence = np.max(pred)
                label = label_encoder.inverse_transform([np.argmax(pred)])[0]

            # 结果显示
            result = threat_descriptions[label]

            st.subheader("检测结果")
            st.markdown(f"""
            <div style="border-left:4px solid #28a745; padding-left:1rem;">
                <h3 style='margin:0;color:#28a745;'>
                    {result['emoji']} {result['desc']['zh']}
                    <small style='font-size:0.8em;'>({label})</small>
                </h3>
                <p>置信度：<strong>{confidence:.2%}</strong></p>
            </div>
            """, unsafe_allow_html=True)

    # 侧边栏说明
    st.sidebar.markdown("""
    ## 使用说明
    1. **粘贴URL：** 在输入框中粘贴您需要检测的网址（例如：www.example.com）。请确保URL格式正确。
    2. **点击「开始检测」按钮：** 点击按钮后，系统将自动分析您输入的URL，判断其安全性。
    3. **等待分析结果：** 检测过程可能需要几秒钟，取决于输入网址的复杂度。请耐心等待。
    4. **查看检测结果：** 系统将展示该网址的安全等级及其置信度，帮助您判断网站的风险性。

    ## 检测类型说明
    - ✅ **安全网址**：表示该网址是可信的、无安全风险的正常网站，您可以放心访问。
    - 💥 **网页篡改**：该网址可能已被恶意修改，内容存在篡改风险，访问时可能会被引导到不安全的页面。
    - 🎣 **钓鱼网站**：这是一个仿冒网站，通常用于盗取您的个人信息（如密码、银行账户等），务必小心。
    - 🦠 **恶意软件**：该网站可能包含病毒或恶意软件，访问后可能对您的设备造成危害或感染。
    """)
