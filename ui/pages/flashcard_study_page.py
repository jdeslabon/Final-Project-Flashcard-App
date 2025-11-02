from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFrame, QProgressBar, QCheckBox)
from PyQt6.QtCore import Qt
from ui.visual.styles.styles import get_study_page_styles
import random

class FlashcardStudyPage(QWidget):
    def __init__(self, main_window, flashcard_set):
        super().__init__()
        self.main_window = main_window
        self.flashcard_set = flashcard_set or {'set_name': 'No Set', 'cards': []}
        self.current_card_index = 0
        self.is_flipped = False
        self.styles = get_study_page_styles()
        self.setup_ui()
        if self.flashcard_set and self.flashcard_set['cards']:
            self.load_card(0)
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # HEADER SECTION
        header_layout = QHBoxLayout()
        
        # Set name
        set_name_text = self.flashcard_set['set_name'] if self.flashcard_set else "No Set Selected"
        self.set_name_label = QLabel(set_name_text)
        self.set_name_label.setStyleSheet(self.styles["title"])
        header_layout.addWidget(self.set_name_label)
        
        header_layout.addStretch()
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setFixedWidth(150)
        self.progress_bar.setStyleSheet(self.styles["progress_bar"])
        header_layout.addWidget(self.progress_bar)
        
        # Stats
        self.stats_label = QLabel("Mastered: 0/0")
        self.stats_label.setStyleSheet(self.styles["stats_label"])
        header_layout.addWidget(self.stats_label)
        
        # Shuffle toggle
        self.shuffle_btn = QPushButton("🔀 Shuffle")
        self.shuffle_btn.setStyleSheet(self.styles["shuffle_button"])
        self.shuffle_btn.clicked.connect(self.shuffle_cards)
        header_layout.addWidget(self.shuffle_btn)
        
        layout.addLayout(header_layout)
        
        # CARD COUNTER
        self.card_counter = QLabel("Card 1 of 1")
        self.card_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_counter.setStyleSheet(self.styles["card_counter"])
        layout.addWidget(self.card_counter)
        
        # FLIP CARD AREA - LARGER SIZE
        card_area_layout = QHBoxLayout()
        card_area_layout.addStretch()
        
        # Flip card container - INCREASED SIZE
        self.flip_card_container = QFrame()
        self.flip_card_container.setFixedSize(1000, 800)
       
        
        # Create flip card
        self.setup_flip_card()
        card_area_layout.addWidget(self.flip_card_container)
        card_area_layout.addStretch()
        
        layout.addLayout(card_area_layout)
        
        # CONTROLS SECTION - CENTERED
        controls_layout = QHBoxLayout()
        controls_layout.addStretch()
        
        # Correct button
        self.correct_btn = QPushButton("✓ Correct")
        self.correct_btn.setStyleSheet(self.styles["correct_button"])
        self.correct_btn.clicked.connect(lambda: self.mark_card(True))
        controls_layout.addWidget(self.correct_btn)
        
        # Wrong button
        self.wrong_btn = QPushButton("✗ Wrong")
        self.wrong_btn.setStyleSheet(self.styles["wrong_button"])
        self.wrong_btn.clicked.connect(lambda: self.mark_card(False))
        controls_layout.addWidget(self.wrong_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # SECONDARY CONTROLS
        secondary_layout = QHBoxLayout()
        secondary_layout.addStretch()
        
        # Reset progress
        self.reset_btn = QPushButton("🔄 Reset Progress")
        self.reset_btn.setStyleSheet(self.styles["reset_button"])
        self.reset_btn.clicked.connect(self.reset_progress)
        secondary_layout.addWidget(self.reset_btn)
        
        # Filter toggle
        self.filter_checkbox = QCheckBox("Show Only Unlearned")
        self.filter_checkbox.setStyleSheet(self.styles["filter_checkbox"])
        self.filter_checkbox.stateChanged.connect(self.apply_filter)
        secondary_layout.addWidget(self.filter_checkbox)
        
        secondary_layout.addStretch()
        layout.addLayout(secondary_layout)
        
        # FOOTER
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        
        self.back_btn = QPushButton("← Back to All Cards")
        self.back_btn.setStyleSheet(self.styles["back_button"])
        self.back_btn.clicked.connect(self.go_back)
        footer_layout.addWidget(self.back_btn)
        
        footer_layout.addStretch()
        layout.addLayout(footer_layout)
        
        self.setLayout(layout)
    
    def setup_flip_card(self):
        self.card_front = QFrame()
        self.card_front.setStyleSheet(self.styles["card_front"])
        
        self.card_back = QFrame()
        self.card_back.setStyleSheet(self.styles["card_back"])
        
        front_layout = QVBoxLayout(self.card_front)
        self.front_label = QLabel()
        self.front_label.setStyleSheet(self.styles["card_text"])
        self.front_label.setWordWrap(True)
        self.front_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        front_layout.addWidget(self.front_label)
        
        back_layout = QVBoxLayout(self.card_back)
        self.back_label = QLabel()
        self.back_label.setStyleSheet(self.styles["card_text"])
        self.back_label.setWordWrap(True)
        self.back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        back_layout.addWidget(self.back_label)
        
        # Start with front visible
        self.card_back.hide()
        self.card_front.show()
        
        flip_layout = QVBoxLayout(self.flip_card_container)
        flip_layout.addWidget(self.card_front)
        flip_layout.addWidget(self.card_back)
        
        # Click to flip
        self.card_front.mousePressEvent = lambda e: self.flip_card()
        self.card_back.mousePressEvent = lambda e: self.flip_card()
    
    def flip_card(self):
        if self.is_flipped:
            self.card_front.show()
            self.card_back.hide()
        else:
            self.card_front.hide()
            self.card_back.show()
        self.is_flipped = not self.is_flipped
    
    def load_card(self, index):
        if not self.flashcard_set or not self.flashcard_set['cards']:
            self.front_label.setText("No flashcards available")
            self.back_label.setText("Please select a flashcard set first")
            return
            
        if 0 <= index < len(self.flashcard_set['cards']):
            self.current_card_index = index
            card = self.flashcard_set['cards'][index]
            
            self.front_label.setText(f"Q: {card['question']}")
            self.back_label.setText(f"A: {card['answer']}")
            
            # Reset flip state
            self.is_flipped = False
            self.card_front.show()
            self.card_back.hide()
            
            # Update UI
            self.update_card_counter()
            self.update_progress()
        
    def update_card_counter(self):
        total = len(self.flashcard_set['cards'])
        current = self.current_card_index + 1
        self.card_counter.setText(f"Card {current} of {total}")
    
    def update_progress(self):
        # Calculate progress
        total_cards = len(self.flashcard_set['cards'])
        learned_cards = sum(1 for card in self.flashcard_set['cards'] 
                          if card.get('progress', {}).get('learned', False))
        
        progress = (learned_cards / total_cards) * 100 if total_cards > 0 else 0
        self.progress_bar.setValue(int(progress))
        self.stats_label.setText(f"Mastered: {learned_cards}/{total_cards}")
    
    def mark_card(self, correct):
        from core.controller import FlashcardController
        controller = FlashcardController()
        
        # Mark card as learned if correct, or reset if wrong
        learned = correct
        controller.update_card_progress(
            self.flashcard_set['set_name'],
            self.current_card_index,
            learned,
            correct
        )
        
        # Update local data
        card = self.flashcard_set['cards'][self.current_card_index]
        if 'progress' not in card:
            card['progress'] = {'learned': False, 'times_correct': 0, 'times_wrong': 0}
        
        if correct:
            card['progress']['times_correct'] += 1
            card['progress']['learned'] = True
        else:
            card['progress']['times_wrong'] += 1
            card['progress']['learned'] = False
        
        # Auto-advance to next card
        self.update_progress()
        if self.current_card_index < len(self.flashcard_set['cards']) - 1:
            self.load_card(self.current_card_index + 1)
        else:
            # End of set - show completion
            self.front_label.setText("🎉 Set Complete!")
            self.back_label.setText(f"You've finished all {len(self.flashcard_set['cards'])} cards!")
            self.correct_btn.setEnabled(False)
            self.wrong_btn.setEnabled(False)
    
    def shuffle_cards(self):
        random.shuffle(self.flashcard_set['cards'])
        self.load_card(0)
        self.correct_btn.setEnabled(True)
        self.wrong_btn.setEnabled(True)
    
    def reset_progress(self):
        from core.controller import FlashcardController
        controller = FlashcardController()
        
        for i in range(len(self.flashcard_set['cards'])):
            controller.update_card_progress(
                self.flashcard_set['set_name'],
                i,
                False,
                False
            )
            if 'progress' in self.flashcard_set['cards'][i]:
                self.flashcard_set['cards'][i]['progress'] = {
                    'learned': False, 
                    'times_correct': 0, 
                    'times_wrong': 0
                }
        
        self.update_progress()
        self.load_card(0)
        self.correct_btn.setEnabled(True)
        self.wrong_btn.setEnabled(True)
    
    def apply_filter(self):
        # TODO: Implement filtering to show only unlearned cards
        pass
    
    def go_back(self):
        self.main_window.show_page(3)  # Back to All Cards page