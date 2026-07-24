# K4 — Ngày 1: Bài Tập & Phản Ánh
## Khám Phá LLM API | Phiếu Thực Hành

**Thời lượng:** 14h00–18h00
**Cách làm:** Trả lời từng câu ngay sau khi hoàn thành block tương ứng —
đừng để dồn hết về cuối buổi. Thay dòng mẫu trả lời bằng câu
trả lời thật (chấm tự động sẽ đếm số câu đã trả lời).

---

## Block 1 — API Cơ Bản (trả lời sau Checkpoint 1)

### Câu 1.1 — Độ nhạy của temperature
Gọi `call_openai` với temperature 0.0, 0.7, 1.2 và 1.8 dùng prompt
**"Hãy kể cho tôi một sự thật thú vị về Hà Nội."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi? Ở mức nào phản hồi bắt đầu
kém mạch lạc?** (2–3 câu)
> Khi temperature thấp như 0.0, phản hồi thường ổn định, trực tiếp và ít biến hóa; khi tăng lên 0.7, câu trả lời tự nhiên và phong phú hơn nhưng vẫn mạch lạc. Ở mức 1.2 nội dung bắt đầu sáng tạo hơn nhưng có thể thêm chi tiết không thật cần thiết; khoảng 1.8 thì phản hồi dễ lan man hoặc kém nhất quán hơn, nên không phù hợp cho câu trả lời cần chính xác.

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho trợ lý soạn thảo hợp đồng pháp lý,
và bao nhiêu cho trợ lý viết slogan quảng cáo? Giải thích khác biệt.**
> Với trợ lý soạn thảo hợp đồng pháp lý, tôi sẽ đặt temperature thấp, khoảng 0.0 đến 0.2, vì cần câu chữ ổn định, ít suy diễn và ưu tiên tính chính xác. Với trợ lý viết slogan quảng cáo, tôi sẽ đặt khoảng 0.9 đến 1.2 để có nhiều ý tưởng đa dạng, mới lạ và giàu cảm xúc hơn. Khác biệt chính là bài toán pháp lý cần kiểm soát rủi ro, còn slogan cần khả năng khám phá nhiều phương án sáng tạo.

### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 20.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 2 lần,
mỗi lần trung bình ~500 token đầu ra.

**Ước tính chi phí mỗi ngày của model lớn so với model nhỏ cho workload này
(dựa trên bảng giá trong template). Nêu một trường hợp model lớn xứng đáng
với chi phí và một trường hợp model nhỏ là lựa chọn đúng:**
> Workload mỗi ngày là 20.000 * 2 * 500 = 20.000.000 token đầu ra. Theo bảng giá trong template, gpt-4o tốn khoảng 20.000.000 / 1000 * 0.010 = 200 USD/ngày, còn gpt-4o-mini tốn khoảng 20.000.000 / 1000 * 0.0006 = 12 USD/ngày. Model lớn xứng đáng khi xử lý tác vụ khó như phân tích pháp lý, y tế, lập luận nhiều bước hoặc câu trả lời ảnh hưởng lớn đến quyết định; model nhỏ phù hợp cho FAQ, tóm tắt đơn giản, phân loại nội dung hoặc chatbot hỗ trợ cơ bản cần tối ưu chi phí.

---

## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích máy học (machine learning) là gì?"** nhưng hai system prompt
khác nhau:
- "Bạn là một nhà thơ, trả lời mọi thứ bằng hình ảnh ví von, tránh thuật ngữ."
- "Bạn là kỹ sư phần mềm senior, trả lời chính xác, có ví dụ code khi phù hợp."

**Hai phản hồi khác nhau như thế nào (giọng văn, độ dài, mức kỹ thuật)?
Từ đó rút ra system prompt điều khiển được những khía cạnh nào của phản hồi?**
(3–4 câu)
> Với persona nhà thơ, câu trả lời có giọng mềm hơn, dùng nhiều hình ảnh ví von như "máy học giống một người học từ kinh nghiệm", ít thuật ngữ và dễ tiếp cận với người mới. Với persona kỹ sư senior, câu trả lời có cấu trúc rõ hơn, dùng khái niệm như dữ liệu huấn luyện, mô hình, dự đoán và có thể kèm ví dụ code hoặc ví dụ kỹ thuật. Điều này cho thấy system prompt điều khiển được vai trò, giọng văn, mức độ kỹ thuật, độ dài, cách tổ chức câu trả lời và loại ví dụ mà model ưu tiên dùng.

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~150 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Nếu dùng ước lượng thô để dự
toán ngân sách API cho ứng dụng tiếng Việt, bạn sẽ dự toán thiếu hay thừa —
và vì sao?**
> Với đoạn tiếng Việt khoảng 150 từ, ước lượng thô theo số từ / 0.75 cho khoảng 200 token, còn `count_tokens` bằng tiktoken thường có thể cho con số cao hơn hoặc thấp hơn tùy dấu tiếng Việt, khoảng trắng và cách mã hóa từng từ. Nếu ví dụ tiktoken đếm khoảng 230 token thì chênh lệch là (230 - 200) / 200 = 15%. Khi dự toán ngân sách cho ứng dụng tiếng Việt, tôi sẽ cộng thêm biên an toàn thay vì chỉ dùng số từ, vì tiếng Việt có dấu và nhiều token hóa không trùng với ranh giới từ tự nhiên nên ước lượng thô có thể làm dự toán thiếu.

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Xét ba ứng dụng: (a) chatbot văn bản, (b) trợ lý giọng nói đọc to phản hồi,
(c) pipeline dịch tài liệu chạy ngầm ban đêm. Ứng dụng nào hưởng lợi nhiều
nhất từ streaming, ứng dụng nào không cần — và tại sao?** (1 đoạn văn)
> Streaming có lợi nhất với chatbot văn bản và trợ lý giọng nói, vì người dùng cảm thấy hệ thống phản hồi ngay lập tức thay vì phải chờ toàn bộ câu trả lời hoàn thành. Với trợ lý giọng nói, streaming còn quan trọng hơn vì có thể bắt đầu đọc từng phần, giảm cảm giác im lặng kéo dài. Pipeline dịch tài liệu chạy ngầm ban đêm thì gần như không cần streaming, vì người dùng chỉ quan tâm kết quả cuối cùng, log trạng thái hoặc thông báo hoàn tất hơn là từng token xuất hiện.

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**Khi API quá tải và hàng nghìn client cùng retry, exponential backoff giúp
gì so với delay cố định? Tra cứu thêm: kỹ thuật "jitter" (thêm độ trễ ngẫu
nhiên) giải quyết vấn đề gì còn sót lại?**
> Exponential backoff giúp giảm áp lực lên API khi hệ thống quá tải, vì mỗi lần retry sau sẽ thưa hơn thay vì tất cả client tiếp tục gọi dồn dập theo một delay cố định. Nếu hàng nghìn client cùng retry sau đúng 1 giây, server có thể bị một đợt tải mới rất lớn; backoff làm các đợt retry giãn ra theo thời gian. Jitter thêm độ trễ ngẫu nhiên để tránh việc nhiều client vẫn retry cùng một nhịp, từ đó giảm hiện tượng "đồng bộ va chạm" và làm tải phân tán mượt hơn.

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Viết lại system prompt bạn dùng cho trợ lý của mình. Chỉ ra 2 chỗ trong
prompt mà nếu xóa đi, hành vi trợ lý sẽ thay đổi rõ rệt — và mô tả thay đổi
đó:**
> System prompt tôi dùng: "Bạn là trợ lý học tập AI thân thiện, trả lời bằng tiếng Việt rõ ràng, ngắn gọn, ưu tiên giải thích từng bước và luôn nói khi không chắc chắn." Nếu xóa cụm "trả lời bằng tiếng Việt rõ ràng, ngắn gọn", trợ lý có thể trả lời dài hơn hoặc lẫn tiếng Anh, làm kém phù hợp với người học trong lớp. Nếu xóa cụm "luôn nói khi không chắc chắn", trợ lý dễ đưa câu trả lời nghe tự tin ngay cả khi thiếu dữ kiện, làm tăng rủi ro sai lệch.

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn giữ history 4 lượt cuối. Hãy mô tả một tình huống hội thoại
cụ thể mà giới hạn này khiến trợ lý trả lời sai/mất ngữ cảnh, và đề xuất một
cách khắc phục (ví dụ: tóm tắt các lượt cũ, tăng giới hạn có chọn lọc...):**
> Một tình huống dễ mất ngữ cảnh là người dùng đưa yêu cầu ban đầu rất quan trọng, ví dụ "hãy giả sử dự án dùng Gemini API, không dùng OpenAI key", sau đó hỏi nhiều lượt về token, streaming, retry và cuối cùng hỏi "sửa hàm đó cho đúng". Nếu history chỉ giữ vài lượt cuối, trợ lý có thể quên ràng buộc ban đầu và quay lại dùng `OPENAI_API_KEY`. Cách khắc phục là lưu một bản tóm tắt bền vững của các ràng buộc quan trọng, hoặc tách "session memory" gồm mục tiêu, công nghệ đang dùng, quyết định đã chốt và luôn ghép nó vào system/developer context trước khi gọi API.

---

## Danh Sách Kiểm Tra Nộp Bài

- [ ] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [ ] Cả 4 checkpoint pytest đều pass
- [ ] Tất cả 9 câu trong file này đã được trả lời
- [ ] Đã copy bài làm vào folder `solution/`, push lên GitHub cá nhân và nộp link repo vào vlearn (theo hướng dẫn README)
