# ui/pages/accounts_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt

class AccountsPage(QWidget):
    """
    Page for managing user accounts — allows switching between saved users
    or returning to the login page to add a new one.
    """

    def __init__(self, data, login_page, profile_page, fade_to_page):
        """
        :param data: Shared data object (stores username, account list, etc.)
        :param login_page: Reference to LoginPage
        :param profile_page: Reference to ProfilePage
        :param fade_to_page: Function that handles fade transitions between pages
        """
        super().__init__()
        self.data = data
        self.login_page = login_page
        self.profile_page = profile_page
        self.fade_to_page = fade_to_page

        self.setObjectName("AccountsPage")
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        self.title = QLabel("Manage Accounts")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.layout.addWidget(self.title)

        # Accounts list
        self.account_list = QListWidget()
        self.account_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #aaa;
                border-radius: 6px;
                font-size: 16px;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
        """)
        self.layout.addWidget(self.account_list)

        # Buttons
        self.switch_button = QPushButton("Switch to Selected Account")
        self.add_button = QPushButton("Add New Account")
        self.delete_button = QPushButton("Delete Selected Account")
        self.back_button = QPushButton("Back to Profile")

        for btn in (self.switch_button, self.add_button, self.delete_button, self.back_button):
            btn.setMinimumHeight(36)
            self.layout.addWidget(btn)

        # Connect signals
        self.switch_button.clicked.connect(self.switch_account)
        self.add_button.clicked.connect(self.add_account)
        self.delete_button.clicked.connect(self.delete_account)
        self.back_button.clicked.connect(lambda: self.fade_to_page(self.profile_page))

        # Load saved accounts
        self.refresh_list()

    # ---------------------------------------
    # Functional Methods
    # ---------------------------------------

    def refresh_list(self):
        """Refresh the account list from shared data."""
        self.account_list.clear()
        accounts = getattr(self.data, "accounts", [])
        for username in accounts:
            item = QListWidgetItem(username)
            if username == self.data.username:
                item.setText(f"{username} (current)")
            self.account_list.addItem(item)

    def switch_account(self):
        """Switch to the selected account and fade to ProfilePage."""
        item = self.account_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Selection", "Please select an account first.")
            return

        username = item.text().replace(" (current)", "")
        self.data.username = username
        print(f"🔄 Switched to account: {username}")

        # Update profile page
        if hasattr(self.profile_page.widget, "set_username"):
            self.profile_page.widget.set_username(username)

        self.fade_to_page(self.profile_page)

    def add_account(self):
        """Fade back to the login page to add a new account."""
        print("➕ Adding new account — returning to login page.")
        self.data.username = None
        self.fade_to_page(self.login_page)

    def delete_account(self):
        """Delete the selected account from the saved list."""
        item = self.account_list.currentItem()
        if not item:
            QMessageBox.warning(self, "No Selection", "Please select an account to delete.")
            return

        username = item.text().replace(" (current)", "")
        confirm = QMessageBox.question(
            self,
            "Delete Account",
            f"Are you sure you want to delete '{username}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            accounts = getattr(self.data, "accounts", [])
            if username in accounts:
                accounts.remove(username)
                self.data.accounts = accounts
                if username == self.data.username:
                    self.data.username = None
                self.refresh_list()
                print(f"🗑️ Deleted account: {username}")
