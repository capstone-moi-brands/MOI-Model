import os
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

os.makedirs("data/sample_cvs", exist_ok=True)

# Helper to render fitz page to image-only PDF (simulating Canva / Scan export)
def rasterize_pdf_page_to_image_pdf(doc_src, output_path, dpi=200):
    new_doc = fitz.open()
    for page in doc_src:
        pix = page.get_pixmap(dpi=dpi)
        img_bytes = pix.tobytes("png")
        # create new page in target doc with same dimensions
        rect = page.rect
        new_page = new_doc.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, stream=img_bytes)
    new_doc.save(output_path)
    new_doc.close()

# 1. ATS Standard EN
def create_cv_01():
    doc = fitz.open()
    page = doc.new_page()
    text = """ALEXANDER WRIGHT
Senior Software Engineer | Jakarta, Indonesia | alex.wright@email.com | +62 812-3456-7890 | linkedin.com/in/alexwright

SUMMARY
Results-oriented Senior Software Engineer with 6+ years of experience specializing in high-throughput backend systems, distributed architectures, and cloud-native solutions using Python, Go, and PostgreSQL. Proven track record of improving system uptime to 99.99% and mentoring junior developers.

EXPERIENCE
Senior Backend Engineer - TechCorp Nusantara (2021 - Present)
* Architected and deployed microservices handling 25,000 requests per second using Python FastAPI, Celery, and Redis.
* Reduced database query latency by 45% through indexing optimizations and partitioned PostgreSQL tables.
* Spearheaded migration from monolithic legacy systems to AWS EKS with zero downtime.

Software Engineer - DataFlow Solusi (2018 - 2021)
* Developed RESTful APIs and real-time Kafka event streams for payment processing gateway.
* Collaborated with cross-functional teams to automate CI/CD pipelines using GitHub Actions and Docker.
* Implemented end-to-end unit and integration testing reaching 92% code coverage.

EDUCATION
Bachelor of Science in Computer Science - Universitas Indonesia (2014 - 2018)
* GPA: 3.82 / 4.00 (Cum Laude)

SKILLS & CERTIFICATIONS
* Languages: Python, Go, SQL, Bash, JavaScript
* Cloud & DevOps: Docker, Kubernetes, AWS (EC2, S3, RDS, Lambda), Terraform, CI/CD
* Databases: PostgreSQL, Redis, MongoDB, Elasticsearch
* Certifications: AWS Certified Solutions Architect - Associate
"""
    page.insert_textbox(fitz.Rect(50, 40, 545, 780), text, fontsize=10, fontname="helv")
    doc.save("data/sample_cvs/cv_01_ats_standard_en.pdf")
    doc.close()

# 2. ATS Standard ID
def create_cv_02():
    doc = fitz.open()
    page = doc.new_page()
    text = """SITI NURHALIZA
Data Analyst | Bandung, Indonesia | siti.nurhaliza@email.co.id | +62 821-9876-5432 | github.com/sitinur

RINGKASAN PROFESIONAL
Data Analyst analitis dan teliti dengan pengalaman 4 tahun dalam mengolah dataset berskala besar, memvisualisasikan insight bisnis, dan membangun model prediktif machine learning untuk meningkatkan konversi penjualan dan retensi pelanggan e-commerce.

PENGALAMAN KERJA
Data Analyst - PT Mega Retail Digital (2022 - Sekarang)
* Mengembangkan dashboard eksekutif interaktif menggunakan Tableau dan Metabase untuk memantau KPI 50+ gerai ritel.
* Melakukan cohort analysis dan churn prediction menggunakan Python (Pandas, Scikit-Learn) yang menurunkan churn rate sebesar 14%.
* Mengoptimalkan query BigQuery SQL dan ETL pipeline harian, mempercepat waktu pelaporan manajemen dari 4 jam menjadi 30 menit.

Junior Data Analyst - Finansial Cerdas Sejahtera (2020 - 2022)
* Mengumpulkan, membersihkan, dan menganalisis data transaksi nasabah lebih dari 100.000 records per hari.
* Membuat laporan visualisasi performa portofolio investasi bulanan untuk jajaran direksi.
* Membantu otomatisasi pelaporan berkala menggunakan skrip Python dan Google Sheets API.

RIWAYAT PENDIDIKAN
Sarjana Statistika - Institut Teknologi Bandung (ITB) (2016 - 2020)
* IPK: 3.75 / 4.00
* Skripsi: Penerapan Algoritma Random Forest dalam Klasifikasi Risiko Kredit

KEAHLIAN & KOMPETENSI
* Bahasa & Alat: Python (Pandas, NumPy, Matplotlib, Seaborn), SQL, R, Tableau, Power BI, Excel Advanced
* Database: Google BigQuery, PostgreSQL, MySQL
* Metodologi: A/B Testing, Predictive Modeling, Time Series Forecasting, ETL Pipeline
"""
    page.insert_textbox(fitz.Rect(50, 40, 545, 780), text, fontsize=10, fontname="helv")
    doc.save("data/sample_cvs/cv_02_ats_standard_id.pdf")
    doc.close()

# 3. Two-Column Modern Layout
def create_cv_03():
    doc = fitz.open()
    page = doc.new_page()
    # Left column (sidebar): x=40 to 180
    sidebar_text = """KONTAK
budi.santoso@email.com
+62 811-2233-4455
Jakarta Selatan, ID

KEAHLIAN
* React.js / Next.js
* TypeScript / JS
* Tailwind CSS
* Redux Toolkit
* REST & GraphQL
* Jest / Cypress
* Git & CI/CD

PENDIDIKAN
S1 Sistem Informasi
Univ Bina Nusantara
2017 - 2021 | IPK 3.65

BAHASA
* Bahasa Indonesia (Native)
* English (Professional)
"""
    # Right column (main): x=200 to 550
    main_text = """BUDI SANTOSO
Frontend Web Developer

TENTANG SAYA
Frontend Engineer berorientasi pengguna dengan pengalaman 3+ tahun mengembangkan aplikasi web responsif dan ramah aksesibilitas. Berdedikasi menghadirkan pengalaman antarmuka yang mulus dan performa render cepat.

PENGALAMAN KERJA
Frontend Lead - Inovasi Solusi Digital (2022 - Sekarang)
* Memimpin tim 4 developer frontend dalam pembuatan dashboard SaaS multi-tenant berbasis Next.js 14 dan TypeScript.
* Meningkatkan Core Web Vitals (LCP dan CLS) aplikasi hingga mencapai skor 96/100 pada Google Lighthouse.
* Menerapkan Design System perusahaan menggunakan Tailwind CSS dan Storybook untuk menjaga konsistensi UI di 5 produk web.

Frontend Developer - TokoOnline Jaya (2021 - 2022)
* Mengembangkan modul checkout dan integrasi payment gateway (Midtrans, Xendit) dengan keamanan tinggi.
* Mengurangi bundle size web aplikasi sebesar 35% melalui code-splitting dan dynamic imports.
* Berkolaborasi erat dengan tim UI/UX Designer untuk menerjemahkan wireframe Figma menjadi komponen siap produksi.

PROYEK UNGGULAN
* E-Commerce Multi-Vendor: Platform belanja online responsif dengan fitur real-time cart dan push notifications.
* Healthcare Booking Portal: Portal reservasi dokter dan konsultasi telemedicine dengan 50k pengguna aktif.
"""
    # Draw a subtle vertical separator line
    page.draw_line(fitz.Point(190, 40), fitz.Point(190, 780), color=(0.8, 0.8, 0.8), width=1)
    page.insert_textbox(fitz.Rect(40, 40, 180, 780), sidebar_text, fontsize=9, fontname="helv")
    page.insert_textbox(fitz.Rect(205, 40, 555, 780), main_text, fontsize=10, fontname="helv")
    doc.save("data/sample_cvs/cv_03_two_column_modern.pdf")
    doc.close()

# 4. Two-Column Reversed (Main on left, sidebar on right)
def create_cv_04():
    doc = fitz.open()
    page = doc.new_page()
    main_text = """MICHAEL CHANG
DevOps & Cloud Infrastructure Specialist

PROFESSIONAL SUMMARY
Experienced DevOps Engineer with 5+ years of designing, automating, and maintaining enterprise Kubernetes environments on AWS and GCP. Strong background in infrastructure as code, zero-downtime blue/green deployments, and cost optimization.

WORK EXPERIENCE
Senior DevOps Engineer - FinTech Cloud Global (2022 - Present)
* Designed and implemented GitOps deployment workflows using ArgoCD and Helm charts across 12 Kubernetes clusters.
* Implemented unified observability platform with Prometheus, Grafana, and OpenTelemetry, decreasing MTTR by 50%.
* Cut monthly cloud spend by 28% through autoscaling policies, Spot instances, and storage lifecycle management.

Cloud Operations Engineer - CyberNet Solutions (2019 - 2022)
* Built automated provisioning templates with Terraform for multi-region VPC and security architectures.
* Managed security compliance audits (ISO 27001, SOC2) by hardening Linux instances and automating vulnerability scans.
"""
    sidebar_text = """CONTACT
m.chang@clouddev.org
+62 813-5566-7788
Tangerang, ID

CORE TOOLS
* Kubernetes (EKS, GKE)
* Terraform & Ansible
* Docker & Containerd
* ArgoCD & Helm
* AWS & GCP
* Linux / Bash / Python

CERTIFICATIONS
* CKA (Certified Kubernetes Admin)
* AWS DevOps Professional
* HashiCorp Terraform Assoc
"""
    page.draw_line(fitz.Point(390, 40), fitz.Point(390, 780), color=(0.8, 0.8, 0.8), width=1)
    page.insert_textbox(fitz.Rect(40, 40, 380, 780), main_text, fontsize=10, fontname="helv")
    page.insert_textbox(fitz.Rect(405, 40, 555, 780), sidebar_text, fontsize=9, fontname="helv")
    doc.save("data/sample_cvs/cv_04_two_column_reversed.pdf")
    doc.close()

# 5. Academic Multi-page CV (3 pages)
def create_cv_05():
    doc = fitz.open()
    p1 = doc.new_page()
    t1 = """DR. ARIF BUDIMAN, Ph.D.
Associate Professor of Artificial Intelligence
Faculty of Computer Science, Universitas Gadjah Mada
Email: arif.budiman@ugm.ac.id | ORCID: 0000-0002-1234-5678

EDUCATION
* Ph.D. in Computer Science - University of Tokyo, Japan (2015 - 2019)
  Dissertation: Deep Transfer Learning for Low-Resource Natural Language Processing
* M.Sc. in Informatics - Universitas Gadjah Mada (2012 - 2014)
* B.Sc. in Computer Science - Universitas Gadjah Mada (2007 - 2011)

ACADEMIC APPOINTMENTS
* Associate Professor - Universitas Gadjah Mada (2022 - Present)
* Assistant Professor - Universitas Gadjah Mada (2019 - 2022)
* Postdoctoral Researcher - National Institute of Informatics (NII), Japan (2019)

RESEARCH INTERESTS
Natural Language Processing, Large Language Models, Multilingual Alignment, Low-Resource Indonesian Dialects, Cross-Lingual Knowledge Transfer.
"""
    p1.insert_textbox(fitz.Rect(50, 40, 545, 780), t1, fontsize=10, fontname="helv")

    p2 = doc.new_page()
    t2 = """SELECTED PEER-REVIEWED PUBLICATIONS
1. Budiman, A., Tanaka, K., & Yamamoto, M. (2023). "Cross-Lingual Knowledge Distillation for Southeast Asian Languages." IEEE Transactions on Audio, Speech, and Language Processing, 31, 1420-1433.
2. Budiman, A., & Pratama, R. (2022). "IndoBERT-Lite: Efficient Pre-trained Language Models for Indonesian Text Classification." In Proceedings of EMNLP 2022 (pp. 512-524).
3. Wijaya, D., Budiman, A., & Lee, H. (2021). "Zero-Shot Relation Extraction via Multilingual Prompting." In ACL Findings 2021 (pp. 890-901).
4. Budiman, A., & Tanaka, K. (2020). "Low-Resource Dialect Adaptation using Meta-Learning." In Proceedings of COLING 2020 (pp. 310-322).

RESEARCH GRANTS & FUNDING
* Principal Investigator: "National Foundation AI for Vernacular Indonesian Languages" - Kemendikbudristek Grant (2022 - 2025, IDR 1,500,000,000)
* Co-Investigator: "AI-Driven Healthcare Diagnostic Assistant" - LPDP RISPRO (2021 - 2023, IDR 2,100,000,000)
"""
    p2.insert_textbox(fitz.Rect(50, 40, 545, 780), t2, fontsize=10, fontname="helv")

    p3 = doc.new_page()
    t3 = """TEACHING & SUPERVISION
Graduate Courses Taught:
* CS 6101: Advanced Natural Language Processing (Fall 2020 - 2024)
* CS 6205: Deep Learning for Computer Vision and Language (Spring 2021 - 2024)

Undergraduate Courses Taught:
* CS 2102: Data Structures and Algorithms (Fall 2019 - 2023)
* CS 3201: Artificial Intelligence Fundamentals (Spring 2020 - 2024)

Doctoral Students Supervised:
* 3 Ph.D. students (in progress)
* 12 Master's theses completed

PROFESSIONAL SERVICE & EDITORIAL ROLES
* Area Chair: ACL 2023, EMNLP 2022
* Reviewer: NeurIPS, ICLR, KDD, IEEE TPAMI
* Member: Association for Computational Linguistics (ACL), IEEE Senior Member
"""
    p3.insert_textbox(fitz.Rect(50, 40, 545, 780), t3, fontsize=10, fontname="helv")
    doc.save("data/sample_cvs/cv_05_academic_multipage.pdf")
    doc.close()

# 6. Canva Image Only EN (Testing OCR Fallback!)
def create_cv_06():
    doc_temp = fitz.open()
    page = doc_temp.new_page()
    text = """JESSICA TAYLOR
Digital Marketing Specialist & SEO Lead
jessica.taylor@growthmedia.com | +62 812-8899-0011 | Jakarta

CAREER PROFILE
Creative and data-driven Digital Marketing Specialist with 5 years of experience leading omnichannel campaigns across Google Ads, Meta, and organic search channels. Successfully scaled organic web traffic by 250% for high-growth tech startups.

KEY ACHIEVEMENTS
* Managed $500K annual performance marketing budget with an average return on ad spend (ROAS) of 4.2x.
* Generated over 120,000 marketing-qualified leads (MQLs) through automated email drip funnels and targeted content strategy.
* Executed full-funnel SEO strategy resulting in 15 first-page Google ranking keywords.

WORK HISTORY
Digital Marketing Lead - GrowSmart Tech (2021 - Present)
* Directed team of content writers, designers, and media buyers across 10 concurrent product campaigns.
* Implemented conversion rate optimization (CRO) tests on landing pages, boosting conversion from 2.1% to 4.8%.

SEO & Content Specialist - BrandPulse Agency (2019 - 2021)
* Conducted keyword research, backlink building, and technical SEO site audits for 20+ clients.
* Built interactive dashboards in Google Looker Studio for client performance reporting.

SKILLS & TOOLS
* Search & Social: Google Ads, Meta Ads Manager, TikTok Ads, SEO (Ahrefs, SEMrush)
* Analytics: Google Analytics 4 (GA4), Mixpanel, Looker Studio, Hotjar
* CRM & Automation: HubSpot, Mailchimp, Zapier, Webflow
"""
    page.insert_textbox(fitz.Rect(50, 40, 545, 780), text, fontsize=10, fontname="helv")
    rasterize_pdf_page_to_image_pdf(doc_temp, "data/sample_cvs/cv_06_canva_image_only_en.pdf", dpi=180)
    doc_temp.close()

# 7. Canva Image Only ID (Testing OCR Fallback in Indonesian!)
def create_cv_07():
    doc_temp = fitz.open()
    page = doc_temp.new_page()
    text = """DEWI LESTARI
Desainer Grafis & UI/UX Specialist
Surabaya, Jawa Timur | dewi.lestari@desainkreatif.id | 0819-3344-5566

PROFIL SINGKAT
Desainer Grafis dan UI/UX kreatif dengan pengalaman 4 tahun menciptakan identitas visual merek, antarmuka aplikasi mobile, dan materi promosi digital yang menarik dan user-friendly.

PENGALAMAN KERJA
Senior Graphic & UI Designer - Studio Kreatif Nusantara (2021 - Sekarang)
* Merancang antarmuka mobile app untuk 8 klien sektor fintech dan e-commerce menggunakan Figma.
* Memimpin proses rebranding perusahaan ritel nasional mencakup logo, tipografi, dan guidelines visual.
* Berkolaborasi dengan tim engineering untuk memastikan kesesuaian aset desain saat implementasi frontend.

Graphic Designer - Agensi Media Digital (2019 - 2021)
* Memproduksi lebih dari 200 konten visual media sosial bulanan (Instagram, YouTube, TikTok banner).
* Membuat desain kemasan produk (packaging) yang meningkatkan daya tarik display produk di pasar retail.

PENDIDIKAN
S1 Desain Komunikasi Visual (DKV) - Institut Teknologi Sepuluh Nopember (ITS)
Tahun Kelulusan: 2019 | IPK: 3.68

PENGUASAAN SOFTWARE & KEAHLIAN
* Desain & Prototyping: Figma, Adobe Photoshop, Adobe Illustrator, Adobe InDesign, After Effects
* UI/UX: Wireframing, User Journey Mapping, Design System, Usability Testing
"""
    page.insert_textbox(fitz.Rect(50, 40, 545, 780), text, fontsize=10, fontname="helv")
    rasterize_pdf_page_to_image_pdf(doc_temp, "data/sample_cvs/cv_07_canva_image_only_id.pdf", dpi=180)
    doc_temp.close()

# 8. Scanned Paper CV with slight blur/noise (Image PDF)
def create_cv_08():
    doc_temp = fitz.open()
    page = doc_temp.new_page()
    text = """HENDRA KURNIAWAN
Financial Controller & Accounting Manager
Jakarta Pusat | hendra.kurniawan@akuntan.id | 0811-7788-9900

PROFESSIONAL EXPERIENCE
PT Astra Multi Niaga - Financial Controller (2020 - Present)
* Supervised full spectrum of financial operations, budgeting, tax compliance, and treasury for corporate group.
* Successfully led annual IFRS financial statement audits with Big 4 audit firms without material findings.
* Managed corporate cash flow forecasting of over IDR 50 Billion monthly.

PT Makmur Sentosa - Senior Accountant (2016 - 2020)
* Handled general ledger entries, monthly account reconciliations, and VAT/PPh tax returns.
* Implemented SAP ERP Financials module across 3 regional branches, improving monthly closing from 10 days to 4 days.

EDUCATION & LICENSES
* Bachelor of Economics in Accounting - Universitas Trisakti (2011 - 2015)
* Certified Public Accountant (CPA) Indonesia - Institut Akuntan Publik Indonesia (IAPI)
* Brevet Pajak A & B Terakreditasi
"""
    page.insert_textbox(fitz.Rect(50, 40, 545, 780), text, fontsize=10, fontname="helv")
    # Rasterize, add slight grayscale effect to simulate physical scan
    pix = page.get_pixmap(dpi=150)
    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data)).convert("L") # convert to grayscale
    # save to buffer
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    buf.seek(0)
    
    doc_scan = fitz.open()
    p_scan = doc_scan.new_page(width=page.rect.width, height=page.rect.height)
    p_scan.insert_image(page.rect, stream=buf.getvalue())
    doc_scan.save("data/sample_cvs/cv_08_scanned_cv_noisy.pdf")
    doc_scan.close()
    doc_temp.close()

# 9. Hybrid Mixed Pages: Page 1 is text, Page 2 is rasterized scanned certificate
def create_cv_09():
    doc = fitz.open()
    # Page 1: normal text CV
    p1 = doc.new_page()
    t1 = """FARHAN RAMADHAN
Cloud Security Architect | farhan.r@cybersec.id | +62 812-7766-5544

CAREER HIGHLIGHTS
* 7+ years of experience securing public cloud infrastructure (AWS/Azure) for regulated banking institutions.
* Designed Zero Trust Network Access architecture protecting over 5,000 corporate remote endpoints.
* Led incident response team mitigating advanced persistent threats (APT) and DDoS attacks.

EXPERIENCE
Lead Security Architect - Bank Digital Sejahtera (2021 - Present)
* Implemented automated cloud compliance scanning reducing policy violations by 80%.
* Conducted threat modeling, vulnerability assessments, and penetration testing on payment microservices.
"""
    p1.insert_textbox(fitz.Rect(50, 40, 545, 780), t1, fontsize=10, fontname="helv")

    # Page 2: image only (Certificate)
    doc_cert = fitz.open()
    p_cert = doc_cert.new_page()
    t_cert = """CERTIFICATE OF ACHIEVEMENT
This is to certify that
FARHAN RAMADHAN
has successfully completed the examination for
CERTIFIED INFORMATION SYSTEMS SECURITY PROFESSIONAL (CISSP)
Certification ID: CISSP-9988221 | Issue Date: November 2022
Credential Verification: verified.isc2.org/credentials"""
    p_cert.insert_textbox(fitz.Rect(60, 200, 500, 500), t_cert, fontsize=12, fontname="helv")
    pix = p_cert.get_pixmap(dpi=180)
    cert_img_bytes = pix.tobytes("png")
    doc_cert.close()

    p2 = doc.new_page()
    p2.insert_image(p2.rect, stream=cert_img_bytes)

    doc.save("data/sample_cvs/cv_09_hybrid_mixed_pages.pdf")
    doc.close()

# 10. Tabular CV (Table layout with borders)
def create_cv_10():
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "RIZKY ADITYA - CURRICULUM VITAE", fontsize=14, fontname="helv")
    page.insert_text((50, 68), "Full Stack Developer | rizky.aditya@tech.co.id | +62 813-1122-3344", fontsize=9, fontname="helv")
    
    # Table headers
    headers = [("Periode", 50, 150), ("Posisi & Perusahaan", 155, 330), ("Deskripsi & Pencapaian Utama", 335, 550)]
    y_start = 100
    page.draw_rect(fitz.Rect(50, y_start, 550, y_start + 20), color=(0.2, 0.4, 0.7), fill=(0.9, 0.94, 0.98))
    for h_text, x1, x2 in headers:
        page.insert_text((x1 + 5, y_start + 14), h_text, fontsize=9, fontname="helv")

    # Row 1
    y1 = y_start + 20
    page.draw_rect(fitz.Rect(50, y1, 550, y1 + 90), color=(0.8, 0.8, 0.8))
    page.insert_textbox(fitz.Rect(55, y1 + 5, 150, y1 + 85), "2022 - Sekarang\n(2 Tahun)", fontsize=8, fontname="helv")
    page.insert_textbox(fitz.Rect(155, y1 + 5, 330, y1 + 85), "Senior Full Stack Dev\nPT Solusi Inovasi Pratama\nJakarta", fontsize=8, fontname="helv")
    page.insert_textbox(fitz.Rect(335, y1 + 5, 545, y1 + 85), "* Mengembangkan aplikasi enterprise ERP berbasis Vue.js dan Django.\n* Membangun modul manajemen inventory yang digunakan oleh 20 cabang.\n* Meningkatkan kecepatan sinkronisasi data POS real-time.", fontsize=8, fontname="helv")

    # Row 2
    y2 = y1 + 90
    page.draw_rect(fitz.Rect(50, y2, 550, y2 + 90), color=(0.8, 0.8, 0.8))
    page.insert_textbox(fitz.Rect(55, y2 + 5, 150, y2 + 85), "2020 - 2022\n(2 Tahun)", fontsize=8, fontname="helv")
    page.insert_textbox(fitz.Rect(155, y2 + 5, 330, y2 + 85), "Junior Web Developer\nPT Kreasi Cipta Mandiri\nBandung", fontsize=8, fontname="helv")
    page.insert_textbox(fitz.Rect(335, y2 + 5, 545, y2 + 85), "* Membangun 15+ website landing page dan dashboard klien.\n* Integrasi REST API dan optimasi database MySQL.\n* Membantu migrasi server on-premise ke cloud hosting.", fontsize=8, fontname="helv")

    doc.save("data/sample_cvs/cv_10_tabular_experience.pdf")
    doc.close()

# 11. Fresh Graduate Tech CV
def create_cv_11():
    doc = fitz.open()
    page = doc.new_page()
    text = """ANINDYA PUTRI
Fresh Graduate in Computer Science | anindya.p@alumni.ac.id | 0812-4455-6677 | Yogyakarta

PROFIL
Lulusan baru Sarjana Ilmu Komputer dengan pemahaman kuat tentang algoritma pemrograman, Machine Learning, dan pengembangan aplikasi web. Antusias untuk berkontribusi sebagai Junior Software Engineer atau AI Apprentice.

PENDIDIKAN
S1 Ilmu Komputer - Universitas Gadjah Mada (UGM) (2020 - 2024)
* IPK: 3.89 / 4.00 (Cum Laude)
* Skripsi: Klasifikasi Sentimen Ulasan Produk Menggunakan Fine-Tuning IndoBERT

PENGALAMAN MAGANG & PROYEK KAMPUS
Machine Learning Intern - PT Startup Kecerdasan Buatan (Feb 2024 - Jul 2024)
* Mengumpulkan dan melakukan preprocessing pada 50.000 data teks dokumen pendaftaran.
* Membangun model ekstraksi entitas bernama (NER) untuk otomatisasi pengenalan identitas pelamar.
* Menulis unit testing dan dokumentasi API endpoint model menggunakan FastAPI.

Ketua Divisi Riset - Komunitas AI & Robotika Mahasiswa UGM (2022 - 2023)
* Mengorganisir workshop Machine Learning tingkat universitas dengan 150+ peserta.
* Membimbing 10 anggota junior dalam proyek deteksi objek computer vision.

PRESTASI & PUBLIKASI
* Juara 1 National Hackathon Innovation Competition 2023
* Sertifikasi Google Cloud Associate Cloud Engineer (2024)
"""
    page.insert_textbox(fitz.Rect(50, 40, 545, 780), text, fontsize=10, fontname="helv")
    doc.save("data/sample_cvs/cv_11_fresh_graduate_tech.pdf")
    doc.close()

# 12. Executive Leadership CV (Dense text)
def create_cv_12():
    doc = fitz.open()
    page = doc.new_page()
    text = """VICTOR PRASETYO, MBA
Chief Technology Officer / VP of Engineering
victor.prasetyo@executive.id | +62 811-0011-2233 | Jakarta, Indonesia

EXECUTIVE PROFILE
Transformational Technology Executive with 14+ years of experience leading engineering organizations of up to 120 engineers in high-growth FinTech and E-Commerce scale-ups. Expert in enterprise architecture modernization, agile engineering culture, tech budget allocation, and board-level stakeholder management.

CORE LEADERSHIP COMPETENCIES
* Engineering Leadership & Scaling | P&L & Multi-Million Dollar Tech Budget Management
* Cloud Native Architecture & Security | Product Delivery Acceleration | Enterprise Risk Mitigation

PROFESSIONAL EXPERIENCE
Vice President of Engineering - Nusantara FinTech Group (2020 - Present)
* Directed an engineering team of 115 engineers across Frontend, Backend, Data Platform, Security, and QA.
* Scaled payment infrastructure from $100M to $1.2B annual gross transaction volume (GTV) with 99.995% uptime.
* Reduced annual infrastructure overhead by $750,000 by re-architecting data pipelines and renegotiating cloud enterprise contracts.
* Instituted engineering career ladders, decreasing annualized engineer turnover from 24% to 8%.

Director of Software Engineering - TokoCepat Logistik (2016 - 2020)
* Spearheaded delivery of nationwide delivery routing engine handling 250,000 parcel dispatches daily.
* Led technological due diligence for Series B fundraising round ($45M raised).

EDUCATION
* Master of Business Administration (MBA) - INSEAD (2015 - 2016)
* Bachelor of Engineering in Electrical Engineering - Institut Teknologi Bandung (ITB) (2006 - 2010)
"""
    page.insert_textbox(fitz.Rect(50, 40, 545, 780), text, fontsize=10, fontname="helv")
    doc.save("data/sample_cvs/cv_12_executive_leadership.pdf")
    doc.close()

# 13. Dense Compact 1-Page CV
def create_cv_13():
    doc = fitz.open()
    page = doc.new_page()
    text = """KEVIN TANUWIJAYA | Mobile Developer (iOS & Android) | kevin.tan@dev.com | +62 856-7890-1234
SUMMARY: Senior Mobile Developer with 5 years experience crafting robust mobile apps with Flutter, Kotlin, and Swift.
EXPERIENCE:
Mobile Engineer Specialist - PT Aplikasi Sejahtera (2022 - Present)
- Architected Flutter multi-platform application serving 1.5M monthly active users on App Store and Google Play.
- Implemented offline-first synchronization using SQLite and WebSockets for real-time delivery status updates.
- Integrated biometrics authentication (FaceID, Fingerprint) and hardware security modules (Keystore / Keychain).
Android Developer - PT Kreasi Solusi Mobile (2019 - 2022)
- Built native Android applications in Kotlin utilizing MVVM, Coroutines, Flow, Jetpack Compose, and Retrofit.
- Decreased app crash rate from 1.8% to 0.05% through robust error handling and Sentry monitoring.
- Automated Google Play Store release process with Fastlane and GitHub Actions CI/CD.
TECHNICAL SKILLS:
- Mobile: Flutter, Dart, Android Native (Kotlin), iOS Native (Swift), Jetpack Compose
- Architecture: MVVM, Clean Architecture, BLoC Pattern, State Management (Provider, Riverpod)
- Tools: Git, Firebase (Auth, Firestore, Cloud Messaging), SQLite, Realm, REST APIs, Fastlane
EDUCATION:
- B.Comp.Sc in Computer Science, Universitas Tarumanagara (2015 - 2019) - GPA: 3.70
"""
    page.insert_textbox(fitz.Rect(40, 30, 555, 800), text, fontsize=9, fontname="helv")
    doc.save("data/sample_cvs/cv_13_dense_compact_1page.pdf")
    doc.close()

# 14. Multilingual Bilingual CV (Indonesian + English)
def create_cv_14():
    doc = fitz.open()
    page = doc.new_page()
    text = """SARAH AMALIA
Human Resources Business Partner (HRBP) & Talent Acquisition Specialist
sarah.amalia@hrconsultant.id | +62 813-7788-2211 | Tangerang Selatan

RINGKASAN KARIR / CAREER SUMMARY
Professional HRBP dengan pengalaman lebih dari 6 tahun dalam strategic talent acquisition, employee relations, dan organizational development di industri teknologi dan retail multinasional. Fluent in both English and Indonesian business communication.

PENGALAMAN PROFESIONAL / PROFESSIONAL EXPERIENCE
HR Business Partner - Global E-Commerce Tech (2021 - Present)
* Partnered with Technology and Product VPs to recruit 150+ senior software engineers, product managers, and data scientists.
* Menerapkan program evaluasi kinerja berbasis OKR (Objectives and Key Results) yang meningkatkan retensi talent kunci hingga 92%.
* Facilitated leadership coaching sessions and quarterly performance calibrations for managerial levels.

Senior Talent Acquisition Specialist - PT Sumber Daya Nusantara (2018 - 2021)
* Mengelola end-to-end recruitment lifecycle mulai dari sourcing, screening CV kandidat, interview psikologi, hingga negosiasi offering.
* Reduced average Time-to-Hire from 45 days to 24 days by standardizing ATS (Applicant Tracking System) screening pipelines.
* Mengorganisir Campus Hiring di 5 universitas terkemuka di Indonesia.

PENDIDIKAN / EDUCATION
Sarjana Psikologi (S.Psi) - Universitas Indonesia (2014 - 2018)
* Specialization in Industrial and Organizational Psychology (Psikologi Industri & Organisasi)
"""
    page.insert_textbox(fitz.Rect(50, 40, 545, 780), text, fontsize=10, fontname="helv")
    doc.save("data/sample_cvs/cv_14_multilingual_cv.pdf")
    doc.close()

# 15. Canva Creative Portfolio (Image only) - Testing OCR Fallback
def create_cv_15():
    doc_temp = fitz.open()
    page = doc_temp.new_page()
    text = """NADIA SAFIRA
Creative Content Producer & Video Editor
Instagram: @nadiacreative | nadia.safira@media.id | 0812-3344-5566 | Bali, Indonesia

ABOUT ME
Passionate Creative Producer with a flair for visual storytelling, viral social media campaigns, and brand documentary production. Over 50 Million views generated across TikTok and YouTube shorts.

NOTABLE PRODUCTION PROJECTS
* Brand Campaign 'Pesona Nusantara': Directed 3-part travel documentary series with 4M views.
* Tech Product Launch Commercial: Produced high-end 3D product motion teaser for SaaS launch.
* Podcast Studio Lead: Managed sound design, multi-cam live switching, and weekly episode editing.

TECHNICAL ARSENAL
* Editing & Motion: Adobe Premiere Pro, DaVinci Resolve Studio, After Effects, Final Cut Pro
* Audio & Sound: Adobe Audition, Logic Pro, Rode Wireless Mic Systems
* Cameras & Equipment: Sony FX3, Blackmagic Cinema 6K, DJI Ronin RS3 Gimbal, Drone Piloting (APDI Certified)

EDUCATION
Diploma in Film & Television Production - Institut Seni Indonesia (ISI) Denpasar (2018 - 2021)
"""
    page.insert_textbox(fitz.Rect(50, 40, 545, 780), text, fontsize=10, fontname="helv")
    rasterize_pdf_page_to_image_pdf(doc_temp, "data/sample_cvs/cv_15_canva_creative_portfolio.pdf", dpi=180)
    doc_temp.close()

# 16. Minimalist Clean Format
def create_cv_16():
    doc = fitz.open()
    page = doc.new_page()
    text = """FACHRI ILHAM
QA Automation Engineer | fachri.ilham@qa.id | +62 878-1122-4455 | Depok, Indonesia

PROFILE
Software QA Engineer with 4 years expertise in automated testing for web, mobile, and API microservices. Passionate about Shift-Left testing, CI/CD integration, and performance benchmarking.

EXPERIENCE
QA Automation Lead - PT Finansial Inovasi Cepat (2022 - Present)
* Built comprehensive end-to-end test automation framework using Playwright (TypeScript) and Cypress.
* Integrated automated regression test suites into GitLab CI, catching 95% of critical bugs prior to staging deployment.
* Executed performance and load testing using k6 and JMeter under 10,000 virtual concurrent users.

Quality Assurance Engineer - PT Aplikasi Mandiri (2020 - 2022)
* Authored 400+ detailed test cases and acceptance criteria in Jira and TestRail.
* Performed API automated testing using Postman Newman and Python PyTest.

SKILLS
* Automation: Playwright, Cypress, Selenium, Appium, PyTest, Jest
* Performance & API: k6, JMeter, Postman, RestAssured
* Tools & CI/CD: Git, Docker, GitLab CI, GitHub Actions, TestRail, Jira

EDUCATION
S1 Teknik Informatika - Universitas Gunadarma (2016 - 2020) | IPK: 3.62
"""
    page.insert_textbox(fitz.Rect(50, 40, 545, 780), text, fontsize=10, fontname="helv")
    doc.save("data/sample_cvs/cv_16_minimalist_clean.pdf")
    doc.close()

if __name__ == "__main__":
    create_cv_01()
    create_cv_02()
    create_cv_03()
    create_cv_04()
    create_cv_05()
    create_cv_06()
    create_cv_07()
    create_cv_08()
    create_cv_09()
    create_cv_10()
    create_cv_11()
    create_cv_12()
    create_cv_13()
    create_cv_14()
    create_cv_15()
    create_cv_16()
    print("Successfully generated 16 diverse CV PDF samples in data/sample_cvs/!")
