from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout, QStackedWidget
)
from PyQt6.QtCore import Qt, QPropertyAnimation
from PyQt6.QtGui import QFont

class FlashcardWidget(QWidget):
    def __init__(self, question, answer):
        super().__init__()
        self.question = question
        self.answer = answer
        self.is_flipped = False

        self.front_label = QLabel(question)
        self.front_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.front_label.setWordWrap(True)

        self.back_label = QLabel(answer)
        self.back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.back_label.setWordWrap(True)
        self.back_label.hide()

        layout = QVBoxLayout(self)
        layout.addWidget(self.front_label)
        layout.addWidget(self.back_label)

        self.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #333;
            }
            QWidget {
                background-color: #FFFFFF;
                border-radius: 15px;
                border: 2px solid #999;
            }
        """)
        self.setFixedHeight(120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mousePressEvent = self.flip_card

    def flip_card(self, event):
        self.is_flipped = not self.is_flipped
        self.front_label.setVisible(not self.is_flipped)
        self.back_label.setVisible(self.is_flipped)


class ExistingFlashcard(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
   
    def setup_ui(self):
        self.setStyleSheet("background-color: #FFF7EB;")  # Light cream background
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)
        self.setLayout(layout)
       
        # Title
        title = QLabel("TOPICS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                background-color: #F27D72;
                color: white;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        layout.addWidget(title)

        # Scroll area for topics
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: transparent;")
        layout.addWidget(self.scroll_area)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(20)
        self.scroll_area.setWidget(self.scroll_widget)

        # Topics
        self.topics = [
            {"name": "English", "color": "#B3D9FF", "icon": "📘"},
            {"name": "Math", "color": "#B9FBC0", "icon": "🧮"},
            {"name": "Science", "color": "#FFE6A7", "icon": "🔬"},
            {"name": "History", "color": "#FFB3B3", "icon": "🌎"},
        ]

        # Flashcard data
        self.qa_sets = {
            "English": [
                ("What is haha?", "haha is a tawa"),
                ("what is huhu?", "huhu is a iyak")
            ],
            "Math": [
                ("1+1", "2"),
                ("2+2", "4")
            ],
            "Science": [
                ("Who discovered gravity?", "Isaac Newton"),
            ],
            "History": [
                ("Who killed Magellan?", "Lapu-Lapu"),
                ("Where is Rizal’s head?", "On the one-peso coin")
            ],
        }

        # Add topic buttons
        for topic in self.topics:
            btn = QPushButton(f"{topic['icon']}   {topic['name']}")
            btn.setMinimumHeight(80)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {topic['color']};
                    border: none;
                    border-radius: 25px;
                    font-size: 20px;
                    font-weight: bold;
                    color: #333;
                    text-align: left;
                    padding-left: 30px;
                }}
                QPushButton:hover {{
                    background-color: #dfefff;
                }}
            """)
            btn.clicked.connect(lambda checked, t=topic['name']: self.open_topic(t))
            self.scroll_layout.addWidget(btn)

        # Back button
        back_btn = QPushButton("↩ Back to Main")
        back_btn.setFixedWidth(160)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #2b7cff;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1a5fd0;
            }
        """)
        back_btn.clicked.connect(lambda: self.main_window.show_page(0))
       
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(back_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def open_topic(self, topic_name):
        """Show example flashcards for the selected topic."""
        # Clear layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Title for selected topic
        topic_title = QLabel(f"{topic_name} Flashcards")
        topic_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        topic_title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #333;
                background-color: #FFEFD5;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.scroll_layout.addWidget(topic_title)

        # Add flashcards
        for q, a in self.qa_sets.get(topic_name, []):
            card = FlashcardWidget(q, a)
            self.scroll_layout.addWidget(card)

        # Add back button
        back_btn = QPushButton("← Back to Topics")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #F27D72;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #d25a50;
            }
        """)
        back_btn.clicked.connect(self.show_topics)
        self.scroll_layout.addWidget(back_btn)

    def show_topics(self):
        """Show the topic list again."""
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for topic in self.topics:
            btn = QPushButton(f"{topic['icon']}   {topic['name']}")
            btn.setMinimumHeight(80)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {topic['color']};
                    border: none;
                    border-radius: 25px;
                    font-size: 20px;
                    font-weight: bold;
                    color: #333;
                    text-align: left;
                    padding-left: 30px;
                }}
                QPushButton:hover {{
                    background-color: #dfefff;
                }}
            """)
            btn.clicked.connect(lambda checked, t=topic['name']: self.open_topic(t))
            self.scroll_layout.addWidget(btn)
