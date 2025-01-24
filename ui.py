# ui.py
import os
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QFrame, QComboBox)

from resolution_controller import ResolutionController





'''
>>> Versión de programa
'''
VERSION = "1.0.0"





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resolution_controller = ResolutionController()
        self.outputs = self.resolution_controller.get_all_outputs()
        self.output = self.outputs[0] if self.outputs else None
        self.current_scale = 1.0
        self.initUI()
        
    def initUI(self):
        """ Inicializar la interfaz de usuario """
        # Configuración de la ventana principal
        self.setWindowTitle(f'SimuRES - v{VERSION}')
        self.setFixedSize(600, 500)

        # Establecer el favicon
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        favicon_path = os.path.join(BASE_DIR, 'Storage', 'Icons', 'favicon_01.png')
        self.setWindowIcon(QIcon(favicon_path))

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:pressed {
                background-color: #4d4d4d;
            }
            QSlider::groove:horizontal {
                border: 1px solid #4d4d4d;
                height: 8px;
                background: #2d2d2d;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #00ff99;
                border: none;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QFrame#statusFrame {
                background-color: #2d2d2d;
                border-radius: 5px;
                padding: 10px;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                border-radius: 5px;
                padding: 8px;
                min-width: 200px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QComboBox:hover {
                background-color: #3d3d3d;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                selection-background-color: #4d4d4d;
                selection-color: #ffffff;
                border: 1px solid #4d4d4d;
            }
        """)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título
        title_label = QLabel('SimuRES')
        title_label.setFont(QFont('Segoe UI', 24))
        title_label.setStyleSheet('color: #00ff99; margin-bottom: 20px;')
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Ícono de estado
        self.status_icon_label = QLabel()
        self.status_icon_label.setAlignment(Qt.AlignCenter)
        self.update_status_icon('normal')  # Estado inicial
        layout.addWidget(self.status_icon_label)
        layout.addSpacing(10)  # Espacio adicional después del ícono

        # Estado de la pantalla con ComboBox
        screen_status = QFrame()
        screen_status.setObjectName("statusFrame")
        screen_status_layout = QHBoxLayout(screen_status)
        
        # Icono de monitor
        screen_icon = QLabel()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        monitor_png_r = os.path.join(BASE_DIR, 'Storage', 'Icons', 'monitor_01.png')
        pixmap = QPixmap(monitor_png_r)
        scaled_pixmap = pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        screen_icon.setPixmap(scaled_pixmap)
        
        # Label descriptivo
        screen_text = QLabel(' Monitor seleccionado: ')
        screen_text.setFont(QFont('Segoe UI', 12))
        
        # ComboBox para selección de monitores
        self.monitor_combo = QComboBox()
        self.monitor_combo.setFont(QFont('Segoe UI', 11))
        self.monitor_combo.addItems(self.outputs if self.outputs else ["No se detectaron monitores"])
        self.monitor_combo.currentTextChanged.connect(self.on_monitor_changed)
        self.monitor_combo.setEnabled(bool(self.outputs))
        
        screen_status_layout.addWidget(screen_icon)
        screen_status_layout.addWidget(screen_text)
        screen_status_layout.addWidget(self.monitor_combo, 1)
        layout.addWidget(screen_status)

        # Valor actual
        self.value_label = QLabel('Resolución actual: 1.0x')
        self.value_label.setFont(QFont('Segoe UI', 12))
        self.value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.value_label)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(200)
        self.slider.setValue(10)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.update_label)
        layout.addWidget(self.slider)

        # Botones
        button_layout = QHBoxLayout()
        self.apply_button = QPushButton('Aplicar cambios')
        self.apply_button.clicked.connect(self.apply_resolution)
        self.apply_button.setCursor(Qt.PointingHandCursor)
        
        self.restore_button = QPushButton('Restaurar valores')
        self.restore_button.clicked.connect(self.restore_resolution)
        self.restore_button.setCursor(Qt.PointingHandCursor)
        
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.restore_button)
        layout.addLayout(button_layout)

        # Estado
        self.status_frame = QFrame()
        self.status_frame.setObjectName("statusFrame")
        status_layout = QVBoxLayout(self.status_frame)
        self.status_label = QLabel('')
        self.status_label.setFont(QFont('Segoe UI', 12))
        self.status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_label)
        layout.addWidget(self.status_frame)

        # Timer para los mensajes de estado
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(lambda: self.status_label.setText(''))
        self.status_timer.setSingleShot(True)

        # Actualizar ícono inicial según el estado de la pantalla
        if not self.outputs:
            self.update_status_icon('error')

    def on_monitor_changed(self, monitor_name):
        """ Manejar el cambio de monitor seleccionado """
        self.output = monitor_name
        self.restore_resolution()  # Restaurar valores al cambiar de monitor

    def update_status_icon(self, status):
        """ Actualizar el ícono de estado """
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        icon_map = {
            'normal': 'favicon_01.png',
            'active': 'favicon_02.png',
            'error': 'favicon_03.png'
        }
        icon_path = os.path.join(BASE_DIR, 'Storage', 'Icons', icon_map[status])
        pixmap = QPixmap(icon_path)
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.status_icon_label.setPixmap(scaled_pixmap)

    def update_label(self):
        """ Actualizar la etiqueta con el valor actual del slider """
        value = self.slider.value() / 10
        self.value_label.setText(f'Resolución seleccionada: {value:.1f}x')

    def apply_resolution(self):
        """ Aplicar la resolución seleccionada """
        scale_factor = self.slider.value() / 10
        
        # Caso especial: cuando regresamos a 1.0x desde otra escala
        if scale_factor == 1.0 and self.current_scale != 1.0:
            if self.resolution_controller.apply_scale(self.output, scale_factor):
                self.show_status("Regresando al enfoque base", "success")
                self.current_scale = scale_factor
                self.update_status_icon('normal')
                return
            else:
                self.show_status("Error: No se detectó ninguna pantalla", "error")
                self.update_status_icon('error')
                return
                
        # Caso normal: cuando estamos en 1.0x y queremos quedarnos ahí
        if scale_factor == 1.0 and self.current_scale == 1.0:
            self.show_status("No hay cambios que aplicar", "success")
            self.update_status_icon('normal')
            return
                
        # Caso para cualquier otra escala
        if self.resolution_controller.apply_scale(self.output, scale_factor):
            self.show_status(f"Resolución aplicada: {scale_factor:.1f}x", "success")
            self.current_scale = scale_factor
            self.update_status_icon('active')
        else:
            self.show_status("Error: No se detectó ninguna pantalla", "error")
            self.update_status_icon('error')

    def restore_resolution(self):
        """ Restaurar la resolución original """
        if self.resolution_controller.restore_scale(self.output):
            self.slider.setValue(10)
            self.show_status("Resolución restaurada a valores originales", "success")
            self.current_scale = 1.0
            self.update_status_icon('normal')
        else:
            self.show_status("Error: No se detectó ninguna pantalla", "error")
            self.update_status_icon('error')

    def show_status(self, message, status_type):
        """ Mostrar mensaje de estado """
        color = "#00ff99" if status_type == "success" else "#ff4444"
        self.status_label.setStyleSheet(f"color: {color}")
        self.status_label.setText(message)
        self.status_timer.start(3000)

    def closeEvent(self, event):
        """ Evento de cierre de la ventana """
        self.restore_resolution()
        event.accept()