import os
import fitz  # PyMuPDF
from pypdf import PdfReader, PdfWriter
import img2pdf
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pytesseract
from pdf2docx import Converter

# 1. PDF Organization Functions
def merge_pdfs(file_paths, output_path):
    writer = PdfWriter()
    for path in file_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
    return True

def split_pdf(file_path, output_dir, split_ranges):
    # split_ranges is a string like "1-3, 4, 5-6"
    reader = PdfReader(file_path)
    total_pages = len(reader.pages)
    
    # Parse ranges
    ranges = []
    for part in split_ranges.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            s_idx = int(start.strip()) - 1
            e_idx = int(end.strip())
            # Clamp index bounds
            s_idx = max(0, min(s_idx, total_pages - 1))
            e_idx = max(1, min(e_idx, total_pages))
            ranges.append((s_idx, e_idx))
        else:
            idx = int(part) - 1
            idx = max(0, min(idx, total_pages - 1))
            ranges.append((idx, idx + 1))
            
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    for idx, (start, end) in enumerate(ranges):
        writer = PdfWriter()
        for page_idx in range(start, end):
            writer.add_page(reader.pages[page_idx])
        out_name = f"{base_name}_part_{idx + 1}_{start + 1}-{end}.pdf"
        out_path = os.path.join(output_dir, out_name)
        with open(out_path, "wb") as f:
            writer.write(f)
    return True

def manage_pages(file_path, output_path, page_numbers, action="extract"):
    # page_numbers is a list of 1-based page integers, e.g. [1, 3, 5]
    reader = PdfReader(file_path)
    writer = PdfWriter()
    total_pages = len(reader.pages)
    
    target_indices = [idx - 1 for idx in page_numbers if 1 <= idx <= total_pages]
    
    if action == "extract":
        for idx in target_indices:
            writer.add_page(reader.pages[idx])
    elif action == "remove":
        for idx in range(total_pages):
            if idx not in target_indices:
                writer.add_page(reader.pages[idx])
                
    with open(output_path, "wb") as f:
        writer.write(f)
    return True

# 2. PDF Optimization Functions
def compress_pdf(file_path, output_path, quality=50):
    # PyMuPDF is extremely fast for compressing/shrinking PDFs.
    # It opens, recompresses images, and saves with garbage collection.
    doc = fitz.open(file_path)
    
    # We can save with deflate and garbage collection options to compress
    doc.save(
        output_path, 
        garbage=4, 
        deflate=True, 
        clean=True
    )
    doc.close()
    return True

def repair_pdf(file_path, output_path):
    # Open and re-save using PyMuPDF to repair broken indices
    doc = fitz.open(file_path)
    doc.save(output_path, garbage=3, clean=True)
    doc.close()
    return True

def ocr_pdf(file_path, output_path, lang="kor+eng"):
    # Render PDF pages as images, OCR them, and write text back to a searchable PDF.
    doc = fitz.open(file_path)
    pdf_writer = fitz.open() # output searchable PDF
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        # Render page to high-res image for OCR
        pix = page.get_pixmap(dpi=150)
        img_data = pix.tobytes("png")
        
        # Load image via PIL
        import io
        img = Image.open(io.BytesIO(img_data))
        
        # Use Tesseract OCR to get searchable PDF page
        pdf_page_data = pytesseract.image_to_pdf_or_hocr(img, lang=lang, extension='pdf')
        
        # Open the single-page searchable PDF in memory and insert it into output PDF
        page_doc = fitz.open("pdf", pdf_page_data)
        pdf_writer.insert_pdf(page_doc)
        page_doc.close()
        
    pdf_writer.save(output_path)
    pdf_writer.close()
    doc.close()
    return True

# 3. Convert to PDF
def convert_jpg_to_pdf(image_paths, output_path):
    # Use img2pdf to merge images to PDF without loss of quality
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(image_paths))
    return True

def convert_office_to_pdf(file_path, output_dir):
    # Headless LibreOffice converter is the standard cross-platform way.
    # It works on Linux, macOS, and Windows if LibreOffice is installed.
    import subprocess
    cmd = ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", output_dir, file_path]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0:
        return True
    else:
        # Check standard paths or raise error
        raise Exception(f"LibreOffice 실행 실패: {res.stderr.decode('utf-8', errors='ignore')}")

# 4. Convert from PDF
def convert_pdf_to_images(file_path, output_dir, img_format="png"):
    # Convert PDF to high-res JPG/PNG images natively via PyMuPDF (no poppler required!)
    doc = fitz.open(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=150)
        out_name = f"{base_name}_page_{page_num + 1}.{img_format}"
        out_path = os.path.join(output_dir, out_name)
        pix.save(out_path)
        
    doc.close()
    return True

def convert_pdf_to_word(file_path, output_path):
    # Convert PDF to docx using pdf2docx
    cv = Converter(file_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()
    return True

# 5. PDF Editing Functions
def rotate_pdf(file_path, output_path, angle):
    # angle is an integer: 90, 180, 270
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(angle)
        writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
    return True

def crop_pdf(file_path, output_path, left, right, top, bottom):
    # Crop page boundaries (expressed in percentage or points, let's use percentage: 0-100)
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        # Get bounding box coordinates
        box = page.mediabox
        width = float(box.width)
        height = float(box.height)
        
        # Calculate new crop box coordinates
        c_left = width * (left / 100.0)
        c_right = width * (1.0 - right / 100.0)
        c_bottom = height * (bottom / 100.0)
        c_top = height * (1.0 - top / 100.0)
        
        page.mediabox.left = c_left
        page.mediabox.right = c_right
        page.mediabox.top = c_top
        page.mediabox.bottom = c_bottom
        writer.add_page(page)
        
    with open(output_path, "wb") as f:
        writer.write(f)
    return True

def add_watermark(file_path, output_path, text, opacity=0.3, font_size=36, angle=45):
    # 1. Create a watermark canvas to a temporary PDF
    temp_watermark_path = "temp_watermark.pdf"
    c = canvas.Canvas(temp_watermark_path, pagesize=letter)
    
    # Save graphics state for transparency
    c.saveState()
    c.setFont("Helvetica", font_size)
    c.setFillColorRGB(0.5, 0.5, 0.5, opacity) # Gray color with opacity
    
    # Translate and rotate to center
    c.translate(300, 400)
    c.rotate(angle)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()
    
    # 2. Merge watermark onto original PDF
    reader = PdfReader(file_path)
    watermark_reader = PdfReader(temp_watermark_path)
    watermark_page = watermark_reader.pages[0]
    
    writer = PdfWriter()
    for page in reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)
        
    with open(output_path, "wb") as f:
        writer.write(f)
        
    # Clean up temp file
    if os.path.exists(temp_watermark_path):
        os.remove(temp_watermark_path)
    return True

def add_page_numbers(file_path, output_path, format_str="Page {num} of {total}", position="bottom_center"):
    # position is one of: bottom_center, bottom_right, top_center, top_right
    reader = PdfReader(file_path)
    total_pages = len(reader.pages)
    
    # We create a multi-page PDF overlay with page numbers
    temp_overlay_path = "temp_overlay.pdf"
    c = canvas.Canvas(temp_overlay_path, pagesize=letter)
    
    for page_num in range(1, total_pages + 1):
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(0.3, 0.3, 0.3)
        text = format_str.format(num=page_num, total=total_pages)
        
        # Calculate coords (assume letter page size: 612x792 pt)
        if position == "bottom_center":
            c.drawCentredString(306, 30, text)
        elif position == "bottom_right":
            c.drawRightString(562, 30, text)
        elif position == "top_center":
            c.drawCentredString(306, 762, text)
        elif position == "top_right":
            c.drawRightString(562, 762, text)
            
        c.showPage()
    c.save()
    
    # Merge overlay with original
    overlay_reader = PdfReader(temp_overlay_path)
    writer = PdfWriter()
    for idx, page in enumerate(reader.pages):
        page.merge_page(overlay_reader.pages[idx])
        writer.add_page(page)
        
    with open(output_path, "wb") as f:
        writer.write(f)
        
    if os.path.exists(temp_overlay_path):
        os.remove(temp_overlay_path)
    return True

# 6. PDF Security Functions
def protect_pdf(file_path, output_path, password):
    reader = PdfReader(file_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    # Encrypt the PDF
    writer.encrypt(user_password=password, owner_password=password, use_128bit=True)
    with open(output_path, "wb") as f:
        writer.write(f)
    return True

def unlock_pdf(file_path, output_path, password):
    reader = PdfReader(file_path)
    if reader.is_encrypted:
        res = reader.decrypt(password)
        if res == 0:
            raise Exception("암호 해독 실패. 비밀번호가 올바르지 않습니다.")
            
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
        
    with open(output_path, "wb") as f:
        writer.write(f)
    return True

def redact_pdf(file_path, output_path, search_terms):
    # Search terms is a list of words, e.g. ["SSN", "Ryu"]
    # We search for text on each page and apply a black mask annotation (Redaction)
    doc = fitz.open(file_path)
    
    for page in doc:
        for term in search_terms:
            if not term.strip(): continue
            # Find coordinates of text matching the term
            rects = page.search_for(term)
            for rect in rects:
                # Add redact annotation
                page.add_redact_annot(rect, fill=(0, 0, 0)) # Fill black
        # Apply redactions to destroy text pixels permanently
        page.apply_redactions()
        
    doc.save(output_path)
    doc.close()
    return True

def compare_pdfs(file1, file2, output_dir):
    # Load both documents and compare their text content page by page
    doc1 = fitz.open(file1)
    doc2 = fitz.open(file2)
    
    pages_to_compare = min(len(doc1), len(doc2))
    diff_found = False
    diff_report = []
    
    for i in range(pages_to_compare):
        text1 = doc1[i].get_text().strip()
        text2 = doc2[i].get_text().strip()
        
        if text1 != text2:
            diff_found = True
            diff_report.append(f"페이지 {i + 1} 텍스트 불일치!")
            
            # Render visual difference side-by-side or highlight
            # We save page renderings to inspect differences
            pix1 = doc1[i].get_pixmap(dpi=100)
            pix2 = doc2[i].get_pixmap(dpi=100)
            
            pix1.save(os.path.join(output_dir, f"compare_page_{i + 1}_file1.png"))
            pix2.save(os.path.join(output_dir, f"compare_page_{i + 1}_file2.png"))
            
    doc1.close()
    doc2.close()
    
    report_path = os.path.join(output_dir, "compare_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        if diff_found:
            f.write("\n".join(diff_report))
        else:
            f.write("두 PDF 문서의 텍스트 구성이 완전히 일치합니다.")
            
    return diff_found, report_path
