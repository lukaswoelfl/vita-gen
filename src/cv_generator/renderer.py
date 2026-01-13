from fpdf import FPDF
from .models import CV, Person, Experience, Education, SkillCategory
import os


class CVRenderer(FPDF):
    def __init__(self, cv: CV):
        super().__init__()
        self.cv = cv
        self.set_auto_page_break(auto=True, margin=15)

        # Add unicode fonts
        font_dir = os.path.join(os.path.dirname(__file__), "fonts")
        self.add_font(
            "Roboto", style="", fname=os.path.join(font_dir, "Roboto-Regular.ttf")
        )
        self.add_font(
            "Roboto", style="B", fname=os.path.join(font_dir, "Roboto-Bold.ttf")
        )
        # Use Regular for Italic if Italic not available
        self.add_font(
            "Roboto", style="I", fname=os.path.join(font_dir, "Roboto-Regular.ttf")
        )

        self.add_page()
        self.set_font("Roboto", size=11)
        self.set_draw_color(200, 200, 200)  # Light grey for lines

    def header(self):
        pass

    def render(self, output_path: str):
        self._render_header()
        self._render_contact_info()
        self._render_section_title("BERUFLICHE LAUFBAHN")
        prev_company = None
        for exp in self.cv.experiences:
            self._render_experience(exp, prev_company)
            prev_company = exp.company

        self.ln(5)
        self._render_section_title("AUSBILDUNG")
        for edu in self.cv.education:
            self._render_education(edu)

        self.ln(5)
        self._render_section_title("KENNTNISSE & SKILLS")
        self._render_skills(self.cv.skills, self.cv.languages)

        self.ln(10)
        self._render_signature()

        self.output(output_path)

    def _render_header(self):
        if self.cv.person.image_path and os.path.exists(self.cv.person.image_path):
            width = self.cv.person.image_width
            # Position image top right: Page Width - Right Margin - Image Width
            # A4 width is 210mm.
            x = 210 - self.r_margin - width
            self.image(self.cv.person.image_path, x=x, y=10, w=width)

        # Name
        self.set_font("Roboto", "B", 24)
        self.cell(0, 10, self.cv.person.name, ln=True)

        # Title
        self.set_font("Roboto", "B", 14)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, self.cv.person.title, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def _render_contact_info(self):
        self.set_font("Roboto", size=10)
        info = f"{self.cv.person.address}\n{self.cv.person.phone} | {self.cv.person.email}\n{self.cv.person.linkedin}\nGeboren am {self.cv.person.birth_date}"
        self.multi_cell(0, 5, info)
        self.ln(5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def _render_section_title(self, title: str):
        # Ensure there is enough space for the title + at least 30mm of content
        if self.get_y() + 30 > self.page_break_trigger:
            self.add_page()

        self.set_font("Roboto", "B", 16)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, title, ln=True, fill=False)
        self.ln(2)

    def _render_experience(self, exp: Experience, prev_company: str = None):
        # Check if we need a page break
        self.set_font("Roboto", size=11)
        desc_height = 0
        effective_width = (
            self.w - self.l_margin - self.r_margin - 6
        )  # Account for bullet area
        for point in exp.description:
            # Calculate height of this bullet point
            h = self.multi_cell(
                effective_width, 5, point.strip(), dry_run=True, output="HEIGHT"
            )
            desc_height += h

        # Total height: Date(6) + Title(6) + Company(6) + Description + Spacing(3) + Potential Spacer(4)
        total_height = 18 + desc_height + 3
        # Add extra height calculation for spacing if new company
        if prev_company is not None and exp.company != prev_company:
            total_height += 4

        if self.get_y() + total_height > self.page_break_trigger:
            self.add_page()

        # Add visual separation between different companies (unless top of page)
        if (
            prev_company is not None
            and exp.company != prev_company
            and self.get_y() > 30
        ):
            self.ln(4)

        self.set_font("Roboto", "B", 11)
        # Date range
        date_range = f"{exp.start_date} - {exp.end_date}"
        self.cell(0, 6, date_range, ln=True)

        # Title
        self.set_font("Roboto", "B", 12)
        self.cell(0, 6, exp.title.upper(), ln=True)

        # Company - ALWAYS PRINT
        # Removed inconsistent internal padding
        self.set_font("Roboto", "I", 11)
        self.cell(0, 6, exp.company, ln=True)
        self.ln(1)

        # Description
        self.set_font("Roboto", size=11)
        for point in exp.description:
            # Bullet point simulation
            self.set_x(self.l_margin + 2)
            self.cell(4, 5, "•")

            # Text with hanging indent
            prev_l_margin = self.l_margin
            self.l_margin += 6
            self.set_x(self.l_margin)
            self.multi_cell(0, 5, point.strip())
            self.l_margin = prev_l_margin

        self.ln(2)

    def _render_education(self, edu: Education):
        # Similar check for education if needed, but experience is more critical for length
        # Let's add it for consistency
        self.set_font("Roboto", size=11)
        details_height = 0
        effective_width = self.w - self.l_margin - self.r_margin - 6
        for detail in edu.details:
            h = self.multi_cell(
                effective_width, 5, detail.strip(), dry_run=True, output="HEIGHT"
            )
            details_height += h

        total_height = 18 + details_height + 3

        if self.get_y() + total_height > self.page_break_trigger:
            self.add_page()

        self.set_font("Roboto", "B", 11)
        date_range = f"{edu.start_date} - {edu.end_date}"
        self.cell(0, 6, date_range, ln=True)

        self.set_font("Roboto", "B", 12)
        self.cell(0, 6, edu.degree.upper(), ln=True)

        self.set_font("Roboto", "I", 11)
        self.cell(0, 6, edu.institution, ln=True)

        self.set_font("Roboto", size=11)
        for detail in edu.details:
            self.set_x(self.l_margin + 2)
            self.cell(4, 5, "•")

            # Text with hanging indent
            prev_l_margin = self.l_margin
            self.l_margin += 6
            self.set_x(self.l_margin)
            self.multi_cell(0, 5, detail.strip())
            self.l_margin = prev_l_margin

        self.ln(3)

    def _render_skills(self, skills: list[SkillCategory], languages: str):
        self.set_font("Roboto", "B", 11)
        for cat in skills:
            # Simple check for skill block height
            # Name(6) + Content(? approx 5-10) + Spacing(2)
            # Assume ~15 units
            if self.get_y() + 20 > self.page_break_trigger:
                self.add_page()

            self.cell(0, 6, cat.name, ln=True)
            self.set_font("Roboto", size=11)
            self.multi_cell(0, 5, cat.skills)
            self.ln(2)
            self.set_font("Roboto", "B", 11)

        # Languages
        if self.get_y() + 15 > self.page_break_trigger:
            self.add_page()

        self.cell(0, 6, "Sprachen", ln=True)
        self.set_font("Roboto", size=11)
        self.multi_cell(0, 5, languages)

    def _render_signature(self):
        if self.cv.person.signature_path and os.path.exists(
            self.cv.person.signature_path
        ):
            # Check for page break before signature block (Image + Line + Text)
            # Approx 15mm for signature height + 5mm spacing + 5mm for text
            block_height = (self.cv.person.signature_width / 2) + 15

            if self.get_y() + block_height > self.page_break_trigger:
                self.add_page()

            # Render signature image
            self.image(
                self.cv.person.signature_path,
                x=self.l_margin,
                y=self.get_y(),
                w=self.cv.person.signature_width,
            )

            # Move down below image
            self.ln((self.cv.person.signature_width / 2) + 2)

            # Draw line
            line_width = self.cv.person.signature_width
            self.line(
                self.l_margin, self.get_y(), self.l_margin + line_width, self.get_y()
            )

            # Add name below line
            self.ln(2)
            self.set_font("Roboto", size=10)
            self.cell(line_width, 5, self.cv.person.name, align="C", ln=True)
