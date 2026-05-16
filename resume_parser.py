import fitz
import pytesseract

from pdf2image import convert_from_bytes

def extract_resume_text(file):

    text = ""

    try:

        pdf = fitz.open(
            stream=file.read(),
            filetype="pdf"
        )

        for page in pdf:

            page_text = page.get_text()

            if page_text:
                text += page_text

        if text.strip() != "":
            return text.lower()

    except:
        pass

    try:

        file.seek(0)

        images = convert_from_bytes(file.read())

        ocr_text = ""

        for image in images:

            ocr_text += pytesseract.image_to_string(image)

        return ocr_text.lower()

    except Exception as e:

        return f"OCR Error: {str(e)}"