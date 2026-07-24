import os
from unittest.mock import patch

from dotenv import load_dotenv

import template


def fake_compare_models(prompt: str) -> dict:
    return {
        "gpt4o_response": f"Model lớn trả lời ngắn gọn cho: {prompt}",
        "mini_response": f"Model nhỏ trả lời nhanh cho: {prompt}",
        "gpt4o_latency": 1.234,
        "mini_latency": 0.456,
        "gpt4o_cost_estimate": 0.00012,
    }


def main() -> None:
    load_dotenv()

    prompts = [
        "Việt Nam có bao nhiêu tỉnh?",
        "Giải thích machine learning trong một câu.",
        "Kể một sự thật thú vị về Hà Nội.",
    ]

    has_api_key = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    if has_api_key:
        print("Running batch_compare with real Gemini API...\n")
        try:
            results = template.batch_compare(prompts)
        except Exception as exc:
            print(f"Real API demo failed: {type(exc).__name__}: {exc}")
            print("Falling back to mock demo so you can still see the output shape.\n")
            with patch.object(template, "compare_models", side_effect=fake_compare_models):
                results = template.batch_compare(prompts)
    else:
        print("No GEMINI_API_KEY or GOOGLE_API_KEY found.")
        print("Running mock demo so you can see the output shape.\n")
        with patch.object(template, "compare_models", side_effect=fake_compare_models):
            results = template.batch_compare(prompts)

    print("Raw results:")
    for index, result in enumerate(results, start=1):
        print(f"\n[{index}] Prompt: {result['prompt']}")
        print(f"GPT-4o response: {result['gpt4o_response']}")
        print(f"Mini response: {result['mini_response']}")
        print(f"GPT-4o latency: {result['gpt4o_latency']:.3f}s")
        print(f"Mini latency: {result['mini_latency']:.3f}s")

    print("\nFormatted table:")
    print(template.format_comparison_table(results))


if __name__ == "__main__":
    main()
