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
> Khi đặt temperature ở mức rất thấp như 0.0, câu trả lời có xu hướng chắc chắn, ngắn gọn và ít thay đổi giữa các lần gọi. Tăng lên khoảng 0.7 thì phản hồi trở nên mềm mại, giàu chi tiết hơn nhưng vẫn giữ được logic. Từ khoảng 1.2 trở lên, model bắt đầu sáng tạo mạnh hơn nhưng cũng dễ thêm ý phụ; đến 1.8 thì câu trả lời có thể lan man và kém nhất quán, nên không nên dùng cho tác vụ cần độ chính xác cao.

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho trợ lý soạn thảo hợp đồng pháp lý,
và bao nhiêu cho trợ lý viết slogan quảng cáo? Giải thích khác biệt.**
> Với trợ lý hỗ trợ soạn hợp đồng pháp lý, em sẽ chọn temperature khoảng 0.0-0.2 để giảm suy diễn và giữ cách diễn đạt nhất quán. Ngược lại, với công cụ viết slogan quảng cáo, mức 0.9-1.2 hợp lý hơn vì cần nhiều phương án mới, bắt tai và có màu sắc sáng tạo. Nói ngắn gọn, tác vụ pháp lý ưu tiên sự an toàn và chính xác, còn tác vụ quảng cáo ưu tiên sự đa dạng ý tưởng.

### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 20.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 2 lần,
mỗi lần trung bình ~500 token đầu ra.

**Ước tính chi phí mỗi ngày của model lớn so với model nhỏ cho workload này
(dựa trên bảng giá trong template). Nêu một trường hợp model lớn xứng đáng
với chi phí và một trường hợp model nhỏ là lựa chọn đúng:**
> Tổng số token đầu ra mỗi ngày là 20.000 * 2 * 500 = 20.000.000 token. Dựa trên bảng giá trong template, gpt-4o sẽ tốn khoảng 200 USD/ngày, còn gpt-4o-mini khoảng 12 USD/ngày cho cùng workload. Model lớn nên dùng khi câu trả lời đòi hỏi lập luận sâu, độ chính xác cao hoặc có tác động lớn như pháp lý, y tế, tư vấn kỹ thuật phức tạp; model nhỏ phù hợp hơn cho FAQ, phân loại, tóm tắt ngắn hoặc các tác vụ lặp lại cần tiết kiệm chi phí.

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
> Khi dùng persona nhà thơ, phần giải thích thường nhẹ nhàng hơn, giàu hình ảnh so sánh và tránh đi sâu vào thuật ngữ kỹ thuật. Khi đổi sang persona kỹ sư phần mềm senior, câu trả lời trở nên có cấu trúc, chính xác hơn và sử dụng các khái niệm như dữ liệu huấn luyện, mô hình, dự đoán hoặc ví dụ code. Qua đó có thể thấy system prompt ảnh hưởng mạnh đến vai trò, giọng văn, độ chuyên sâu, cách trình bày và kiểu ví dụ mà model lựa chọn.

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~150 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Nếu dùng ước lượng thô để dự
toán ngân sách API cho ứng dụng tiếng Việt, bạn sẽ dự toán thiếu hay thừa —
và vì sao?**
> Với một đoạn tiếng Việt khoảng 150 từ, công thức ước lượng số từ / 0.75 cho ra xấp xỉ 200 token, trong khi `count_tokens` bằng tiktoken có thể cho kết quả khác do cách tách token phụ thuộc vào dấu tiếng Việt, ký tự và khoảng trắng. Nếu tiktoken đếm được khoảng 230 token thì mức chênh lệch là khoảng 15% so với ước lượng thô. Vì vậy khi dự toán chi phí cho ứng dụng tiếng Việt, em sẽ cộng thêm một phần dự phòng, vì cách đếm theo từ có thể đánh giá thấp số token thực tế.

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Xét ba ứng dụng: (a) chatbot văn bản, (b) trợ lý giọng nói đọc to phản hồi,
(c) pipeline dịch tài liệu chạy ngầm ban đêm. Ứng dụng nào hưởng lợi nhiều
nhất từ streaming, ứng dụng nào không cần — và tại sao?** (1 đoạn văn)
> Streaming đem lại giá trị rõ nhất cho chatbot văn bản và trợ lý giọng nói vì người dùng có thể thấy hoặc nghe phản hồi xuất hiện ngay từ những giây đầu tiên. Với trợ lý giọng nói, điều này đặc biệt quan trọng vì khoảng lặng dài khiến trải nghiệm kém tự nhiên. Ngược lại, pipeline dịch tài liệu chạy ngầm ban đêm không cần streaming nhiều, vì người dùng chủ yếu quan tâm bản dịch hoàn chỉnh, trạng thái tiến độ hoặc thông báo khi công việc kết thúc.

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**Khi API quá tải và hàng nghìn client cùng retry, exponential backoff giúp
gì so với delay cố định? Tra cứu thêm: kỹ thuật "jitter" (thêm độ trễ ngẫu
nhiên) giải quyết vấn đề gì còn sót lại?**
> Exponential backoff giúp hệ thống tránh việc retry quá dồn dập khi API đang quá tải, vì thời gian chờ sẽ tăng dần sau mỗi lần thất bại. Nếu dùng delay cố định, nhiều client có thể cùng gửi lại request tại cùng một thời điểm và tạo thêm một đợt nghẽn mới. Jitter giải quyết phần còn lại bằng cách thêm độ trễ ngẫu nhiên, giúp các lần retry được phân tán hơn thay vì đồng loạt rơi vào cùng một nhịp.

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Viết lại system prompt bạn dùng cho trợ lý của mình. Chỉ ra 2 chỗ trong
prompt mà nếu xóa đi, hành vi trợ lý sẽ thay đổi rõ rệt — và mô tả thay đổi
đó:**
> Persona em chọn là: "Bạn là trợ lý học tập AI thân thiện, trả lời bằng tiếng Việt rõ ràng, ngắn gọn, ưu tiên giải thích từng bước và luôn nói khi không chắc chắn." Nếu bỏ phần "trả lời bằng tiếng Việt rõ ràng, ngắn gọn", trợ lý có thể trả lời dài dòng hơn hoặc dùng lẫn tiếng Anh, khiến câu trả lời khó theo dõi hơn với người học. Nếu bỏ yêu cầu "luôn nói khi không chắc chắn", trợ lý có thể đưa ra câu trả lời quá tự tin dù thiếu thông tin, làm tăng nguy cơ gây hiểu nhầm.

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn giữ history 4 lượt cuối. Hãy mô tả một tình huống hội thoại
cụ thể mà giới hạn này khiến trợ lý trả lời sai/mất ngữ cảnh, và đề xuất một
cách khắc phục (ví dụ: tóm tắt các lượt cũ, tăng giới hạn có chọn lọc...):**
> Ví dụ, ngay đầu cuộc trò chuyện người dùng nói rằng dự án chỉ được dùng Gemini API key, sau đó tiếp tục hỏi nhiều lượt về token, streaming, retry và cách tổ chức hàm. Nếu trợ lý chỉ giữ vài lượt gần nhất, ràng buộc ban đầu có thể bị rơi khỏi history, khiến trợ lý vô tình quay lại dùng `OPENAI_API_KEY` hoặc model không phù hợp. Một cách cải thiện là duy trì bản tóm tắt các quyết định quan trọng của phiên làm việc, hoặc lưu riêng các ràng buộc bền vững rồi luôn đưa chúng vào context khi gọi model.

---

## Danh Sách Kiểm Tra Nộp Bài

- [ ] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [ ] Cả 4 checkpoint pytest đều pass
- [ ] Tất cả 9 câu trong file này đã được trả lời
- [ ] Đã copy bài làm vào folder `solution/`, push lên GitHub cá nhân và nộp link repo vào vlearn (theo hướng dẫn README)
