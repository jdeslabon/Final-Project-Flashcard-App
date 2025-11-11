# ui/pages/profile_page.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QLineEdit, QFormLayout, QSpinBox
)


# Profile Page for viewing and editing user profile settings updated (LOGIN)
class ProfilePage(QWidget):
    def __init__(self, parent=None, switch_account_callback=None):
        super().__init__(parent)
        self.switch_account_callback = switch_account_callback

        self.username = None
        self.setup_ui()
    
    def setup_ui(self):
        self.layout = QVBoxLayout()
        
        self.title = QLabel("<h1>Profile Settings</h1>")
        self.user_label = QLabel("")  # will show the logged-in user
        self.user_label.setStyleSheet("font-weight: bold; color: #434190;")

        # Form layout
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.age_spinbox = QSpinBox()
        self.age_spinbox.setRange(1, 100)
        self.save_btn = QPushButton("Save Profile")
        self.save_btn.clicked.connect(self.save_profile)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Age:", self.age_spinbox)
        form_layout.addRow("", self.save_btn)

        # Switch account
        self.switch_btn = QPushButton("Switch Account")
        self.switch_btn.setStyleSheet("background-color: #FC483D; color: white; padding: 6px; border-radius: 6px;")
        self.switch_btn.clicked.connect(self.confirm_switch)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.user_label)
        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.switch_btn)
        self.layout.addStretch()
        self.setLayout(self.layout)
        
    def confirm_switch(self):
        """Ask for confirmation before switching accounts."""
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to switch accounts?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if callable(self.switch_account_callback):
                self.switch_account_callback()

            
    def save_profile(self):
        """Save profile information to a local JSON file."""
        import json, os

        profile_data = {
            "full_name": self.name_input.text(),
            "email": self.email_input.text(),
            "age": self.age_spinbox.value()
        }

        path = "user_profiles.json"
        all_data = {}

        # Load existing data if it exists
        if os.path.exists(path):
            with open(path, "r") as f:
                all_data = json.load(f)

        # Update this user's profile
        all_data[self.username or "unknown"] = profile_data

        # Save back to file
        with open(path, "w") as f:
            json.dump(all_data, f, indent=4)

        print(f"✅ Saved profile for {self.username or 'unknown'}")

    def load_profile(self, username, full_name):
        """Pre-fill name and display current logged-in user."""
        import json, os

        self.username = username
        self.user_label.setText(f"Logged in as: {full_name} ({username})")

        # Try to load existing profile data
        path = "user_profiles.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                all_profiles = json.load(f)
            profile = all_profiles.get(username, {})
            self.name_input.setText(profile.get("full_name", full_name))
            self.email_input.setText(profile.get("email", ""))
            self.age_spinbox.setValue(profile.get("age", 0))
        else:
            # Default if file missing
            self.name_input.setText(full_name)
            self.email_input.clear()
            self.age_spinbox.setValue(0)
            
    def switch_account(self):
        """Go to the Accounts Page."""
        if callable(self.switch_account_callback):
            self.switch_account_callback()
        else:
            print("⚠️ switch_account_callback not set in ProfilePage")

