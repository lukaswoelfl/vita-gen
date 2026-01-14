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
    type: str = typer.Option(
        "both", help="Type of document to generate: cv, cover_letter, or both"
    ),
):
    """
    Generate a CV PDF and/or Cover Letter.
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
        print(f"Loading data from {config_path}...")
        try:
            cv_object = load_cv_data(config_path)
        except Exception as e:
            print(f"Error loading config {config_path}: {e}")
            continue

        # Override image if provided via CLI
        if image:
            cv_object.person.image_path = image

        if image_width:
            cv_object.person.image_width = image_width

        # Override signature if provided via CLI
        if signature:
            cv_object.person.signature_path = signature

        if signature_width:
            cv_object.person.signature_width = signature_width

        # Check if assets exist
        if cv_object.person.image_path and not os.path.exists(
            cv_object.person.image_path
        ):
            print(f"Warning: Image file not found at {cv_object.person.image_path}")

        if cv_object.person.signature_path and not os.path.exists(
            cv_object.person.signature_path
        ):
            print(
                f"Warning: Signature file not found at {cv_object.person.signature_path}"
            )

        # Determine output base
        current_output = output
        if len(configs) > 1 or os.path.isdir(config):
            out_dir = os.path.dirname(output) if output.endswith(".pdf") else output
            if not out_dir:
                out_dir = "."

            base_name = os.path.splitext(os.path.basename(config_path))[0]
            current_output = os.path.join(out_dir, f"{base_name}.pdf")

        # If explicit output file defined and single config, we might need to adjust logic
        # But for simplicity, let's strictly follow convention if type!=cv

        out_dir = os.path.dirname(current_output)
        base_filename = os.path.basename(current_output)
        if base_filename.startswith("cv_"):
            base_filename = base_filename[3:]
        if base_filename.endswith(".pdf"):
            base_filename = base_filename[:-4]

        # Generate CV
        if type in ["cv", "both"]:
            cv_output = os.path.join(out_dir, f"cv_{base_filename}.pdf")
            print(f"Rendering CV to {cv_output}...")
            renderer = CVRenderer(cv_object)
            renderer.render(cv_output)
            print(f"Successfully generated CV at {cv_output}")

        # Generate Cover Letter
        if type in ["cover_letter", "both"]:
            if cv_object.cover_letter:
                from .cover_letter_renderer import CoverLetterRenderer

                cl_output = os.path.join(out_dir, f"cl_{base_filename}.pdf")
                print(f"Rendering Cover Letter to {cl_output}...")
                renderer = CoverLetterRenderer(cv_object)
                renderer.render(cl_output)
                print(f"Successfully generated Cover Letter at {cl_output}")
            elif type == "cover_letter":
                print(f"No cover letter data found in {config_path}")


def main():
    app()


if __name__ == "__main__":
    main()
