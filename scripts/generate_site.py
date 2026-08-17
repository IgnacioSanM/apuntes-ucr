from pathlib import Path
from dataclasses import dataclass
import re
import unicodedata
import shutil
import subprocess
import os

# ==========================================
# Configuración
# ==========================================
ROOT = Path(__file__).resolve().parent.parent
LATEX_DIR = ROOT / "latex" / "courses"
DOCS_DIR = ROOT / "docs"
COURSES_DOCS = DOCS_DIR / "courses"
# ==========================================
# Clase
# ==========================================
@dataclass
class Document:
    course: str
    course_slug: str
    title: str
    slug: str
    author: str
    tex_path: Path
    course_path:Path
# ==========================================
# Funciones
# ==========================================
def clean_output():

    if COURSES_DOCS.exists():
        shutil.rmtree(COURSES_DOCS)

    COURSES_DOCS.mkdir(parents=True, exist_ok=True)

    pdf_root = DOCS_DIR / "pdf"

    if pdf_root.exists():
        shutil.rmtree(pdf_root)

    pdf_root.mkdir(parents=True, exist_ok=True)
def print_header(title):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

def extract_command(text: str, command: str):

    pattern = rf"\\{command}\{{(.*?)\}}"

    match = re.search(pattern, text)

    if match:
        return match.group(1).strip()

    return ""

def slugify(text: str) -> str:
    """
    Convierte un texto a un slug.

    Ejemplos:
        Introducción a la Economía
            ↓
        introduccion_a_la_economia
    """

    # Eliminar acentos
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore").decode("utf8")

    # Minúsculas
    text = text.lower()

    # Espacios → _
    text = text.replace(" ", "_")

    return text

def read_document(tex_file: Path):

    document_folder = tex_file.parent
    course_folder = document_folder.parent

    course_slug = course_folder.name
    course_file = course_folder / "course.tex"
    if not course_file.exists():
        print(f"⚠ Se omitió {course_folder.name}: falta course.tex")
        return None
    
    course_text = course_file.read_text(encoding="utf8")
    tex_text = tex_file.read_text(encoding="utf8")

    course = extract_command(course_text, "course")
    title = extract_command(tex_text, "doctitle")
    if not title:
        title = extract_command(tex_text, "title")
    author = extract_command(tex_text, "author")
    document_slug = slugify(title)
    return Document(
        course=course,
        course_slug=course_slug,
        title=title,
        author=author,
        tex_path=tex_file,
        course_path=course_folder,
        slug=document_slug,
    )

def build_library():
    documents = []
    for tex_file in LATEX_DIR.rglob("main.tex"):

        document = read_document(tex_file)

        if document is not None:
            documents.append(document)
    library = {}
    for document in documents:

        library.setdefault(document.course, []).append(document)
    return library

def generate_markdown(library):

    for course_name, docs in library.items():

        course_slug = docs[0].course_slug

        write_course_page(
            course_slug,
            course_name,
            docs
        )

        print(f"✓ {course_name}")

def write_course_page(course_slug: str, course_name: str, docs: list[Document]):

    output_dir = COURSES_DOCS / course_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    index = output_dir / "index.md"
    name= course_slug.replace("_", " ").title()
    lines = []

    lines.append(f"# {course_name}")
    lines.append("")
    lines.append("## Documentos")
    lines.append("")

    docs = sorted(docs, key=lambda d: d.title)

    for doc in docs:

        lines.append(f"###  {doc.title}")
        lines.append("")
        lines.append(f"**Autor:** {doc.author}")
        lines.append("")
        pdf_name = doc.slug + ".pdf"
        lines.append(
            f"[Abrir {doc.title}](../../pdf/{course_slug}/{pdf_name})"
        )
        lines.append("")
        lines.append("---")
        lines.append("")

    index.write_text(
        "\n".join(lines),
        encoding="utf8"
    )

def compile_pdfs(library):

    print()
    print("=" * 60)
    print("Compilando documentos...")
    print("=" * 60)

    pdf_root = DOCS_DIR / "pdf"

    if pdf_root.exists():
        shutil.rmtree(pdf_root)

    pdf_root.mkdir(parents=True, exist_ok=True)

    for _, course_docs in library.items():

        course_slug = course_docs[0].course_slug
        course_pdf_dir = pdf_root / course_slug
        course_pdf_dir.mkdir(parents=True, exist_ok=True)

        for doc in course_docs:

            print(f"📄 {doc.title}")

            # ------------------------------------------
            # Limpiar compilaciones anteriores
            # ------------------------------------------

            subprocess.run(
                ["latexmk", "-C"],
                cwd=doc.tex_path.parent,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # ------------------------------------------
            # Compilar desde cero
            # ------------------------------------------

            result = subprocess.run(
                [
                    "latexmk",
                    "-xelatex",
                    "-shell-escape",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    doc.tex_path.name,
                ],
                cwd=doc.tex_path.parent,
            )

            # ------------------------------------------
            # Verificar que realmente exista el PDF
            # ------------------------------------------

            pdf_source = doc.tex_path.with_suffix(".pdf")

            if result.returncode != 0 or not pdf_source.exists():

                print(f"❌ Error compilando {doc.title}")
                continue

            # ------------------------------------------
            # Copiar PDF a docs/pdf
            # ------------------------------------------

            pdf_dest = course_pdf_dir / f"{doc.slug}.pdf"

            shutil.copy2(
                pdf_source,
                pdf_dest
            )

            print(f"✓ {doc.title}")

            # ------------------------------------------
            # Limpiar archivos auxiliares
            # ------------------------------------------

            subprocess.run(
                ["latexmk", "-c"],
                cwd=doc.tex_path.parent,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

def update_mkdocs(library):

    base_file = ROOT / "mkdocs_base.yml"
    output_file = ROOT / "mkdocs.yml"

    text = base_file.read_text(encoding="utf8")

    base = text.split("nav:")[0]

    lines = [base]
    lines.append("nav:")
    lines.append("  - Inicio: index.md")
    lines.append("  - Cursos:")

    for course_name, docs in sorted(library.items()):

        course_slug = docs[0].course_slug

        lines.append(
            f"      - {course_name}: courses/{course_slug}/index.md"
        )

    output_file.write_text(
        "\n".join(lines),
        encoding="utf8"
    )

def generate_homepage(library):

    index = DOCS_DIR / "index.md"

    lines = []

    lines.append("# Notas UCR")
    lines.append("")
    lines.append(
        " "
    )
    lines.append("")
    lines.append("## Cursos")
    lines.append("")

    for course_name, docs in sorted(library.items()):

        course_slug = docs[0].course_slug

        lines.append(
            f"- [{course_name}](courses/{course_slug}/index.md)"
        )

    lines.append("")
    lines.append("---")
    lines.append("")

    index.write_text(
        "\n".join(lines),
        encoding="utf8",
    )

# ==========================================
# Programa principal
# ==========================================

def main():

    clean_output()

    library = build_library()

    print_header("Biblioteca")

    compile_pdfs(library)

    print_header("Generando páginas")

    generate_markdown(library)
    generate_homepage(library)
    update_mkdocs(library)

if __name__ == "__main__":
    main()