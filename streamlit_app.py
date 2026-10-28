import streamlit as st
import json
import random
import requests
import datetime
import os
import re

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="HSK 3 Vocabulary Master - Cô Bảo Ngọc",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- WEBHOOK CONFIG ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwwH0wE3X1zJ5kK5M3N7P8Q9R0S1T2U3V4W5X6Y7Z/exec"

def send_to_google_sheet(user_name, group_name, score, total, percentage):
    vn_tz = datetime.timezone(datetime.timedelta(hours=7))
    vn_now = datetime.datetime.now(vn_tz)
    payload = {
        "timestamp": vn_now.strftime("%Y-%m-%d %H:%M:%S"),
        "name": user_name,
        "group": group_name,
        "score": f"{score}/{total}",
        "percentage": f"{percentage:.1f}%"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=8)
        if response.status_code == 200:
            return True, "Thành công"
        else:
            return False, f"HTTP Status {response.status_code}"
    except Exception as e:
        return False, str(e)

# --- CSS STYLING (PASTEL NHẸ NHÀNG, FONT TAHOMA, CÂU HỎI MÀU NỔI BẬT) ---
st.markdown("""
<style>
    /* 1. Ẩn Sidebar & Streamlit Header/Footer */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }

    /* 2. Ép font chữ Tahoma cho TOÀN BỘ ứng dụng */
    html, body, [class*="st-"], .stApp, button, input, select, textarea, div, span, p, label {
        font-family: 'Tahoma', Geneva, Verdana, sans-serif !important;
    }

    /* 3. Nền Gradient Pastel dịu mát */
    .stApp {
        background: linear-gradient(135deg, #FAF5FF 0%, #F3E8FF 50%, #EFF6FF 100%) !important;
    }

    /* 4. Header Box - Pastel Purple & Pink */
    .header-box {
        text-align: center;
        padding: 24px 20px;
        background: linear-gradient(135deg, #C084FC 0%, #F472B6 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 8px 20px rgba(192, 132, 252, 0.25);
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.15);
        font-family: 'Tahoma', Geneva, sans-serif !important;
    }
    .sub-title {
        font-size: 1.05rem;
        opacity: 0.95;
        margin-top: 6px;
        font-family: 'Tahoma', Geneva, sans-serif !important;
    }

    /* 5. Khung thông tin học viên */
    .user-info-card {
        background: #FFFFFF;
        padding: 18px 20px;
        border-radius: 16px;
        border: 2px solid #E9D5FF;
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.05);
        margin-bottom: 22px;
    }

    /* 6. Flashcard 3D */
    .flip-card {
        background-color: transparent;
        width: 100%;
        height: 240px;
        perspective: 1000px;
        margin-bottom: 15px;
    }
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s;
        transform-style: preserve-3d;
        cursor: pointer;
    }
    .flip-card:hover .flip-card-inner {
        transform: rotateY(180deg);
    }
    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        box-shadow: 0 6px 20px rgba(147, 51, 234, 0.08);
    }
    .flip-card-front {
        background: linear-gradient(135deg, #FFFFFF 0%, #FAF5FF 100%);
        border: 3px solid #DDD6FE;
        color: #5B21B6;
    }
    .flip-card-back {
        background: linear-gradient(135deg, #8B5CF6 0%, #A855F7 100%);
        color: white;
        transform: rotateY(180deg);
        border: 3px solid #7C3AED;
    }

    /* 7. Style Câu hỏi - In đậm + Màu sắc Pastel đậm nổi bật (Phân biệt rõ với đáp án) */
    .question-box {
        background-color: #F3E8FF;
        border-left: 5px solid #8B5CF6;
        padding: 12px 16px;
        border-radius: 10px;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    .question-title {
        font-size: 1.12rem;
        font-weight: 800;
        color: #4C1D95;
        line-height: 1.5;
        font-family: 'Tahoma', Geneva, sans-serif !important;
    }

    /* 8. Tùy chỉnh Các thẻ Tabs pastel */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F3E8FF;
        padding: 6px;
        border-radius: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 14px;
        font-weight: 700;
        color: #6B21A8;
        background-color: transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #7E22CE !important;
        box-shadow: 0 2px 8px rgba(126, 34, 206, 0.12);
    }

    /* 9. Nút bấm Nộp bài & Thao tác */
    div.stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-family: 'Tahoma', Geneva, sans-serif !important;
        transition: all 0.2s ease !important;
    }

    /* 10. Chữ ký giáo viên */
    .teacher-footer {
        text-align: center;
        color: #7E22CE;
        font-size: 1.35rem;
        font-weight: 900;
        margin-top: 40px;
        margin-bottom: 25px;
        padding-top: 15px;
        border-top: 2px dashed #E9D5FF;
        font-family: 'Tahoma', Geneva, sans-serif !important;
    }

    /* 11. Bảng điểm Chúc mừng */
    .congrats-card {
        background-color: #DCFCE7;
        border: 2px solid #22C55E;
        border-radius: 14px;
        padding: 15px;
        text-align: center;
        color: #15803D !important;
        font-size: 1.25rem;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 12px;
        font-family: 'Tahoma', Geneva, sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA (ĐỌC ĐƯỜNG DẪN TUYỆT ĐỐI AN TOÀN TRÊN STREAMLIT CLOUD) ---
@st.cache_data
def load_data():
    json_path = os.path.join(os.path.dirname(__file__), "data.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

ORDERED_GROUPS = load_data()

# --- HEADER ---
st.markdown('<div class="header-box"><div class="main-title">✨ CHINH PHỤC TỪ VỰNG HSK 3 ✨</div><div class="sub-title">Cùng học và ôn từ vựng HSK3 nhé</div></div>', unsafe_allow_html=True)

# --- USER NAME INPUT ---
st.markdown('<div class="user-info-card">', unsafe_allow_html=True)
user_name = st.text_input("👤 Họ và tên người học (Bắt buộc nhập tên để nộp bài):", value="", placeholder="Vui lòng nhập họ và tên của bạn tại đây...", key="user_name_input")
st.markdown('</div>', unsafe_allow_html=True)

# --- GROUP SELECTOR ---
group_titles = [g["title"] for g in ORDERED_GROUPS]
selected_group_title = st.selectbox("📌 Chọn Nhóm từ vựng để học và làm bài tập:", options=group_titles, index=0)

group_info = next(g for g in ORDERED_GROUPS if g["title"] == selected_group_title)

st.markdown(f"### 📌 {group_info['title']} (20 từ vựng & Bài tập)")

# PHẦN 1: FLASHCARD & BẢNG TỪ VỰNG
fc_key = f"fc_index_{group_info['id']}"
show_table_key = f"show_table_{group_info['id']}"

if fc_key not in st.session_state:
    st.session_state[fc_key] = 0
if show_table_key not in st.session_state:
    st.session_state[show_table_key] = False

vocab_list = group_info["vocab"]
curr_idx = st.session_state[fc_key]
curr_item = vocab_list[curr_idx]

flip_card_html = f"""
<div class="flip-card">
  <div class="flip-card-inner">
    <div class="flip-card-front">
      <div style="font-size:0.95rem; color:#8B5CF6; font-weight:800; margin-bottom:8px;">✦ CLICK / DI CHUỘT ĐỂ XEM NGHĨA ✦</div>
      <div style="font-size:3.2rem; font-weight:900; color:#4C1D95;">{curr_item['hanzi']}</div>
    </div>
    <div class="flip-card-back">
      <div style="font-size:2.2rem; font-weight:900; margin-bottom:4px;">{curr_item['hanzi']}</div>
      <div style="font-size:1.3rem; font-weight:700; color:#FDE047; margin-bottom:6px;">[{curr_item['pinyin']}] • {curr_item['type']}</div>
      <div style="font-size:1.4rem; font-weight:900; margin-bottom:10px;">👉 {curr_item['meaning']}</div>
      <div style="font-size:1.05rem; background:rgba(255,255,255,0.2); padding:8px 12px; border-radius:10px;">💡 {curr_item['example']}</div>
    </div>
  </div>
</div>
"""
st.markdown(flip_card_html, unsafe_allow_html=True)

col_prev, col_num, col_next = st.columns([1, 2, 1])
with col_prev:
    if st.button("⬅️ Từ trước", key=f"prev_{group_info['id']}", use_container_width=True):
        st.session_state[fc_key] = (curr_idx - 1) % len(vocab_list)
        st.rerun()
with col_num:
    st.markdown(f"<div style='text-align:center; font-weight:800; font-size:1.1rem; padding-top:6px; color:#6B21A8;'>Thẻ {curr_idx + 1} / {len(vocab_list)}</div>", unsafe_allow_html=True)
with col_next:
    if st.button("Từ tiếp ➡️", key=f"next_{group_info['id']}", use_container_width=True):
        st.session_state[fc_key] = (curr_idx + 1) % len(vocab_list)
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
btn_table_label = "🙈 Thu gọn Bảng từ vựng" if st.session_state[show_table_key] else "📖 Mở rộng Bảng 20 từ vựng Nhóm này"
if st.button(btn_table_label, key=f"btn_tb_{group_info['id']}", use_container_width=True):
    st.session_state[show_table_key] = not st.session_state[show_table_key]
    st.rerun()

if st.session_state[show_table_key]:
    table_md = "| STT | Chữ Hán | Phiên âm | Từ loại | Ý nghĩa | Ví dụ minh họa |\n| :---: | :---: | :---: | :---: | :--- | :--- |\n"
    for v_i, v_data in enumerate(vocab_list, 1):
        table_md += f"| {v_i} | **{v_data['hanzi']}** | {v_data['pinyin']} | *{v_data['type']}* | {v_data['meaning']} | {v_data['example']} |\n"
    st.markdown(table_md)

st.markdown("<hr style='border:1px dashed #DDD6FE; margin:25px 0;'>", unsafe_allow_html=True)

# PHẦN 2: BÀI TẬP 4 TABS
def render_quiz_section(sub_quiz_data, sub_key):
    submitted_flag = f"sub_submitted_{group_info['id']}_{sub_key}"
    res_data_flag = f"sub_res_data_{group_info['id']}_{sub_key}"

    if submitted_flag not in st.session_state:
        st.session_state[submitted_flag] = False

    if st.session_state[submitted_flag] and res_data_flag in st.session_state:
        res = st.session_state[res_data_flag]
        st.markdown('''<div class="congrats-card">🎉 Chúc mừng bạn đã làm xong! Chăm chỉ quá!</div>''', unsafe_allow_html=True)

        st.metric("Kết quả làm bài", f"{res['score']} / {res['total']} câu đúng", f"{res['pct']:.1f}%")

        if res['score'] < res['total']:
            st.markdown('''<div style="background-color: #FEF3C7; border: 2px solid #F59E0B; border-radius: 12px; padding: 12px 16px; margin-top: 10px; margin-bottom: 15px; color: #92400E; font-weight: 800; text-align: center; font-size: 1.05rem;">💡 Bạn hãy kiểm tra lại danh sách câu hỏi bên dưới để xem đáp án đúng và lời giải thích chi tiết cho các câu làm chưa chính xác nhé!</div>''', unsafe_allow_html=True)

        if res['ok']:
            st.success(f"✅ Đã gửi điểm về Sheet cho cô Bảo Ngọc ({user_name.strip()}: {res['score']}/{res['total']})")
        else:
            st.info(f"ℹ️ Đã ghi nhận điểm trên ứng dụng: {res['score']}/{res['total']} câu đúng. ({res['msg']})")

    user_ans = {}
    for q_i, q_data in enumerate(sub_quiz_data):
        # 🟢 XÓA DƯ SỐ ĐẦU CÂU (Loại bỏ các số thứ tự thừa như "1. ", "2. ")
        clean_q_text = re.sub(r"^\d+\.\s*", "", q_data['q'])

        # 🟢 ĐỊNH DẠNG CÂU HỎI IN ĐẬM VỚI MÀU TÍM PASTEL ĐẬM NỔI BẬT KHÁC VỚI ĐÁP ÁN
        st.markdown(f'''<div class="question-box"><div class="question-title">Câu {q_i + 1}: {clean_q_text}</div></div>''', unsafe_allow_html=True)

        shuffled_key = f"shuffled_opts_{group_info['id']}_{sub_key}_{q_i}"
        if shuffled_key not in st.session_state:
            opts = list(q_data["options"])
            random.shuffle(opts)
            st.session_state[shuffled_key] = opts
        else:
            opts = st.session_state[shuffled_key]

        radio_key = f"q_{group_info['id']}_{sub_key}_{q_i}"
        ans = st.radio(
            f"Chọn đáp án cho câu {q_i + 1}:",
            opts,
            key=radio_key,
            index=None,
            label_visibility="collapsed"
        )
        user_ans[q_i] = ans

        if st.session_state[submitted_flag]:
            if ans == q_data["ans"]:
                st.success(f"✅ Đúng! ({q_data['ans']}) — {q_data['exp']}")
            elif ans is not None:
                st.error(f"❌ Chưa đúng! Đáp án đúng là: **{q_data['ans']}** — 💡 {q_data['exp']}")
            else:
                st.warning(f"⚠️ Chưa trả lời. Đáp án đúng là: **{q_data['ans']}** — 💡 {q_data['exp']}")

        st.markdown("<hr style='margin:12px 0; border:0; border-top:1px dashed #E9D5FF;'>", unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        sub_btn = st.button(f"🚀 Nộp bài - {sub_key}", key=f"btn_sub_{group_info['id']}_{sub_key}", type="primary", use_container_width=True)
    with col_btn2:
        redo_btn = st.button(f"🔄 Làm lại phần này", key=f"btn_redo_{group_info['id']}_{sub_key}", use_container_width=True)

    if redo_btn:
        st.session_state[submitted_flag] = False
        if res_data_flag in st.session_state:
            del st.session_state[res_data_flag]
        for q_i in range(len(sub_quiz_data)):
            r_k = f"q_{group_info['id']}_{sub_key}_{q_i}"
            if r_k in st.session_state:
                del st.session_state[r_k]
        st.rerun()

    if sub_btn:
        if not user_name or not user_name.strip() or user_name.strip().lower() in ["", "học viên hsk3"]:
            st.warning("⚠️ Vui lòng nhập Họ và tên ở ô thông tin phía trên trước khi nộp bài!")
        else:
            st.session_state[submitted_flag] = True
            score = 0
            unans = 0
            for q_i, q_data in enumerate(sub_quiz_data):
                ans = user_ans.get(q_i)
                if ans is None:
                    unans += 1
                elif ans == q_data["ans"]:
                    score += 1

            total = len(sub_quiz_data)
            pct = (score / total) * 100

            with st.spinner("Đang gửi điểm về Google Sheet cho cô Bảo Ngọc..."):
                ok, msg = send_to_google_sheet(
                    user_name=user_name.strip(),
                    group_name=f"{group_info['title']} - {sub_key}",
                    score=score,
                    total=total,
                    percentage=pct
                )

            st.session_state[res_data_flag] = {
                "score": score,
                "total": total,
                "pct": pct,
                "unans": unans,
                "ok": ok,
                "msg": msg
            }

            st.rerun()

sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs(["📝 1. Kiểm tra từ vựng", "✏️ 2. Điền vào chỗ trống", "🧩 3. Sắp xếp câu", "💬 4. Chọn câu trả lời"])

with sub_tab1:
    render_quiz_section(group_info["tab1"], "Kiểm tra từ vựng")
with sub_tab2:
    render_quiz_section(group_info["tab2"], "Điền vào chỗ trống")
with sub_tab3:
    render_quiz_section(group_info["tab3"], "Sắp xếp câu")
with sub_tab4:
    render_quiz_section(group_info["tab4"], "Chọn câu trả lời")

st.markdown('<div class="teacher-footer">黄宝玉老师</div>', unsafe_allow_html=True)
