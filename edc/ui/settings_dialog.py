from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout
from pathlib import Path

class SettingsDialog(QDialog):
    def __init__(self, current_journal_dir: str | None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self._journal_dir = current_journal_dir or ""

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Elite Dangerous Journal Folder:"))

        row = QHBoxLayout()
        self.edit = QLineEdit(self._journal_dir)
        browse = QPushButton("Browse…")
        row.addWidget(self.edit)
        row.addWidget(browse)
        layout.addLayout(row)

        buttons = QHBoxLayout()
        save = QPushButton("Save")
        cancel = QPushButton("Cancel")
        buttons.addWidget(save)
        buttons.addWidget(cancel)
        layout.addLayout(buttons)

        browse.clicked.connect(self._browse)
        save.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)

    def _browse(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Journal Folder")
        if folder:
            self.edit.setText(folder)

    def journal_dir(self) -> str:
        return self.edit.text().strip()
