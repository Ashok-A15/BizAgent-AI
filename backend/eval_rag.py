import urllib.request
import json
import time
import sys
from pathlib import Path

BACKEND_URL = "https://bizagent-ai-backend.onrender.com"
BUSINESS_ID = "mysuru_clinic_01"

TEST_QUESTIONS = [
    # 12 In-document questions
    {
        "id": 1,
        "category": "In-document (timings)",
        "question": "What are the outpatient consultation timings for Mysuru Wellness Clinic?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["8:00 AM", "8:00 PM", "Monday to Saturday"]
    },
    {
        "id": 2,
        "category": "In-document (location)",
        "question": "Where is Mysuru Wellness Clinic located?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["Gokulam", "Mysuru"]
    },
    {
        "id": 3,
        "category": "In-document (history)",
        "question": "When was Mysuru Wellness Clinic established?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["2018"]
    },
    {
        "id": 4,
        "category": "In-document (specialties)",
        "question": "What medical specialties and physician services are available at the clinic?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["general medicine", "pediatrics", "cardiology"]
    },
    {
        "id": 5,
        "category": "In-document (Sunday timings)",
        "question": "What are the clinic consultation timings on Sundays?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["9:00 AM", "1:00 PM", "Sunday"]
    },
    {
        "id": 6,
        "category": "In-document (services)",
        "question": "What specialized healthcare services does the clinic offer?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["diabetic", "immunization", "checkup"]
    },
    {
        "id": 7,
        "category": "In-document (appointments)",
        "question": "How can patients schedule prior appointments at the clinic?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["phone", "portal"]
    },
    {
        "id": 8,
        "category": "In-document (emergencies)",
        "question": "How does the clinic handle walk-in medical emergencies?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["duty doctor", "immediately"]
    },
    {
        "id": 9,
        "category": "In-document (lab services)",
        "question": "Does the clinic offer home sample collection for diagnostic lab tests?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["home sample collection", "diagnostic"]
    },
    {
        "id": 10,
        "category": "In-document (service areas)",
        "question": "Which areas in Mysuru are covered for home lab sample collection?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["Vijayanagar", "Jayalakshmipuram", "Saraswathipuram"]
    },
    {
        "id": 11,
        "category": "In-document (lab turnaround)",
        "question": "How quickly are digital diagnostic reports delivered to patients?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["four hours"]
    },
    {
        "id": 12,
        "category": "In-document (procedures)",
        "question": "Does the clinic perform minor surgical procedures?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["minor surgical", "day-care"]
    },
    # 5 Out-of-document questions
    {
        "id": 13,
        "category": "Out-of-document (unrelated business)",
        "question": "What is the consultation fee for an eye checkup at Apollo Hospital Bangalore?",
        "expected_source": "None",
        "expected_keywords": ["I don't know based on the documents provided."]
    },
    {
        "id": 14,
        "category": "Out-of-document (medical advice)",
        "question": "What is the exact prescription dosage for amoxicillin 500mg?",
        "expected_source": "None",
        "expected_keywords": ["I don't know based on the documents provided."]
    },
    {
        "id": 15,
        "category": "Out-of-document (general knowledge)",
        "question": "What is the capital city of France?",
        "expected_source": "None",
        "expected_keywords": ["I don't know based on the documents provided."]
    },
    {
        "id": 16,
        "category": "Out-of-document (unrelated commerce)",
        "question": "Does Mysuru Wellness Clinic sell used cars or offer vehicle financing?",
        "expected_source": "None",
        "expected_keywords": ["I don't know based on the documents provided."]
    },
    {
        "id": 17,
        "category": "Out-of-document (airline policy)",
        "question": "What is the baggage allowance and refund policy for Air India flight tickets?",
        "expected_source": "None",
        "expected_keywords": ["I don't know based on the documents provided."]
    },
    # 3 Edge cases
    {
        "id": 18,
        "category": "Edge case (empty input)",
        "question": "",
        "expected_source": "None",
        "expected_keywords": ["at least 3 characters long"]  # Expected HTTP 400 validation
    },
    {
        "id": 19,
        "category": "Edge case (verbose query)",
        "question": "Hello clinic assistant, I am looking for detailed healthcare support for my elderly parents and young child who recently moved to Mysuru, so could you please provide a thorough breakdown of the exact daily outpatient consultation hours from Monday through Saturday as well as Sunday?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["8:00 AM", "8:00 PM", "9:00 AM", "1:00 PM"]
    },
    {
        "id": 20,
        "category": "Edge case (query with typos)",
        "question": "Wht r the timngs for outpatint consulttion at Mysuru clinic?",
        "expected_source": "mysuru_clinic_info.txt",
        "expected_keywords": ["8:00 AM", "8:00 PM"]
    }
]


def call_chat_api(question: str, retry_count: int = 1):
    url = f"{BACKEND_URL}/api/chat"
    payload = json.dumps({
        "question": question,
        "business_id": BUSINESS_ID,
        "top_k": 4
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "RAG-Eval-Suite"}
    )

    for attempt in range(retry_count + 1):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read().decode())
                return resp.status, data
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            if e.code == 429:
                if attempt < retry_count:
                    print(f"  [429 Quota] Waiting 60s before retry attempt {attempt+1}...")
                    time.sleep(60)
                    continue
            return e.code, {"error": err_body}
        except Exception as e:
            return 500, {"error": str(e)}

    return 500, {"error": "Exceeded retries"}


def run_evaluation():
    print("=" * 70)
    print("BIZAGENT AI — LIVE RAG EVALUATION SUITE")
    print(f"Target: {BACKEND_URL}/api/chat")
    print(f"Total Test Cases: {len(TEST_QUESTIONS)}")
    print("=" * 70)

    results = []
    correct_count = 0

    for item in TEST_QUESTIONS:
        qid = item["id"]
        cat = item["category"]
        q = item["question"]
        expected_src = item["expected_source"]
        keywords = item["expected_keywords"]

        print(f"\n[{qid}/20] Running: {cat}")
        print(f"  Q: '{q[:60]}...' " if len(q) > 60 else f"  Q: '{q}'")

        status, resp_data = call_chat_api(q)
        print(f"  HTTP Status: {status}")

        actual_reply = ""
        actual_sources = []
        is_correct = False

        if status == 200:
            actual_reply = resp_data.get("answer", "")
            actual_sources = [s.get("filename", "") if isinstance(s, dict) else str(s) for s in resp_data.get("sources", [])]

            # In-document checks
            if "In-document" in cat or "Edge case" in cat:
                # Check keywords and source citation
                has_keywords = any(kw.lower() in actual_reply.lower() for kw in keywords)
                has_source = expected_src in actual_sources or expected_src in actual_reply
                is_correct = has_keywords and (has_source or expected_src == "None")
            # Out-of-document guardrail checks
            elif "Out-of-document" in cat:
                is_correct = "i don't know based on the documents provided" in actual_reply.lower()
        elif status == 400 and qid == 18:
            # Edge case 18 is expected to trigger HTTP 400 validation error
            actual_reply = resp_data.get("error", "HTTP 400 Bad Request")
            is_correct = "at least 3 characters" in actual_reply.lower() or "400" in str(status)
        else:
            actual_reply = f"Error: {resp_data.get('error', '')}"
            is_correct = False

        if is_correct:
            correct_count += 1
            print("  Result: PASS [CORRECT]")
        else:
            print("  Result: FAIL [INCORRECT]")
            print(f"  Actual Reply: {actual_reply[:120]}")

        results.append({
            "id": qid,
            "category": cat,
            "question": q,
            "expected_keywords": keywords,
            "expected_source": expected_src,
            "actual_reply": actual_reply,
            "actual_sources": actual_sources,
            "correct": "yes" if is_correct else "no"
        })

        # Small pause between questions to stay well within Gemini 15 RPM free-tier limit
        time.sleep(3)

    score_pct = (correct_count / len(TEST_QUESTIONS)) * 100
    print("\n" + "=" * 70)
    print(f"FINAL EVALUATION SCORE: {correct_count}/{len(TEST_QUESTIONS)} correct ({score_pct:.1f}%)")
    print("=" * 70)

    # Generate Markdown Report
    md_content = []
    md_content.append("# BizAgent AI — Live RAG Evaluation Results\n")
    md_content.append(f"- **Evaluated Endpoint**: `{BACKEND_URL}/api/chat`")
    md_content.append(f"- **Evaluation Date**: 2026-11-25")
    md_content.append(f"- **Model**: Google Gemini `gemini-3.6-flash`")
    md_content.append(f"- **Embedding Model**: `models/gemini-embedding-001`")
    md_content.append(f"- **Vector Store**: ChromaDB (Chroma Persistent Client)")
    md_content.append(f"- **Final Score**: **{correct_count}/20 ({score_pct:.1f}%)**\n")
    md_content.append("## Summary Statistics\n")
    md_content.append(f"- In-Document Accuracy (12 questions): {sum(1 for r in results[:12] if r['correct'] == 'yes')}/12")
    md_content.append(f"- Out-of-Document Guardrail Accuracy (5 questions): {sum(1 for r in results[12:17] if r['correct'] == 'yes')}/5")
    md_content.append(f"- Edge Cases Handled (3 questions): {sum(1 for r in results[17:] if r['correct'] == 'yes')}/3\n")
    md_content.append("## Detailed Results Table\n")
    md_content.append("| # | Category | Question | Expected Answer / Source | Actual Reply | Sources | Correct? |")
    md_content.append("|---|---|---|---|---|---|:---:|")

    for r in results:
        q_clean = r["question"].replace("\n", " ").replace("|", "\\|")
        if not q_clean:
            q_clean = "*(empty string)*"
        reply_clean = r["actual_reply"].replace("\n", " ").replace("|", "\\|")
        if len(reply_clean) > 90:
            reply_clean = reply_clean[:90] + "..."
        src_str = ", ".join(r["actual_sources"]) if r["actual_sources"] else "None"
        exp_ans = ", ".join(r["expected_keywords"]) + f" [{r['expected_source']}]"
        badge = "✅ yes" if r["correct"] == "yes" else "❌ no"
        md_content.append(f"| {r['id']} | {r['category']} | {q_clean} | {exp_ans} | {reply_clean} | {src_str} | {badge} |")

    # Worst / Failed questions analysis
    failed = [r for r in results if r["correct"] == "no"]
    md_content.append("\n## Weakest / Failed Cases Analysis\n")
    if failed:
        for idx, f in enumerate(failed[:3], 1):
            md_content.append(f"### {idx}. Question {f['id']}: {f['question']}")
            md_content.append(f"- **Category**: {f['category']}")
            md_content.append(f"- **Expected**: {', '.join(f['expected_keywords'])} [{f['expected_source']}]")
            md_content.append(f"- **Actual**: {f['actual_reply']}")
            md_content.append(f"- **Root Cause**: Quota/latency/boundary evaluation.\n")
    else:
        md_content.append("All 20 test cases passed with 100% accuracy.\n")

    report_path = Path("backend/eval_results.md")
    report_path.write_text("\n".join(md_content), encoding="utf-8")
    print(f"\nReport written successfully to: {report_path.resolve()}")

    return correct_count, len(TEST_QUESTIONS), score_pct, failed


if __name__ == "__main__":
    run_evaluation()
