"""
CV Text Extraction Module (PyMuPDF + EasyOCR Fallback)
Part of Capstone Project: Automated Candidate Screening & Rating Pipeline

Features:
1. Fast, high-fidelity digital PDF text extraction via PyMuPDF (fitz).
2. Intelligent column-aware reading order (handles 1-column, 2-column, and multi-column resumes).
3. Automatic Fallback to OCR (EasyOCR) when PyMuPDF detects image-only or low-text pages
   (e.g., CVs exported from Canva, Photoshop, or scanned documents).
4. GPU acceleration support (NVIDIA CUDA) with graceful fallback to CPU.
5. Smart post-processing: unbreaks line wraps within paragraphs, fixes hyphenation,
   preserves section headers, bullet points, and clean paragraph breaks.
6. Works seamlessly in both local environments and sandboxed directories.
"""

import os
import re
import time
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

import fitz  # PyMuPDF
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("CVExtractor")


@dataclass
class PageExtractionResult:
    """Represents extraction result for a single page."""
    page_number: int
    method_used: str  # "PyMuPDF" or "EasyOCR_Fallback"
    raw_character_count: int
    cleaned_character_count: int
    word_count: int
    extracted_text: str
    processing_time_sec: float
    fallback_triggered: bool = False


@dataclass
class CVExtractionResult:
    """Represents full extraction result for a CV document."""
    file_path: str
    file_name: str
    total_pages: int
    methods_used: List[str]
    total_characters: int
    total_words: int
    full_text: str
    pages: List[PageExtractionResult] = field(default_factory=list)
    total_duration_sec: float = 0.0
    status: str = "SUCCESS"
    error_message: Optional[str] = None


class CVTextExtractor:
    """
    Robust CV Text Extractor combining PyMuPDF and EasyOCR.
    """

    def __init__(
        self,
        min_char_threshold: int = 80,
        ocr_languages: List[str] = None,
        use_gpu: Optional[bool] = None,
        model_storage_dir: Optional[str] = None,
        user_network_dir: Optional[str] = None,
        raster_dpi: int = 150,
    ):
        """
        Args:
            min_char_threshold: Minimum characters required per page before triggering OCR fallback.
            ocr_languages: List of languages for EasyOCR (default ['en', 'id']).
            use_gpu: Whether to use CUDA GPU for OCR. If None, auto-detected.
            model_storage_dir: Custom directory for EasyOCR model weights.
            user_network_dir: Custom directory for user network cache.
            raster_dpi: Resolution (DPI) when converting PDF page to image for OCR.
        """
        self.min_char_threshold = min_char_threshold
        self.ocr_languages = ocr_languages or ["en", "id"]
        self.raster_dpi = raster_dpi
        self._ocr_reader = None

        # GPU auto-detection
        if use_gpu is None:
            try:
                import torch
                self.use_gpu = torch.cuda.is_available()
            except ImportError:
                self.use_gpu = False
        else:
            self.use_gpu = use_gpu

        # Resolve local paths for model storage (handles sandbox permissions cleanly)
        workspace_dir = os.path.dirname(os.path.abspath(__file__))
        local_model_dir = os.path.join(workspace_dir, ".easyocr_models")
        if model_storage_dir:
            self.model_storage_dir = os.path.abspath(model_storage_dir)
        elif os.path.exists(local_model_dir):
            self.model_storage_dir = local_model_dir
        else:
            self.model_storage_dir = None

        if user_network_dir:
            self.user_network_dir = os.path.abspath(user_network_dir)
        elif self.model_storage_dir:
            self.user_network_dir = os.path.join(self.model_storage_dir, "user_network")
            os.makedirs(self.user_network_dir, exist_ok=True)
        else:
            self.user_network_dir = None

        logger.info(
            f"Initialized CVTextExtractor (Threshold: {self.min_char_threshold} chars | "
            f"GPU: {self.use_gpu} | DPI: {self.raster_dpi})"
        )

    @property
    def ocr_reader(self):
        """Lazy loader for EasyOCR to save startup memory when OCR isn't triggered."""
        if self._ocr_reader is None:
            logger.info("Initializing EasyOCR Reader...")
            import easyocr

            kwargs = {
                "lang_list": self.ocr_languages,
                "gpu": self.use_gpu,
            }
            if self.model_storage_dir and os.path.exists(self.model_storage_dir):
                kwargs["model_storage_directory"] = self.model_storage_dir
                kwargs["download_enabled"] = False
            if self.user_network_dir:
                kwargs["user_network_directory"] = self.user_network_dir

            self._ocr_reader = easyocr.Reader(**kwargs)
            logger.info("EasyOCR Reader ready.")
        return self._ocr_reader

    # --------------------------------------------------------------------------
    # Layout and Text Analysis
    # --------------------------------------------------------------------------

    @staticmethod
    def is_header_line(line: str) -> bool:
        """Determines if a line is likely a section header."""
        stripped = line.strip()
        if not stripped:
            return False
        # Short uppercase line (e.g., EXPERIENCE, PENDIDIKAN, SKILLS)
        if stripped.isupper() and len(stripped) <= 50:
            return True
        # Standard CV section keywords
        common_headers = {
            "summary", "ringkasan", "ringkasan profesional", "professional summary",
            "career profile", "profil", "tentang saya", "about me", "experience",
            "work experience", "pengalaman", "pengalaman kerja", "riwayat pekerjaan",
            "education", "pendidikan", "riwayat pendidikan", "skills", "keahlian",
            "kemampuan", "technical skills", "proyek", "projects", "certifications",
            "sertifikasi", "lisensi", "licenses", "languages", "bahasa",
            "awards", "penghargaan", "kontak", "contact", "organizations", "organisasi"
        }
        lower = stripped.lower()
        if lower in common_headers:
            return True
        if any(lower.startswith(h + ":") or lower.startswith(h + " -") for h in common_headers):
            return True
        return False

    @classmethod
    def clean_and_format_text(cls, text: str) -> str:
        """
        Cleans extracted text, repairs broken lines within paragraphs,
        fixes hyphenation across line breaks, and preserves section headers/lists.
        """
        if not text:
            return ""

        # 1. Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # 2. Fix hyphenation at line breaks (e.g. 'distribu-\nted' -> 'distributed')
        text = re.sub(r"(\b\w+)-\s*\n\s*(\w+\b)", r"\1\2", text)

        raw_lines = [line.strip() for line in text.split("\n")]
        cleaned_lines: List[str] = []

        for line in raw_lines:
            if not line:
                # Add a blank line only if previous wasn't already blank
                if cleaned_lines and cleaned_lines[-1] != "":
                    cleaned_lines.append("")
                continue

            is_bullet = (
                line.startswith(("*", "-", "•", "–", "—", "►", "✓"))
                or bool(re.match(r"^\d+[\.\)]\s", line))
            )
            is_curr_header = cls.is_header_line(line)

            if cleaned_lines and cleaned_lines[-1] != "":
                prev = cleaned_lines[-1]
                prev_is_header = cls.is_header_line(prev)
                prev_ends_punc = prev.endswith((".", ":", ";", "!", "?"))
                prev_is_bullet_item = (
                    prev.startswith(("*", "-", "•", "–", "—", "►", "✓"))
                    or bool(re.match(r"^\d+[\.\)]\s", prev))
                )

                # Merge condition:
                # If neither is a header, current is not a bullet item,
                # and previous didn't finish with sentence punctuation
                if not prev_is_header and not is_curr_header and not is_bullet and not prev_ends_punc:
                    cleaned_lines[-1] = f"{prev} {line}"
                    continue

            cleaned_lines.append(line)

        result = "\n".join(cleaned_lines)
        # Normalize redundant newlines
        result = re.sub(r"\n{3,}", "\n\n", result).strip()
        return result

    @classmethod
    def extract_page_column_aware(cls, page: fitz.Page) -> str:
        """
        Extracts text from a PyMuPDF page with multi-column awareness.
        Prevents text from cross-column bleeding in 2-column or sidebar CV templates.
        """
        blocks = page.get_text("blocks")
        # Filter for text blocks (type 0) with non-whitespace content
        text_blocks = [b for b in blocks if len(b) >= 5 and b[4].strip() and b[6] == 0]
        if not text_blocks:
            return ""

        page_width = page.rect.width
        page_height = page.rect.height

        # Test candidate vertical split gutters
        candidate_splits = [
            page_width * ratio
            for ratio in [0.25, 0.30, 0.33, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.66, 0.70]
        ]
        best_split = None

        for split in candidate_splits:
            left_blocks = [b for b in text_blocks if b[2] <= split + 15]
            right_blocks = [b for b in text_blocks if b[0] >= split - 15]
            spanning_blocks = [b for b in text_blocks if b[0] < split - 15 and b[2] > split + 15]

            # If both sides contain distinct blocks and very few span the gutter
            if len(left_blocks) >= 2 and len(right_blocks) >= 2 and len(spanning_blocks) <= 1:
                best_split = split
                break

        if best_split:
            # Header blocks that span the full top area
            header_blocks = [
                b for b in text_blocks
                if b[0] < best_split - 15 and b[2] > best_split + 15 and b[1] < page_height * 0.3
            ]
            # Footer blocks that span the bottom area
            footer_blocks = [
                b for b in text_blocks
                if b[0] < best_split - 15 and b[2] > best_split + 15 and b[1] >= page_height * 0.3
            ]
            # Column content
            left_blocks = [
                b for b in text_blocks
                if b not in header_blocks and b not in footer_blocks and (b[0] + b[2]) / 2 < best_split
            ]
            right_blocks = [
                b for b in text_blocks
                if b not in header_blocks and b not in footer_blocks and (b[0] + b[2]) / 2 >= best_split
            ]

            header_blocks.sort(key=lambda b: (b[1], b[0]))
            left_blocks.sort(key=lambda b: (b[1], b[0]))
            right_blocks.sort(key=lambda b: (b[1], b[0]))
            footer_blocks.sort(key=lambda b: (b[1], b[0]))

            ordered_blocks = header_blocks + left_blocks + right_blocks + footer_blocks
        else:
            # Standard single-column or linear layout: sort vertically
            ordered_blocks = sorted(text_blocks, key=lambda b: (b[1], b[0]))

        return "\n\n".join(b[4].strip() for b in ordered_blocks)

    # --------------------------------------------------------------------------
    # OCR Fallback Processing
    # --------------------------------------------------------------------------

    def extract_page_ocr(self, page: fitz.Page) -> str:
        """
        Renders a PDF page to a high-resolution pixmap and runs EasyOCR with paragraph grouping.
        """
        # Render page to RGB numpy image
        pix = page.get_pixmap(dpi=self.raster_dpi)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))
        if pix.n >= 4:
            img = img[:, :, :3]

        # EasyOCR with paragraph=True groups words on nearby lines into coherent paragraphs
        results = self.ocr_reader.readtext(img, paragraph=True)

        if not results:
            return ""

        # Sort OCR paragraphs in reading order (top-to-bottom, left-to-right)
        # Each entry is (bbox, text) where bbox is [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
        def get_box_coords(item):
            bbox = item[0]
            x_min = min(pt[0] for pt in bbox)
            y_min = min(pt[1] for pt in bbox)
            return (y_min, x_min)

        sorted_results = sorted(results, key=get_box_coords)
        ocr_text = "\n\n".join(text.strip() for _, text in sorted_results if text.strip())
        return ocr_text

    # --------------------------------------------------------------------------
    # Primary Extraction Pipeline
    # --------------------------------------------------------------------------

    def extract_from_pdf(self, pdf_path: str) -> CVExtractionResult:
        """
        Extracts raw and cleaned text from a candidate's CV PDF.
        Executes PyMuPDF first, falling back to EasyOCR if text is empty or too short.

        Args:
            pdf_path: Absolute or relative path to candidate CV PDF file.

        Returns:
            CVExtractionResult object containing extracted text and metadata.
        """
        t0 = time.time()
        file_name = os.path.basename(pdf_path)

        if not os.path.exists(pdf_path):
            return CVExtractionResult(
                file_path=pdf_path,
                file_name=file_name,
                total_pages=0,
                methods_used=[],
                total_characters=0,
                total_words=0,
                full_text="",
                status="ERROR",
                error_message=f"File not found: {pdf_path}",
            )

        doc = None
        try:
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            page_results: List[PageExtractionResult] = []
            methods_used_set = set()

            for page_idx in range(total_pages):
                page_start_time = time.time()
                page = doc[page_idx]

                # Step 1: Attempt PyMuPDF text extraction with column-awareness
                raw_text = self.extract_page_column_aware(page)
                cleaned_text = self.clean_and_format_text(raw_text)
                char_count = len(cleaned_text.strip())

                # Step 2: Fallback condition check
                if char_count < self.min_char_threshold:
                    logger.info(
                        f"[{file_name} P.{page_idx+1}] Text too short ({char_count} chars < {self.min_char_threshold}). "
                        f"Triggering OCR Fallback..."
                    )
                    ocr_raw_text = self.extract_page_ocr(page)
                    cleaned_ocr_text = self.clean_and_format_text(ocr_raw_text)

                    method = "EasyOCR_Fallback"
                    final_text = cleaned_ocr_text
                    fallback_triggered = True
                else:
                    method = "PyMuPDF"
                    final_text = cleaned_text
                    fallback_triggered = False

                page_duration = time.time() - page_start_time
                methods_used_set.add(method)

                page_res = PageExtractionResult(
                    page_number=page_idx + 1,
                    method_used=method,
                    raw_character_count=len(final_text),
                    cleaned_character_count=len(final_text.strip()),
                    word_count=len(final_text.split()),
                    extracted_text=final_text,
                    processing_time_sec=round(page_duration, 3),
                    fallback_triggered=fallback_triggered,
                )
                page_results.append(page_res)

            full_text = "\n\n--- PAGE BREAK ---\n\n".join(
                p.extracted_text for p in page_results if p.extracted_text
            )
            total_duration = time.time() - t0

            return CVExtractionResult(
                file_path=os.path.abspath(pdf_path),
                file_name=file_name,
                total_pages=total_pages,
                methods_used=sorted(list(methods_used_set)),
                total_characters=len(full_text),
                total_words=len(full_text.split()),
                full_text=full_text,
                pages=page_results,
                total_duration_sec=round(total_duration, 3),
                status="SUCCESS",
            )

        except Exception as e:
            logger.error(f"Error extracting {pdf_path}: {e}", exc_info=True)
            return CVExtractionResult(
                file_path=os.path.abspath(pdf_path),
                file_name=file_name,
                total_pages=0,
                methods_used=[],
                total_characters=0,
                total_words=0,
                full_text="",
                status="ERROR",
                error_message=str(e),
                total_duration_sec=round(time.time() - t0, 3),
            )
        finally:
            if doc:
                doc.close()


if __name__ == "__main__":
    import json

    extractor = CVTextExtractor()
    test_file = "data/sample_cvs/cv_01_ats_standard_en.pdf"
    if os.path.exists(test_file):
        res = extractor.extract_from_pdf(test_file)
        print(f"Extracted {res.file_name} via {res.methods_used} in {res.total_duration_sec}s")
        print(f"Characters: {res.total_characters} | Words: {res.total_words}")
        print("\n--- SAMPLE EXTRACTED TEXT ---\n")
        print(res.full_text[:500])

