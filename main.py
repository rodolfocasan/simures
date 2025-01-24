# main.py
import sys
import signal
import argparse
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor

from _ascii import logo_01

from ui import MainWindow
from resolution_controller import ResolutionController





'''
>>> Definición de funciones
'''
def signal_handler(sig, frame):
    """ Manejador de señales para cierres forzados """
    print(f"\n[WARN] Señal recibida ({sig}), restaurando resolución...")
    app = QApplication.instance()
    if app:
        window = app.activeWindow()
        if window:
            window.restore_resolution()
    sys.exit(0)

def handle_cli_signals(output):
    """ Retorna un manejador de señales con la salida especificada """
    def handler(sig, frame):
        print(f"\n[INTERRUPCIÓN] Restaurando resolución en {output}...")
        controller = ResolutionController()
        controller.restore_scale(output)
        sys.exit(0)
    return handler

def main():
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(
        prog='main.py',
        description=f'{logo_01()}\nSimuRES - Herramienta de escalado de resolución\n\n'
                    'Modos de uso:\n'
                    '  GUI: Ejecutar sin argumentos\n'
                    '  CLI: Usar --start para aplicar escala o --stop para restaurar',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='Ejemplos:\n'
               '  main.py --start 1.5 --output HDMI-1  # Escala 1.5x en HDMI-1\n'
               '  main.py --stop --output HDMI-1       # Restaura HDMI-1\n'
               '  main.py --list-outputs               # Lista pantallas disponibles\n'
               '  main.py                              # Inicia interfaz gráfica'
    )
    parser.add_argument('--start', type=float, metavar='VALOR',
                       help='Factor de escala (1.0 a 20.0)')
    parser.add_argument('--stop', action='store_true',
                       help='Restaurar resolución original')
    parser.add_argument('--list-outputs', action='store_true',
                       help='Listar todas las pantallas disponibles')
    parser.add_argument('--output', type=str, metavar='NOMBRE',
                       help='Especificar nombre de salida de pantalla')
    
    args = parser.parse_args()

    # Manejar --list-outputs primero
    if args.list_outputs:
        controller = ResolutionController()
        outputs = controller.get_all_outputs()
        if outputs:
            print("Pantallas disponibles:")
            for out in outputs:
                print(f"  - {out}")
            sys.exit(0)
        else:
            print("[ERROR] No se detectaron pantallas")
            sys.exit(1)

    # Modo CLI
    if args.start or args.stop:
        controller = ResolutionController()
        outputs = controller.get_all_outputs()
        
        # Validar --output si se especificó
        output = None
        if args.output:
            if args.output in outputs:
                output = args.output
            else:
                print(f"[ERROR] La pantalla '{args.output}' no existe")
                if outputs:
                    print("Pantallas disponibles:", ", ".join(outputs))
                else:
                    print("No se detectaron pantallas disponibles")
                sys.exit(1)
        else:
            output = controller.get_output_name()
            if not output:
                print("[ERROR] No se detectaron pantallas")
                sys.exit(1)

        # Configurar manejador de señales con la salida específica
        signal.signal(signal.SIGINT, handle_cli_signals(output))
        signal.signal(signal.SIGTERM, handle_cli_signals(output))
        
        if args.start:
            if not 1.0 <= args.start <= 20.0:
                print("[ERROR] Escala debe estar entre 1.0 y 20.0")
                sys.exit(1)
                
            if controller.apply_scale(output, args.start):
                print(f"[OK] Escala {args.start}x aplicada en {output}")
                sys.exit(0)
            else:
                print("[ERROR] Fallo al aplicar escala")
                sys.exit(1)
                
        elif args.stop:
            if controller.restore_scale(output):
                print(f"[OK] Resolución restaurada en {output}")
                sys.exit(0)
            else:
                print("[ERROR] Fallo al restaurar")
                sys.exit(1)

    # Modo GUI
    else:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        app = QApplication(sys.argv)
        
        # Configurar paleta de colores
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#1e1e1e"))
        palette.setColor(QPalette.WindowText, QColor("#ffffff"))
        app.setPalette(palette)
        
        window = MainWindow()
        window.show()
        
        try:
            sys.exit(app.exec_())
        except Exception as e:
            print("[ERROR] Error inesperado:", e)
            window.restore_resolution()





'''
>>> Inicialización
'''
if __name__ == '__main__':
    main()