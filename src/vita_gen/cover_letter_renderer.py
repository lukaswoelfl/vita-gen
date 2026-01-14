from fpdf import FPDF
from .models import CV
import os
from datetime import datetime


class CoverLetterRenderer(FPDF):
    def __init__(self, cv: CV):
        super().__init__()
        self.cv = cv
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(20, 10, 20)

        # Add unicode fonts
        font_dir = os.path.join(os.path.dirname(__file__), "fonts")
        self.add_font(
            "Roboto", style="", fname=os.path.join(font_dir, "Roboto-Regular.ttf")
        )
        self.add_font(
            "Roboto", style="B", fname=os.path.join(font_dir, "Roboto-Bold.ttf")
        )
        self.add_font(
            "Roboto", style="I", fname=os.path.join(font_dir, "Roboto-Regular.ttf")
        )

        self.add_page()
        self.set_draw_color(200, 200, 200)  # Light grey for lines

    def header(self):
        # We handle header manually in render to start on first page only
        pass

    def render(self, output_path: str):
        if not self.cv.cover_letter:
            print("No cover letter data found in CV configuration.")
            return

        self._render_header()
        self._render_addresses()
        self._render_date()
        self._render_subject()
        self._render_body()
        self._render_signature()

        self.output(output_path)

    def _render_header(self):
        # Similar header to CV but maybe simpler
        if self.cv.person.image_path and os.path.exists(self.cv.person.image_path):
            width = self.cv.person.image_width
            x = 210 - self.r_margin - width
            self.image(self.cv.person.image_path, x=x, y=10, w=width)

        # Sender Info (Top Left)
        self.set_y(10)
        self.set_font("Roboto", "B", 11)
        self.cell(0, 5, self.cv.person.name, ln=True)
        self.set_font("Roboto", size=9)
        self.set_text_color(100, 100, 100)

        # Split address into lines for stack
        address_parts = self.cv.person.address.split(",")
        for part in address_parts:
            self.cell(0, 4, part.strip(), ln=True)

        self.cell(0, 4, self.cv.person.email, ln=True)
        self.cell(0, 4, self.cv.person.phone, ln=True)
        self.set_text_color(0, 0, 0)

        # Reduced spacing after header but readable
        self.ln(3)

    def _render_addresses(self):
        # Recipient Address
        self.ln(3)
        self.set_font("Roboto", size=9)

        cl = self.cv.cover_letter

        self.cell(0, 4, cl.company.name, ln=True)
        if cl.company.contact_person:
            self.cell(0, 4, cl.company.contact_person, ln=True)

        # Handle multiline company address
        for line in cl.company.address.split("\n"):
            self.cell(0, 4, line.strip(), ln=True)

    def _render_date(self):
        self.ln(3)
        # Right aligned date
        date_str = self.cv.person.signature_date
        if not date_str:
            date_str = datetime.now().strftime("%d. %B %Y")

        self.cell(0, 4, date_str, align="R", ln=True)
        self.ln(3)

    def _render_subject(self):
        self.ln(2)
        self.set_font("Roboto", "B", 11)
        self.cell(0, 6, self.cv.cover_letter.title, ln=True)
        self.ln(8)

    def _render_body(self):
        self.set_font("Roboto", size=10)  # Restored to 10 (was 9)
        self.set_xy(self.l_margin, self.get_y())

        # Simple multi_cell for text body
        # Assuming text uses \n\n for paragraphs
        text = self.cv.cover_letter.text

        # Split by double newlines for paragraphs to add spacing
        paragraphs = text.split("\n\n")

        for p in paragraphs:
            self.multi_cell(0, 5, p.strip())  # Increased line height to 5 (was 4)
            self.ln(2.5)  # Increased paragraph spacing to 2.5 (was 1.5)

    def _render_signature(self):
        self.ln(5)
        self.cell(
            0,
            5,
            (
                "Best regards,"
                if "english" in self.cv.languages.lower()
                and "German" not in self.cv.languages
                else "Mit freundlichen Grüßen,"
            ),
            ln=True,
        )
        self.ln(3)

        if self.cv.person.signature_path and os.path.exists(
            self.cv.person.signature_path
        ):
            self.image(
                self.cv.person.signature_path,
                x=self.l_margin,
                y=self.get_y(),
                w=self.cv.person.signature_width,
            )
            # Match CV renderer spacing logic
            self.ln((self.cv.person.signature_width / 2) - 10)

            # Draw line
            line_width = self.cv.person.signature_width
            self.line(
                self.l_margin, self.get_y(), self.l_margin + line_width, self.get_y()
            )

            # Add name below line
            self.ln(2)
            self.set_font("Roboto", size=10)

            # Print name centered under line
            self.cell(line_width, 5, self.cv.person.name, align="C", ln=True)

        else:
            # Fallback if no signature image
            self.ln(10)
            self.cell(0, 5, self.cv.person.name, ln=True)
