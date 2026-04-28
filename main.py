import os
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QFileDialog,
                             QCheckBox, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt

def collect_files_code(root_dir, extensions, output_file):
    """
    遍历指定目录及其子目录，提取指定扩展名文件的内容，写入txt文件
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for foldername, subfolders, filenames in os.walk(root_dir):
                for filename in filenames:
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in extensions:
                        file_path = os.path.join(foldername, filename)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                # 尝试读取确定是否为纯文本
                                content = f.read()
                            relative_path = os.path.relpath(file_path, root_dir)
                            out_f.write(f"《{relative_path}》\n\n")
                            out_f.write(content)
                            out_f.write("\n\n" + "-"*80 + "\n\n")
                        except Exception as e:
                            # 忽略无法读取的二进制文件或编码错误
                            pass
        return True, "提取成功！"
    except Exception as e:
        return False, str(e)


def get_available_extensions(root_dir):
    """扫描目录及其子目录，返回存在的文本文件扩展名集合"""
    found_exts = set()
    if not os.path.isdir(root_dir):
        return found_exts
    
    # 为了避免扫描太久，可以限制深度或者仅取部分
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext:
                found_exts.add(ext)
    return found_exts


class DropLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            self.setText(path)


class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(40)
        self.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(10)
        
        from PyQt6.QtGui import QPixmap, QIcon
        icon_label = QLabel()
        logo_pixmap = QPixmap("logo.png")
        if not logo_pixmap.isNull():
            icon_label.setPixmap(logo_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            icon_label.setText("")
            
        if parent:
            parent.setWindowIcon(QIcon("logo.png"))

        title_label = QLabel("代码收集器")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        
        btn_min = QPushButton("-")
        btn_min.setFixedSize(30, 30)
        btn_min.clicked.connect(self.parent_window.showMinimized)
        
        btn_close = QPushButton("×")
        btn_close.setFixedSize(30, 30)
        btn_close.clicked.connect(self.parent_window.close)
        
        for btn in (btn_min, btn_close):
            btn.setStyleSheet("QPushButton { border: none; border-radius: 4px; font-size: 16px; font-weight: bold; background: transparent; color: #555; } QPushButton:hover { background: rgba(0,0,0,0.1); }")
        btn_close.setStyleSheet("QPushButton { border: none; border-radius: 4px; font-size: 16px; font-weight: bold; background: transparent; color: #555; } QPushButton:hover { background: #ff4d4f; color: white; }")
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(btn_min)
        layout.addWidget(btn_close)
        
        self._is_tracking = False
        self._start_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_tracking = True
            self._start_pos = event.globalPosition().toPoint() - self.parent_window.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._is_tracking:
            self.parent_window.move(event.globalPosition().toPoint() - self._start_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_tracking = False
            event.accept()

class CodeCollectorApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # 预定义的分类与对应拓展名
        self.common_exts_metadata = {
            "🐍 Python (.py)": { "exts": [".py"] },
            "⚙️ C/C++ (.c, .cpp, .h)": { "exts": [".c", ".cpp", ".cc", ".h", ".hpp"] },
            "☕ Java (.java)": { "exts": [".java"] },
            "🟨 JavaScript (.js, .jsx)": { "exts": [".js", ".jsx", ".mjs"] },
            "🟦 TypeScript (.ts, .tsx)": { "exts": [".ts", ".tsx"] },
            "🌐 HTML/CSS (.html, .css)": { "exts": [".html", ".htm", ".css", ".scss", ".sass", ".less"] },
            "🐹 Go (.go)": { "exts": [".go"] },
            "🦀 Rust (.rs)": { "exts": [".rs"] },
            "🟣 C# (.cs)": { "exts": [".cs"] },
            "🐘 PHP (.php)": { "exts": [".php"] },
            "💎 Ruby (.rb)": { "exts": [".rb"] },
            "🦅 Swift (.swift)": { "exts": [".swift"] },
            "🟣 Kotlin (.kt)": { "exts": [".kt"] },
            "🐚 Shell/Bash (.sh, .bat)": { "exts": [".sh", ".bat", ".cmd"] },
            "🟩 Vue/Svelte (.vue, .svelte)": { "exts": [".vue", ".svelte"] },
            "📝 Markdown (.md)": { "exts": [".md", ".markdown"] },
            "📄 JSON/XML (.json, .xml)": { "exts": [".json", ".xml"] },
            "📄 YAML/TOML (.yaml, .toml)": { "exts": [".yaml", ".yml", ".toml"] },
            "📝 Text (.txt)": { "exts": [".txt"] },
        }
        
        self.checkboxes = {}
        
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        from PyQt6.QtGui import QColor
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(960, 640)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 0)
        
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(15, 15, 15, 15)
        
        self.main_container = QWidget()
        self.main_container.setObjectName("MainContainer")
        self.main_container.setGraphicsEffect(shadow)
        outer_layout.addWidget(self.main_container)
        
        self.layout_main = QVBoxLayout(self.main_container)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setSpacing(0)
        
        self.title_bar = TitleBar(self)
        self.layout_main.addWidget(self.title_bar)
        
        content_hbox = QHBoxLayout()
        self.layout_main.addLayout(content_hbox)
        
        content_wrapper = QWidget()
        content_wrapper.setObjectName("ContentWrapper")
        content_wrapper.setStyleSheet("QWidget#ContentWrapper { background: transparent; }")
        self.layout_content = QVBoxLayout(content_wrapper)
        self.layout_content.setContentsMargins(20, 5, 20, 20)
        self.layout_content.setSpacing(12)
        
        self.initUI()
        content_hbox.addWidget(content_wrapper, 7)
        content_hbox.addStretch(3)
        
        self.applyStyle()

    def create_card(self, title, desc, icon):
        card = QWidget()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(8)
        
        header_layout = QHBoxLayout()
        lbl_title = QLabel(f"{icon} {title}")
        lbl_title.setObjectName("CardTitle")
        lbl_desc = QLabel(desc)
        lbl_desc.setObjectName("CardDesc")
        
        header_layout.addWidget(lbl_title)
        header_layout.addWidget(lbl_desc)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        return card, layout

    def initUI(self):
        # 1. 目标目录
        self.card_dir, layout_dir = self.create_card("要遍历的目录", "可手动输入、浏览或将文件夹拖放至此处", "📁")
        dir_input_layout = QHBoxLayout()
        self.dir_input = DropLineEdit()
        self.dir_input.setPlaceholderText("请输入目录路径或拖放文件夹到此处")
        self.dir_input.textChanged.connect(self.on_dir_changed)
        btn_browse_dir = QPushButton("📁 选择目录")
        btn_browse_dir.setObjectName("BrowseBtn")
        btn_browse_dir.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_browse_dir.clicked.connect(self.browse_dir)
        dir_input_layout.addWidget(self.dir_input)
        dir_input_layout.addWidget(btn_browse_dir)
        layout_dir.addLayout(dir_input_layout)
        self.layout_content.addWidget(self.card_dir)

        # 2. 输出目录
        self.card_out, layout_out = self.create_card("输出文件夹", "默认为目标目录，也可自定义输出目录", "📁")
        out_input_layout = QHBoxLayout()
        self.out_input = QLineEdit()
        self.out_input.setPlaceholderText("请输入输出文件夹路径")
        btn_browse_out = QPushButton("📁 选择输出文件夹")
        btn_browse_out.setObjectName("BrowseBtn")
        btn_browse_out.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_browse_out.clicked.connect(self.browse_out)
        out_input_layout.addWidget(self.out_input)
        out_input_layout.addWidget(btn_browse_out)
        layout_out.addLayout(out_input_layout)
        self.layout_content.addWidget(self.card_out)

        # 3. 常见文件类型
        self.card_ext, layout_ext = self.create_card("常见文件类型", "(请先选择遍历目录以扫描可用类型)", "🏷️")
        
        self.ext_grid = QGridLayout()
        self.ext_grid.setSpacing(10)
        self.ext_grid.setContentsMargins(0, 5, 0, 0)
        layout_ext.addLayout(self.ext_grid)
        self.layout_content.addWidget(self.card_ext)
        
        lbl_empty = QLabel("请先选择上方「要遍历的目录」以扫描其中包含的文件类型...")
        lbl_empty.setObjectName("CardDesc")
        lbl_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ext_grid.addWidget(lbl_empty, 0, 0, 1, 3)
        self.empty_label = lbl_empty

        # 4. 其他类型
        card_custom, layout_custom = self.create_card("其他文件后缀名", "(可选) 例如: .md .txt .json (空格分隔)", "🏷️")
        self.custom_ext_input = QLineEdit()
        self.custom_ext_input.setPlaceholderText("在此手动输入后缀名...")
        layout_custom.addWidget(self.custom_ext_input)
        self.layout_content.addWidget(card_custom)

        self.layout_content.addStretch()

        # 5. 执行按钮
        btn_run = QPushButton("▶ 开始提取代码")
        btn_run.setObjectName("RunButton")
        btn_run.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_run.clicked.connect(self.run_extraction)
        self.layout_content.addWidget(btn_run)

    def applyStyle(self):
        bg_path = os.path.abspath("background.png").replace("\\", "/")
        self.setStyleSheet(f"""
            QWidget#MainContainer {{
                background-color: white;
                border-image: url({bg_path}) 0 0 0 0 stretch stretch;
                border-radius: 12px;
            }}
            QWidget#Card {{
                background-color: rgba(255, 255, 255, 0.88);
                border: 1px solid rgba(221, 236, 250, 0.9);
                border-radius: 10px;
            }}
            QLabel#CardTitle {{
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
            }}
            QLabel#CardDesc {{
                color: #7f8c8d;
                font-size: 12px;
            }}
            QLineEdit {{
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                color: #333;
            }}
            QLineEdit:focus {{
                border: 1px solid #3b82f6;
                background: white;
            }}
            QPushButton#BrowseBtn {{
                background: transparent;
                border: 1px solid #4379FA;
                color: #4379FA;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton#BrowseBtn:hover {{
                background: rgba(67, 121, 250, 0.1);
            }}
            QPushButton#RunButton {{
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton#RunButton:hover {{
                background: #2563eb;
            }}
            QCheckBox {{
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #e1e8f2;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 13px;
                color: #334155;
            }}
            QCheckBox:hover {{
                border: 1px solid #93c5fd;
                background: white;
            }}
        """)

    def browse_dir(self):
        d = QFileDialog.getExistingDirectory(self, "选择要遍历的目录")
        if d:
            self.dir_input.setText(d)

    def browse_out(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if d:
            self.out_input.setText(d)

    def on_dir_changed(self):
        target_dir = self.dir_input.text().strip()
        
        for i in reversed(range(self.ext_grid.count())): 
            widget = self.ext_grid.itemAt(i).widget()
            if widget is not None: 
                widget.setParent(None)
        self.checkboxes.clear()

        card_desc = self.card_ext.findChild(QLabel, "CardDesc")

        if not target_dir or not os.path.isdir(target_dir):
            if card_desc: card_desc.setText("(请先选择有效目录)")
            self.empty_label = QLabel("无效或未选择的目录，无法扫描...")
            self.empty_label.setObjectName("CardDesc")
            self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ext_grid.addWidget(self.empty_label, 0, 0, 1, 3)
            return

        if card_desc: card_desc.setText("(正在扫描...)")
        QApplication.processEvents()

        available_exts = get_available_extensions(target_dir)
        matched_categories = {}
        for name, data in self.common_exts_metadata.items():
            intersection = set(data["exts"]).intersection(available_exts)
            if intersection:
                matched_categories[name] = data

        if card_desc: card_desc.setText("(已在目录中找到以下文本代码类型)")

        if not matched_categories:
            self.empty_label = QLabel("该目录中未找到常见的代码/文本类型，可使用下方自定义后缀名功能。")
            self.empty_label.setObjectName("CardDesc")
            self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ext_grid.addWidget(self.empty_label, 0, 0, 1, 3)
            return

        row, col = 0, 0
        for name, data in matched_categories.items():
            cb = QCheckBox(name)
            self.checkboxes[name] = cb
            self.ext_grid.addWidget(cb, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def run_extraction(self):
        target_dir = self.dir_input.text().strip()
        out_dir = self.out_input.text().strip()
        custom_exts = self.custom_ext_input.text().strip()

        if not target_dir or not os.path.isdir(target_dir):
            QMessageBox.warning(self, "错误", "请选择有效的遍历目录！")
            return

        out_dir = out_dir if out_dir else target_dir
        if not os.path.isdir(out_dir):
            try:
                os.makedirs(out_dir)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法创建输出文件夹: {e}")
                return

        extensions = set()
        for name, cb in self.checkboxes.items():
            if cb.isChecked():
                exts = self.common_exts_metadata[name]["exts"]
                extensions.update(exts)
        
        if custom_exts:
            for ext in custom_exts.split():
                ext = ext.strip().lower()
                if not ext.startswith('.'):
                    ext = '.' + ext
                extensions.add(ext)

        if not extensions:
            QMessageBox.warning(self, "错误", "请至少勾选或输入一种文件后缀名！")
            return

        out_file = os.path.join(out_dir, "All_Code.txt")
        success, msg = collect_files_code(target_dir, extensions, out_file)
        
        if success:
            QMessageBox.information(self, "成功", f"文件内容已成功写入:\n{out_file}")
        else:
            QMessageBox.critical(self, "失败", f"提取时发生错误:\n{msg}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ex = CodeCollectorApp()
    ex.show()
    sys.exit(app.exec())