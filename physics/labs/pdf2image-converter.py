import sys
from pathlib import Path
from pdf2image import convert_from_path


def convert_pdf_to_png(pdf_path: Path):
    """
    Converts a single PDF to PNG images in the same directory.
    Returns a list of generated image paths.
    """
    generated_images = []
    try:
        pages = convert_from_path(str(pdf_path), dpi=200)
        for i, page in enumerate(pages, start=1):
            output_file = pdf_path.with_name(f"{pdf_path.stem}_page{i}.png")
            page.save(output_file, "PNG")
            generated_images.append(output_file)
            print(f"Saved: {output_file}")
    except Exception as e:
        print(f"Failed to convert {pdf_path}: {e}")
    return generated_images


def write_markdown(images, md_path: Path):
    """
    Writes a Markdown file with sequential image links.
    """
    with open(md_path, "w") as f:
        for img in images:
            f.write(f"![{img.name}]({img.name})\n\n")
    print(f"Markdown file created: {md_path}")


def recursive_convert_and_markdown(target_name: str):
    """
    Recursively searches for PDFs matching target_name from current directory,
    converts them to images, and writes a Markdown file with all pages.
    """
    cwd = Path.cwd()
    for pdf_file in cwd.rglob("*.pdf"):
        if pdf_file.stem == target_name:
            print(f"Found PDF: {pdf_file}")
            images = convert_pdf_to_png(pdf_file)
            if images:
                md_file = pdf_file.with_name(f"{pdf_file.stem}.md")
                write_markdown(images, md_file)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_png_md.py <pdf_name_without_extension>")
        sys.exit(1)

    pdf_name = sys.argv[1]
    recursive_convert_and_markdown(pdf_name)
