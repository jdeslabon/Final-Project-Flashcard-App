# FINAL PROJECT FLASHCARD APP / main.py

import sys
import os
from PyQt6.QtWidgets import QApplication, QStackedWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt 

# Enable high DPI scaling with proper fallbacks
if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

# Set environment variables for scaling
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"

from ui.pages.bootup_page import BootupPage
from ui.pages.welcome_page import WelcomePage
from ui.main_window import MainWindow
from utils.path_helper import get_asset_path
<<<<<<< HEAD
from PyQt6.QtGui import QPalette, QColor
=======
from ui.visual.animations import FadeInMainWindow
>>>>>>> 778bbdfbe3b15d51664449e416843cd3677c082c

class AppStack(QStackedWidget):
    """welcome page and main window"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #FFF5E5")
        self.setWindowTitle("Remora")
        
        #pages for welcome page and main window
        self.welcome_page = WelcomePage(self)
        self.main_window = MainWindow()
        
        #pages add to stack
        self.addWidget(self.welcome_page) #index 0
        self.addWidget(self.main_window)  #index 1
        
        #start with welcome page for this stacked widget (bootup is independent)
        self.setCurrentWidget(self.welcome_page)
        
    def show_main_window(self):
        """Switch from welcome page to the main window page"""
        self.setCurrentWidget(self.main_window)
        
        #animation
        self.setCurrentWidget(self.main_window)
        self.fade_anim = FadeInMainWindow(self.main_window, duration=600)
        self.fade_anim.fade_in()
        self.main_window.show_page(0)
        
        self.main_window.show_page(0)
         
#bootup page setup   
def main():
    app = QApplication(sys.argv)


    app.setWindowIcon(QIcon(get_asset_path("AppIcon.png")))
<<<<<<< HEAD

    # KILL PURPLE SELECTION
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#B4D7FF"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#000000"))
    app.setPalette(palette)


    # Create main window but don’t show yet
    main_window = MainWindow()

    # Create welcome page (it will show main window later)
    class AppController:
        def __init__(self):
            self.main_window = main_window
            
        def show_main_window(self):
            self.welcome_page.close()
            self.main_window.showMaximized()

    controller = AppController()
    controller.welcome_page = WelcomePage(app=controller)

    # Bootup page → Welcome page
    def on_bootup_finished():
=======
    
    stacked_app = AppStack()
    
    def on_bootup_complete():
>>>>>>> 778bbdfbe3b15d51664449e416843cd3677c082c
        bootup_page.close()
        stacked_app.showMaximized()
    
    bootup_page = BootupPage(on_finish_callback=on_bootup_complete)
    bootup_page.show()
    
    sys.exit(app.exec())
        
if __name__ == "__main__":
    main()