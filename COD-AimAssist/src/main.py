import sys
import os
import webbrowser
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QGroupBox, QGridLayout, QSizePolicy, QSpacerItem,
                             QMessageBox, QFrame)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QTimer

def resource_path(relative_path):
    """ احصل على المسار المطلق للمورد، يعمل للتطبيق وفترة التطوير """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AimAssistApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COD AimAssist v1.5")
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))
        self.setGeometry(100, 100, 900, 700)
        self.aim_assist_active = None
        self.setup_ui()
        
    def setup_ui(self):
        # إنشاء التبويبات الرئيسية
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(False)
        
        # تبويبات المحتوى
        self.multiplayer_tab = self.create_multiplayer_tab()
        self.settings_tab = self.create_settings_tab()
        self.contact_tab = self.create_contact_tab()
        
        self.tabs.addTab(self.multiplayer_tab, "Multiplayer")
        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.contact_tab, "Contact")
        
        # شريط الحالة
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setStyleSheet("color: #AAAAAA; padding: 5px;")
        
        # وضع كل شيء في تخطيط رئيسي
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.status_label)
        main_widget.setLayout(main_layout)
        
        self.setCentralWidget(main_widget)
        
        # تخصيص مظهر التطبيق
        self.apply_styles()
        
        # مؤقت لتحديث الحالة
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)
    
    def create_multiplayer_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # عنوان القسم
        title = QLabel("Aim Assist Multiplayer")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #FFA500; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # إنشاء أزرار المساعدة
        aim_assist_group = self.create_aim_assist_group()
        layout.addWidget(aim_assist_group)
        
        # أزرار إضافية
        additional_buttons = self.create_additional_buttons()
        layout.addWidget(additional_buttons)
        
        # معلومات الإصدار
        version = QLabel("Version 1.5 | Updated: 2023-11-15")
        version.setFont(QFont("Arial", 9))
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet("color: #666666; margin-top: 20px;")
        layout.addWidget(version)
        
        tab.setLayout(layout)
        return tab
    
    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Settings & Configuration")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1E90FF; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # إعدادات الماوس
        mouse_group = QGroupBox("Mouse Settings")
        mouse_group.setStyleSheet("QGroupBox { font-weight: bold; color: #CCCCCC; }")
        mouse_layout = QGridLayout()
        
        mouse_layout.addWidget(QLabel("Sensitivity:"), 0, 0)
        mouse_layout.addWidget(QLabel("Aim Smoothing:"), 1, 0)
        mouse_layout.addWidget(QLabel("ADS Multiplier:"), 2, 0)
        mouse_layout.addWidget(QLabel("Scope Sensitivity:"), 3, 0)
        
        # يمكن إضافة عناصر تحكم حقيقية هنا
        for i in range(4):
            value_label = QLabel("Default")
            value_label.setStyleSheet("background-color: #333333; padding: 5px; border-radius: 4px;")
            mouse_layout.addWidget(value_label, i, 1)
        
        mouse_group.setLayout(mouse_layout)
        layout.addWidget(mouse_group)
        
        # إعدادات المساعدة في التصويب
        assist_group = QGroupBox("Aim Assist Settings")
        assist_group.setStyleSheet("QGroupBox { font-weight: bold; color: #CCCCCC; }")
        assist_layout = QGridLayout()
        
        assist_layout.addWidget(QLabel("Strength:"), 0, 0)
        assist_layout.addWidget(QLabel("FOV:"), 1, 0)
        assist_layout.addWidget(QLabel("Max Distance:"), 2, 0)
        assist_layout.addWidget(QLabel("Target Priority:"), 3, 0)
        
        # يمكن إضافة عناصر تحكم حقيقية هنا
        for i in range(4):
            value_label = QLabel("Default")
            value_label.setStyleSheet("background-color: #333333; padding: 5px; border-radius: 4px;")
            assist_layout.addWidget(value_label, i, 1)
        
        assist_group.setLayout(assist_layout)
        layout.addWidget(assist_group)
        
        # أزرار التحكم
        btn_save = self.create_button("Save Settings", "#4CAF50")
        btn_save.setFixedHeight(50)
        btn_reset = self.create_button("Reset to Default", "#F44336")
        btn_reset.setFixedHeight(50)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_reset)
        layout.addLayout(btn_layout)
        
        # إضافة مساحة
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        tab.setLayout(layout)
        return tab
    
    def create_contact_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("Contact & Support")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1E90FF; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # بطاقات الاتصال
        contact_frame = QFrame()
        contact_frame.setStyleSheet("background-color: #252525; border-radius: 10px; padding: 20px;")
        contact_layout = QVBoxLayout()
        
        # البريد الإلكتروني
        email_card = self.create_contact_card(
            "Email Support", 
            "support@codassist.com", 
            "Send us an email for any issues or questions", 
            "#FF5722"
        )
        email_card.clicked.connect(lambda: self.open_email("support@codassist.com"))
        contact_layout.addWidget(email_card)
        
        # ديسكورد
        discord_card = self.create_contact_card(
            "Discord Community", 
            "discord.gg/codassist", 
            "Join our Discord server for real-time support", 
            "#7289DA"
        )
        discord_card.clicked.connect(lambda: webbrowser.open("https://discord.gg/codassist"))
        contact_layout.addWidget(discord_card)
        
        # موقع الويب
        website_card = self.create_contact_card(
            "Official Website", 
            "www.codassist.com", 
            "Visit our website for updates and documentation", 
            "#4CAF50"
        )
        website_card.clicked.connect(lambda: webbrowser.open("https://www.codassist.com"))
        contact_layout.addWidget(website_card)
        
        # التحديثات
        updates_card = self.create_contact_card(
            "Check for Updates", 
            "Version 1.5 (Latest)", 
            "Click to check for software updates", 
            "#2196F3"
        )
        updates_card.clicked.connect(self.check_for_updates)
        contact_layout.addWidget(updates_card)
        
        contact_frame.setLayout(contact_layout)
        layout.addWidget(contact_frame)
        
        # معلومات حقوق النشر
        copyright = QLabel("© 2023 COD AimAssist. All rights reserved.")
        copyright.setFont(QFont("Arial", 9))
        copyright.setAlignment(Qt.AlignCenter)
        copyright.setStyleSheet("color: #666666; margin-top: 30px;")
        layout.addWidget(copyright)
        
        tab.setLayout(layout)
        return tab
    
    def create_contact_card(self, title, subtitle, description, color):
        card = QPushButton()
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet(
            f"QPushButton {{ text-align: left; padding: 15px; border-radius: 8px; background-color: {color}; }}"
            f"QPushButton:hover {{ background-color: {self.lighten_color(color)}; }}"
        )
        
        card_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        card_layout.addWidget(title_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Arial", 12))
        subtitle_label.setStyleSheet("color: white; margin-top: 5px;")
        card_layout.addWidget(subtitle_label)
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 10))
        desc_label.setStyleSheet("color: rgba(255,255,255,0.8); margin-top: 10px;")
        card_layout.addWidget(desc_label)
        
        card.setLayout(card_layout)
        return card
    
    def create_aim_assist_group(self):
        group = QGroupBox()
        group.setStyleSheet("QGroupBox { border: 2px solid #444444; border-radius: 10px; }")
        layout = QGridLayout()
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(15)
        
        # أنواع المساعدة في التصويب
        assist_types = [
            ("Lite AimAssist", "#4CAF50", "Low intensity assist for subtle aiming help"),
            ("Normal AimAssist", "#2196F3", "Standard assist for balanced gameplay"),
            ("Middle AimAssist", "#FF9800", "Enhanced assist for more aggressive play"),
            ("Super AimAssist", "#F44336", "Maximum assist for competitive advantage")
        ]
        
        # إنشاء أزرار لكل نوع
        for i, (name, color, tip) in enumerate(assist_types):
            # زر التشغيل
            btn = self.create_button(name, color, tip)
            btn.setFixedHeight(60)
            layout.addWidget(btn, i, 0)
            
            # زر الإيقاف
            stop_btn = self.create_button(f"Stop {name}", "#555555", "Deactivate this aim assist level")
            stop_btn.setFixedHeight(60)
            layout.addWidget(stop_btn, i, 1)
            
            # ربط الأحداث
            btn.clicked.connect(lambda _, n=name: self.activate_aim_assist(n))
            stop_btn.clicked.connect(lambda _, n=name: self.deactivate_aim_assist(n))
        
        group.setLayout(layout)
        return group
    
    def create_additional_buttons(self):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # أزرار إضافية
        buttons = [
            ("Head", "#9C27B0", "Focus aim on head shots"),
            ("Random", "#00BCD4", "Randomize aim pattern for unpredictability"),
            ("Chests", "#795548", "Prioritize chest shots for consistent damage")
        ]
        
        for name, color, tip in buttons:
            btn = self.create_button(name, color, tip)
            btn.setFixedHeight(50)
            layout.addWidget(btn)
            btn.clicked.connect(lambda _, n=name: self.handle_additional_button(n))
        
        widget.setLayout(layout)
        return widget
    
    def create_button(self, text, color, tooltip=""):
        btn = QPushButton(text)
        btn.setFont(QFont("Arial", 12, QFont.Bold))
        btn.setCursor(Qt.PointingHandCursor)
        if tooltip:
            btn.setToolTip(tooltip)
        btn.setStyleSheet(
            f"QPushButton {{ background-color: {color}; color: white; border-radius: 8px; padding: 10px; }}"
            f"QPushButton:hover {{ background-color: {self.lighten_color(color)}; }}"
            f"QPushButton:pressed {{ background-color: {self.darken_color(color)}; }}"
            f"QToolTip {{ background-color: #333333; color: #FFFFFF; border: 1px solid #555555; }}"
        )
        return btn
    
    def lighten_color(self, hex_color, factor=0.3):
        """جعل اللون أفتح"""
        color = QColor(hex_color)
        return color.lighter(int(100 + factor * 100)).name()
    
    def darken_color(self, hex_color, factor=0.3):
        """جعل اللون أغمق"""
        color = QColor(hex_color)
        return color.darker(int(100 + factor * 100)).name()
    
    def apply_styles(self):
        # تطبيق التصميم الداكن
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QTabWidget::pane {
                border: 1px solid #333333;
                border-radius: 4px;
                background: #1E1E1E;
                margin-top: 5px;
            }
            QTabBar::tab {
                background: #252525;
                color: #CCCCCC;
                padding: 12px 25px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: 1px solid #333333;
                margin-right: 2px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #2D2D2D;
                color: #FFFFFF;
                border-bottom: 3px solid #FFA500;
            }
            QTabBar::tab:hover {
                background: #3A3A3A;
            }
            QGroupBox {
                color: #CCCCCC;
                font-size: 14px;
                margin-top: 20px;
                font-weight: bold;
            }
            QLabel {
                color: #CCCCCC;
            }
        """)
    
    def activate_aim_assist(self, name):
        self.aim_assist_active = name
        self.status_label.setText(f"Active: {name} | Press F8 to stop")
        # هنا سيتم تفعيل وظيفة مساعدة التصويب للماوس
        
    def deactivate_aim_assist(self, name):
        if self.aim_assist_active == name:
            self.aim_assist_active = None
            self.status_label.setText("Aim assist deactivated")
            # هنا سيتم إيقاف وظيفة مساعدة التصويب للماوس
        
    def handle_additional_button(self, name):
        self.status_label.setText(f"Mode set to: {name}")
        # هنا سيتم تفعيل الوظائف الإضافية للماوس
        
    def open_email(self, email):
        webbrowser.open(f"mailto:{email}")
        
    def check_for_updates(self):
        QMessageBox.information(
            self, 
            "Software Update", 
            "You are using the latest version (v1.5)\n\n"
            "No updates available at this time.",
            QMessageBox.Ok
        )
        
    def update_status(self):
        if self.aim_assist_active:
            self.status_label.setText(f"Active: {self.aim_assist_active} | Press F8 to stop")
        else:
            self.status_label.setText("Ready | Select an aim assist mode")

if __name__ == "__main__":
    # إخفاء نافذة الكونسول على Windows
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # تخصيص لوحة الألوان للتطبيق
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.Base, QColor(45, 45, 45))
    palette.setColor(QPalette.AlternateBase, QColor(60, 60, 60))
    palette.setColor(QPalette.ToolTipBase, QColor(45, 45, 45))
    palette.setColor(QPalette.ToolTipText, QColor(220, 220, 220))
    palette.setColor(QPalette.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.Button, QColor(60, 60, 60))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.Highlight, QColor(255, 165, 0))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)
    
    window = AimAssistApp()
    window.show()
    sys.exit(app.exec_())
