import json
import os
import traceback
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from socketserver import TCPServer
from typing import Any
from urllib.parse import urlparse

from dotenv import load_dotenv

import template


HOST = "127.0.0.1"
PORT = int(os.getenv("PORT", "8000"))
LOG_FILE = Path(__file__).with_name("web_app.log")


HTML = r"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LLM API Lab UI</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --ink: #1f2937;
      --muted: #667085;
      --line: #d8dee8;
      --accent: #0f766e;
      --accent-strong: #115e59;
      --danger: #b42318;
      --soft: #eef6f5;
      --mono: "Cascadia Mono", "Consolas", monospace;
      --sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: var(--sans);
      line-height: 1.45;
    }

    header {
      border-bottom: 1px solid var(--line);
      background: var(--panel);
      padding: 18px 24px;
    }

    .topbar {
      align-items: center;
      display: flex;
      gap: 16px;
      justify-content: space-between;
      margin: 0 auto;
      max-width: 1180px;
    }

    h1 {
      font-size: 22px;
      font-weight: 700;
      letter-spacing: 0;
      margin: 0;
    }

    .status {
      align-items: center;
      color: var(--muted);
      display: flex;
      font-size: 14px;
      gap: 8px;
      white-space: nowrap;
    }

    .dot {
      background: var(--accent);
      border-radius: 50%;
      display: inline-block;
      height: 9px;
      width: 9px;
    }

    main {
      margin: 0 auto;
      max-width: 1180px;
      padding: 22px 24px 36px;
    }

    .tabs {
      border-bottom: 1px solid var(--line);
      display: flex;
      gap: 6px;
      margin-bottom: 18px;
      overflow-x: auto;
    }

    .tab {
      background: transparent;
      border: 0;
      border-bottom: 3px solid transparent;
      color: var(--muted);
      cursor: pointer;
      font: inherit;
      font-weight: 650;
      padding: 12px 14px 10px;
    }

    .tab.active {
      border-color: var(--accent);
      color: var(--accent-strong);
    }

    .view { display: none; }
    .view.active { display: block; }

    .workspace {
      display: grid;
      gap: 18px;
      grid-template-columns: minmax(280px, 420px) minmax(0, 1fr);
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }

    h2 {
      font-size: 16px;
      letter-spacing: 0;
      margin: 0 0 14px;
    }

    label {
      color: var(--muted);
      display: block;
      font-size: 13px;
      font-weight: 650;
      margin: 14px 0 7px;
    }

    textarea,
    input {
      background: #fff;
      border: 1px solid var(--line);
      border-radius: 6px;
      color: var(--ink);
      font: inherit;
      min-height: 42px;
      outline: none;
      padding: 10px 11px;
      resize: vertical;
      width: 100%;
    }

    textarea:focus,
    input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.13);
    }

    .actions {
      align-items: center;
      display: flex;
      gap: 10px;
      margin-top: 14px;
    }

    .param-grid {
      display: grid;
      gap: 10px;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      margin-top: 10px;
    }

    .param-grid label {
      margin-top: 0;
    }

    .param-grid input {
      min-height: 38px;
    }

    button.primary {
      background: var(--accent);
      border: 1px solid var(--accent);
      border-radius: 6px;
      color: #fff;
      cursor: pointer;
      font: inherit;
      font-weight: 700;
      min-height: 40px;
      padding: 9px 13px;
    }

    button.primary:disabled {
      cursor: wait;
      opacity: 0.68;
    }

    .hint {
      color: var(--muted);
      font-size: 13px;
    }

    .output {
      background: #0f172a;
      border-radius: 8px;
      color: #e5e7eb;
      font-family: var(--mono);
      font-size: 13px;
      min-height: 220px;
      overflow: auto;
      padding: 14px;
      white-space: pre-wrap;
    }

    .metrics {
      display: grid;
      gap: 10px;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      margin-bottom: 14px;
    }

    .metric {
      background: var(--soft);
      border: 1px solid #cfe4e1;
      border-radius: 8px;
      padding: 10px;
    }

    .metric span {
      color: var(--muted);
      display: block;
      font-size: 12px;
      font-weight: 650;
    }

    .metric strong {
      display: block;
      font-size: 17px;
      margin-top: 3px;
    }

    .error {
      background: #fff3f2;
      border: 1px solid #fecdca;
      border-radius: 8px;
      color: var(--danger);
      display: none;
      font-size: 14px;
      margin-bottom: 14px;
      padding: 10px 12px;
    }

    .error.show { display: block; }

    @media (max-width: 820px) {
      .topbar { align-items: flex-start; flex-direction: column; }
      .workspace { grid-template-columns: 1fr; }
      .metrics { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <div class="topbar">
      <h1>LLM API Lab UI</h1>
      <div class="status"><span class="dot"></span><span>localhost stdlib server</span></div>
    </div>
  </header>

  <main>
    <div class="tabs" role="tablist">
      <button class="tab active" data-tab="chat" type="button">Chat Persona</button>
      <button class="tab" data-tab="compare" type="button">Compare Models</button>
      <button class="tab" data-tab="batch" type="button">Batch Compare</button>
    </div>

    <section class="view active" id="chat">
      <div class="workspace">
        <div class="panel">
          <h2>Chat Persona</h2>
          <label for="systemPrompt">System prompt</label>
          <textarea id="systemPrompt" rows="5">Bạn là trợ lý học tập AI thân thiện, trả lời bằng tiếng Việt rõ ràng và ngắn gọn.</textarea>
          <label for="userPrompt">User prompt</label>
          <textarea id="userPrompt" rows="5">Giải thích machine learning là gì?</textarea>
          <div class="param-grid">
            <div>
              <label for="chatTemperature">Temperature</label>
              <input id="chatTemperature" type="number" min="0" max="2" step="0.1" value="0.7">
            </div>
            <div>
              <label for="chatTopP">Top-p</label>
              <input id="chatTopP" type="number" min="0" max="1" step="0.05" value="0.9">
            </div>
            <div>
              <label for="chatMaxTokens">Max tokens</label>
              <input id="chatMaxTokens" type="number" min="1" step="1" value="256">
            </div>
          </div>
          <div class="actions">
            <button class="primary" id="chatRun" type="button">Run Chat</button>
            <span class="hint">Calls chat_with_system_prompt()</span>
          </div>
        </div>
        <div>
          <div class="error" id="chatError"></div>
          <div class="metrics">
            <div class="metric"><span>Latency</span><strong id="chatLatency">-</strong></div>
            <div class="metric"><span>Function</span><strong>chat</strong></div>
            <div class="metric"><span>Status</span><strong id="chatStatus">Idle</strong></div>
          </div>
          <pre class="output" id="chatOutput">Response will appear here.</pre>
        </div>
      </div>
    </section>

    <section class="view" id="compare">
      <div class="workspace">
        <div class="panel">
          <h2>Compare Models</h2>
          <label for="comparePrompt">Prompt</label>
          <textarea id="comparePrompt" rows="7">Việt Nam có bao nhiêu tỉnh?</textarea>
          <div class="param-grid">
            <div>
              <label for="compareTemperature">Temperature</label>
              <input id="compareTemperature" type="number" min="0" max="2" step="0.1" value="0.7">
            </div>
            <div>
              <label for="compareTopP">Top-p</label>
              <input id="compareTopP" type="number" min="0" max="1" step="0.05" value="0.9">
            </div>
            <div>
              <label for="compareMaxTokens">Max tokens</label>
              <input id="compareMaxTokens" type="number" min="1" step="1" value="256">
            </div>
          </div>
          <div class="actions">
            <button class="primary" id="compareRun" type="button">Run Compare</button>
            <span class="hint">Calls compare_models()</span>
          </div>
        </div>
        <div>
          <div class="error" id="compareError"></div>
          <div class="metrics">
            <div class="metric"><span>Primary latency</span><strong id="primaryLatency">-</strong></div>
            <div class="metric"><span>Mini latency</span><strong id="miniLatency">-</strong></div>
            <div class="metric"><span>Cost estimate</span><strong id="costEstimate">-</strong></div>
          </div>
          <pre class="output" id="compareOutput">Comparison result will appear here.</pre>
        </div>
      </div>
    </section>

    <section class="view" id="batch">
      <div class="workspace">
        <div class="panel">
          <h2>Batch Compare</h2>
          <label for="batchPrompts">Prompts, one per line</label>
          <textarea id="batchPrompts" rows="9">Việt Nam có bao nhiêu tỉnh?
Thủ đô của Việt Nam là gì?
Kể một sự thật thú vị về Hà Nội.</textarea>
          <div class="actions">
            <button class="primary" id="batchRun" type="button">Run Batch</button>
            <span class="hint">Calls batch_compare() + format_comparison_table()</span>
          </div>
        </div>
        <div>
          <div class="error" id="batchError"></div>
          <div class="metrics">
            <div class="metric"><span>Prompts</span><strong id="batchCount">-</strong></div>
            <div class="metric"><span>Function</span><strong>batch</strong></div>
            <div class="metric"><span>Status</span><strong id="batchStatus">Idle</strong></div>
          </div>
          <pre class="output" id="batchOutput">Batch table will appear here.</pre>
        </div>
      </div>
    </section>
  </main>

  <script>
    const $ = (id) => document.getElementById(id);

    document.querySelectorAll(".tab").forEach((button) => {
      button.addEventListener("click", () => {
        document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("active"));
        document.querySelectorAll(".view").forEach((view) => view.classList.remove("active"));
        button.classList.add("active");
        $(button.dataset.tab).classList.add("active");
      });
    });

    async function postJson(path, payload) {
      const response = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok || data.error) {
        throw new Error(data.error || `HTTP ${response.status}`);
      }
      return data;
    }

    function setBusy(button, busy, label) {
      button.disabled = busy;
      button.textContent = busy ? "Running..." : label;
    }

    function showError(id, message) {
      const node = $(id);
      node.textContent = message || "";
      node.classList.toggle("show", Boolean(message));
    }

    function readFloat(id, fallback) {
      const value = parseFloat($(id).value);
      return Number.isFinite(value) ? value : fallback;
    }

    function readInt(id, fallback) {
      const value = parseInt($(id).value, 10);
      return Number.isFinite(value) ? value : fallback;
    }

    $("chatRun").addEventListener("click", async () => {
      const button = $("chatRun");
      setBusy(button, true, "Run Chat");
      showError("chatError", "");
      $("chatStatus").textContent = "Running";
      try {
        const data = await postJson("/api/chat", {
          system_prompt: $("systemPrompt").value,
          user_prompt: $("userPrompt").value,
          temperature: readFloat("chatTemperature", 0.7),
          top_p: readFloat("chatTopP", 0.9),
          max_tokens: readInt("chatMaxTokens", 256),
        });
        $("chatLatency").textContent = `${data.latency_seconds.toFixed(3)}s`;
        $("chatOutput").textContent = data.response_text;
        $("chatStatus").textContent = "Done";
      } catch (error) {
        showError("chatError", error.message);
        $("chatStatus").textContent = "Error";
      } finally {
        setBusy(button, false, "Run Chat");
      }
    });

    $("compareRun").addEventListener("click", async () => {
      const button = $("compareRun");
      setBusy(button, true, "Run Compare");
      showError("compareError", "");
      try {
        const data = await postJson("/api/compare", {
          prompt: $("comparePrompt").value,
          temperature: readFloat("compareTemperature", 0.7),
          top_p: readFloat("compareTopP", 0.9),
          max_tokens: readInt("compareMaxTokens", 256),
        });
        const result = data.result;
        $("primaryLatency").textContent = `${result.gpt4o_latency.toFixed(3)}s`;
        $("miniLatency").textContent = `${result.mini_latency.toFixed(3)}s`;
        $("costEstimate").textContent = `$${result.gpt4o_cost_estimate.toExponential(2)}`;
        $("compareOutput").textContent =
          `Primary response:\n${result.gpt4o_response}\n\nMini response:\n${result.mini_response}\n\nRaw JSON:\n${JSON.stringify(result, null, 2)}`;
      } catch (error) {
        showError("compareError", error.message);
      } finally {
        setBusy(button, false, "Run Compare");
      }
    });

    $("batchRun").addEventListener("click", async () => {
      const button = $("batchRun");
      setBusy(button, true, "Run Batch");
      showError("batchError", "");
      $("batchStatus").textContent = "Running";
      const prompts = $("batchPrompts").value
        .split("\n")
        .map((line) => line.trim())
        .filter(Boolean);
      $("batchCount").textContent = String(prompts.length);
      try {
        const data = await postJson("/api/batch", { prompts });
        $("batchOutput").textContent =
          `${data.table}\n\nRaw JSON:\n${JSON.stringify(data.results, null, 2)}`;
        $("batchStatus").textContent = "Done";
      } catch (error) {
        showError("batchError", error.message);
        $("batchStatus").textContent = "Error";
      } finally {
        setBusy(button, false, "Run Batch");
      }
    });
  </script>
</body>
</html>
"""


def has_api_key() -> bool:
    return bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))


def json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def friendly_error(exc: Exception) -> str:
    message = str(exc).strip()
    if not message:
        message = exc.__class__.__name__
    return f"{exc.__class__.__name__}: {message}"


def log_event(message: str) -> None:
    line = f"[web_app] {datetime.now().isoformat(timespec='seconds')} {message}"
    print(line, flush=True)
    try:
        with LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except Exception:
        pass


def mock_chat_response(system_prompt: str, user_prompt: str) -> tuple[str, float]:
    response_text = (
        f"[MOCK] {system_prompt[:80]}\n"
        f"Trả lời cho: {user_prompt}"
    )
    return response_text, 0.123


def mock_compare_result(prompt: str) -> dict[str, Any]:
    return {
        "gpt4o_response": f"[MOCK] GPT-4o response for: {prompt}",
        "mini_response": f"[MOCK] Mini response for: {prompt}",
        "gpt4o_latency": 0.321,
        "mini_latency": 0.123,
        "gpt4o_cost_estimate": 0.00042,
        "source": "mock",
    }


def _read_float(payload: dict[str, Any], key: str, default: float) -> float:
    try:
        value = float(payload.get(key, default))
    except (TypeError, ValueError):
        return default
    return value


def _read_int(payload: dict[str, Any], key: str, default: int) -> int:
    try:
        value = int(payload.get(key, default))
    except (TypeError, ValueError):
        return default
    return value


class LabRequestHandler(BaseHTTPRequestHandler):
    server_version = "LabLLMWeb/1.0"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        log_event(f"GET {parsed.path}")
        if parsed.path != "/":
            self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return

        body = HTML.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        log_event(f"POST {parsed.path}")
        try:
            payload = self.read_json()
            log_event(f"Payload keys: {list(payload.keys())}")
            if not has_api_key():
                log_event("Missing GEMINI_API_KEY / GOOGLE_API_KEY")
                self.send_json(
                    {
                        "error": (
                            "Missing GEMINI_API_KEY or GOOGLE_API_KEY. "
                            "Add it to .env before calling the real API."
                        )
                    },
                    HTTPStatus.BAD_REQUEST,
                )
                return

            if parsed.path == "/api/chat":
                self.handle_chat(payload)
            elif parsed.path == "/api/compare":
                self.handle_compare(payload)
            elif parsed.path == "/api/batch":
                self.handle_batch(payload)
            else:
                self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON body"}, HTTPStatus.BAD_REQUEST)
        except Exception as exc:
            self.send_json({"error": friendly_error(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def handle_chat(self, payload: dict[str, Any]) -> None:
        system_prompt = str(payload.get("system_prompt", "")).strip()
        user_prompt = str(payload.get("user_prompt", "")).strip()
        temperature = _read_float(payload, "temperature", 0.7)
        top_p = _read_float(payload, "top_p", 0.9)
        max_tokens = _read_int(payload, "max_tokens", 256)
        log_event(
            f"handle_chat: system_prompt={len(system_prompt)} chars, "
            f"user_prompt={len(user_prompt)} chars, "
            f"temperature={temperature}, top_p={top_p}, max_tokens={max_tokens}"
        )
        if not system_prompt or not user_prompt:
            self.send_json(
                {"error": "system_prompt and user_prompt are required"},
                HTTPStatus.BAD_REQUEST,
            )
            return

        try:
            log_event("Calling template.chat_with_system_prompt()")
            response_text, latency_seconds = template.chat_with_system_prompt(
                system_prompt,
                user_prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
            )
            source = "real"
            log_event(f"Chat succeeded in {latency_seconds:.3f}s")
        except Exception as exc:
            log_event(f"Chat failed: {friendly_error(exc)}")
            traceback.print_exc()
            response_text, latency_seconds = mock_chat_response(system_prompt, user_prompt)
            source = "mock"
            response_text += f"\n\n[Fallback because {friendly_error(exc)}]"
        self.send_json(
            {
                "response_text": response_text,
                "latency_seconds": latency_seconds,
                "source": source,
            }
        )

    def handle_compare(self, payload: dict[str, Any]) -> None:
        prompt = str(payload.get("prompt", "")).strip()
        temperature = _read_float(payload, "temperature", 0.7)
        top_p = _read_float(payload, "top_p", 0.9)
        max_tokens = _read_int(payload, "max_tokens", 256)
        log_event(f"handle_compare: prompt={len(prompt)} chars")
        if not prompt:
            self.send_json({"error": "prompt is required"}, HTTPStatus.BAD_REQUEST)
            return

        try:
            log_event("Calling template.compare_models()")
            result = template.compare_models(
                prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
            )
            result["source"] = "real"
            log_event("Compare succeeded")
        except Exception as exc:
            log_event(f"Compare failed: {friendly_error(exc)}")
            traceback.print_exc()
            result = mock_compare_result(prompt)
            result["note"] = friendly_error(exc)
        self.send_json({"result": result})

    def handle_batch(self, payload: dict[str, Any]) -> None:
        prompts_value = payload.get("prompts", [])
        if not isinstance(prompts_value, list):
            self.send_json({"error": "prompts must be a list of strings"}, HTTPStatus.BAD_REQUEST)
            return

        prompts = [str(prompt).strip() for prompt in prompts_value if str(prompt).strip()]
        log_event(f"handle_batch: {len(prompts)} prompts")
        if not prompts:
            self.send_json({"error": "At least one prompt is required"}, HTTPStatus.BAD_REQUEST)
            return

        try:
            log_event("Calling template.batch_compare()")
            results = template.batch_compare(prompts)
            source = "real"
            log_event("Batch compare succeeded")
        except Exception as exc:
            log_event(f"Batch compare failed: {friendly_error(exc)}")
            traceback.print_exc()
            results = [dict(mock_compare_result(prompt), prompt=prompt) for prompt in prompts]
            source = "mock"
            batch_error = friendly_error(exc)
        else:
            batch_error = ""
        table = template.format_comparison_table(results)
        payload_out = {"results": results, "table": table, "source": source}
        if batch_error:
            payload_out["note"] = batch_error
        self.send_json(payload_out)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        if not body:
            return {}
        payload = json.loads(body.decode("utf-8"))
        if not isinstance(payload, dict):
            raise json.JSONDecodeError("JSON body must be an object", "", 0)
        return payload

    def send_json(
        self,
        payload: dict[str, Any],
        status: HTTPStatus = HTTPStatus.OK,
    ) -> None:
        body = json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        print(f"{self.address_string()} - {format % args}")


def make_server() -> ThreadingHTTPServer:
    TCPServer.allow_reuse_address = True
    return ThreadingHTTPServer((HOST, PORT), LabRequestHandler)


def main() -> None:
    load_dotenv()
    server = make_server()
    url = f"http://{HOST}:{PORT}"
    log_event(f"LLM API Lab UI running at {url}")
    log_event("Press Ctrl+C to stop.")
    log_event(
        "API key status: "
        + ("present" if has_api_key() else "missing")
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
