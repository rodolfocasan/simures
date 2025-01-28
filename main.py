# main.py
import sys
import signal
import argparse
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor

from _ascii import logo_01

from ui import MainWindow
from resolution_controller import ResolutionController
from colors_controller import ColorsController





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
        description=f'{logo_01()}\nSimuRES - Herramienta de escalado de resolución y simulación de negativos\n\n'
                    'Modos de uso:\n'
                    '  GUI: Ejecutar sin argumentos\n'
                    '  CLI: \n'
                    '    - Escalar resolución: --start <valor> [--output <pantalla>]\n'
                    '    - Aplicar negativo:   --cneg --mode <1|2|3>\n'
                    '    - Restaurar valores:  --stop\n'
                    '    - Listar pantallas:   --list-outputs',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='Ejemplos:\n'
               '  main.py --start 1.5 --output HDMI-1  # Escala 1.5x en HDMI-1\n'
               '  main.py --cneg --mode 1              # Aplica negativo clásico\n'
               '  main.py --cneg --mode 2              # Aplica negativo frío\n'
               '  main.py --cneg --mode 3              # Aplica negativo cálido\n'
               '  main.py --stop                       # Restaura resolución y colores\n'
               '  main.py --list-outputs               # Lista pantallas disponibles\n'
               '  main.py                              # Inicia interfaz gráfica\n\n'
               'Notas:\n'
               '  - El argumento --mode solo puede usarse junto con --cneg\n'
               '  - Los modos de negativo son: 1=Clásico, 2=Frío, 3=Cálido'
    )
    parser.add_argument('--start', type=float, metavar='VALOR',
                       help='Factor de escala (1.0 a 20.0)')
    parser.add_argument('--stop', action='store_true',
                       help='Restaurar resolución y colores originales')
    parser.add_argument('--list-outputs', action='store_true',
                       help='Listar todas las pantallas disponibles')
    parser.add_argument('--output', type=str, metavar='NOMBRE',
                       help='Especificar nombre de salida de pantalla')
    parser.add_argument('--cneg', action='store_true',
                       help='Activar modo de color negativo (requiere --mode)')
    parser.add_argument('--mode', type=int, choices=[1, 2, 3],
                       help='Modo de negativo (solo usar con --cneg): 1=Clásico, 2=Frío, 3=Cálido')
    
    args = parser.parse_args()

    # Validar combinación de argumentos
    if args.mode and not args.cneg:
        print("[ERROR] El argumento --mode solo puede usarse junto con --cneg")
        sys.exit(1)

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

    # Inicializar controladores
    res_controller = ResolutionController()
    color_controller = ColorsController()

    # Modo CLI
    if args.start or args.stop or args.cneg:
        # Validar combinación de argumentos
        if args.cneg and not args.mode and not args.stop:
            print("[ERROR] --cneg requiere especificar --mode (1, 2 o 3)")
            sys.exit(1)

        # Manejar --stop (restaurar todo)
        if args.stop:
            success_res = True
            success_color, msg_color = color_controller.restore_colors()
            
            # Restaurar resolución solo si se especificó una salida o si hay una pantalla detectada
            if args.output:
                success_res = res_controller.restore_scale(args.output)
            else:
                output = res_controller.get_output_name()
                if output:
                    success_res = res_controller.restore_scale(output)
            
            if success_res and success_color:
                print("[OK] Valores originales restaurados")
                sys.exit(0)
            else:
                print("[ERROR] Fallo al restaurar uno o más valores")
                sys.exit(1)

        # Manejar --start (escalar resolución)
        if args.start:
            outputs = res_controller.get_all_outputs()
            
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
                output = res_controller.get_output_name()
                if not output:
                    print("[ERROR] No se detectaron pantallas")
                    sys.exit(1)

            # Configurar manejador de señales
            signal.signal(signal.SIGINT, handle_cli_signals(output))
            signal.signal(signal.SIGTERM, handle_cli_signals(output))
            
            if not 1.0 <= args.start <= 20.0:
                print("[ERROR] Escala debe estar entre 1.0 y 20.0")
                sys.exit(1)
                
            if res_controller.apply_scale(output, args.start):
                print(f"[OK] Escala {args.start}x aplicada en {output}")
            else:
                print("[ERROR] Fallo al aplicar escala")
                sys.exit(1)

        # Manejar --cneg (aplicar negativo)
        if args.cneg:
            if args.mode:
                success, msg = color_controller.apply_negative(args.mode)
                if success:
                    mode_names = {1: "clásico", 2: "frío", 3: "cálido"}
                    print(f"[OK] Modo negativo {mode_names[args.mode]} aplicado")
                    if "Advertencia" in msg:
                        print(f"[WARN] {msg}")
                else:
                    print(f"[ERROR] {msg}")
                    sys.exit(1)
        sys.exit(0)

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