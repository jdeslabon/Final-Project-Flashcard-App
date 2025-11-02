from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
                            QPushButton, QMessageBox, QFrame, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt
from ui.visual.styles.styles import get_create_flashcard_styles

class AllCards(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.styles = get_create_flashcard_styles()
        self.setup_ui()
        self.load_flashcards()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("All Flashcard Sets")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(self.styles["title"])
        layout.addWidget(title)
        
        
        # Refresh button
        refresh_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setStyleSheet(self.styles["add_button"])
        self.refresh_btn.clicked.connect(self.load_flashcards)
        refresh_layout.addWidget(self.refresh_btn)
        refresh_layout.addStretch()
        layout.addLayout(refresh_layout)
        
        # Scroll area for flashcard sets
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(self.styles["scroll_area"])
        
        # Container for flashcard set cards
        self.sets_container = QWidget()
        self.sets_layout = QGridLayout(self.sets_container)
        self.sets_layout.setSpacing(15)
        self.sets_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll_area.setWidget(self.sets_container)
        layout.addWidget(self.scroll_area)
        
        self.setLayout(layout)
    
    def load_flashcards(self):
        try:
            # Clear existing sets
            for i in reversed(range(self.sets_layout.count())):
                self.sets_layout.itemAt(i).widget().setParent(None)
            
            # Import and use controller to load saved sets
            from core.controller import FlashcardController
            controller = FlashcardController()
            all_sets = controller.get_all_sets()
            
            if not all_sets:
                no_sets_label = QLabel("No flashcard sets found.\nCreate some flashcards first!")
                no_sets_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                no_sets_label.setStyleSheet("color: #6C7086; font-size: 16px; padding: 40px;")
                self.sets_layout.addWidget(no_sets_label, 0, 0)
                return
            
            # Add each set as a styled card
            row, col = 0, 0
            for flashcard_set in all_sets:
                set_card = self.create_set_card(flashcard_set)
                self.sets_layout.addWidget(set_card, row, col)
                
                col += 1
                if col > 1:  # 2 cards per row
                    col = 0
                    row += 1
                    
        except Exception as e:
            error_label = QLabel(f"Error loading flashcards:\n{str(e)}")
            error_label.setStyleSheet("color: #F38BA8; font-size: 14px; padding: 20px;")
            self.sets_layout.addWidget(error_label)
    
    def create_set_card(self, flashcard_set):
        """Create a styled card for a flashcard set"""
        card_frame = QFrame()
        card_frame.setStyleSheet(self.styles["card_frame"])
        card_frame.setMinimumWidth(300)
        
        card_layout = QVBoxLayout(card_frame)
        card_layout.setSpacing(10)
        card_layout.setContentsMargins(15, 15, 15, 15)
        
        # Set name
        name_label = QLabel(flashcard_set['set_name'])
        name_label.setStyleSheet(self.styles["card_number"])
        name_label.setWordWrap(True)
        card_layout.addWidget(name_label)
        
        # Set info
        info_text = f"Cards: {len(flashcard_set['cards'])}\nCreated: {flashcard_set['created_date']}"
        info_label = QLabel(info_text)
        info_label.setStyleSheet("color: #6C7086; font-size: 12px;")
        card_layout.addWidget(info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Study button
        study_btn = QPushButton("📖 Study")
        study_btn.setStyleSheet(self.styles["save_button"])
        study_btn.clicked.connect(lambda: self.study_set(flashcard_set))
        button_layout.addWidget(study_btn)
        
        # Delete button
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setStyleSheet(self.styles["cancel_button"])
        delete_btn.clicked.connect(lambda: self.delete_set(flashcard_set['set_name']))
        button_layout.addWidget(delete_btn)
        
        card_layout.addLayout(button_layout)
        
        return card_frame
    
    def study_set(self, flashcard_set):
        """Start studying this flashcard set"""
        try:
            self.main_window.show_flashcard_study_with_set(flashcard_set)
                
        except Exception as e:
            import traceback
            traceback.print_exc()
    
    def delete_set(self, set_name):
        """Delete a flashcard set with confirmation"""
        reply = QMessageBox.question(self, "Confirm Delete", 
                                f"Are you sure you want to delete '{set_name}'?",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            from core.controller import FlashcardController
            controller = FlashcardController()
            
            error_message = controller.delete_flashcard_set(set_name)
            
            if error_message:
                QMessageBox.critical(self, "Delete Error", f"Failed to delete set:\n{error_message}")
            else:
                QMessageBox.information(self, "Success", f"Flashcard set '{set_name}' deleted successfully!")
                self.load_flashcards()  # Refresh the list