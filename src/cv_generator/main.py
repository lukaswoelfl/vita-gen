import typer
from .content import load_cv_data
from .renderer import CVRenderer
import os

app = typer.Typer()


@app.command()
def generate(
    output: str = "data/cv.pdf",
    config: str = typer.Option(
        "data/cv_data.yaml", help="Path to the YAML configuration file"
    ),
    image: str = typer.Option(None, help="Path to an override profile image"),
    image_width: float = typer.Option(None, help="Width of the profile image in mm"),
    signature: str = typer.Option(None, help="Path to an override signature image"),
    signature_width: float = typer.Option(
        None, help="Width of the signature image in mm"
    ),
):
    """
    Generate a CV PDF.
    """
    print(f"Loading CV data from {config}...")
    try:
        cv = load_cv_data(config)
    except Exception as e:
        print(f"Error loading config: {e}")
        return

    # Override image if provided via CLI
    if image:
        cv.person.image_path = image

    if image_width:
        cv.person.image_width = image_width

    # Override signature if provided via CLI
    if signature:
        cv.person.signature_path = signature

    if signature_width:
        cv.person.signature_width = signature_width

    # Check if image path in cv exists, if not warn
    if cv.person.image_path and not os.path.exists(cv.person.image_path):
        print(f"Warning: Image file not found at {cv.person.image_path}")

    if cv.person.signature_path and not os.path.exists(cv.person.signature_path):
        print(f"Warning: Signature file not found at {cv.person.signature_path}")

    print(f"Rendering CV to {output}...")
    renderer = CVRenderer(cv)
    renderer.render(output)
    print(f"Successfully generated CV at {output}")


def main():
    app()


if __name__ == "__main__":
    main()
