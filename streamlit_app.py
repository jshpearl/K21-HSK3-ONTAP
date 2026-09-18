import streamlit as st
import random
import requests
import datetime

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="HSK 3 Vocabulary Master - Cô Bảo Ngọc",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- TÙY CHỈNH GIAO DIỆN (Chữ đen rõ ràng, Ẩn Sidebar & Header/Toolbar, Nút bấm nền trắng chữ đen) ---
st.markdown("""
<style>
    /* 1. Ẩn hoàn toàn Sidebar & Header/Toolbar/Logo góc phải */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }

    /* 2. Style tổng thể */
    .stApp {
        background-color: #F8FAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        color: #000000 !important;
    }
    
    body, p, div, span, label, li, input {
        color: #000000 !important;
    }

    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 680px !important;
    }

    /* Tiêu đề */
    .main-title {
        color: #D32F2F !important;
        text-align: center;
        font-size: 1.9rem;
        font-weight: 900;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #00695C !important;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
    }

    /* Form học viên */
    .user-box {
        background-color: #FFFFFF;
        border: 2px solid #CBD5E0;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }

    /* Flashcard Quizlet 3D Flip */
    .flip-card {
        background-color: transparent;
        width: 100%;
        height: 230px;
        perspective: 1000px;
        margin: 10px 0 15px 0;
        cursor: pointer;
    }
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s;
        transform-style: preserve-3d;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
    }
    .flip-card:hover .flip-card-inner, .flip-card:active .flip-card-inner {
        transform: rotateY(180deg);
    }
    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        border-radius: 16px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 20px;
        box-sizing: border-box;
    }
    .flip-card-front {
        background-color: #FFFFFF;
        border: 3px solid #D32F2F;
        color: #000000;
    }
    .flip-card-back {
        background-color: #F0FFF4;
        border: 3px solid #38A169;
        color: #000000;
        transform: rotateY(180deg);
    }

    /* Chữ Hán & Nghĩa */
    .card-hanzi {
        font-size: 3.8rem;
        font-weight: 900;
        color: #000000 !important;
        line-height: 1.1;
    }
    .card-pos {
        display: inline-block;
        background-color: #E6FFFA;
        color: #000000 !important;
        border: 1px solid #00695C;
        padding: 3px 12px;
        border-radius: 10px;
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .card-meaning {
        font-size: 1.5rem;
        font-weight: 800;
        color: #000000 !important;
    }

    /* Custom Button: Nền trắng chữ đen */
    .stButton>button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #CBD5E0 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        border-color: #D32F2F !important;
        background-color: #FFF5F5 !important;
        color: #D32F2F !important;
    }

    /* Đề câu hỏi màu đậm nổi bật */
    .question-title {
        color: #1E3A8A !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        margin-top: 10px;
        margin-bottom: 6px;
    }

    /* Custom Radio cho đáp án */
    .stRadio label {
        color: #000000 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    /* Đáp án giải thích */
    .exp-correct {
        background-color: #DEF7EC;
        border-left: 5px solid #0E9F6E;
        color: #000000 !important;
        padding: 10px 12px;
        border-radius: 6px;
        margin-top: 6px;
        font-size: 0.95rem;
    }
    .exp-wrong {
        background-color: #FDE8E8;
        border-left: 5px solid #F05252;
        color: #000000 !important;
        padding: 10px 12px;
        border-radius: 6px;
        margin-top: 6px;
        font-size: 0.95rem;
    }

    /* Sub-tabs cho 4 phần bài tập */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: nowrap;
        background-color: #EDF2F7;
        border-radius: 8px 8px 0px 0px;
        padding: 4px 10px;
        font-weight: 800;
        font-size: 0.9rem;
        color: #000000 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
    }

    /* Khung chúc mừng */
    .congrats-card {
        background-color: #C6F6D5;
        border: 2px solid #2F855A;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: #000000 !important;
        font-size: 1.3rem;
        font-weight: 900;
        margin: 15px 0;
    }

    /* Footer Teacher */
    .teacher-footer {
        text-align: center;
        color: #000000 !important;
        font-size: 1.3rem;
        font-weight: 900;
        margin-top: 35px;
        margin-bottom: 25px;
        padding-top: 15px;
        border-top: 2px dashed #CBD5E0;
    }
</style>
""", unsafe_allow_html=True)

# --- DỮ LIỆU TỪ VỰNG NHÓM 1 (20 từ - Không ngoặc đơn) ---
VOCAB_G1 = [
    {"hanzi": "裙子", "type": "danh từ", "meaning": "váy"},
    {"hanzi": "刻", "type": "lượng từ", "meaning": "15 phút, khắc"},
    {"hanzi": "除了", "type": "giới từ", "meaning": "ngoài… ra"},
    {"hanzi": "上网", "type": "động từ", "meaning": "lên mạng"},
    {"hanzi": "为", "type": "giới từ", "meaning": "vì, cho"},
    {"hanzi": "过去", "type": "danh từ", "meaning": "quá khứ"},
    {"hanzi": "起来", "type": "động từ", "meaning": "đứng dậy, lên"},
    {"hanzi": "瘦", "type": "tính từ", "meaning": "gầy"},
    {"hanzi": "留学", "type": "động từ", "meaning": "du học"},
    {"hanzi": "像", "type": "động từ", "meaning": "giống"},
    {"hanzi": "花", "type": "danh từ", "meaning": "hoa"},
    {"hanzi": "简单", "type": "tính từ", "meaning": "đơn giản"},
    {"hanzi": "明白", "type": "tính từ/động từ", "meaning": "rõ ràng, hiểu"},
    {"hanzi": "提高", "type": "động từ", "meaning": "nâng cao"},
    {"hanzi": "还是", "type": "liên từ", "meaning": "hay là"},
    {"hanzi": "花", "type": "động từ", "meaning": "tốn, tiêu tốn"},
    {"hanzi": "灯", "type": "danh từ", "meaning": "đèn"},
    {"hanzi": "生气", "type": "động từ", "meaning": "tức giận"},
    {"hanzi": "会议", "type": "danh từ", "meaning": "cuộc họp"},
    {"hanzi": "被", "type": "giới từ", "meaning": "bị, được (bị động)"}
]

# --- DỮ LIỆU BÀI TẬP 4 TAB (TỔNG 60 CÂU RÕ RÀNG) ---

# TAB 1: Kiểm tra từ vựng (20 câu: Nhận diện chữ Hán, từ loại & nghĩa)
QUIZ_TAB1 = [
    {"q": "1. Chữ Hán '裙子' thuộc từ loại gì và mang nghĩa là gì?", "options": ["Danh từ - Váy", "Tính từ - Gầy", "Động từ - Du học", "Giới từ - Bị"], "ans": "Danh từ - Váy", "exp": "裙子 (qúnzi) là danh từ mang nghĩa 'váy'."},
    {"q": "2. Từ nào mang nghĩa '15 phút, khắc'?", "options": ["刻", "灯", "瘦", "为"], "ans": "刻", "exp": "刻 (kè) là lượng từ chỉ 15 phút (khắc)."},
    {"q": "3. Từ '除了' mang nghĩa là gì?", "options": ["Ngoài… ra", "Mặc dù", "Cho nên", "Bởi vì"], "ans": "Ngoài… ra", "exp": "除了 (chúle) mang nghĩa 'ngoài ... ra'."},
    {"q": "4. Từ nào mang nghĩa 'lên mạng'?", "options": ["上网", "留学", "提高", "生气"], "ans": "上网", "exp": "上网 (shàng wǎng) nghĩa là 'lên mạng'."},
    {"q": "5. Giới từ '为' trong HSK 3 mang nghĩa gì?", "options": ["Vì, cho", "Ở, tại", "Cùng, với", "Từ, đến"], "ans": "Vì, cho", "exp": "为 (wèi) là giới từ mang nghĩa 'vì, cho'."},
    {"q": "6. Từ '过去' chỉ khoảng thời gian nào?", "options": ["Quá khứ", "Hiện tại", "Tương lai", "Bây giờ"], "ans": "Quá khứ", "exp": "过去 (guòqù) là danh từ chỉ 'quá khứ'."},
    {"q": "7. Động từ '起来' mang nghĩa là gì?", "options": ["Đứng dậy, lên", "Đi xuống", "Rời khỏi", "Trở về"], "ans": "Đứng dậy, lên", "exp": "起来 (qǐlai) nghĩa là 'đứng dậy, lên'."},
    {"q": "8. Tính từ '瘦' trái nghĩa với từ nào?", "options": ["胖 (Béo)", "高 (Cao)", "矮 (Thấp)", "老 (Già)"], "ans": "胖 (Béo)", "exp": "瘦 (shòu - gầy) trái nghĩa với 胖 (pàng - béo)."},
    {"q": "9. Từ nào mang nghĩa 'du học'?", "options": ["留学", "复习", "练习", "学习"], "ans": "留学", "exp": "留学 (liúxué) có nghĩa là 'du học'."},
    {"q": "10. Động từ '像' mang nghĩa là gì?", "options": ["Giống", "Khác", "Muốn", "Cần"], "ans": "Giống", "exp": "像 (xiàng) có nghĩa là 'giống'."},
    {"q": "11. Chữ '花' khi là danh từ mang nghĩa gì?", "options": ["Hoa", "Tiêu tiền", "Trái cây", "Cỏ"], "ans": "Hoa", "exp": "花 (huā) danh từ nghĩa là 'hoa'."},
    {"q": "12. Tính từ '简单' mang nghĩa là gì?", "options": ["Đơn giản", "Phức tạp", "Khó khăn", "Nghiêm túc"], "ans": "Đơn giản", "exp": "简单 (jiǎndān) nghĩa là 'đơn giản'."},
    {"q": "13. Từ '明白' mang nghĩa là gì?", "options": ["Rõ ràng, hiểu", "Quên mất", "Sợ hãi", "Lo lắng"], "ans": "Rõ ràng, hiểu", "exp": "明白 (míngbai) có nghĩa là 'rõ ràng, hiểu'."},
    {"q": "14. Từ '提高' mang nghĩa là gì?", "options": ["Nâng cao", "Hạ thấp", "Thay đổi", "Bắt đầu"], "ans": "Nâng cao", "exp": "提高 (tígāo) nghĩa là 'nâng cao'."},
    {"q": "15. Liên từ '还是' dùng trong câu nào?", "options": ["Câu hỏi lựa chọn (Hay là)", "Câu trần thuật (Hoặc là)", "Câu điều kiện (Nếu)", "Câu bị động"], "ans": "Câu hỏi lựa chọn (Hay là)", "exp": "还是 (háishì) dùng trong câu hỏi lựa chọn 'A hay là B'."},
    {"q": "16. Chữ '花' trong '花钱' thuộc từ loại gì?", "options": ["Động từ (Tiêu tốn)", "Danh từ", "Tính từ", "Lượng từ"], "ans": "Động từ (Tiêu tốn)", "exp": "花 (huā) trong 花钱 là động từ nghĩa là 'tiêu, tốn'."},
    {"q": "17. Danh từ '灯' mang nghĩa là gì?", "options": ["Đèn", "Bảng", "Bàn", "Ghế"], "ans": "Đèn", "exp": "灯 (dēng) nghĩa là 'đèn'."},
    {"q": "18. Từ '生气' mang nghĩa là gì?", "options": ["Tức giận", "Vui vẻ", "Cảm động", "Buồn rầu"], "ans": "Tức giận", "exp": "生气 (shēng qì) nghĩa là 'tức giận'."},
    {"q": "19. Danh từ '会议' mang nghĩa là gì?", "options": ["Cuộc họp", "Trường học", "Bệnh viện", "Công ty"], "ans": "Cuộc họp", "exp": "会议 (huìyì) nghĩa là 'cuộc họp'."},
    {"q": "20. Giới từ '被' dùng trong kiểu câu nào?", "options": ["Câu bị động", "Câu so sánh", "Câu chữ 把", "Câu tồn tại"], "ans": "Câu bị động", "exp": "被 (bèi) là giới từ dùng trong câu bị động."}
]

# TAB 2: Điền vào chỗ trống (20 câu: 10 Dễ, 7 TB, 3 Khó)
QUIZ_TAB2 = [
    # 10 câu Dễ (Hiểu nghĩa cơ bản)
    {"q": "1. [Dễ] 妹妹今天穿了一条漂亮的新（  ）。", "options": ["裙子", "灯", "会议", "刻"], "ans": "裙子", "exp": "Dễ: 裙子 (váy) đi với lượng từ 条."},
    {"q": "2. [Dễ] 现在是八点一（  ），会议马上就要开始了。", "options": ["刻", "瘦", "花", "被"], "ans": "刻", "exp": "Dễ: 一刻 nghĩa là 15 phút (8 giờ 15 phút)."},
    {"q": "3. [Dễ] 爷爷每天晚饭后都喜欢在房间里（  ）看新闻。", "options": ["上网", "留学", "提高", "生气"], "ans": "上网", "exp": "Dễ: 上网看新闻 (lên mạng xem tin tức)."},
    {"q": "4. [Dễ] 事情已经过去了，你就不要再（  ）了。", "options": ["生气", "简单", "明白", "瘦"], "ans": "生气", "exp": "Dễ: 生气 (tức giận)."},
    {"q": "5. [Dễ] 生病之后，他的身体比以前（  ）多了。", "options": ["瘦", "简单", "明白", "还是"], "ans": "瘦", "exp": "Dễ: 瘦 (gầy đi)."},
    {"q": "6. [Dễ] 毕业以后，他打算去中国（  ）两年。", "options": ["留学", "上网", "生气", "提高"], "ans": "留学", "exp": "Dễ: 去中国留学 (du học Trung Quốc)."},
    {"q": "7. [Dễ] 桌子上摆着一盆新鲜的（  ）。", "options": ["花", "灯", "裙子", "会议"], "ans": "花", "exp": "Dễ: 一盆花 (một chậu hoa)."},
    {"q": "8. [Dễ] 房间里太暗了，请把（  ）打开吧。", "options": ["灯", "裙子", "花", "会议"], "ans": "灯", "exp": "Dễ: 把灯打开 (bật đèn lên)."},
    {"q": "9. [Dễ] 经理正在三楼开一个重要的（  ）。", "options": ["会议", "裙子", "灯", "刻"], "ans": "会议", "exp": "Dễ: 开会议 (họp cuộc họp)."},
    {"q": "10. [Dễ] 为了买这辆新车，他（  ）了不少钱。", "options": ["花", "瘦", "起", "刻"], "ans": "花", "exp": "Dễ: 花钱 (tiêu tiền)."},

    # 7 câu Trung bình (Ngữ cảnh & Loại từ)
    {"q": "11. [Trung bình] （  ）他以外，其他人今天都按时参加了活动。", "options": ["除了", "还是", "过去", "起来"], "ans": "除了", "exp": "TB: Cấu trúc 除了……以外 (Ngoài ... ra)."},
    {"q": "12. [Trung bình] 大家（  ）这次考试做了充分的准备。", "options": ["为", "被", "像", "刻"], "ans": "为", "exp": "TB: 为……做准备 (Chuẩn bị cho ...)."},
    {"q": "13. [Trung bình] 他站（  ），向大家热情地打招呼。", "options": ["起来", "过去", "提高", "留学"], "ans": "起来", "exp": "TB: Bổ ngữ xu hướng 站起来 (đứng dậy)."},
    {"q": "14. [Trung bình] 这个孩子长得非常（  ）他的爸爸。", "options": ["像", "为", "被", "除了"], "ans": "像", "exp": "TB: 长得很像 (Trông rất giống)."},
    {"q": "15. [Trung bình] 这道数学题非常（  ），大家很快就做出来了。", "options": ["简单", "生气", "瘦", "被"], "ans": "简单", "exp": "TB: 非常简单 (Rất đơn giản)."},
    {"q": "16. [Trung bình] 经过这段时间的练习，他的汉语水平（  ）了不少。", "options": ["提高", "过去", "像", "为"], "ans": "提高", "exp": "TB: 水平提高 (Trình độ nâng cao)."},
    {"q": "17. [Trung bình] 你想喝热茶，（  ）想喝冷饮？", "options": ["还是", "除了", "被", "刻"], "ans": "还是", "exp": "TB: 还是 dùng trong câu hỏi lựa chọn."},

    # 3 câu Khó (Ngữ pháp nâng cao HSK 3)
    {"q": "18. [Khó] 他的自行车（  ）别人借走了，到现在还没还。", "options": ["被", "为", "像", "除了"], "ans": "被", "exp": "Khó: Câu bị động HSK 3: Chủ ngữ + 被 + Đối tượng tác động + Động từ."},
    {"q": "19. [Khó] 老师讲得很清楚，我现在完全（  ）这句话的意思了。", "options": ["明白", "提高", "留学", "上网"], "ans": "明白", "exp": "Khó: 明白 đóng vai trò kết quả hành động hiểu rõ."},
    {"q": "20. [Khó] 你别（  ）了，有话好好说，大家都是为了工作。", "options": ["生气", "简单", "明白", "提高"], "ans": "生气", "exp": "Khó: Phố từ 别 + Động từ 生气 (Đừng tức giận)."}
]

# TAB 3: Sắp xếp câu (10 câu)
QUIZ_TAB3 = [
    {"q": "1. Sắp xếp: 这条 / 裙子 / 买的 / 是 / 在超市", "options": ["这条裙子是在超市买的。", "是在超市买的这条裙子。", "超市买的是这条裙子。", "这条裙子买的是在超市。"], "ans": "这条裙子是在超市买的。", "exp": "Cấu trúc nhấn mạnh 是……的: S + 是 + Địa điểm + V + 的."},
    {"q": "2. Sắp xếp: 现在 / 八点 / 差一刻 / 是", "options": ["现在是八点差一刻。", "八点差一刻是现在。", "差一刻是八点现在。", "现在差一刻是八点。"], "ans": "现在是八点差一刻。", "exp": "Trật tự thời gian: 现在是 + 八点差一刻 (8h kém 15)."},
    {"q": "3. Sắp xếp: 除了 / 他 / 都 / 来了 / 以外", "options": ["除了他以外大家都来了。", "Ngoài ra mọi người đều đến.", "大家都来了除了他以外。", "他除了以外大家都来了。"], "ans": "除了他以外大家都来了。", "exp": "Mẫu câu: 除了 + N + 以外，S + 都 + V."},
    {"q": "4. Sắp xếp: 喜欢 / 晚饭后 / 上网 / 查资料 / 我", "options": ["晚饭后我喜欢上网查资料。", "我上网查资料喜欢晚饭后。", "查资料晚饭后我上网。", "上网晚饭后我查资料。"], "ans": "晚饭后我喜欢上网查资料。", "exp": "Trạng ngữ thời gian (晚饭后) + Chủ ngữ (我) + V."},
    {"q": "5. Sắp xếp: 大家 / 为 / 成功 / 庆祝 / 他的", "options": ["大家为他的成功庆祝。", "大家庆祝为他的成功。", "他的成功为大家庆祝。", "为他的成功大家庆祝。"], "ans": "大家为他的成功庆祝。", "exp": "Mẫu câu: S + 为 + N + V (Mọi người chúc mừng cho thành công của anh ấy)."},
    {"q": "6. Sắp xếp: 站起来 / 请 / 慢慢地 / 大家", "options": ["请大家慢慢地站起来。", "大家请慢慢地站起来。", "慢慢地请大家站起来。", "站起来请大家慢慢地。"], "ans": "请大家慢慢地站起来。", "exp": "Mẫu câu lịch sự: 请 + S + Trạng ngữ (慢慢地) + Động từ (站起来)."},
    {"q": "7. Sắp xếp: 瘦了 / 很多 / 运动 / 以后 / 他", "options": ["运动以后他瘦了很多。", "他瘦了很多运动以后。", "运动以后瘦了很多他。", "瘦了很多以后他运动。"], "ans": "运动以后他瘦了很多。", "exp": "Thời gian (运动以后) + Chủ ngữ (他) + Tính từ (瘦了)+ Bổ ngữ (很多)."},
    {"q": "8. Sắp xếp: 打算 / 去 / 留学 / 弟弟 / 英国", "options": ["弟弟打算去英国留学。", "弟弟去英国打算留学。", "打算去英国留学弟弟。", "英国弟弟打算去留学。"], "ans": "弟弟打算去英国留学。", "exp": "Trật tự: S (弟弟) + 打算 + 去 + Địa điểm (英国) + V (留学)."},
    {"q": "9. Sắp xếp: 明白 / 这句话的 / 我 / 意思 / 不", "options": ["我不明白这句话的意思。", "我明白不这句话的意思。", "这句话的意思我不明白。", "不明白我这句话的意思。"], "ans": "我不明白这句话的意思。", "exp": "Phủ định: S + 不 + V (明白) + Tân ngữ (这句话的意思)."},
    {"q": "10. Sắp xếp: 被 / 拿走了 / 字典 / 别人 / 我的", "options": ["我的字典被别人拿走了。", "别人被我的字典拿走了。", "我的字典拿走了被别人。", "被别人我的字典拿走了。"], "ans": "我的字典被别人拿走了。", "exp": "Câu bị động: Bị thể (我的字典) + 被 + Đối tượng tác động (别人) + V (拿走了)."}
]

# TAB 4: Chọn câu trả lời (10 câu)
QUIZ_TAB4 = [
    {"q": "1. 问：你想吃面条还是吃米饭？——答：（  ）", "options": ["给我一碗面条吧。", "我吃了一碗面条。", "面条很好吃。", "我不喜欢吃米饭。"], "ans": "给我一碗面条吧。", "exp": "Câu hỏi 还是 yêu cầu chọn 1 phương án cụ thể."},
    {"q": "2. 问：你的汉语成绩怎么提高了 constitutional 这么快？——答：（  ）", "options": ["因为我每天都认真练习。", "考试题太难了。", "我还没有复习。", "明天就要考试了。"], "ans": "因为我每天都认真练习。", "exp": "Hỏi 怎么 (tại sao) trả lời bằng 因为 (vì chăm chỉ)."},
    {"q": "3. 问：房间里的灯怎么没开？——答：（  ）", "options": ["灯坏了，还没有换新的。", "外面天气很好。", "灯非常漂亮。", "我买了三个灯。"], "ans": "灯坏了，还没有换新的。", "exp": "Giải thích nguyên nhân đèn chưa bật (đèn hỏng)."},
    {"q": "4. 问：他怎么突然生气了？——答：（  ）", "options": ["因为大家都没有听他的解释。", "他今天很高兴。", "他在办公室开会。", "他已经去睡觉了。"], "ans": "因为大家都没有听他的解释。", "exp": "Trở lời lý do tức giận (vì không ai nghe giải thích)."},
    {"q": "5. 问： your 护照找不到了，怎么办？——答：（  ）", "options": ["别着急，一定被放在哪个包里了。", "护照是红色的。", "我已经买好机票了。", "护照非常重要。"], "ans": "别着急，一定被放在哪个包里了。", "exp": "An ủi và đưa giải pháp (Đừng lo, chắc ở trong túi)."},
    {"q": "6. 问：你去过中国留学吗？——答：（  ）", "options": ["去过，我在北京留学了两年。", "我不喜欢去中国。", "中国很大。", "明天我去留学。"], "ans": "去过，我在北京留学了两年。", "exp": "Trả lời câu hỏi kinh nghiệm 去过 ... 吗?"},
    {"q": "7. 问：这条裙子贵不贵？——答：（  ）", "options": ["不太贵，打折后很便宜。", "裙子是红色的。", "我很喜欢穿裙子。", "我在超市买的。"], "ans": "不太贵，打折后很便宜。", "exp": "Trả lời về giá cả (不贵)."},
    {"q": "8. 问：你现在有时间吗？我们开个短会。——答：（  ）", "options": ["好的，我马上过去。", "我现在没在开会。", "会议非常重要。", "我不太明白。"], "ans": "好的，我马上过去。", "exp": "Đồng ý và ứng đáp lịch sự (Được, tôi sang ngay)."},
    {"q": "9. 问：这个数学题简单吗？——答：（  ）", "options": ["非常简单，我一分钟就做出来了。", "数学很有趣。", "我不喜欢数学。", "老师还没来。"], "ans": "非常简单，我一分钟就做出来了。", "exp": "Trả lời độ khó (rất đơn giản)."},
    {"q": "10. 问：除了汉语，你还会说什么语言？——答：（  ）", "options": ["除了汉语以外，我还会说英语。", "我汉语说得很好。", "英语很难学。", "我很喜欢学语言。"], "ans": "除了汉语以外，我还会说英语。", "exp": "Trả lời bằng cấu trúc 除了……以外，还……"}
]

# Webhook URL mặc định gửi điểm cho cô Bảo Ngọc
DEFAULT_WEBHOOK = "https://script.google.com/macros/s/AKfycbykR1r2_VTPvB5SVrDSMhmBqQhWYdQjPacrLBmoCIsE2WbBqGA0mBDZA0uUmLd2-Hli/exec"

# --- HÀM GỬI ĐIỂM VỀ GOOGLE SHEETS VIA WEBHOOK ---
def send_to_google_sheet(sheet_url, user_name, group_name, score, total, percentage):
    if not sheet_url:
        return False, "Chưa cấu hình URL"
    payload = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": user_name,
        "group": group_name,
        "score": f"{score}/{total}",
        "percentage": f"{percentage:.1f}%"
    }
    try:
        response = requests.post(sheet_url, json=payload, timeout=8)
        if response.status_code == 200:
            return True, "Thành công"
        else:
            return False, f"HTTP Status: {response.status_code}"
    except Exception as e:
        return False, str(e)

# --- GIAO DIỆN CHÍNH ---
st.markdown('<div class="main-title">✨ CHINH PHỤC TỪ VỰNG HSK 3 ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Cùng học và ôn từ vựng HSK3 nhé</div>', unsafe_allow_html=True)

# Form nhập tên học viên ở trang chính (Dễ dùng trên điện thoại)
st.markdown('<div class="user-box">', unsafe_allow_html=True)
u_col1, u_col2 = st.columns([1.2, 1.8])
with u_col1:
    user_name = st.text_input("👤 Họ và tên học viên:", value="Học viên HSK3")
with u_col2:
    sheet_webhook = st.text_input("📊 Webhook URL Google Sheet:", value=DEFAULT_WEBHOOK)
st.markdown('</div>', unsafe_allow_html=True)

# Tabs nhóm từ vựng
st.subheader("📌 Nhóm 1 (20 từ vựng & Bài tập)")

# -------------------------------------------------------------
# PHẦN 1: FLASHCARD TỪ VỰNG (LẬT KIỂU QUIZLET)
# -------------------------------------------------------------
st.markdown("### 🎴 Phần 1: Flashcard Từ Vựng (Lật kiểu Quizlet)")

fc_key = "fc_index_G1"
if fc_key not in st.session_state:
    st.session_state[fc_key] = 0

curr_idx = st.session_state[fc_key]
curr_item = VOCAB_G1[curr_idx]

# Bảng thẻ 3D Flip (Rê/Chạm vào thẻ để lật)
st.markdown(f"""
<div class="flip-card">
  <div class="flip-card-inner">
    <div class="flip-card-front">
      <div style="color: #A0AEC0; font-size: 0.85rem; font-weight:700;">MẶT TRƯỚC (CHẠM VÀO ĐỂ LẬT)</div>
      <div class="card-hanzi">{curr_item['hanzi']}</div>
      <div style="color: #A0AEC0; font-size: 0.85rem;">Thẻ {curr_idx + 1} / {len(VOCAB_G1)}</div>
    </div>
    <div class="flip-card-back">
      <div style="color: #2F855A; font-size: 0.85rem; font-weight:700;">MẶT SAU</div>
      <div class="card-hanzi" style="color:#2F855A; font-size: 3.2rem;">{curr_item['hanzi']}</div>
      <div class="card-meaning">{curr_item['meaning']}</div>
      <div><span class="card-pos">{curr_item['type']}</span></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# 3 Nút chuyển thẻ nền trắng chữ đen
b_col1, b_col2, b_col3 = st.columns([1, 1, 1])
with b_col1:
    if st.button("⬅️ Thẻ trước", key="prev_btn", use_container_width=True):
        st.session_state[fc_key] = (curr_idx - 1) % len(VOCAB_G1)
        st.rerun()
with b_col2:
    if st.button("🔀 Ngẫu nhiên", key="rand_btn", use_container_width=True):
        st.session_state[fc_key] = random.randint(0, len(VOCAB_G1) - 1)
        st.rerun()
with b_col3:
    if st.button("Thẻ sau ➡️", key="next_btn", use_container_width=True):
        st.session_state[fc_key] = (curr_idx + 1) % len(VOCAB_G1)
        st.rerun()

# NÚT XEM TỪ VỰNG DẠNG BẢNG (Có thể thu nhỏ lại)
st.markdown("<br>", unsafe_allow_html=True)
show_table_key = "show_vocab_table_G1"
if show_table_key not in st.session_state:
    st.session_state[show_table_key] = False

if not st.session_state[show_table_key]:
    if st.button("📊 Xem từ vựng dạng bảng", key="btn_show_table", use_container_width=True):
        st.session_state[show_table_key] = True
        st.rerun()
else:
    if st.button("▲ Thu nhỏ bảng (Ẩn bảng từ vựng)", key="btn_hide_table", use_container_width=True):
        st.session_state[show_table_key] = False
        st.rerun()
        
    st.markdown("##### 📋 Bảng tổng hợp 20 từ vựng Nhóm 1")
    table_html = """
    <table style="width:100%; border-collapse: collapse; margin-top: 10px; background-color: #FFFFFF; border: 1px solid #CBD5E0;">
      <thead>
        <tr style="background-color: #EDF2F7; color: #000000; text-align: center; font-weight: bold;">
          <th style="padding: 8px; border: 1px solid #CBD5E0;">STT</th>
          <th style="padding: 8px; border: 1px solid #CBD5E0;">Chữ Hán</th>
          <th style="padding: 8px; border: 1px solid #CBD5E0;">Từ loại</th>
          <th style="padding: 8px; border: 1px solid #CBD5E0;">Ý nghĩa</th>
        </tr>
      </thead>
      <tbody>
    """
    for idx, v in enumerate(VOCAB_G1):
        table_html += f"""
        <tr style="text-align: center; color: #000000; border: 1px solid #CBD5E0;">
          <td style="padding: 6px; border: 1px solid #CBD5E0; font-weight: bold;">{idx+1}</td>
          <td style="padding: 6px; border: 1px solid #CBD5E0; font-size: 1.3rem; font-weight: bold; color: #D32F2F;">{v['hanzi']}</td>
          <td style="padding: 6px; border: 1px solid #CBD5E0;">{v['type']}</td>
          <td style="padding: 6px; border: 1px solid #CBD5E0; font-weight: bold;">{v['meaning']}</td>
        </tr>
        """
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)

st.markdown("<hr style='margin: 25px 0;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# PHẦN 2: BÀI TẬP CHIA THÀNH 4 TAB
# -------------------------------------------------------------
st.markdown("### 📝 Phần 2: Bài Tập Ôn Luyện (4 Phần)")

quiz_tab1, quiz_tab2, quiz_tab3, quiz_tab4 = st.tabs([
    "1. Kiểm tra từ vựng",
    "2. Điền vào chỗ trống",
    "3. Sắp xếp câu",
    "4. Chọn câu trả lời"
])

def render_quiz_section(tab_obj, quiz_data, tab_prefix):
    with tab_obj:
        submitted_key = f"sub_{tab_prefix}"
        if submitted_key not in st.session_state:
            st.session_state[submitted_key] = False
            
        user_ans = {}
        with st.form(key=f"form_{tab_prefix}"):
            for q_i, q_item in enumerate(quiz_data):
                st.markdown(f'<div class="question-title">{q_item["q"]}</div>', unsafe_allow_html=True)
                user_ans[q_i] = st.radio(
                    label=f"Câu {q_i+1}",
                    options=q_item["options"],
                    key=f"q_{tab_prefix}_{q_i}",
                    index=None,
                    label_visibility="collapsed"
                )
                
                if st.session_state[submitted_key]:
                    selected = user_ans[q_i]
                    correct = q_item["ans"]
                    exp = q_item.get("exp", "")
                    if selected == correct:
                        st.markdown(f'<div class="exp-correct">✅ <b>Đúng!</b> Đáp án: <b>{correct}</b><br>💡 <i>{exp}</i></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="exp-wrong">❌ <b>Chưa chính xác!</b><br>• Đã chọn: <span style="text-decoration:line-through; color:#C53030;">{selected if selected else "Chưa chọn"}</span><br>• Đáp án đúng: <b>{correct}</b><br>💡 <i>{exp}</i></div>', unsafe_allow_html=True)
                st.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)
                
            btn_sub = st.form_submit_button("🚀 Nộp bài phần này", use_container_width=True)
            
        if btn_sub:
            st.session_state[submitted_key] = True
            score = 0
            for q_i, q_item in enumerate(quiz_data):
                if user_ans.get(q_i) == q_item["ans"]:
                    score += 1
            total = len(quiz_data)
            pct = (score / total) * 100
            
            st.markdown('<div class="congrats-card">🎉 Chúc mừng bạn đã làm xong! Chăm chỉ quá!</div>', unsafe_allow_html=True)
            st.metric("Kết quả phần này", f"{score} / {total} câu đúng", f"{pct:.1f}%")
            
            with st.spinner("Đang gửi kết quả về Google Sheet..."):
                ok, msg = send_to_google_sheet(
                    sheet_url=sheet_webhook,
                    user_name=user_name,
                    group_name=f"Nhóm 1 - {tab_prefix}",
                    score=score,
                    total=total,
                    percentage=pct
                )
                if ok:
                    st.success("✅ Đã gửi điểm về Sheet cho cô Bảo Ngọc")
                else:
                    st.error("❌ Gửi không thành công, hãy chụp màn hình gửi cô Bảo Ngọc")
            st.rerun()

render_quiz_section(quiz_tab1, QUIZ_TAB1, "Tab1_KiemTraTuVung")
render_quiz_section(quiz_tab2, QUIZ_TAB2, "Tab2_DienChoTrong")
render_quiz_section(quiz_tab3, QUIZ_TAB3, "Tab3_SapXepCau")
render_quiz_section(quiz_tab4, QUIZ_TAB4, "Tab4_ChonCauTraLoi")

# --- FOOTER ---
st.markdown("""
<div class="teacher-footer">
    黄宝玉老师
</div>
""", unsafe_allow_html=True)
