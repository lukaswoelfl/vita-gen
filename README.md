# vita_gen - Portfolio CV Generator

A Python-based tool to generate a professional CV/Resume in PDF format. Designed to be customizable via YAML configuration and easily deployable.

## Features
- **YAML Configuration**: All personal data and content are stored in `data/cv_data.yaml`.
- **Promotion Grouping**: Automatically groups consecutive roles at the same company to highlight career progression.
- **Unicode Support**: Uses Roboto fonts to support international characters.
- **Smart Page Breaks**: Automatically prevents splitting experience items or the signature across pages.
- **Visual Assets**:
  - **Profile Picture**: Embeds a profile picture from `data/profile_pic.png`.
  - **Signature**: Embeds a signature image from `data/signature.png` at the end of the document.

## Installation

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency management.

1.  **Clone the repository** (if applicable).
2.  **Install dependencies**:
    ```bash
    uv sync
    ```

## Configuration

1.  **Edit Data**: Modify `data/cv_data.yaml`. Below is a complete example of what this file should look like:
    ```yaml
    person:
      name: "JOHN DOE"
      title: "Software Engineer | M.Sc. Computer Science"
      address: "123 Tech Street, 12345 Innovation City"
      phone: "+49 123 4567890"
      email: john.doe@example.com
      linkedin: linkedin.com/in/johndoe/
      birth_date: "01. January 1990"
      image_path: "data/profile_pic.png"
      image_width: 32.0
      signature_path: "data/signature.png"
      signature_width: 40.0
      signature_date: "City, 05. February 2026"

    section_titles:
      experiences: "WORK EXPERIENCE"
      education: "EDUCATION"
      skills: "SKILLS & EXPERTISE"
      languages: "LANGUAGES"

    labels:
      born_on: "Born on"

    education:
      - degree: "COMPUTER SCIENCE (M.Sc.)"
        institution: "Tech University"
        start_date: "10/2018"
        end_date: "09/2020"
        details:
          - "Focus on Artificial Intelligence and Distributed Systems"
      - degree: "COMPUTER SCIENCE (B.Sc.)"
        institution: "State University"
        start_date: "10/2014"
        end_date: "09/2018"
        details:
          - "Software Engineering fundamentals and Mathematics"

    experiences:
      - title: "SENIOR SOFTWARE ENGINEER"
        company: "Tech Solutions GmbH"
        start_date: "01/2021"
        end_date: "Present"
        description:
          - "Lead development of high-performance microservices using Python and FastAPI."
          - "Architected and implemented a scalable data processing pipeline on AWS."
          - "Mentored junior developers and improved code quality through rigorous reviews."
      - title: "JUNIOR DEVELOPER"
        company: "Early Stage Startup"
        start_date: "10/2020"
        end_date: "12/2020"
        description:
          - "Developed interactive frontend components using React and TypeScript."
          - "Contributed to the backend API development and database optimization."

    skills:
      - name: "Languages & Frameworks"
        skills: "Python, Java, JavaScript, TypeScript, FastAPI, React, Node.js"
      - name: "Infrastructure & Tools"
        skills: "AWS, Docker, Kubernetes, Git, CI/CD, Terraform"

    languages: "English (Native), German (Fluent)"
    ```
2.  **Visual Assets**: Place your images in the `data/` directory or reference them from anywhere else using absolute or relative paths.

## Usage

Generate your CV by running:

```bash
uv run vita-gen
```

This will create `data/cv.pdf`.

### Combined CLI Overrides

You can override both images and their dimensions in a single command:

```bash
uv run vita-gen \
  --image custom_pic.jpg --image-width 35 \
  --signature custom_sig.png --signature-width 45
```

### Custom Profile Image

Override the profile picture from the config:

```bash
uv run vita-gen --image path/to/photo.jpg --image-width 50
```

### Custom Signature

Override the signature image and width:

```bash
uv run vita-gen --signature path/to/sig.png --signature-width 45
```

### Custom Configuration

You can specify a different configuration file:

```bash
uv run vita-gen --config path/to/my_cv.yaml
```


## Structure

-   `src/vita_gen/`: Source code.
-   `data/`: Configuration and assets (ignored by git).
-   `cv.pdf`: Generated output (ignored by git).

## License

[MIT](LICENSE)
