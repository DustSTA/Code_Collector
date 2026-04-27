import os
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QFileDialog,
                             QCheckBox, QGroupBox, QGridLayout, QMessageBox,
                             QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

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


class CodeCollectorApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # 预定义的分类与对应拓展名
        self.common_exts_metadata = {
            "Python (.py)": { "exts": [".py"] },
            "C/C++ (.c, .cpp, .h)": { "exts": [".c", ".cpp", ".cc", ".h", ".hpp"] },
            "Java (.java)": { "exts": [".java"] },
            "JavaScript (.js, .jsx)": { "exts": [".js", ".jsx", ".mjs"] },
            "TypeScript (.ts, .tsx)": { "exts": [".ts", ".tsx"] },
            "HTML/CSS (.html, .css)": { "exts": [".html", ".htm", ".css", ".scss", ".sass", ".less"] },
            "Go (.go)": { "exts": [".go"] },
            "Rust (.rs)": { "exts": [".rs"] },
            "C# (.cs)": { "exts": [".cs"] },
            "PHP (.php)": { "exts": [".php"] },
            "Ruby (.rb)": { "exts": [".rb"] },
            "Swift (.swift)": { "exts": [".swift"] },
            "Kotlin (.kt)": { "exts": [".kt"] },
            "Shell/Bash (.sh, .bat)": { "exts": [".sh", ".bat", ".cmd"] },
            "Vue/Svelte (.vue, .svelte)": { "exts": [".vue", ".svelte"] },
            "Markdown (.md)": { "exts": [".md", ".markdown"] },
            "JSON/XML (.json, .xml)": { "exts": [".json", ".xml"] },
            "YAML/TOML (.yaml, .toml)": { "exts": [".yaml", ".yml", ".toml"] },
            "Text (.txt)": { "exts": [".txt"] },
        }
        
        self.checkboxes = {}
        self.initUI()
        self.applyStyle()

    def initUI(self):
        self.setWindowTitle('代码收集器')
        self.resize(750, 550)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # 1. 目标目录 (支持拖拽)
        dir_block = QVBoxLayout()
        dir_block.setSpacing(8)
        
        dir_label_layout = QHBoxLayout()
        dir_icon_label = QLabel("🔄 要遍历的目录")
        dir_icon_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
        dir_desc_label = QLabel("可手动输入、浏览或将文件夹拖放至此处")
        dir_desc_label.setStyleSheet("color: #888; font-size: 12px;")
        dir_label_layout.addWidget(dir_icon_label)
        dir_label_layout.addWidget(dir_desc_label)
        dir_label_layout.addStretch()
        dir_block.addLayout(dir_label_layout)

        dir_input_layout = QHBoxLayout()
        self.dir_input = DropLineEdit()
        self.dir_input.setPlaceholderText("请输入目录路径或拖放文件夹到此处")
        self.dir_input.textChanged.connect(self.on_dir_changed)
        btn_browse_dir = QPushButton("📂 选择目录")
        btn_browse_dir.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_browse_dir.clicked.connect(self.browse_dir)
        dir_input_layout.addWidget(self.dir_input)
        dir_input_layout.addWidget(btn_browse_dir)
        dir_block.addLayout(dir_input_layout)
        
        main_layout.addLayout(dir_block)

        # 2. 输出文件夹
        out_block = QVBoxLayout()
        out_block.setSpacing(8)
        
        out_label_layout = QHBoxLayout()
        out_icon_label = QLabel("📁 输出文件夹")
        out_icon_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
        out_desc_label = QLabel("默认为目标目录，也可自定义输出目录")
        out_desc_label.setStyleSheet("color: #888; font-size: 12px;")
        out_label_layout.addWidget(out_icon_label)
        out_label_layout.addWidget(out_desc_label)
        out_label_layout.addStretch()
        out_block.addLayout(out_label_layout)

        out_input_layout = QHBoxLayout()
        self.out_input = QLineEdit()
        self.out_input.setPlaceholderText("请输入输出文件夹路径")
        btn_browse_out = QPushButton("📂 选择输出文件夹")
        btn_browse_out.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_browse_out.clicked.connect(self.browse_out)
        out_input_layout.addWidget(self.out_input)
        out_input_layout.addWidget(btn_browse_out)
        out_block.addLayout(out_input_layout)
        
        main_layout.addLayout(out_block)

        # 3. 常见文件类型 (动态生成)
        self.ext_group = QGroupBox("</> 常见文件类型 (请先选择遍历目录以扫描可用类型)")
        self.ext_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; color: #333; border: 1px solid #ddd; border-radius: 8px; margin-top: 5px; padding-top: 30px; padding-bottom: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; top: 0px; }")
        
        self.ext_grid = QGridLayout()
        self.ext_grid.setSpacing(12)
        self.ext_grid.setContentsMargins(15, 10, 15, 10)
        self.ext_group.setLayout(self.ext_grid)
        main_layout.addWidget(self.ext_group)
        
        # 初始化时显示提示文本
        self.empty_label = QLabel("请先选择上方「要遍历的目录」以扫描其中包含的文件类型...")
        self.empty_label.setStyleSheet("color: #888; margin: 10px;")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ext_grid.addWidget(self.empty_label, 0, 0, 1, 3)

        # 4. 手动输入扩展名
        custom_ext_layout = QHBoxLayout()
        icon_label_custom = QLabel("🏷️ 其他文件后缀名 (可选)")
        icon_label_custom.setStyleSheet("font-weight: bold; font-size: 13px; color: #333;")
        self.custom_ext_input = QLineEdit()
        self.custom_ext_input.setPlaceholderText("例如: .md .txt .json (空格分隔)")
        custom_ext_layout.addWidget(icon_label_custom)
        custom_ext_layout.addWidget(self.custom_ext_input)
        
        custom_widget = QWidget()
        custom_widget.setLayout(custom_ext_layout)
        custom_widget.setStyleSheet("QWidget { border: 1px solid #ddd; border-radius: 8px; padding: 5px; background-color: #fafafa; } QLineEdit { border: none; background-color: transparent; } QLabel { border: none; padding-left: 10px; padding-right: 10px; }")
        main_layout.addWidget(custom_widget)

        main_layout.addStretch()

        # 5. 执行按钮
        btn_run = QPushButton("▶ 开始提取代码")
        btn_run.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_run.setObjectName("RunButton")
        btn_run.clicked.connect(self.run_extraction)
        main_layout.addWidget(btn_run)

        self.setLayout(main_layout)

    def applyStyle(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 13px;
                background-color: #fafafa;
            }
            QLineEdit:focus {
                border: 1px solid #3b82f6;
                background-color: #ffffff;
            }
            QPushButton {
                padding: 10px 15px;
                background-color: #ffffff;
                border: 1px solid #3b82f6;
                color: #3b82f6;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #eff6ff;
            }
            QPushButton#RunButton {
                background-color: #3b82f6;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border-radius: 6px;
                padding: 12px;
                margin-top: 10px;
            }
            QPushButton#RunButton:hover {
                background-color: #2563eb;
            }
            QCheckBox {
                spacing: 8px;
                padding: 8px 12px;
                border: 1px solid #eee;
                border-radius: 6px;
                background-color: #fafafa;
            }
            QCheckBox:hover {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
            }
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
        """当目录改变时，扫描目录，动态生成复选框"""
        target_dir = self.dir_input.text().strip()
        
        # 清除现有
        for i in reversed(range(self.ext_grid.count())): 
            widget = self.ext_grid.itemAt(i).widget()
            if widget is not None: 
                widget.setParent(None)
        self.checkboxes.clear()

        if not target_dir or not os.path.isdir(target_dir):
            self.ext_group.setTitle("</> 常见文件类型 (请先选择有效目录)")
            self.empty_label = QLabel("无效或未选择的目录，无法扫描...")
            self.empty_label.setStyleSheet("color: #888;")
            self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ext_grid.addWidget(self.empty_label, 0, 0, 1, 3)
            return

        self.ext_group.setTitle("</> 常见文件类型 (正在扫描...)")
        QApplication.processEvents()

        # 扫描存在的文件类型
        available_exts = get_available_extensions(target_dir)
        
        # 匹配元数据，只显示包含实际存在的拓展名的分类
        matched_categories = {}
        for name, data in self.common_exts_metadata.items():
            category_exts = data["exts"]
            # 如果该分类下有任何一个拓展名存在于扫描结果中
            intersection = set(category_exts).intersection(available_exts)
            if intersection:
                matched_categories[name] = data

        self.ext_group.setTitle("</> 常见文件类型 (已在目录中找到以下文本代码类型)")

        if not matched_categories:
            self.empty_label = QLabel("该目录中未找到常见的代码/文本类型，可使用下方自定义后缀名功能。")
            self.empty_label.setStyleSheet("color: #888;")
            self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ext_grid.addWidget(self.empty_label, 0, 0, 1, 3)
            return

        # 动态创建UI
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
    ex = CodeCollectorApp()
    ex.show()
    sys.exit(app.exec())