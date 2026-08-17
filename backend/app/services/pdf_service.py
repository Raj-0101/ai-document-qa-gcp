import pymupdf


class PDFService:

    @staticmethod
    def extract_text(file):

        pdf_bytes = file.file.read()

        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        pages = []

        for page in document:

            text = page.get_text(
                "text",
                sort=True
            )

            if text.strip():
                pages.append(text)

        document.close()

        return "\n".join(pages)