import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_frontend_files_exist():
    print("Checking frontend files...")

    required_files = [
        "frontend/app.py",
        "frontend/utils.py",
        "frontend/pages/upload.py",
        "frontend/pages/analysis.py",
        "frontend/pages/clause.py",
        "frontend/pages/faq.py"
    ]

    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] Found: {file}")
        else:
            print(f"[MISSING] {file}")

def test_import_utils():
    print("\nChecking frontend.utils import...")
    try:
        from frontend.utils import save_uploaded_file, analyze_uploaded_document
        print("[OK] frontend.utils imported successfully")
    except Exception as e:
        print("[ERROR] frontend.utils import failed")
        print(e)

def test_import_pages():
    print("\nChecking frontend page imports...")

    pages = [
        "frontend.pages.upload",
        "frontend.pages.analysis",
        "frontend.pages.clause",
        "frontend.pages.faq"
    ]

    for page in pages:
        try:
            __import__(page)
            print(f"[OK] Imported: {page}")
        except Exception as e:
            print(f"[ERROR] Failed to import: {page}")
            print(e)

if __name__ == "__main__":
    print("===== Running UI Tests =====\n")

    test_frontend_files_exist()
    test_import_utils()
    test_import_pages()

    print("\n===== UI Test Finished =====")