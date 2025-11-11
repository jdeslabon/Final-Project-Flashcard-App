#ui/pages/welcome_page.py #jose

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel,
    QLineEdit, QMessageBox
    )
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QPixmap
from ui.visual.styles.styles import ( 
    APP_STYLE, APP_STYLE_LIGHT, APP_STYLE_DARK, FONT_SUBTITLE, FONT_LARGE_BOLD,
    FONT_MEDIUM, FONT_BUTTON, FONT_LABEL, MESSAGE_WARNING
    )
from ui.visual.animations import FadeWidget
from data.user_and_theme import AppData
from utils.path_helper import get_asset_path
from ui.pages.login_page import LoginPage #added (LOGIN)
from ui.pages.profile_page import ProfilePage #added (LOGIN)
from ui.pages.accounts_page import AccountsPage #added (LOGIN)

class WelcomePage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.data = AppData()
        self.app = app
        self.apply_theme()
        
        self.setWindowTitle("Remora App Flow")
        self.setStyleSheet(APP_STYLE)
        self.setWindowIcon(QIcon(get_asset_path("AppIcon.png")))
        
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.clicked.connect(self.toggle_btn)
        
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.theme_btn)
        
        self.stacked = QStackedWidget()
        
        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.stacked)
        self.setLayout(layout)
        
        # Pages
        self.start_page = FadeWidget(self.create_start_page(), self)
        self.login_page = FadeWidget(LoginPage(self.show_greet), self) #replaced, all self.name_page replaced with self.login_page (LOGIN)
        self.greet_page = FadeWidget(QLabel(alignment=Qt.AlignmentFlag.AlignCenter), self)
        self.greet_page.widget.setFont(FONT_MEDIUM)
        self.welcome_page = FadeWidget(self.create_welcome_page(), self)
        #removed self.ask_page (LOGIN)
        
        self.profile_page = FadeWidget(ProfilePage(self, self.switch_account), self) #switch account to login page (LOGIN)
        
        self.main_page = FadeWidget(QWidget(), self)
        
        self.tutorial_page = FadeWidget(self.create_tutorial_page(), self)
        self.current_tutorial_step = 0  # track which tutorial slide we're on

        self.welcome_back_page = FadeWidget(QLabel(alignment=Qt.AlignmentFlag.AlignCenter), self)
        self.welcome_back_page.widget.setFont(FONT_MEDIUM)

        #ADDED ACCOUNTS PAGE (LOGIN)
        self.accounts_page = FadeWidget(
            AccountsPage(self.data, self.login_page, self.profile_page, self.fade_to_page),
            self
        )
        self.stacked.addWidget(self.accounts_page)

        for page in [self.start_page, self.login_page, self.greet_page, self.welcome_page, self.main_page, self.profile_page]: #removed self.ask_page (LOGIN)
            self.stacked.addWidget(page) #added profile page (LOGIN)
            
        self.stacked.addWidget(self.tutorial_page)
        self.stacked.addWidget(self.welcome_back_page)
        
        # Connections
        self.start_btn.clicked.connect(lambda: self.start_page.fade_out(self.login_page)) #replaced self.name_page with self.login_page (LOGIN)
        
        #removed yes and no btn (LOGIN)

        # Start page
        self.stacked.setCurrentWidget(self.start_page)
        self.start_page.fade_in()

        # Apply default theme
        self.apply_theme()
        
    def toggle_btn(self):
        """Switch between light and dark themes."""
        self.data.theme = "dark" if self.data.theme == "light" else "light"
        self.apply_theme()
        self.theme_btn.setText("☀️" if self.data.theme == "dark" else "🌙")

    def apply_theme(self):
        if self.data.theme == "dark":
            self.setStyleSheet(APP_STYLE_DARK)
        else:
            self.setStyleSheet(APP_STYLE_LIGHT)
            
        for page_name in [
            "main_page", "topics_page", "create_flashcard_page",
            "saved_flashcards_page", "existing_flashcard_page"
        ]:
            if hasattr(self, page_name):
                getattr(self, page_name).setStyleSheet(
                    APP_STYLE_DARK if self.data.theme == "dark" else APP_STYLE_LIGHT
                )
            
    def toggle_theme(self):
        if self.data.theme == "light":
            self.data.theme = "dark"
        else:
            self.data.theme = "light"
    
        self.apply_theme()

    def create_start_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        pixmap = QPixmap(get_asset_path("AppIcon.png"))
        pixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("READY WHEN YOU ARE!")
        subtitle.setFont(FONT_SUBTITLE)
        subtitle.setStyleSheet("color: #FC483D; letter-spacing: 2px; font-weight: 900;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.start_btn = QPushButton("BEGIN")
        self.start_btn.setFont(FONT_LARGE_BOLD)
        
        layout.addStretch()
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        return widget

    #removed create_name_page() (LOGIN)
    
    def switch_account(self): #added (LOGIN)
        self.fade_to_page(self.accounts_page)

    #removed create_ask_page() (LOGIN)
    
    def create_tutorial_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
    
        self.tutorial_title = QLabel()
        self.tutorial_title.setFont(FONT_LARGE_BOLD)
        self.tutorial_title.setStyleSheet("color: #434190; font-weight: bold;")
        self.tutorial_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.tutorial_desc = QLabel()
        self.tutorial_desc.setFont(FONT_LABEL)
        self.tutorial_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tutorial_desc.setWordWrap(True)
        self.tutorial_desc.setStyleSheet("color: #555;")
    
        self.next_btn = QPushButton("Next ➜")
        self.next_btn.setFont(FONT_BUTTON)
        self.next_btn.clicked.connect(self.next_tutorial_step)
        
        self.skip_btn = QPushButton("Skip Tutorial ⏭️")
        self.skip_btn.setFont(FONT_BUTTON)
        self.skip_btn.clicked.connect(lambda: self.tutorial_page.fade_out(None, on_finish=self.app.show_main_window))
        self.tutorial_desc.setStyleSheet("color: #555; padding: 0 40px;")
        
        layout.addStretch()
        layout.addWidget(self.tutorial_title)
        layout.addWidget(self.tutorial_desc)
        layout.addSpacing(20)
        layout.addWidget(self.next_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.skip_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
    
        return widget

    #REMOVED show_tutorial() (LOGIN)
        
    def update_tutorial_step(self):
        """Update tutorial content based on current step"""
        steps = [
            {
                "title": "Adding Flashcards",
                "desc": "Click the '+' button or 'Add Flashcard' in the main screen to create a new flashcard.\nYou can enter a question, an answer, and save it instantly."
            },
            {
                "title": "Navigating the App",
                "desc": "Use the sidebar ☰ to explore:\n🏠 Home – View your flashcards\n👤 Profile – Check your info\n⚙️ Settings – Customize your theme\n📊 Statistics – See your study progress."
            },
            {
                "title": "Using Existing Flashcards",
                "desc": "Select any flashcard to study. Flip the card to see the answer and mark if you got it right or wrong. Remora tracks your progress automatically!"
            }
        ]
    
        # Update content
        step = steps[self.current_tutorial_step]
        self.tutorial_title.setText(step["title"])
        self.tutorial_desc.setText(step["desc"])
    
        # Update button text
        if self.current_tutorial_step < len(steps) - 1:
            self.next_btn.setText("Next ➜")
        else:
            self.next_btn.setText("Finish ✅")

    def next_tutorial_step(self):
        """Handle next step or finish tutorial"""
        self.current_tutorial_step += 1
        if self.current_tutorial_step < 3:
            self.update_tutorial_step()
        else:
            # End tutorial and go to main page
            self.tutorial_page.fade_out(None, on_finish=self.app.show_main_window)

    def show_welcome_back(self, username): #changed (LOGIN)
        """Show a short welcome-back message before going to the main window."""
        self.welcome_back_page.widget.setText(f"Welcome back, {username}! 👋")
        self.welcome_back_page.widget.setStyleSheet("color: #434190;")
        
        # Fade from greet → welcome back
        self.greet_page.fade_out(self.welcome_back_page)
        
        # After a short delay, go to the main app
        QTimer.singleShot(1500, lambda: self.welcome_back_page.fade_out(None, on_finish=self.app.show_main_window))

    def show_greet(self, username=None, is_new=False): #changed (LOGIN)
        """Called after login or registration success."""
        name = username or "User"
        self.data.username = name

        # Load full name for profile display
        full_name = self.get_full_name(name)
        self.profile_page.widget.load_profile(name, full_name)

        # Show greeting message
        self.greet_page.widget.setText(f"Hi, {name}!")
        self.greet_page.widget.setStyleSheet("color: #434190")
        self.login_page.fade_out(self.greet_page)

        # After greeting, decide what to show next
        if is_new:
            QTimer.singleShot(1000, lambda: self.start_tutorial(username))
        else:
            QTimer.singleShot(1000, lambda: self.show_welcome_back(username))

        
    def start_tutorial(self, username): #added (LOGIN)
        """Start tutorial automatically for new users."""
        self.current_tutorial_step = 0
        self.greet_page.fade_out(self.tutorial_page)
        self.update_tutorial_step()
        
    def open_main_profile(self, username): #added (LOGIN)
        """Switch to the main window's Profile Page after login."""
        try:
            # Use the app reference (AppStack)
            if hasattr(self.app, "show_main_window"):
                self.app.show_main_window()  # triggers fade-in animation correctly
            else:
                print("⚠️ AppStack reference not found.")
        except Exception as e:
            print(f"Error opening main profile: {e}")
            
    def get_full_name(self, username): #added (LOGIN)
        """Get the user's full name from saved profile data."""
        import json, os
        path = "user_profiles.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
            return data.get(username, {}).get("full_name", username)
        return username
        
    def create_welcome_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        pixmap = QPixmap(get_asset_path("AppIcon.png"))
        pixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("WELCOME!")
        title.setFont(FONT_LARGE_BOLD)
        title.setStyleSheet("color: #FC483D; font-weight: 900; letter-spacing: 2px;")
        
        subtitle = QLabel("Remora is a flashcard for students")
        subtitle.setFont(FONT_LABEL)
        subtitle.setStyleSheet("color: #A0522D; font-weight: bold;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        return widget
    
    def show_welcome(self):
        self.greet_page.fade_out(self.welcome_page)
        QTimer.singleShot(1500, lambda: self.welcome_page.fade_out(self.ask_page))
    
    def fade_to_page(self, target_page): #added (login)
        """Fade from the current stacked page to the target page."""
        current = self.stacked.currentWidget()
        if hasattr(current, "fade_out"):
            current.fade_out(target_page)
        else:
            self.stacked.setCurrentWidget(target_page)