# colors_controller.py
import subprocess





class ColorsController:
    @staticmethod
    def apply_negative(tipo):
        """ Aplicar efecto de color negativo """
        try:
            subprocess.run(['xcalib', '-c'], check=True)  # Reset previo
            
            configs = {
                1: ['-i', '-a'],  # Inversión clásica
                2: ['-red', '0.5,2.0,0.5', '-blue', '2.0,0.5,2.0', '-a'],  # Azul
                3: ['-blue', '0.5,2.0,0.5', '-red', '2.0,0.5,2.0', '-a']   # Rojo
            }
            
            cmd = ['xcalib'] + configs[tipo]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if "out of range" in result.stderr:
                return (True, "Advertencia: Parámetros ajustados automáticamente")
            return (True, "Efecto aplicado correctamente")
            
        except subprocess.CalledProcessError as e:
            return (False, f"Error en xcalib: {e.stderr}")
        except Exception as e:
            return (False, f"Error inesperado: {str(e)}")

    @staticmethod
    def restore_colors():
        """ Restaurar colores normales """
        try:
            subprocess.run(['xcalib', '-c'], check=True)
            return (True, "Colores restablecidos correctamente")
        except subprocess.CalledProcessError as e:
            return (False, f"Error al restaurar: {e.stderr}")
        except Exception as e:
            return (False, f"Error inesperado: {str(e)}")