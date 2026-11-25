# BizAgent AI — Live RAG Evaluation Results

- **Evaluated Endpoint**: `https://bizagent-ai-backend.onrender.com/api/chat`
- **Evaluation Date**: 2026-11-25
- **Model**: Google Gemini `gemini-3.6-flash`
- **Embedding Model**: `models/gemini-embedding-001`
- **Vector Store**: ChromaDB (Chroma Persistent Client)
- **Final Score**: **15/20 (75.0%)**

## Summary Statistics

- In-Document Accuracy (12 questions): 10/12
- Out-of-Document Guardrail Accuracy (5 questions): 4/5
- Edge Cases Handled (3 questions): 1/3

## Detailed Results Table

| # | Category | Question | Expected Answer / Source | Actual Reply | Sources | Correct? |
|---|---|---|---|---|---|:---:|
| 1 | In-document (timings) | What are the outpatient consultation timings for Mysuru Wellness Clinic? | 8:00 AM, 8:00 PM, Monday to Saturday [mysuru_clinic_info.txt] | The outpatient consultation timings for Mysuru Wellness Clinic are: * **Monday to Saturday... | mysuru_clinic_info.txt | ✅ yes |
| 2 | In-document (location) | Where is Mysuru Wellness Clinic located? | Gokulam, Mysuru [mysuru_clinic_info.txt] | Mysuru Wellness Clinic is located in Gokulam, Mysuru [mysuru_clinic_info.txt]. | mysuru_clinic_info.txt | ✅ yes |
| 3 | In-document (history) | When was Mysuru Wellness Clinic established? | 2018 [mysuru_clinic_info.txt] | Mysuru Wellness Clinic was established in 2018 [mysuru_clinic_info.txt]. | mysuru_clinic_info.txt | ✅ yes |
| 4 | In-document (specialties) | What medical specialties and physician services are available at the clinic? | general medicine, pediatrics, cardiology [mysuru_clinic_info.txt] | Based on the provided document, the clinic offers the following medical specialties and ph... | mysuru_clinic_info.txt | ✅ yes |
| 5 | In-document (Sunday timings) | What are the clinic consultation timings on Sundays? | 9:00 AM, 1:00 PM, Sunday [mysuru_clinic_info.txt] | On Sundays, the clinic offers consultations from 9:00 AM to 1:00 PM for urgent consultatio... | mysuru_clinic_info.txt | ✅ yes |
| 6 | In-document (services) | What specialized healthcare services does the clinic offer? | diabetic, immunization, checkup [mysuru_clinic_info.txt] | Based on the provided documents, the clinic offers the following specialized services:  * ... | mysuru_clinic_info.txt | ✅ yes |
| 7 | In-document (appointments) | How can patients schedule prior appointments at the clinic? | phone, portal [mysuru_clinic_info.txt] | Patients can schedule prior appointments via phone or through the clinic digital portal [m... | mysuru_clinic_info.txt | ✅ yes |
| 8 | In-document (emergencies) | How does the clinic handle walk-in medical emergencies? | duty doctor, immediately [mysuru_clinic_info.txt] | Walk-in emergencies are attended to by duty doctors immediately [mysuru_clinic_info.txt]. | mysuru_clinic_info.txt | ✅ yes |
| 9 | In-document (lab services) | Does the clinic offer home sample collection for diagnostic lab tests? | home sample collection, diagnostic [mysuru_clinic_info.txt] | Yes, the clinic provides home sample collection for diagnostic lab tests across the Vijaya... | mysuru_clinic_info.txt | ✅ yes |
| 10 | In-document (service areas) | Which areas in Mysuru are covered for home lab sample collection? | Vijayanagar, Jayalakshmipuram, Saraswathipuram [mysuru_clinic_info.txt] | Based on `mysuru_clinic_info.txt`, home lab sample collection is provided across the follo... | mysuru_clinic_info.txt | ✅ yes |
| 11 | In-document (lab turnaround) | How quickly are digital diagnostic reports delivered to patients? | four hours [mysuru_clinic_info.txt] | Error: Internal Server Error | None | ❌ no |
| 12 | In-document (procedures) | Does the clinic perform minor surgical procedures? | minor surgical, day-care [mysuru_clinic_info.txt] | Error: Internal Server Error | None | ❌ no |
| 13 | Out-of-document (unrelated business) | What is the consultation fee for an eye checkup at Apollo Hospital Bangalore? | I don't know based on the documents provided. [None] | I don't know based on the documents provided. | None | ✅ yes |
| 14 | Out-of-document (medical advice) | What is the exact prescription dosage for amoxicillin 500mg? | I don't know based on the documents provided. [None] | Error: Internal Server Error | None | ❌ no |
| 15 | Out-of-document (general knowledge) | What is the capital city of France? | I don't know based on the documents provided. [None] | I don't know based on the documents provided. | None | ✅ yes |
| 16 | Out-of-document (unrelated commerce) | Does Mysuru Wellness Clinic sell used cars or offer vehicle financing? | I don't know based on the documents provided. [None] | I don't know based on the documents provided. | None | ✅ yes |
| 17 | Out-of-document (airline policy) | What is the baggage allowance and refund policy for Air India flight tickets? | I don't know based on the documents provided. [None] | I don't know based on the documents provided. | None | ✅ yes |
| 18 | Edge case (empty input) | *(empty string)* | at least 3 characters long [None] | {"detail":"Question is required and must be at least 3 characters long."} | None | ✅ yes |
| 19 | Edge case (verbose query) | Hello clinic assistant, I am looking for detailed healthcare support for my elderly parents and young child who recently moved to Mysuru, so could you please provide a thorough breakdown of the exact daily outpatient consultation hours from Monday through Saturday as well as Sunday? | 8:00 AM, 8:00 PM, 9:00 AM, 1:00 PM [mysuru_clinic_info.txt] | Error: Internal Server Error | None | ❌ no |
| 20 | Edge case (query with typos) | Wht r the timngs for outpatint consulttion at Mysuru clinic? | 8:00 AM, 8:00 PM [mysuru_clinic_info.txt] | Error: Internal Server Error | None | ❌ no |

## Weakest / Failed Cases Analysis

### 1. Question 11: How quickly are digital diagnostic reports delivered to patients?
- **Category**: In-document (lab turnaround)
- **Expected**: four hours [mysuru_clinic_info.txt]
- **Actual**: Error: Internal Server Error
- **Root Cause**: Quota/latency/boundary evaluation.

### 2. Question 12: Does the clinic perform minor surgical procedures?
- **Category**: In-document (procedures)
- **Expected**: minor surgical, day-care [mysuru_clinic_info.txt]
- **Actual**: Error: Internal Server Error
- **Root Cause**: Quota/latency/boundary evaluation.

### 3. Question 14: What is the exact prescription dosage for amoxicillin 500mg?
- **Category**: Out-of-document (medical advice)
- **Expected**: I don't know based on the documents provided. [None]
- **Actual**: Error: Internal Server Error
- **Root Cause**: Quota/latency/boundary evaluation.
