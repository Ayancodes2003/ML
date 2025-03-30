import streamlit as st
import os
import time
#import base64

# Page Configuration
st.set_page_config(page_title="AI Security Analyzer", page_icon="🚀", layout="centered")

# Custom CSS for Styling
st.markdown(
    """
    <style>
        body {
            background-color: #1e1e2f;
            color: #e0e0e0;
        }
        .stApp {
            background: linear-gradient(135deg, #4A00E0, #8E2DE2);
        }
        .title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: #FFFFFF;
            animation: glow 2s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 10px #FFFFFF; }
            to { text-shadow: 0 0 20px #8E2DE2; }
        }
        .upload-box {
            border: 3px dashed #ffffff;
            background-color: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-top: 20px;
        }
        .success-text {
            color: #00FF7F;
        }
        .error-text {
            color: #FF6347;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown("<p class='title'>Code Quality Analysis(Prob State: 9)</p>", unsafe_allow_html=True)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# File Upload Section
st.markdown("<div class='upload-box'>📥 Upload a file for detailed security analysis (Supported: .py, .js, .java, .cpp)</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["py", "js", "java", "cpp"], label_visibility="collapsed")

if uploaded_file:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ File {uploaded_file.name} uploaded successfully!")
    
    # Security Analysis Simulation
    with st.spinner("⚙ Performing AI-Powered Security Analysis..."):
        docker_cmd = f"docker run -v {os.getcwd()}:/target " \
                     f"-e GOOGLE_API_KEY={os.environ.get('GOOGLE_API_KEY')} " \
                     f"-e GEMINI_API_KEY={os.environ.get('GEMINI_API_KEY')} " \
                     f"ai-security-analyzer dir -v -t /target/uploads -o /target/security_design.md " \
                     f"--agent-provider google --agent-model gemini-2.0-flash-thinking-exp"
        time.sleep(3)
        os.system(docker_cmd)

    st.success("🎉 Analysis Complete! Download your security report below.")
    
    # Report Display and Download
    report_path = "security_design.md"
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            report_content = f.read()
        
        st.text_area("📜 Security Report:", report_content, height=400)
        st.download_button("⬇ Download Report", data=report_content, file_name="security_design.md", mime="text/markdown")
    else:
        st.error("❌ Analysis failed! Please check the logs.")