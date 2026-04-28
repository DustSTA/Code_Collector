[中文](README.md) | [English](README_en.md)

# Code Collector

A graphical user interface tool developed with PyQt6, mainly used to recursively traverse specified directories and extract the contents of various code and text files, merging them into a single `.txt` file (default output is `All_Code.txt`). This is extremely useful for project archiving, code review, or providing context for Large Language Models (LLMs) like ChatGPT or Claude.

---

## 🧩 Core Features

- **🎨 Modern GUI**: Simple and clear PyQt6 interface, say goodbye to typing complex parameters in the command line.
- **📁 Drag and Drop Support**: Directly drag the target folder into the input box to quickly lock the path.
- **🔍 Smart Type Scanning**: After selecting a directory, the application will automatically scan and find the common code file types actually present in that directory, and display the relevant checkboxes on demand.
- **✅ Rich Multi-language Support**: Natively supports archiving Python, C/C++, Java, JS/TS, HTML/CSS, Go, Rust, C#, PHP, Vue, Markdown, and a variety of other main languages and configuration files.
- **🏷️ Custom Extensions**: In addition to predefined common languages, it allows manually inputting any specific file suffixes you want to extract (e.g., `.ini`, `.env`).
- **📂 Custom Output Directory**: Output the generated large text to the target directory or flexibly specify any custom save location.
- **📝 Elegant Content Formatting**: It automatically adds a relative path title for each file when writing (e.g., `《src/app.py》`) along with line separators. The content layout is clear and readable.

---

## 📦 Dependencies

The project runs on Python and requires the `PyQt6` dependency:

```bash
pip install PyQt6
```

---

## 🚀 Usage

1. Install Python 3 (Python 3.8+ recommended);
2. Install the necessary `PyQt6` library;
3. Run the code:

```bash
python main.py
```

4. **GUI Operation Steps**:
   - **Target Directory**: Click "Browse" or directly drag the local folder you want to collect into the input area.
   - **Output Directory**: Choose where to store the generated text file (if left blank, it defaults to the Target Directory).
   - **Select Code Types**: Wait for the directory scan to complete, then check the types you want to extract; if there is no corresponding checkbox, you can supplement it in the "Other file extensions" below.
   - **Start Extraction**: Click the execution button and wait for the system to finish extracting automatically. The result will be a long text file named `All_Code.txt` in the output directory.

---

## 🎯 Common Scenarios

- Need to send your massive project code to ChatGPT/Claude for AI assistance, but manual copy-pasting is too tedious? Use this tool to pack all the target source code for AI in one click!
- Unified source code snapshot archiving and organization for huge personal projects.
- Extracting specific language snippets for project documentation or offline reading backups.
