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

# --- TÙY CHỈNH GIAO DIỆN (Chữ màu đen sắc nét, Ô điền tên nền trắng viền đen, Nộp bài & Chọn đáp án nền nhạt chữ đen) ---
st.markdown("""
<style>
    /* 1. Ẩn hoàn toàn Thanh bên (Sidebar) & Header/Logo/Toolbar góc phải trên */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }

    /* 2. Tổng thể & Chữ màu đen sắc nét */
    .stApp {
        background-color: #F8FAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        color: #000000 !important;
    }
    
    body, p, div, span, label, li, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }

    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 680px !important;
    }

    /* Header tiêu đề */
    .main-title {
        color: #D32F2F !important;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 900;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #00695C !important;
        text-align: center;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
    }

    /* Ô điền tên: Nền màu trắng, viền đen */
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        color: #000000 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 8px 12px !important;
    }
    div[data-testid="stTextInput"] label {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
    }

    /* Các đáp án lựa chọn: Nền màu nhạt, viền bo tròn nhẹ, chữ đen */
    div[role="radiogroup"] {
        gap: 8px !important;
        margin-top: 4px !important;
        margin-bottom: 8px !important;
    }
    div[role="radiogroup"] label {
        background-color: #FFF5F7 !important;
        border: 1.5px solid #FBCFE8 !important;
        border-radius: 10px !important;
        padding: 8px 14px !important;
        width: 100% !important;
        margin: 2px 0 !important;
        transition: all 0.2s ease !important;
    }
    div[role="radiogroup"] label:hover {
        background-color: #FCE7F3 !important;
        border-color: #F472B6 !important;
    }
    div[role="radiogroup"] label p {
        color: #000000 !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }

    /* Chỗ Nộp bài: Nền màu nhạt, chữ đen */
    div[data-testid="stFormSubmitButton"] button {
        background-color: #FFE4E6 !important;
        color: #000000 !important;
        border: 2px solid #FDA4AF !important;
        border-radius: 12px !important;
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        padding: 12px 20px !important;
        box-shadow: 0 3px 8px rgba(0,0,0,0.08) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background-color: #FECDD3 !important;
        border-color: #F43F5E !important;
        color: #000000 !important;
    }

    /* Nút bấm chuyển thẻ Flashcard (Nền trắng, chữ đen, viền xám) */
    .stButton button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    .stButton button:hover {
        background-color: #F1F5F9 !important;
        border-color: #94A3B8 !important;
        color: #000000 !important;
    }

    /* 3D Flip Flashcard kiểu Quizlet */
    .flip-card {
        background-color: transparent;
        width: 100%;
        height: 260px;
        perspective: 1000px;
        margin: 10px 0 20px 0;
        cursor: pointer;
    }
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        transform-style: preserve-3d;
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
        border-radius: 18px;
        padding: 20px 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
    }
    .flip-card-front {
        background: #FFFFFF;
        border: 3px solid #FF8A8A;
        color: #000000;
    }
    .flip-card-back {
        background: #FFF5F5;
        border: 3px solid #48BB78;
        color: #000000;
        transform: rotateY(180deg);
    }
    .card-hanzi {
        font-size: 4rem;
        color: #000000 !important;
        font-weight: 900;
        margin-bottom: 6px;
    }
    .card-pinyin-back {
        font-size: 1.4rem;
        color: #D32F2F !important;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .card-meaning {
        font-size: 1.3rem;
        color: #000000 !important;
        font-weight: 800;
    }
    .card-example {
        font-size: 1.05rem;
        color: #1E3A8A !important;
        font-weight: 700;
        margin-top: 8px;
        background-color: #EFF6FF;
        padding: 6px 12px;
        border-radius: 8px;
        border-left: 3px solid #3B82F6;
    }
    .card-pos {
        display: inline-block;
        background-color: #E6FFFA;
        color: #000000 !important;
        border: 1px solid #00695C;
        padding: 2px 10px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 800;
        margin-top: 4px;
    }

    /* Các Tab Bài tập có màu Hồng Nhạt Pastel khi kích hoạt */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 2px solid #FBCFE8 !important;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        white-space: nowrap;
        background-color: #F1F5F9;
        border-radius: 10px 10px 0px 0px;
        padding: 6px 12px;
        font-weight: 800;
        color: #000000 !important;
        border: 1px solid #CBD5E1;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFD1DC !important;
        color: #831843 !important;
        border: 2px solid #F472B6 !important;
        border-bottom: none !important;
    }

    /* Câu hỏi có màu đậm (xanh đậm) */
    .question-title {
        color: #1E3A8A !important;
        font-size: 1.1rem !important;
        font-weight: 900 !important;
        margin-top: 10px !important;
        margin-bottom: 6px !important;
    }

    /* Dòng chữ cô Bảo Ngọc màu Tím Pastel Đậm trang trọng */
    .teacher-footer {
        text-align: center;
        color: #6B46C1 !important;
        font-size: 1.4rem;
        font-weight: 900;
        margin-top: 40px;
        margin-bottom: 25px;
        padding-top: 15px;
        border-top: 2px dashed #D8B4FE;
    }

    .congrats-card {
        background-color: #DCFCE7;
        border: 2px solid #16A34A;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: #000000 !important;
        font-size: 1.3rem;
        font-weight: 900;
        margin-top: 15px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- DỮ LIỆU NHÓM 1 ---
VOCAB_G1 = [
    {"hanzi": "裙子", "pinyin": "qúnzi", "type": "danh từ", "meaning": "váy", "example": "妹妹穿了一条新裙子。(Em gái mặc một chiếc váy mới.)"},
    {"hanzi": "刻", "pinyin": "kè", "type": "lượng từ", "meaning": "15 phút, khắc", "example": "现在是八点一刻。(Bây giờ là 8 giờ 15 phút.)"},
    {"hanzi": "除了", "pinyin": "chúle", "type": "giới từ", "meaning": "ngoài… ra", "example": "除了他以外，大家都来了。(Ngoài anh ấy ra, mọi người đều đã đến.)"},
    {"hanzi": "上网", "pinyin": "shàng wǎng", "type": "động từ", "meaning": "lên mạng", "example": "我喜欢上网查资料。(Tôi thích lên mạng tra tài liệu.)"},
    {"hanzi": "为", "pinyin": "wèi", "type": "giới từ", "meaning": "vì, cho", "example": "大家为他的成功高兴。(Mọi người vui mừng vì thành công của anh ấy.)"},
    {"hanzi": "过去", "pinyin": "guòqù", "type": "danh từ", "meaning": "quá khứ", "example": "过去的事情就让它过去吧。(Chuyện quá khứ hãy để nó qua đi.)"},
    {"hanzi": "起来", "pinyin": "qǐlai", "type": "động từ", "meaning": "đứng dậy, lên", "example": "请大家站起来。(Mời mọi người đứng dậy.)"},
    {"hanzi": "瘦", "pinyin": "shòu", "type": "tính từ", "meaning": "gầy", "example": "生病以后他瘦了很多。(Sau khi ốm anh ấy gầy đi nhiều.)"},
    {"hanzi": "留学", "pinyin": "liúxué", "type": "động từ", "meaning": "du học", "example": "哥哥打算去中国留学。(Anh trai dự định đi Trung Quốc du học.)"},
    {"hanzi": "像", "pinyin": "xiàng", "type": "động từ", "meaning": "giống", "example": "这个孩子长得很像爸爸。(Đứa trẻ này trông rất giống bố.)"},
    {"hanzi": "花", "pinyin": "huā", "type": "danh từ", "meaning": "hoa", "example": "桌子上有一盆鲜花。(Trên bàn có một chậu hoa tươi.)"},
    {"hanzi": "简单", "pinyin": "jiǎndān", "type": "tính từ", "meaning": "đơn giản", "example": "这道题非常简单。(Câu hỏi này rất đơn giản.)"},
    {"hanzi": "明白", "pinyin": "míngbai", "type": "tính/động từ", "meaning": "rõ ràng, hiểu", "example": "我已经听明白了。(Tôi đã nghe hiểu rõ rồi.)"},
    {"hanzi": "提高", "pinyin": "tígāo", "type": "động từ", "meaning": "nâng cao", "example": "我的汉语水平提高了。(Trình độ tiếng Trung của tôi đã nâng cao.)"},
    {"hanzi": "还是", "pinyin": "háishì", "type": "liên từ", "meaning": "hay là", "example": "你想喝茶还是咖啡？(Bạn muốn uống trà hay là cà phê?)"},
    {"hanzi": "花", "pinyin": "huā", "type": "động từ", "meaning": "tốn, tiêu tốn", "example": "买这件衣服花了许多钱。(Mua bộ đồ này tốn không ít tiền.)"},
    {"hanzi": "灯", "pinyin": "dēng", "type": "danh từ", "meaning": "đèn", "example": "房间里请把灯打开。(Trong phòng xin hãy bật đèn lên.)"},
    {"hanzi": "生气", "pinyin": "shēng qì", "type": "động từ", "meaning": "tức giận", "example": "请你不要生气了。(Xin bạn đừng tức giận nữa.)"},
    {"hanzi": "会议", "pinyin": "huìyì", "type": "danh từ", "meaning": "cuộc họp", "example": "经理在参加一个会议。(Giám đốc đang tham gia một cuộc họp.)"},
    {"hanzi": "被", "pinyin": "bèi", "type": "giới từ", "meaning": "bị, được (bị động)", "example": "苹果被弟弟吃了。(Quả táo bị em trai ăn mất rồi.)"}
]

# --- TAB 1: KIỂM TRA TỪ VỰNG (20 CÂU) ---
QUIZ_TAB1 = [
    {"q": "1. Từ '裙子' nghĩa là gì?", "options": ["Váy", "Áo sơ mi", "Quần", "Mũ"], "ans": "Váy", "exp": "裙子 (qúnzi) nghĩa là chiếc váy."},
    {"q": "2. Từ '刻' mang ý nghĩa thời gian nào?", "options": ["15 phút", "30 phút", "45 phút", "10 phút"], "ans": "15 phút", "exp": "一刻 (yí kè) = 15 phút."},
    {"q": "3. Từ '除了' thuộc từ loại gì và mang nghĩa gì?", "options": ["Giới từ - Ngoài... ra", "Động từ - Tham gia", "Danh từ - Lịch sử", "Tính từ - Đơn giản"], "ans": "Giới từ - Ngoài... ra", "exp": "除了...以外 nghĩa là ngoài... ra."},
    {"q": "4. Từ nào mang nghĩa 'lên mạng'?", "options": ["上网", "留学", "提高", "生气"], "ans": "上网", "exp": "上网 (shàng wǎng) nghĩa là lên mạng."},
    {"q": "5. Từ '为' trong '为你高兴' mang nghĩa là gì?", "options": ["Vì, cho", "Bị, được", "Giống", "Hay là"], "ans": "Vì, cho", "exp": "为 (wèi) làm giới từ mang nghĩa vì, cho."},
    {"q": "6. Từ '过去' chỉ thời gian nào?", "options": ["Quá khứ", "Hiện tại", "Tương lai", "Cuối tuần"], "ans": "Quá khứ", "exp": "过去 (guòqù) nghĩa là quá khứ."},
    {"q": "7. Từ '起来' trong '站起来' mang nghĩa gì?", "options": ["Đứng dậy, lên", "Đi qua", "Chạy xuống", "Ngồi xuống"], "ans": "Đứng dậy, lên", "exp": "起来 (qǐlai) chỉ xu hướng đi lên, đứng dậy."},
    {"q": "8. Từ trái nghĩa với '胖' (béo) là từ nào?", "options": ["瘦", "老", "矮", "短"], "ans": "瘦", "exp": "瘦 (shòu) nghĩa là gầy, trái nghĩa với 胖 (pàng)."},
    {"q": "9. Từ '留学' có nghĩa là gì?", "options": ["Du học", "Luyện tập", "Ôn tập", "Kiểm tra"], "ans": "Du học", "exp": "留学 (liúxué) nghĩa là đi du học."},
    {"q": "10. '长得很像' mang nghĩa là gì?", "options": ["Trông rất giống", "Trông rất cao", "Rất thông minh", "Rất xinh đẹp"], "ans": "Trông rất giống", "exp": "像 (xiàng) nghĩa là giống."},
    {"q": "11. Từ '花' trong '一盆花' là từ loại gì?", "options": ["Danh từ (hoa)", "Động từ (tiêu tiền)", "Tính từ (đẹp)", "Lượng từ"], "ans": "Danh từ (hoa)", "exp": "花 ở đây là danh từ chỉ bông hoa."},
    {"q": "12. Từ '简单' nghĩa là gì?", "options": ["Đơn giản", "Phức tạp", "Khó khăn", "Rõ ràng"], "ans": "Đơn giản", "exp": "简单 (jiǎndān) nghĩa là đơn giản."},
    {"q": "13. Từ nào mang nghĩa 'hiểu, rõ ràng'?", "options": ["明白", "提高", "生气", "习惯"], "ans": "明白", "exp": "明白 (míngbai) nghĩa là hiểu rõ, rõ ràng."},
    {"q": "14. Từ '提高' mang nghĩa là gì?", "options": ["Nâng cao", "Giảm xuống", "Thay đổi", "Bắt đầu"], "ans": "Nâng cao", "exp": "提高 (tígāo) nghĩa là nâng cao (trình độ, thành tích)."},
    {"q": "15. Trong câu hỏi lựa chọn 'A ____ B?', ta dùng từ nào?", "options": ["还是", "或者", "但是", "所以"], "ans": "还是", "exp": "还是 (háishì) dùng trong câu hỏi lựa chọn (hay là)."},
    {"q": "16. Từ '花' trong '花钱' là từ loại gì?", "options": ["Động từ (tiêu tốn)", "Danh từ (bông hoa)", "Tính từ", "Phó từ"], "ans": "Động từ (tiêu tốn)", "exp": "花钱 nghĩa là tiêu tiền, tốn tiền (động từ)."},
    {"q": "17. Từ '灯' nghĩa là gì?", "options": ["Đèn", "Bảng", "Cửa", "Sách"], "ans": "Đèn", "exp": "灯 (dēng) nghĩa là cái đèn."},
    {"q": "18. '别生气了' nghĩa là gì?", "options": ["Đừng tức giận nữa", "Đừng lo lắng nữa", "Đừng đi nữa", "Đừng khóc nữa"], "ans": "Đừng tức giận nữa", "exp": "生气 (shēngqì) nghĩa là tức giận."},
    {"q": "19. Từ '会议' nghĩa là gì?", "options": ["Cuộc họp", "Công ty", "Trường học", "Bệnh viện"], "ans": "Cuộc họp", "exp": "会议 (huìyì) nghĩa là cuộc họp, hội nghị."},
    {"q": "20. Từ '被' dùng trong loại câu nào?", "options": ["Câu bị động", "Câu so sánh", "Câu tồn tại", "Câu nghi vấn"], "ans": "Câu bị động", "exp": "被 (bèi) là giới từ chỉ bị động (bị, được)."}
]

# --- TAB 2: ĐIỀN VÀO CHỖ TRỐNG (20 CÂU) ---
QUIZ_TAB2 = [
    # Dễ (10 câu)
    {"q": "1. [Dễ] 妹妹穿了一条漂亮的新（  ）。", "options": ["裙子", "灯", "会议", "刻"], "ans": "裙子", "exp": "Đi với lượng từ 条 (tiáo) chỉ trang phục dài như 裙子 (váy)."},
    {"q": "2. [Dễ] 现在是八点一（  ），会议马上开始了。", "options": ["刻", "瘦", "被", "像"], "ans": "刻", "exp": "一刻 = 15 phút. 八点一刻 = 8 giờ 15 phút."},
    {"q": "3. [Dễ] 爷爷每天晚上都在房间里（  ）看新闻。", "options": ["上网", "生气", "提高", "留学"], "ans": "上网", "exp": "上网看新闻 = lên mạng xem tin tức."},
    {"q": "4. [Dễ] 房间里太暗了，请把（  ）打开吧。", "options": ["灯", "裙子", "会议", "花"], "ans": "灯", "exp": "把灯打开 = bật đèn lên."},
    {"q": "5. [Dễ] 这道题非常（  ），大家很快就做出来了。", "options": ["简单", "瘦", "生气", "被"], "ans": "简单", "exp": "简单 = đơn giản."},
    {"q": "6. [Dễ] 经理正在三楼开一个重要的（  ）。", "options": ["会议", "裙子", "灯", "刻"], "ans": "会议", "exp": "开会议 = họp cuộc họp."},
    {"q": "7. [Dễ] 你想喝热茶，（  ）想喝冷饮？", "options": ["还是", "除了", "被", "为"], "ans": "还是", "exp": "Câu hỏi lựa chọn giữa A và B dùng 还是."},
    {"q": "8. [Dễ] 生病之后，他的身体比以前（  ）多了。", "options": ["瘦", "简单", "明白", "过去"], "ans": "瘦", "exp": "瘦 = gầy (sau khi ốm gầy đi)."},
    {"q": "9. [Dễ] 你别（  ）了，有话好好说。", "options": ["生气", "简单", "提高", "明白"], "ans": "生气", "exp": "别生气 = đừng tức giận."},
    {"q": "10. [Dễ] 桌子上摆着一盆新鲜的（  ）。", "options": ["花", "灯", "裙子", "会议"], "ans": "花", "exp": "一盆花 = một chậu hoa."},

    # Trung bình (7 câu)
    {"q": "11. [Trung bình] （  ）他以外，其他人今天都按时参加了活动。", "options": ["除了", "还是", "过去", "起来"], "ans": "除了", "exp": "Cấu trúc 除了...以外 = ngoài ... ra."},
    {"q": "12. [Trung bình] 大家（  ）这次考试做了充分的准备。", "options": ["为", "被", "像", "刻"], "ans": "为", "exp": "为...做准备 = chuẩn bị cho ..."},
    {"q": "13. [Trung bình] 经过这段时间的练习，他的汉语水平（  ）了不少。", "options": ["提高", "过去", "像", "为"], "ans": "提高", "exp": "水平提高 = trình độ nâng cao."},
    {"q": "14. [Trung bình] 毕业以后，他打算去中国（  ）两年。", "options": ["留学", "上网", "生气", "提高"], "ans": "留学", "exp": "去中国留学 = đi Trung Quốc du học."},
    {"q": "15. [Trung bình] 这个孩子长得非常（  ）他的爸爸。", "options": ["像", "为", "被", "除了"], "ans": "像", "exp": "长得很像 = trông rất giống."},
    {"q": "16. [Trung bình] 老师讲得很清楚，我现在完全（  ）了。", "options": ["明白", "提高", "留学", "上网"], "ans": "明白", "exp": "听明白 = nghe hiểu rõ."},
    {"q": "17. [Trung bình] 为了买这辆新车，他（  ）了不少钱。", "options": ["花", "瘦", "起", "刻"], "ans": "花", "exp": "花钱 = tiêu tốn tiền."},

    # Khó (3 câu)
    {"q": "18. [Khó] 他的自行车（  ）别人借走了，到现在还没还。", "options": ["被", "为", "像", "除了"], "ans": "被", "exp": "Câu bị động: Bị thể (自行车) + 被 + Chủ thể (别人) + V (借走)."},
    {"q": "19. [Khó] 听到这个好消息，他高兴地站了（  ）。", "options": ["起来", "过去", "提高", "留学"], "ans": "起来", "exp": "站起来 = đứng dậy (bổ ngữ xu hướng 起来)."},
    {"q": "20. [Khó] 那些（  ）的事情就别再提了，要向前看。", "options": ["过去", "简单", "明白", "提高"], "ans": "过去", "exp": "过去的事情 = những chuyện đã qua trong quá khứ."}
]

# --- TAB 3: SẮP XẾP CÂU (10 CÂU) ---
QUIZ_TAB3 = [
    {"q": "1. Sắp xếp: 这条 / 裙子 / 买的 / 是 / 在超市", "options": ["这条裙子是在超市买的。", "是在超市买的这条裙子。", "超市买的是这条裙子。", "这条裙子买的是在超市。"], "ans": "这条裙子是在超市买的。", "exp": "Cấu trúc nhấn mạnh 是...的: Chủ ngữ + 是 + Trạng ngữ nơi chốn + Động từ + 的."},
    {"q": "2. Sắp xếp: 现在 / 八点 / 差一刻 / 是", "options": ["现在是八点差一刻。", "八点差一刻是现在。", "差一刻是八点现在。", "现在差一刻是八点。"], "ans": "现在是八点差一刻。", "exp": "Thời gian: Bây giờ là 8 giờ kém 15 (八点差一刻)."},
    {"q": "3. Sắp xếp: 除了 / 他 / 都 / 来了 / 以外", "options": ["除了他以外大家都来了。", "Ngoài ra mọi người đều đến.", "除了大家都来了以外他。", "大家都来了除了他以外。"], "ans": "除了他以外大家都来了。", "exp": "Cấu trúc: 除了 + N + 以外，S + 都 + V."},
    {"q": "4. Sắp xếp: 喜欢 / 晚饭后 / 上网 / 查资料 / 我", "options": ["晚饭后我喜欢上网查资料。", "我上网查资料喜欢晚饭后。", "查资料晚饭后我上网。", "上网晚饭后我查资料。"], "ans": "晚饭后我喜欢上网查资料。", "exp": "Trạng ngữ chỉ thời gian (晚饭后) + Chủ ngữ (我) + Động từ (喜欢...)"},
    {"q": "5. Sắp xếp: 大家 / 为 / 成功 / 庆祝 / 他的", "options": ["大家为他的成功庆祝。", "大家庆祝为他的成功。", "他的成功为大家庆祝。", "为他的成功大家庆祝。"], "ans": "大家为他的成功庆祝。", "exp": "Mẫu câu: S + 为 + N + V (Mọi người chúc mừng vì thành công của anh ấy)."},
    {"q": "6. Sắp xếp: 站起来 / 请 / 慢慢地 / 大家", "options": ["请大家慢慢地站起来。", "大家请慢慢地站起来。", "慢慢地请大家站起来。", "站起来请大家慢慢地。"], "ans": "请大家慢慢地站起来。", "exp": "Câu cầu khiến lịch sự: 请 + S + Trạng ngữ + Động từ."},
    {"q": "7. Sắp xếp: 瘦了 / 很多 / 运动 / 以后 / 他", "options": ["运动以后他瘦了很多。", "他瘦了很多运动以后。", "运动以后瘦了很多他。", "瘦了很多以后他运动。"], "ans": "运动以后他瘦了很多。", "exp": "Cụm thời gian (运动以后) + S (他) + V/Adj (瘦了很多)."},
    {"q": "8. Sắp xếp: 打算 / 去 / 留学 / 弟弟 / 英国", "options": ["弟弟打算去英国留学。", "弟弟去英国打算留学。", "打算去英国留学弟弟。", "英国弟弟打算去留学。"], "ans": "弟弟打算去英国留学。", "exp": "Chủ ngữ (弟弟) + 打算 + Động từ liên tiếp (去英国留学)."},
    {"q": "9. Sắp xếp: 明白 / 这句话的 / 我 / 意思 / 不", "options": ["我不明白这句话的意思。", "我明白不这句话的意思。", "这句话的意思我不明白。", "不明白我这句话的意思。"], "ans": "我不明白这句话的意思。", "exp": "Câu phủ định: S + 不 + V (明白) + Tân ngữ (这句话的意思)."},
    {"q": "10. Sắp xếp: 被 / 拿走了 / 字典 / 别人 / 我的", "options": ["我的字典被别人拿走了。", "别人被我的字典拿走了。", "我的字典拿走了被别人。", "被别人我的字典拿走了。"], "ans": "我的字典被别人拿走了。", "exp": "Câu bị động: Bị thể (我的字典) + 被 + Chủ thể (别人) + V + Bổ ngữ (拿走了)."}
]

# --- TAB 4: CHỌN CÂU TRẢ LỜI CHO CÂU HỎI (10 CÂU) ---
QUIZ_TAB4 = [
    {"q": "1. 问：你想吃面条还是吃米饭？——答：（  ）", "options": ["给我一碗面条吧。", "我吃了一碗面条。", "面条很好吃。", "我不喜欢吃米饭。"], "ans": "给我一碗面条吧。", "exp": "Câu hỏi 还是 (lựa chọn) đưa ra đáp án cụ thể 'Cho tôi một bát mì đi'."},
    {"q": "2. 问：你的汉语成绩怎么提高了这么快？——答：（  ）", "options": ["因为我每天都认真练习。", "考试题太难了。", "我还没有复习。", "明天就要考试了。"], "ans": "因为我每天都认真练习。", "exp": "Trả lời câu hỏi nguyên nhân 怎么 (tại sao) bằng 因为 (vì...)"},
    {"q": "3. 问：房间里的灯怎么没开？——答：（  ）", "options": ["灯坏了，还没有换新的。", "外面天气很好。", "灯非常漂亮。", "我买了三个灯。"], "ans": "灯坏了，还没有换新的。", "exp": "Giải thích lý do đèn chưa bật: Đèn hỏng rồi chưa thay cái mới."},
    {"q": "4. 问：他怎么突然生气了？——答：（  ）", "options": ["因为大家都没有听他的解释。", "他今天很高兴。", "他在办公室开会。", "他已经去睡觉了。"], "ans": "因为大家都没有听他的解释。", "exp": "Giải thích nguyên nhân tức giận: Vì mọi người không nghe giải thích của anh ấy."},
    {"q": "5. 问：你的护照找不到了，怎么办？——答：（  ）", "options": ["别着急，一定被放在哪个包里了。", "护照是红色的。", "我已经买好机票了。", "护照 very 重要。"], "ans": "别着急，一定被放在哪个包里了。", "exp": "Đưa ra lời khuyên và động viên: Đừng lo, chắc chắn bị để ở trong túi nào rồi."},
    {"q": "6. 问：你想买这件衬衫还是那条裙子？——答：（  ）", "options": ["我买那条裙子吧。", "我不喜欢衬衫。", "裙子很长。", "在超市买的。"], "ans": "我买那条裙子吧。", "exp": "Lựa chọn 1 trong 2 vế trong câu hỏi 还是."},
    {"q": "7. 问：你的字典在哪里？——答：（  ）", "options": ["被同桌借走了。", "字典很有用。", "我已经买字典了。", "我不明白这个词。"], "ans": "被同桌借走了。", "exp": "Trả lời vị trí/trạng thái của cuốn từ điển: Bị bạn cùng bàn mượn đi rồi."},
    {"q": "8. 问：你是什么时候去中国留学的？——答：（  ）", "options": ["我是去年九月去的。", "去中国学习汉语。", "留学非常好。", "我和朋友一起去。"], "ans": "我是去年九月去的。", "exp": "Cấu trúc 是...的 nhấn mạnh thời gian (tháng 9 năm ngoái)."},
    {"q": "9. 问：除了汉语以外，你还会说什么语言？——答：（  ）", "options": ["我还会说英语。", "除了汉语我都喜欢。", "汉语不难。", "我会说汉语。"], "ans": "我还会说英语。", "exp": "Mẫu câu 除了...以外，还... (Ngoài tiếng Trung tôi còn biết nói tiếng Anh)."},
    {"q": "10. 问：这道题你明白怎么做了吗？——答：（  ）", "options": ["明白了，谢谢老师！", "这道题很长。", "我不喜欢做题。", "老师正在讲课。"], "ans": "明白了，谢谢老师！", "exp": "Trả lời câu hỏi 明白了吗 (Đã hiểu rõ chưa): Hiểu rồi, cảm ơn thầy/cô!"}
]

GROUPS_DATA = [
    {
        "id": "G1", 
        "title": "Nhóm 1", 
        "vocab": VOCAB_G1, 
        "tab1": QUIZ_TAB1, 
        "tab2": QUIZ_TAB2, 
        "tab3": QUIZ_TAB3, 
        "tab4": QUIZ_TAB4
    }
]

ORDERED_GROUPS = list(reversed(GROUPS_DATA))

# Webhook URL cố định của cô Bảo Ngọc
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbykR1r2_VTPvB5SVrDSMhmBqQhWYdQjPacrLBmoCIsE2WbBqGA0mBDZA0uUmLd2-Hli/exec"

def send_to_google_sheet(user_name, group_name, score, total, percentage):
    payload = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
            return False, f"HTTP Status: {response.status_code}"
    except Exception as e:
        return False, str(e)

# --- GIAO DIỆN CHÍNH ---
st.markdown('<div class="main-title">✨ CHINH PHỤC TỪ VỰNG HSK 3 ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Cùng học và ôn từ vựng HSK3 nhé</div>', unsafe_allow_html=True)

# Khung nhập tên người học (Nền màu trắng, viền đen sắc nét)
user_name = st.text_input("👤 Họ và tên người học (Nhập tên để nộp điểm):", value="Học viên HSK3", key="user_name_input")

# Dựng các Tab Nhóm (Nhóm mới cập nhật nằm ở đầu)
group_titles = [g["title"] for g in ORDERED_GROUPS]
main_tabs = st.tabs(group_titles)

for idx, group_info in enumerate(ORDERED_GROUPS):
    with main_tabs[idx]:
        st.markdown(f"### 📌 {group_info['title']} (20 từ vựng & Bài tập)")
        
        # -------------------------------------------------------------
        # PHẦN 1: FLASHCARD 3D FLIP CARD & BẢNG TỪ VỰNG
        # -------------------------------------------------------------
        st.markdown("#### 🎴 Phần 1: Flashcard Từ Vựng")
        
        fc_key = f"fc_index_{group_info['id']}"
        show_table_key = f"show_table_{group_info['id']}"
        
        if fc_key not in st.session_state:
            st.session_state[fc_key] = 0
        if show_table_key not in st.session_state:
            st.session_state[show_table_key] = False
            
        vocab_list = group_info["vocab"]
        curr_idx = st.session_state[fc_key]
        curr_item = vocab_list[curr_idx]
        
        # Flashcard 3D HTML / CSS Flip Card
        flip_card_html = f"""
        <div class="flip-card">
          <div class="flip-card-inner">
            <div class="flip-card-front">
              <div style="color: #64748B; font-size: 0.85rem; font-weight: 700;">MẶT TRƯỚC</div>
              <div class="card-hanzi">{curr_item['hanzi']}</div>
              <div style="color: #94A3B8; font-size: 0.85rem; font-weight: 700;">Thẻ {curr_idx + 1} / {len(vocab_list)}</div>
            </div>
            <div class="flip-card-back">
              <div style="color: #166534; font-size: 0.85rem; font-weight: 800;">MẶT SAU</div>
              <div class="card-hanzi" style="color:#15803D !important; font-size: 3.2rem;">{curr_item['hanzi']}</div>
              <div class="card-pinyin-back">{curr_item['pinyin']}</div>
              <div class="card-meaning">{curr_item['meaning']} <span class="card-pos">{curr_item['type']}</span></div>
              <div class="card-example">📝 <b>Ví dụ:</b> {curr_item['example']}</div>
            </div>
          </div>
        </div>
        """
        st.markdown(flip_card_html, unsafe_allow_html=True)
        
        # Nút chuyển thẻ
        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            if st.button("⬅️ Thẻ trước", key=f"prev_{group_info['id']}", use_container_width=True):
                st.session_state[fc_key] = (curr_idx - 1) % len(vocab_list)
                st.rerun()
        with btn_c2:
            if st.button("🔀 Ngẫu nhiên", key=f"rand_{group_info['id']}", use_container_width=True):
                st.session_state[fc_key] = random.randint(0, len(vocab_list) - 1)
                st.rerun()
        with btn_c3:
            if st.button("Thẻ sau ➡️", key=f"next_{group_info['id']}", use_container_width=True):
                st.session_state[fc_key] = (curr_idx + 1) % len(vocab_list)
                st.rerun()
                
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Nút bấm xem Từ vựng dạng Bảng
        if not st.session_state[show_table_key]:
            if st.button("📊 Xem từ vựng dạng bảng", key=f"btn_show_tbl_{group_info['id']}", use_container_width=True):
                st.session_state[show_table_key] = True
                st.rerun()
        else:
            if st.button("▲ Thu nhỏ bảng (Ẩn bảng từ vựng)", key=f"btn_hide_tbl_{group_info['id']}", use_container_width=True):
                st.session_state[show_table_key] = False
                st.rerun()
                
            st.markdown("##### 📋 Bảng tổng hợp 20 từ vựng")
            table_markdown = "| STT | Chữ Hán | Phiên âm | Từ loại | Nghĩa | Ví dụ |\n| :---: | :---: | :--- | :--- | :--- | :--- |\n"
            for v_i, v_item in enumerate(vocab_list):
                table_markdown += f"| {v_i+1} | **{v_item['hanzi']}** | {v_item['pinyin']} | {v_item['type']} | {v_item['meaning']} | {v_item['example']} |\n"
            st.markdown(table_markdown)

        st.markdown("---")

        # -------------------------------------------------------------
        # PHẦN 2: BÀI TẬP TRẮC NGHIỆM CHIA 4 TAB
        # -------------------------------------------------------------
        st.markdown("#### 📝 Phần 2: Bài Tập Ôn Tập Từ Vựng & Ngữ Pháp")
        st.caption("Chọn đáp án cho từng câu hỏi. Làm xong bấm 'Nộp bài kiểm tra' ở cuối để chấm điểm và nhận giải thích.")

        sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
            "Kiểm tra từ vựng", 
            "Điền vào chỗ trống", 
            "Sắp xếp câu", 
            "Chọn câu trả lời"
        ])

        def render_quiz_section(sub_quiz_data, sub_key):
            submitted_flag = f"sub_submitted_{group_info['id']}_{sub_key}"
            if submitted_flag not in st.session_state:
                st.session_state[submitted_flag] = False

            user_ans = {}
            with st.form(key=f"form_{group_info['id']}_{sub_key}"):
                for q_i, q_data in enumerate(sub_quiz_data):
                    st.markdown(f'<div class="question-title">{q_data["q"]}</div>', unsafe_allow_html=True)
                    user_ans[q_i] = st.radio(
                        label=f"Câu {q_i+1}:",
                        options=q_data["options"],
                        key=f"rad_{group_info['id']}_{sub_key}_{q_i}",
                        index=None,
                        label_visibility="collapsed"
                    )

                    if st.session_state[submitted_flag]:
                        sel = user_ans[q_i]
                        cor = q_data["ans"]
                        exp = q_data.get("exp", "")
                        if sel == cor:
                            st.markdown(f"""
                            <div style="background-color:#DCFCE7; border-left:4px solid #16A34A; padding:8px 12px; margin-top:4px; border-radius:6px;">
                                <b>✅ Đúng!</b> Đáp án: <b>{cor}</b><br>
                                <span style="font-size:0.95rem;">💡 <i>Giải thích: {exp}</i></span>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="background-color:#FEE2E2; border-left:4px solid #DC2626; padding:8px 12px; margin-top:4px; border-radius:6px;">
                                <b>❌ Chưa chính xác!</b><br>
                                • Bạn chọn: <span style="text-decoration:line-through; color:#991B1B;">{sel if sel else "Chưa chọn"}</span><br>
                                • Đáp án đúng: <b>{cor}</b><br>
                                <span style="font-size:0.95rem;">💡 <i>Giải thích: {exp}</i></span>
                            </div>
                            """, unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)

                sub_btn = st.form_submit_button("🚀 Nộp bài kiểm tra", use_container_width=True)

            if sub_btn:
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

                st.markdown("""
                <div class="congrats-card">
                    🎉 Chúc mừng bạn đã làm xong! Chăm chỉ quá!
                </div>
                """, unsafe_allow_html=True)

                st.metric("Kết quả làm bài", f"{score} / {total} câu đúng", f"{pct:.1f}%")
                if unans > 0:
                    st.warning(f"Lưu ý: Còn {unans} câu chưa chọn đáp án.")

                with st.spinner("Đang gửi điểm về Google Sheet cho cô Bảo Ngọc..."):
                    ok, msg = send_to_google_sheet(
                        user_name=user_name,
                        group_name=f"{group_info['title']} - {sub_key}",
                        score=score,
                        total=total,
                        percentage=pct
                    )
                    if ok:
                        st.success("✅ Đã gửi điểm về Sheet cho cô Bảo Ngọc")
                    else:
                        st.error("❌ Gửi không thành công, hãy chụp màn hình gửi cô Bảo Ngọc")

                st.rerun()

        with sub_tab1:
            render_quiz_section(group_info["tab1"], "Kiểm tra từ vựng")
        with sub_tab2:
            render_quiz_section(group_info["tab2"], "Điền vào chỗ trống")
        with sub_tab3:
            render_quiz_section(group_info["tab3"], "Sắp xếp câu")
        with sub_tab4:
            render_quiz_section(group_info["tab4"], "Chọn câu trả lời")

# --- CHỮ KÝ CÔ BẢO NGỌC CUỐI TRANG ---
st.markdown("""
<div class="teacher-footer">
    黄宝玉老师
</div>
""", unsafe_allow_html=True)
