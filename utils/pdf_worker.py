from PySide6.QtCore import QThread, Signal
from utils.pdf_operations import (
    merge_pdfs, split_pdf, manage_pages, compress_pdf, repair_pdf,
    ocr_pdf, convert_jpg_to_pdf, convert_office_to_pdf,
    convert_pdf_to_images, convert_pdf_to_word,
    rotate_pdf, crop_pdf, add_watermark, add_page_numbers,
    protect_pdf, unlock_pdf, redact_pdf, compare_pdfs
)

class PdfWorker(QThread):
    finished_signal = Signal(bool, str) # Emits (success, message_or_path)

    def __init__(self, operation_type, params):
        super().__init__()
        self.operation_type = operation_type
        self.params = params

    def run(self):
        try:
            success = False
            msg = "작업 완료"

            if self.operation_type == "merge":
                success = merge_pdfs(self.params["file_paths"], self.params["output_path"])
                msg = f"성공적으로 병합되어 저장되었습니다:\n{self.params['output_path']}"
                
            elif self.operation_type == "split":
                success = split_pdf(self.params["file_path"], self.params["output_dir"], self.params["split_ranges"])
                msg = f"성공적으로 분할되어 폴더에 저장되었습니다:\n{self.params['output_dir']}"
                
            elif self.operation_type == "manage_pages":
                success = manage_pages(
                    self.params["file_path"], 
                    self.params["output_path"], 
                    self.params["page_numbers"], 
                    self.params["action"]
                )
                msg = f"페이지 처리 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "compress":
                success = compress_pdf(self.params["file_path"], self.params["output_path"])
                msg = f"압축 최적화 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "repair":
                success = repair_pdf(self.params["file_path"], self.params["output_path"])
                msg = f"문서 복구 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "ocr":
                success = ocr_pdf(self.params["file_path"], self.params["output_path"], self.params.get("lang", "kor+eng"))
                msg = f"OCR 및 검색 가능한 PDF 변환 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "convert_images_to_pdf":
                success = convert_jpg_to_pdf(self.params["image_paths"], self.params["output_path"])
                msg = f"이미지 PDF 변환 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "convert_office_to_pdf":
                success = convert_office_to_pdf(self.params["file_path"], self.params["output_dir"])
                msg = f"오피스 문서 PDF 변환 완료."
                
            elif self.operation_type == "convert_pdf_to_images":
                success = convert_pdf_to_images(self.params["file_path"], self.params["output_dir"], self.params.get("img_format", "png"))
                msg = f"PDF 페이지 이미지 파일 변환 완료:\n{self.params['output_dir']}"
                
            elif self.operation_type == "convert_pdf_to_word":
                success = convert_pdf_to_word(self.params["file_path"], self.params["output_path"])
                msg = f"Word 문서 변환 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "rotate":
                success = rotate_pdf(self.params["file_path"], self.params["output_path"], self.params["angle"])
                msg = f"회전 적용 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "crop":
                success = crop_pdf(
                    self.params["file_path"], 
                    self.params["output_path"], 
                    self.params["left"], self.params["right"], 
                    self.params["top"], self.params["bottom"]
                )
                msg = f"크롭 영역 분할 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "watermark":
                success = add_watermark(
                    self.params["file_path"], 
                    self.params["output_path"], 
                    self.params["text"], 
                    self.params.get("opacity", 0.3), 
                    self.params.get("font_size", 36), 
                    self.params.get("angle", 45)
                )
                msg = f"워터마크 삽입 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "page_numbers":
                success = add_page_numbers(
                    self.params["file_path"], 
                    self.params["output_path"], 
                    self.params.get("format_str", "Page {num} of {total}"), 
                    self.params.get("position", "bottom_center")
                )
                msg = f"페이지 번호 생성 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "protect":
                success = protect_pdf(self.params["file_path"], self.params["output_path"], self.params["password"])
                msg = f"보안 암호 설정 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "unlock":
                success = unlock_pdf(self.params["file_path"], self.params["output_path"], self.params["password"])
                msg = f"보안 암호 해제 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "redact":
                success = redact_pdf(self.params["file_path"], self.params["output_path"], self.params["search_terms"])
                msg = f"영구 텍스트 검열 마스킹 완료:\n{self.params['output_path']}"
                
            elif self.operation_type == "compare":
                diff_found, report_path = compare_pdfs(self.params["file1"], self.params["file2"], self.params["output_dir"])
                success = True
                msg = f"비교 보고서 및 이미지 추출 완료:\n{report_path}"
                if diff_found:
                    msg += "\n(두 파일 간의 텍스트가 다른 페이지가 감지되었습니다.)"
                else:
                    msg += "\n(두 파일이 완전히 동일합니다.)"
                    
            self.finished_signal.emit(success, msg)
            
        except Exception as e:
            self.finished_signal.emit(False, str(e))
