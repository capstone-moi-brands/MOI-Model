import os
import glob
import pandas as pd
from cv_extractor import CVTextExtractor

def run_cv_benchmark(folder_path="data/sample_cvs"):
    pdf_files = sorted(glob.glob(os.path.join(folder_path, "*.pdf")))
    if not pdf_files:
        print(f"No PDF files found in {folder_path}")
        return None

    extractor = CVTextExtractor(min_char_threshold=80)
    records = []

    print(f"=== STARTING BENCHMARK ON {len(pdf_files)} CV FORMATS ===")
    for idx, pdf in enumerate(pdf_files, 1):
        file_name = os.path.basename(pdf)
        res = extractor.extract_from_pdf(pdf)

        # Paragraph integrity check
        # Paragraphs shouldn't be empty, should have reasonable lengths, and no trailing hyphens
        paragraphs = [p for p in res.full_text.split("\n\n") if p.strip()]
        avg_para_len = sum(len(p) for p in paragraphs) / max(len(paragraphs), 1)
        has_severed_hyphen = any(p.endswith("-") for p in paragraphs)
        
        # Check integrity status
        if res.total_characters > 200 and not has_severed_hyphen and len(paragraphs) >= 3:
            integrity = "PASS (Cohesive)"
        elif res.total_characters > 50:
            integrity = "PASS (Acceptable)"
        else:
            integrity = "WARNING (Low Content)"

        records.append({
            "No": idx,
            "CV File": file_name,
            "Pages": res.total_pages,
            "Method Used": ", ".join(res.methods_used),
            "Characters": res.total_characters,
            "Words": res.total_words,
            "Paragraphs": len(paragraphs),
            "Time (s)": res.total_duration_sec,
            "Integrity": integrity
        })

        print(f"[{idx:02d}/{len(pdf_files)}] {file_name:<32} | {res.methods_used} | Chars: {res.total_characters:5d} | {res.total_duration_sec:.3f}s | {integrity}")

    df = pd.DataFrame(records)
    print("\n=== BENCHMARK SUMMARY TABLE ===")
    print(df.to_string(index=False))
    return df

if __name__ == "__main__":
    df = run_cv_benchmark()

