# ui.py
import os
import sys
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QSlider, QFrame, 
                            QComboBox, QTabWidget)

from resolution_controller import ResolutionController
from colors_controller import ColorsController





'''
>>> Metadata de versión
'''
VERSION = "1.1.0"





'''
>>> UI
'''
class ResolutionTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        # Selección de monitor
        screen_status = QFrame()
        screen_status.setObjectName("statusFrame")
        screen_layout = QHBoxLayout(screen_status)
        screen_layout.setContentsMargins(10, 10, 10, 10)
        screen_layout.setSpacing(15)

        icon_label = QLabel()
        icon_path = self.parent.resource_path(os.path.join('Storage', 'Icons', 'monitor_01.png'))
        if os.path.exists(icon_path):
            icon_label.setPixmap(QPixmap(icon_path).scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignVCenter)
        
        screen_text = QLabel('Monitor:')
        screen_text.setFont(QFont('Segoe UI', 11))
        screen_text.setAlignment(Qt.AlignVCenter)
        
        self.monitor_combo = QComboBox()
        self.monitor_combo.setFont(QFont('Segoe UI', 10))
        self.monitor_combo.addItems(self.parent.outputs if self.parent.outputs else ["No hay monitores detectados"])
        self.monitor_combo.currentTextChanged.connect(self.parent.on_monitor_changed)
        self.monitor_combo.setEnabled(bool(self.parent.outputs))
        self.monitor_combo.setFixedHeight(32)
        
        screen_layout.addWidget(icon_label)
        screen_layout.addWidget(screen_text)
        screen_layout.addWidget(self.monitor_combo, 1)
        layout.addWidget(screen_status)

        # Sección del control deslizante
        self.value_label = QLabel('Resolución actual: 1.0x')
        self.value_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("color: #00ff99;")
        layout.addWidget(self.value_label)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(200)
        self.slider.setValue(10)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #404040;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #00ff99;
                width: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QSlider::sub-page:horizontal {
                background: #00ff99;
                border-radius: 4px;
            }
        """)
        self.slider.valueChanged.connect(self.parent.update_res_label)
        layout.addWidget(self.slider)

        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        button_style = """
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:pressed {
                background-color: #4d4d4d;
            }
        """
        
        self.apply_btn = QPushButton('Aplicar cambios')
        self.apply_btn.clicked.connect(self.parent.apply_resolution)
        self.apply_btn.setStyleSheet(button_style)
        self.apply_btn.setCursor(Qt.PointingHandCursor)
        
        self.restore_btn = QPushButton('Restaurar valores')
        self.restore_btn.clicked.connect(self.parent.restore_resolution)
        self.restore_btn.setStyleSheet(button_style)
        self.restore_btn.setCursor(Qt.PointingHandCursor)
        
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.restore_btn)
        layout.addLayout(btn_layout)

class ColorTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(25)

        # Descripción
        desc = QLabel(
            "Seleccione un modo de color negativo:\n"
            "1. Clásico - Inversión RGB estándar\n"
            "2. Azul - Tonalidades frías\n"
            "3. Rojo - Tonalidades cálidas"
        )
        desc.setFont(QFont('Segoe UI', 12))
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Botones de modo
        btn_container = QHBoxLayout()
        btn_container.setSpacing(20)
        
        def create_image_button(icon_path, size=QSize(160, 160)):
            btn = QPushButton()
            btn.setFixedSize(size)
            full_path = self.parent.resource_path(icon_path)
            
            if os.path.exists(full_path):
                pixmap = QPixmap(full_path)
                if not pixmap.isNull():
                    scaled = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    icon = QLabel(btn)
                    icon.setPixmap(scaled)
                    icon.setAlignment(Qt.AlignCenter)
                    layout = QVBoxLayout(btn)
                    layout.setContentsMargins(0, 0, 0, 0)
                    layout.addWidget(icon)

            btn.setStyleSheet("""
                QPushButton {
                    background: #2d2d2d;
                    border: 2px solid #404040;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: #3d3d3d;
                    border-color: #505050;
                }
                QPushButton:pressed {
                    background: #4d4d4d;
                }
            """)
            return btn

        # Crear botones con imágenes
        self.btn_classic = create_image_button(os.path.join('Storage', 'Icons', 'negative_01.png'))
        self.btn_classic.clicked.connect(lambda: self.parent.apply_color_mode(1))
        
        self.btn_blue = create_image_button(os.path.join('Storage', 'Icons', 'negative_02.png'))
        self.btn_blue.clicked.connect(lambda: self.parent.apply_color_mode(2))
        
        self.btn_red = create_image_button(os.path.join('Storage', 'Icons', 'negative_03.png'))
        self.btn_red.clicked.connect(lambda: self.parent.apply_color_mode(3))
        
        btn_container.addWidget(self.btn_classic)
        btn_container.addWidget(self.btn_blue)
        btn_container.addWidget(self.btn_red)
        layout.addLayout(btn_container)

        # Botón de restauración
        self.restore_btn = QPushButton('Restaurar Colores')
        self.restore_btn.clicked.connect(self.parent.restore_colors)
        self.restore_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        self.restore_btn.setCursor(Qt.PointingHandCursor)
        self.restore_btn.setFixedSize(200, 40)
        layout.addWidget(self.restore_btn, 0, Qt.AlignCenter)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.res_controller = ResolutionController()
        self.color_controller = ColorsController()
        self.outputs = self.res_controller.get_all_outputs()
        self.output = self.outputs[0] if self.outputs else None
        self.current_scale = 1.0
        self.init_ui()
    
    def resource_path(self, relative_path):
        """ Maneja rutas de recursos para desarrollo y versiones empaquetadas """
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, *relative_path.split('/'))

    def init_ui(self):
        self.setWindowTitle(f'SimuRES - v{VERSION}')
        self.setFixedSize(680, 680)

        # Widget principal y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Título
        title = QLabel('SimuRES')
        title.setFont(QFont('Segoe UI', 28, QFont.Bold))
        title.setStyleSheet('color: #00ff99;')
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Icono de estado
        self.status_icon = QLabel()
        self.status_icon.setAlignment(Qt.AlignCenter)
        self.update_status_icon('normal')
        main_layout.addWidget(self.status_icon)

        # Widget de pestañas
        tabs = QTabWidget()
        tabs.setFont(QFont('Segoe UI', 10))
        self.res_tab = ResolutionTab(self)
        self.color_tab = ColorTab(self)
        
        tabs.addTab(self.res_tab, "Resoluciones")
        tabs.addTab(self.color_tab, "Negativos")
        main_layout.addWidget(tabs)

        # Barra de estado
        self.status_bar = QFrame()
        self.status_bar.setObjectName("statusFrame")
        status_layout = QVBoxLayout(self.status_bar)
        status_layout.setContentsMargins(15, 10, 15, 10)
        self.status_msg = QLabel()
        self.status_msg.setFont(QFont('Segoe UI', 11))
        self.status_msg.setAlignment(Qt.AlignCenter)
        self.status_msg.setWordWrap(True)
        status_layout.addWidget(self.status_msg)
        main_layout.addWidget(self.status_bar)

        # Temporizador de estado
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(lambda: self.status_msg.setText(''))
        self.status_timer.setSingleShot(True)

        # Estado inicial
        if not self.outputs:
            self.update_status_icon('error')
            self.status_msg.setText("Error: No se detectaron monitores")

        # Estilos globales
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QFrame#statusFrame {
                background-color: #252525;
                border-radius: 8px;
                padding: 12px;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: #252525;
                color: #888888;
                padding: 12px 30px;
                border: none;
                font-size: 12px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #2d2d2d;
                color: #ffffff;
                border-bottom: 3px solid #00ff99;
            }
            QTabBar::tab:hover {
                background: #333333;
            }
            QComboBox {
                background: #2d2d2d;
                color: white;
                padding: 5px 10px;
                border: 1px solid #404040;
                border-radius: 4px;
            }
            QComboBox::drop-down {
                width: 25px;
                border-left: 1px solid #404040;
            }
        """)

    def update_status_icon(self, state):
        icons = {
            'normal': os.path.join('Storage', 'Icons', 'favicon_01.png'),
            'active': os.path.join('Storage', 'Icons', 'favicon_02.png'),
            'error': os.path.join('Storage', 'Icons', 'favicon_03.png')
        }
        icon_path = self.resource_path(icons[state])
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                self.status_icon.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def on_monitor_changed(self, name):
        self.output = name
        self.restore_resolution()

    def update_res_label(self):
        value = self.res_tab.slider.value() / 10
        self.res_tab.value_label.setText(f'Resolución seleccionada: {value:.1f}x')

    def apply_resolution(self):
        scale = self.res_tab.slider.value() / 10
        if scale == 1.0 and self.current_scale != 1.0:
            if self.res_controller.apply_scale(self.output, scale):
                self.show_status("Resolución base restaurada", "success")
                self.current_scale = 1.0
                self.update_status_icon('normal')
            else:
                self.show_status("Error al restaurar resolución", "error")
            return

        if self.res_controller.apply_scale(self.output, scale):
            self.show_status(f"Escala {scale}x aplicada", "success")
            self.current_scale = scale
            self.update_status_icon('active')
        else:
            self.show_status("Error al aplicar escala", "error")
            self.update_status_icon('error')

    def restore_resolution(self):
        if self.res_controller.restore_scale(self.output):
            self.res_tab.slider.setValue(10)
            self.show_status("Resolución original restaurada", "success")
            self.current_scale = 1.0
            self.update_status_icon('normal')
        else:
            self.show_status("Error al restaurar resolución", "error")

    def apply_color_mode(self, mode):
        success, msg = self.color_controller.apply_negative(mode)
        self.show_status(msg, "success" if success else "error")
        self.update_status_icon('active' if success else 'error')

    def restore_colors(self):
        success, msg = self.color_controller.restore_colors()
        self.show_status(msg, "success" if success else "error")
        self.update_status_icon('normal' if success else 'error')

    def show_status(self, message, msg_type):
        color = "#00ff99" if msg_type == "success" else "#ff4444"
        self.status_msg.setStyleSheet(f"""
            color: {color}; 
            font-weight: 500;
            padding: 3px;
        """)
        self.status_msg.setText(message)
        self.status_timer.start(3000)

    def closeEvent(self, event):
        self.restore_resolution()
        self.color_controller.restore_colors()
        event.accept()