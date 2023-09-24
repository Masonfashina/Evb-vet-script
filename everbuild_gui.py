from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout
import sys

# Import your existing functions here
from freelancer_script import extract_text_from_pdf, analyze_freelancer

def on_submit():
    file_path_or_url = text_box.text()
    # Call your existing functions here
    # text = extract_text_from_pdf(file_path_or_url)
    # result = analyze_freelancer(text)
    # Do something with the result, like displaying it in the GUI
    label.setText(f"Analyzed: {file_path_or_url}")  # Replace with actual result

app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout()

text_box = QLineEdit()
submit_btn = QPushButton('Submit')
label = QLabel('Result will be displayed here.')

submit_btn.clicked.connect(on_submit)

layout.addWidget(text_box)
layout.addWidget(submit_btn)
layout.addWidget(label)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
