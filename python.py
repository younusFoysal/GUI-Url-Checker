import requests
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QFileDialog, QProgressBar
from tqdm import tqdm
import threading

class URLCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("URL Checker")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        file_label = QLabel("Select File:")
        layout.addWidget(file_label)

        self.file_entry = QLineEdit()
        layout.addWidget(self.file_entry)

        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.browse_file)
        layout.addWidget(browse_button)

        check_button = QPushButton("Check URLs", self)
        check_button.clicked.connect(self.check_urls_from_file)
        layout.addWidget(check_button)

        self.result_text = QTextEdit()
        layout.addWidget(self.result_text)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar {border: 1px solid grey; border-radius: 5px; text-align: center; background-color: #C0C0C0;}"
                                        "QProgressBar::chunk {background-color: green;}")
        layout.addWidget(self.progress_bar)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.file_entry.setText(file_path)

    def check_url_status(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return f"{url} - Status Code: 200 (OK)"
            else:
                return f"{url} - Status Code: {response.status_code}"
        except requests.RequestException as e:
            return f"{url} - Error: {e}"

    def check_urls(self, urls):
        results = []
        total_urls = len(urls)
        self.progress_bar.setMaximum(total_urls)
        for i, url in enumerate(tqdm(urls, desc="Checking URLs", unit="URL")):
            result = self.check_url_status(url)
            results.append(result)
            self.progress_bar.setValue(i + 1)
        return results

    def check_urls_from_file(self):
        file_path = self.file_entry.text()
        try:
            with open(file_path, 'r') as file:
                urls = file.read().splitlines()
        except FileNotFoundError:
            self.result_text.append("File not found. Please check the file path and try again.")
            return

        self.result_text.clear()

        def check_urls_thread():
            results = self.check_urls(urls)
            for result in results:
                self.result_text.append(result)

        thread = threading.Thread(target=check_urls_thread)
        thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = URLCheckerApp()
    window.show()
    sys.exit(app.exec_())
