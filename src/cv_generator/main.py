import typer
from .content import load_cv_data
from .renderer import CVRenderer
import os

app = typer.Typer()


@app.command()
def generate(
    output: str = "data/cv.pdf",
    config: str = typer.Option(
        "data", help="Path to the YAML configuration file or directory"
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
    configs = []
    if os.path.isdir(config):
        # Find all yaml files in the directory
        for f in os.listdir(config):
            if f.endswith(".yaml") or f.endswith(".yml"):
                configs.append(os.path.join(config, f))
    else:
        configs.append(config)

    for config_path in configs:
        print(f"Loading CV data from {config_path}...")
        try:
            cv = load_cv_data(config_path)
        except Exception as e:
            print(f"Error loading config {config_path}: {e}")
            continue

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

        # Determine output path
        # If processing multiple files or a directory, name output based on config filename
        current_output = output
        if len(configs) > 1 or os.path.isdir(config):
            # If output is a directory (or default), put files there
            # If output is a file path but we have multiple configs, treat dirname as output dir
            out_dir = os.path.dirname(output) if output.endswith(".pdf") else output
            if not out_dir:
                out_dir = "."

            base_name = os.path.splitext(os.path.basename(config_path))[0]
            current_output = os.path.join(out_dir, f"cv_{base_name}.pdf")

        print(f"Rendering CV to {current_output}...")
        renderer = CVRenderer(cv)
        renderer.render(current_output)
        print(f"Successfully generated CV at {current_output}")


def main():
    app()


if __name__ == "__main__":
    main()
