import streamlit as st
import random
import requests
import datetime

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="HSK 3 Vocabulary Master - Cô Bảo Ngọc",
    page_icon="🎓",
    layout="wide"
)

# --- TÙY CHỈNH GIAO DIỆN (CSS tươi tắn, chữ rõ ràng, KHÔNG PINYIN) ---
st.markdown("""
<style>
    /* Tổng thể & Nền */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header chính */
    .main-title {
        color: #FF5A5F;
        text-align: center;
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #00A699;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    
    /* Flashcard Style */
    .flashcard-box {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF5F5 100%);
        border: 3px solid #FF8A8A;
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(255, 90, 95, 0.15);
        margin: 20px auto;
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .card-hanzi {
        font-size: 4.8rem;
        color: #2D3748;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .card-meaning {
        font-size: 1.8rem;
        color: #2B6CB0;
        font-weight: bold;
        margin-top: 10px;
    }
    .card-pos {
        display: inline-block;
        background-color: #E6FFFA;
        color: #234E52;
        padding: 6px 16px;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 10px;
    }

    /* Tab Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #E2E8F0;
        border-radius: 12px 12px 0px 0px;
        gap: 2px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: bold;
        color: #4A5568;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF5A5F !important;
        color: white !important;
    }

    /* Success Box */
    .congrats-card {
        background-color: #C6F6D5;
        border: 2px solid #38A169;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: #22543D;
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* Question Feedback Cards */
    .q-correct {
        background-color: #F0FFF4;
        border-left: 5px solid #38A169;
        padding: 12px 16px;
        margin-top: 8px;
        border-radius: 6px;
    }
    .q-wrong {
        background-color: #FFF5F5;
        border-left: 5px solid #E53E3E;
        padding: 12px 16px;
        margin-top: 8px;
        border-radius: 6px;
    }
    
    /* Footer Style */
    .teacher-footer {
        text-align: center;
        color: #2D3748;
        font-size: 1.6rem;
        font-weight: bold;
        margin-top: 50px;
        margin-bottom: 20px;
        padding: 20px;
        border-top: 2px dashed #CBD5E0;
    }
</style>
""", unsafe_allow_html=True)

# --- DỮ LIỆU NHÓM 1 (KHÔNG PINYIN - DÙNG CHỮ HÁN VÀ NGHĨA) ---
VOCAB_G1 = [
    {
        "hanzi": "裙子",
        "type": "danh từ",
        "meaning": "váy"
    },
    {
        "hanzi": "刻",
        "type": "lượng từ",
        "meaning": "15 phút, khắc"
    },
    {
        "hanzi": "除了",
        "type": "giới từ",
        "meaning": "ngoài… ra"
    },
    {
        "hanzi": "上网",
        "type": "động từ",
        "meaning": "lên mạng"
    },
    {
        "hanzi": "为",
        "type": "giới từ",
        "meaning": "vì, cho"
    },
    {
        "hanzi": "过去",
        "type": "danh từ",
        "meaning": "quá khứ"
    },
    {
        "hanzi": "起来",
        "type": "động từ",
        "meaning": "đứng dậy, lên"
    },
    {
        "hanzi": "瘦",
        "type": "tính từ",
        "meaning": "gầy"
    },
    {
        "hanzi": "留学",
        "type": "động từ",
        "meaning": "du học"
    },
    {
        "hanzi": "像",
        "type": "động từ",
        "meaning": "giống"
    },
    {
        "hanzi": "花（名词）",
        "type": "danh từ",
        "meaning": "hoa"
    },
    {
        "hanzi": "简单",
        "type": "tính từ",
        "meaning": "đơn giản"
    },
    {
        "hanzi": "明白",
        "type": "tính từ/động từ",
        "meaning": "rõ ràng, hiểu"
    },
    {
        "hanzi": "提高",
        "type": "động từ",
        "meaning": "nâng cao"
    },
    {
        "hanzi": "还是",
        "type": "liên từ",
        "meaning": "hay là"
    },
    {
        "hanzi": "花（动词）",
        "type": "động từ",
        "meaning": "tốn, tiêu tốn"
    },
    {
        "hanzi": "灯",
        "type": "danh từ",
        "meaning": "đèn"
    },
    {
        "hanzi": "生气",
        "type": "động từ",
        "meaning": "tức giận"
    },
    {
        "hanzi": "会议",
        "type": "danh từ",
        "meaning": "cuộc họp"
    },
    {
        "hanzi": "被",
        "type": "giới từ",
        "meaning": "bị, được (bị động)"
    }
]

# 35 CÂU HỎI TRẮC NGHIỆM CHO NHÓM 1
QUIZ_G1 = [
    {
        "q": "1. 妹妹今天穿了一条漂亮的新（  ）。",
        "options": [
            "裙子",
            "灯",
            "会议",
            "刻"
        ],
        "ans": "裙子",
        "exp": "裙子 nghĩa là 'váy', đi với lượng từ 条 (tiáo)."
    },
    {
        "q": "2. 现在是八点一（  ），会议马上就要开始了。",
        "options": [
            "瘦",
            "刻",
            "花",
            "被"
        ],
        "ans": "刻",
        "exp": "一刻 nghĩa là 15 phút (khắc). 八点一刻 = 8 giờ 15 phút."
    },
    {
        "q": "3. （  ）他以外，其他人今天都按时参加了活动。",
        "options": [
            "除了",
            "还是",
            "过去",
            "起来"
        ],
        "ans": "除了",
        "exp": "Cấu trúc 除了……以外 nghĩa là 'ngoài ... ra'."
    },
    {
        "q": "4. 爷爷每天晚饭后都喜欢在房间里（  ）看新闻。",
        "options": [
            "留学",
            "提高",
            "上网",
            "生气"
        ],
        "ans": "上网",
        "exp": "上网看新闻 nghĩa là 'lên mạng xem tin tức'."
    },
    {
        "q": "5. 大家（  ）这次考试做了充分的准备。",
        "options": [
            "被",
            "为",
            "像",
            "刻"
        ],
        "ans": "为",
        "exp": "为……做准备 nghĩa là 'chuẩn bị cho ...'."
    },
    {
        "q": "6. 事情已经过去了，你就不要再（  ）了。",
        "options": [
            "生气",
            "简单",
            "明白",
            "瘦"
        ],
        "ans": "生气",
        "exp": "生气 nghĩa là 'tức giận' (chuyện đã qua rồi đừng tức giận nữa)."
    },
    {
        "q": "7. 他站（  ），向大家热情地打招呼。",
        "options": [
            "起来",
            "过去",
            "提高",
            "留学"
        ],
        "ans": "起来",
        "exp": "站起来 nghĩa là 'đứng dậy'."
    },
    {
        "q": "8. 生病之后，他的身体比以前（  ）多了。",
        "options": [
            "简单",
            "瘦",
            "明白",
            "还是"
        ],
        "ans": "瘦",
        "exp": "瘦 nghĩa là 'gầy' (sau khi ốm gầy đi nhiều)."
    },
    {
        "q": "9. 毕业以后，他打算去中国（  ）两年。",
        "options": [
            "留学",
            "上网",
            "生气",
            "提高"
        ],
        "ans": "留学",
        "exp": "去中国留学 nghĩa là 'đi Trung Quốc du học'."
    },
    {
        "q": "10. 这个孩子长得非常（  ）他的爸爸。",
        "options": [
            "像",
            "为",
            "被",
            "除了"
        ],
        "ans": "像",
        "exp": "长得很像 nghĩa là 'trông rất giống'."
    },
    {
        "q": "11. 桌子上摆着一盆新鲜的（  ）。",
        "options": [
            "花",
            "灯",
            "裙子",
            "会议"
        ],
        "ans": "花",
        "exp": "一盆花 nghĩa là 'một chậu hoa'."
    },
    {
        "q": "12. 这道数学题非常（  ），大家很快就做出来了。",
        "options": [
            "生气",
            "简单",
            "瘦",
            "被"
        ],
        "ans": "简单",
        "exp": "简单 nghĩa là 'đơn giản' (bài toán đơn giản)."
    },
    {
        "q": "13. 老师讲得很清楚，我现在完全（  ）了。",
        "options": [
            "提高",
            "明白",
            "留学",
            "上网"
        ],
        "ans": "明白",
        "exp": "明白 nghĩa là 'hiểu, rõ ràng'."
    },
    {
        "q": "14. 经过这段时间的练习，他的汉语水平（  ）了不少。",
        "options": [
            "过去",
            "提高",
            "像",
            "为"
        ],
        "ans": "提高",
        "exp": "水平提高 nghĩa là 'trình độ được nâng cao'."
    },
    {
        "q": "15. 你想喝热茶，（  ）想喝冷饮？",
        "options": [
            "除了",
            "还是",
            "被",
            "刻"
        ],
        "ans": "还是",
        "exp": "还是 dùng trong câu hỏi lựa chọn (A hay là B?)."
    },
    {
        "q": "16. 为了买这辆新车，他（  ）了不少钱。",
        "options": [
            "花",
            "瘦",
            "起",
            "刻"
        ],
        "ans": "花",
        "exp": "花钱 nghĩa là 'tiêu tiền, tốn tiền'."
    },
    {
        "q": "17. 房间里太暗了，请把（  ）打开吧。",
        "options": [
            "裙子",
            "灯",
            "花",
            "会议"
        ],
        "ans": "灯",
        "exp": "把灯打开 nghĩa là 'bật đèn lên'."
    },
    {
        "q": "18. 你别（  ）了，有话好好说。",
        "options": [
            "简单",
            "生气",
            "明白",
            "提高"
        ],
        "ans": "生气",
        "exp": "别生气 nghĩa là 'đừng tức giận'."
    },
    {
        "q": "19. 经理正在三楼开一个重要的（  ）。",
        "options": [
            "会议",
            "裙子",
            "灯",
            "刻"
        ],
        "ans": "会议",
        "exp": "开会议 nghĩa là 'mở/họp cuộc họp'."
    },
    {
        "q": "20. 他的自行车（  ）别人借走了。",
        "options": [
            "被",
            "为",
            "像",
            "除了"
        ],
        "ans": "被",
        "exp": "被 dùng trong câu bị động (xe đạp bị người khác mượn đi)."
    },
    {
        "q": "21. Sắp xếp: 这条 / 裙子 / 买的 / 是 / 在超市",
        "options": [
            "这条裙子是在超市买的。",
            "是在超市买的这条裙子。",
            "超市买的是这条裙子。",
            "这条裙子买的是在超市。"
        ],
        "ans": "这条裙子是在超市买的。",
        "exp": "Cấu trúc nhấn mạnh 是……的: Chủ ngữ + 是 + Địa điểm + Động từ + 的."
    },
    {
        "q": "22. Sắp xếp: 现在 / 八点 / 差一刻 / 是",
        "options": [
            "现在是八点差一刻。",
            "八点差一刻是现在。",
            "差一刻是八点现在。",
            "现在差一刻是八点。"
        ],
        "ans": "现在是八点差一刻。",
        "exp": "Thứ tự thời gian: Bây giờ là 8 giờ kém 15 phút (八点差一刻)."
    },
    {
        "q": "23. Sắp xếp: 除了 / 他 / 都 / 来了 / 以外",
        "options": [
            "除了他以外大家都来了。",
            "除了大家都来了以外他。",
            "大家都来了除了他以外。",
            "他除了以外大家都来了。"
        ],
        "ans": "除了他以外大家都来了。",
        "exp": "Mẫu câu: 除了 + N + 以外，S + 都 + V."
    },
    {
        "q": "24. Sắp xếp: 喜欢 / 晚饭后 / 上网 / 查资料 / 我",
        "options": [
            "晚饭后我喜欢上网查资料。",
            "我上网查资料喜欢晚饭后。",
            "查资料晚饭后我 liquidation 上网。",
            "上网晚饭后我 liquidation 查资料。"
        ],
        "ans": "晚饭后我喜欢上网查资料。",
        "exp": "Trạng ngữ chỉ thời gian (晚饭后) đứng trước hoặc sau Chủ ngữ (我)."
    },
    {
        "q": "25. Sắp xếp: 大家 / 为 / 成功 / 庆祝 / 他的",
        "options": [
            "大家为他的成功庆祝。",
            "大家庆祝为他的成功。",
            "他的成功为大家庆祝。",
            "为他的成功大家庆祝。"
        ],
        "ans": "大家为他的成功庆祝。",
        "exp": "Mẫu câu: S + 为 + N + V (Mọi người chúc mừng cho thành công của anh ấy)."
    },
    {
        "q": "26. Sắp xếp: 站起来 / 请 / 慢慢地 / 大家",
        "options": [
            "请大家慢慢地站起来。",
            "大家请慢慢地站起来。",
            "慢慢地请大家站起来。",
            "站起来请大家慢慢地。"
        ],
        "ans": "请大家慢慢地站起来。",
        "exp": "Mẫu câu lịch sự: 请 + S + Trạng ngữ (慢慢地) + Động từ (站起来)."
    },
    {
        "q": "27. Sắp xếp: 瘦了 / 很多 / 运动 / 以后 / 他",
        "options": [
            "运动以后他瘦了很多。",
            "他瘦了很多运动以后。",
            "运动以后瘦了很多 he。",
            "瘦了很多以后他运动。"
        ],
        "ans": "运动以后他瘦了很多。",
        "exp": "Thời gian (运动以后) + Chủ ngữ (他) + Tính từ/Bổ ngữ (瘦了很多)."
    },
    {
        "q": "28. Sắp xếp: 打算 / 去 / 留学 / 弟弟 / 英国",
        "options": [
            "弟弟打算去英国留学。",
            "弟弟去英国打算留学。",
            "打算去英国留学弟弟。",
            "英国弟弟打算去留学。"
        ],
        "ans": "弟弟打算去英国留学。",
        "exp": "Cấu trúc: S (弟弟) + 打算 + 去 + Địa điểm (英国) + V (留学)."
    },
    {
        "q": "29. Sắp xếp: 明白 / 这句话的 / 我 / 意思 / 不",
        "options": [
            "我不明白这句话的意思。",
            "我明白不这句话的意思。",
            "这句话的意思我不明白。",
            "不明白我这句话的意思。"
        ],
        "ans": "我不明白这句话的意思。",
        "exp": "Cấu trúc phủ định: S + 不 + V (明白) + Tân ngữ (这句话的意思)."
    },
    {
        "q": "30. Sắp xếp: 被 / 拿走了 / 字典 / 别人 / 我的",
        "options": [
            "我的字典被别人拿走了。",
            "别人被我的字典拿走了。",
            "我的字典拿走了被别人。",
            "被别人我的字典拿走了。"
        ],
        "ans": "我的字典被别人拿走了。",
        "exp": "Câu bị động: Bị thể (我的字典) + 被 + Chủ thể tác động (别人) + V + Bổ ngữ (拿走了)."
    },
    {
        "q": "31. 问：你想吃面条还是吃米饭？——答：（  ）",
        "options": [
            "给我一碗面条吧。",
            "我吃了一碗面条。",
            "面条很好吃。",
            "我不喜欢吃米饭。"
        ],
        "ans": "给我一碗面条吧。",
        "exp": "Câu hỏi 还是 yêu cầu đưa ra lựa chọn cụ thể ('Cho tôi một bát mì đi')."
    },
    {
        "q": "32. 问：你的汉语成绩怎么提高了这么快？——答：（  ）",
        "options": [
            "因为我每天都认真练习。",
            "考试题太难了。",
            "我还没有复习。",
            "明天就要考试了。"
        ],
        "ans": "因为我每天都认真练习。",
        "exp": "Câu hỏi 怎么 (tại sao) trả lời bằng nguyên nhân 因为 (vì tôi chăm chỉ luyện tập)."
    },
    {
        "q": "33. 问：房间里的灯怎么没开？——答：（  ）",
        "options": [
            "灯坏了，还没有换新的。",
            "外面天气很好。",
            "灯非常漂亮。",
            "我买了三个灯。"
        ],
        "ans": "灯坏了，还没有换新的。",
        "exp": "Giải thích lý do đèn chưa bật: Đèn hỏng rồi chưa thay cái mới."
    },
    {
        "q": "34. 问：他怎么突然生气了？——答：（  ）",
        "options": [
            "因为大家都没有听他的解释。",
            "他今天很高兴。",
            "他在办公室开会。",
            " intuition 他已经去睡觉了。"
        ],
        "ans": "因为大家都没有听他的解释。",
        "exp": "Giải thích nguyên nhân tức giận: Vì mọi người không nghe giải thích của anh ấy."
    },
    {
        "q": "35. 问：你的护照找不到了，怎么办？——答：（  ）",
        "options": [
            "别着急，一定被放在哪个包里了。",
            "护照是红色的。",
            "我已经买好机票了。",
            "护照非常重要。"
        ],
        "ans": "别着急，一定被放在哪个包里了。",
        "exp": "Khuyên nhủ và đưa ra hướng giải quyết: Đừng lo, chắc chắn bị để trong cái túi nào rồi."
    }
]

# Danh sách nhóm (Nhóm mới cập nhật sẽ ở đầu)
GROUPS_DATA = [
    {"id": "G1", "title": "Nhóm 1", "vocab": VOCAB_G1, "quiz": QUIZ_G1}
]

# Đảo ngược để nhóm mới luôn hiển thị ở Tab ĐẦU TIÊN
ORDERED_GROUPS = list(reversed(GROUPS_DATA))

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
st.markdown('<div class="sub-title">Luyện Flashcard & Làm 35 câu trắc nghiệm tự động chấm điểm</div>', unsafe_allow_html=True)

# Sidebar cấu hình
st.sidebar.header("⚙️ Thông tin học viên")
user_name = st.sidebar.text_input("👤 Họ và tên người học:", value="Học viên HSK3")
sheet_webhook = st.sidebar.text_input("📊 Webhook URL Google Sheet:", value=DEFAULT_WEBHOOK)
st.sidebar.info("💡 Điểm số sau khi nộp sẽ tự động chuyển về Sheet của cô Bảo Ngọc.")

# Dựng các Tab (Nhóm mới nằm ở ĐẦU)
tab_titles = [g["title"] for g in ORDERED_GROUPS]
tabs = st.tabs(tab_titles)

for idx, group_info in enumerate(ORDERED_GROUPS):
    with tabs[idx]:
        st.subheader(f"📌 {group_info['title']} (20 từ vựng cốt lõi & 35 câu trắc nghiệm)")
        
        # Chia 2 cột: Cột trái (Flashcard), Cột phải (Quiz 35 câu)
        col_flash, col_quiz = st.columns([1, 1.2], gap="large")
        
        # -------------------------------------------------------------
        # PHẦN 1: FLASHCARD (ĐÃ XÓA HẾT PHIÊN ÂM PINYIN)
        # -------------------------------------------------------------
        with col_flash:
            st.markdown("### 🎴 Phần 1: Flashcard Từ Vựng (Không phiên âm)")
            st.caption("Luyện nhận diện trực tiếp chữ Hán mà không dựa vào Pinyin.")
            
            fc_key = f"fc_index_{group_info['id']}"
            flip_key = f"fc_flip_{group_info['id']}"
            
            if fc_key not in st.session_state:
                st.session_state[fc_key] = 0
            if flip_key not in st.session_state:
                st.session_state[flip_key] = False
                
            vocab_list = group_info["vocab"]
            curr_idx = st.session_state[fc_key]
            curr_item = vocab_list[curr_idx]
            
            # Thẻ Flashcard
            if not st.session_state[flip_key]:
                # Mặt trước (Chỉ có Chữ Hán)
                st.markdown(f"""
                <div class="flashcard-box">
                    <div style="color: #A0AEC0; font-size: 0.95rem;">MẶT TRƯỚC (Bấm 'Lật thẻ' để xem nghĩa)</div>
                    <div class="card-hanzi">{curr_item['hanzi']}</div>
                    <div style="color: #A0AEC0; font-size: 0.9rem;">Thẻ {curr_idx + 1} / {len(vocab_list)}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Mặt sau (Chữ Hán + Loại từ + Nghĩa tiếng Việt, KHÔNG CÓ PINYIN)
                st.markdown(f"""
                <div class="flashcard-box" style="border-color: #48BB78; background: linear-gradient(135deg, #FFFFFF 0%, #F0FFF4 100%);">
                    <div style="color: #A0AEC0; font-size: 0.95rem;">MẶT SAU</div>
                    <div class="card-hanzi" style="color:#2F855A; font-size: 4rem;">{curr_item['hanzi']}</div>
                    <div class="card-meaning">{curr_item['meaning']}</div>
                    <div><span class="card-pos">{curr_item['type']}</span></div>
                </div>
                """, unsafe_allow_html=True)
                
            # Điều khiển Flashcard
            btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
            with btn_col1:
                if st.button("⬅️ Trước", key=f"prev_{group_info['id']}"):
                    st.session_state[fc_key] = (curr_idx - 1) % len(vocab_list)
                    st.session_state[flip_key] = False
                    st.rerun()
            with btn_col2:
                if st.button("🔄 Lật thẻ", key=f"flip_{group_info['id']}"):
                    st.session_state[flip_key] = not st.session_state[flip_key]
                    st.rerun()
            with btn_col3:
                if st.button("Sau ➡️", key=f"next_{group_info['id']}"):
                    st.session_state[fc_key] = (curr_idx + 1) % len(vocab_list)
                    st.session_state[flip_key] = False
                    st.rerun()
            with btn_col4:
                if st.button("🔀 Ngẫu nhiên", key=f"rand_{group_info['id']}"):
                    st.session_state[fc_key] = random.randint(0, len(vocab_list) - 1)
                    st.session_state[flip_key] = False
                    st.rerun()

        # -------------------------------------------------------------
        # PHẦN 2: CÂU HỎI TRẮC NGHIỆM (ĐỦ 35 CÂU)
        # -------------------------------------------------------------
        with col_quiz:
            st.markdown("### 📝 Phần 2: Bài Tập Trắc Nghiệm (35 câu)")
            st.caption("Chọn đáp án cho 35 câu hỏi. Nộp bài xong sẽ biết điểm, đáp án đúng/sai và lời giải thích.")
            
            quiz_list = group_info["quiz"]
            submitted_key = f"quiz_submitted_{group_info['id']}"
            score_key = f"quiz_score_{group_info['id']}"
            
            if submitted_key not in st.session_state:
                st.session_state[submitted_key] = False
                
            user_answers = {}
            
            with st.form(key=f"quiz_form_{group_info['id']}"):
                for q_idx, q_item in enumerate(quiz_list):
                    st.markdown(f"**{q_item['q']}**")
                    user_answers[q_idx] = st.radio(
                        label=f"Câu {q_idx+1}:",
                        options=q_item["options"],
                        key=f"q_{group_info['id']}_{q_idx}",
                        index=None,
                        label_visibility="collapsed"
                    )
                    
                    # Nếu đã nộp bài, hiển thị ngay đúng/sai và giải thích cho từng câu
                    if st.session_state[submitted_key]:
                        selected = user_answers[q_idx]
                        correct = q_item["ans"]
                        explanation = q_item.get("exp", "")
                        
                        if selected == correct:
                            st.markdown(f"""
                            <div class="q-correct">
                                <b>✅ Đúng!</b> Đáp án: <b>{correct}</b><br>
                                <span style="color:#276749; font-size:0.95rem;">💡 <i>Giải thích: {explanation}</i></span>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="q-wrong">
                                <b>❌ Chưa chính xác!</b><br>
                                • Đáp án bạn chọn: <span style="text-decoration: line-through; color: #C53030;">{selected if selected else "Chưa chọn"}</span><br>
                                • Đáp án đúng: <b>{correct}</b><br>
                                <span style="color:#9B2C2C; font-size:0.95rem;">💡 <i>Giải thích chi tiết: {explanation}</i></span>
                            </div>
                            """, unsafe_allow_html=True)
                            
                    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                
                submit_button = st.form_submit_button("🚀 Nộp bài kiểm tra", use_container_width=True)
                
            if submit_button:
                st.session_state[submitted_key] = True
                
                # Tính điểm 35 câu
                score = 0
                unanswered = 0
                for q_idx, q_item in enumerate(quiz_list):
                    ans = user_answers.get(q_idx)
                    if ans is None:
                        unanswered += 1
                    elif ans == q_item["ans"]:
                        score += 1
                
                total_q = len(quiz_list)
                pct = (score / total_q) * 100
                st.session_state[score_key] = score
                
                # 1. Dòng chữ chúc mừng khi nộp xong
                st.markdown("""
                <div class="congrats-card">
                    🎉 Chúc mừng bạn đã làm xong! Chăm chỉ quá!
                </div>
                """, unsafe_allow_html=True)
                
                # 2. Hiển thị điểm số
                st.metric("Kết quả bài thi (35 câu)", f"{score} / {total_q} câu đúng", f"{pct:.1f}%")
                if unanswered > 0:
                    st.warning(f"Lưu ý: Bạn còn {unanswered} câu chưa chọn đáp án.")
                
                # 3. Gửi điểm về Sheet và hiển thị thông báo chính xác theo yêu cầu
                with st.spinner("Đang gửi kết quả về Google Sheet..."):
                    ok, msg = send_to_google_sheet(
                        sheet_url=sheet_webhook,
                        user_name=user_name,
                        group_name=group_info["title"],
                        score=score,
                        total=total_q,
                        percentage=pct
                    )
                    if ok:
                        st.success("✅ Đã gửi điểm về Sheet cho cô Bảo Ngọc")
                    else:
                        st.error("❌ Gửi không thành công, hãy chụp màn hình gửi cô Bảo Ngọc")
                        st.caption(f"Lỗi kết nối: {msg}")
                
                # Trigger rerun để cập nhật giao diện đáp án ngay bên trong form
                st.rerun()

# --- HIỂN THỊ DÒNG CHỮ CUỐI TRANG ---
st.markdown("""
<div class="teacher-footer">
    黄宝玉老师
</div>
""", unsafe_allow_html=True)
