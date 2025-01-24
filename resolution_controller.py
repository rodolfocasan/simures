# resolution_controller.py
import subprocess





class ResolutionController:
    @staticmethod
    def get_output_name():
        """ Obtener el nombre de la pantalla conectada """
        try:
            result = subprocess.check_output(["xrandr"]).decode("utf-8")
            for line in result.splitlines():
                if " connected" in line:
                    return line.split()[0]
        except Exception as e:
            print("Error obteniendo la salida de video:", e)
            return None

    @staticmethod
    def get_all_outputs():
        """ Obtener lista de todas las pantallas conectadas """
        try:
            result = subprocess.check_output(["xrandr"]).decode("utf-8")
            outputs = []
            for line in result.splitlines():
                if " connected" in line:
                    outputs.append(line.split()[0])
            return outputs
        except Exception as e:
            print("Error obteniendo las salidas de video:", e)
            return []

    @staticmethod
    def apply_scale(output, scale_factor):
        """ Aplicar un factor de escala a la resolución """
        if output:
            cmd = f"xrandr --output {output} --scale {scale_factor}x{scale_factor}"
            subprocess.run(cmd, shell=True)
            return True
        return False

    @staticmethod
    def restore_scale(output):
        """ Restaurar la resolución original """
        if output:
            cmd = f"xrandr --output {output} --scale 1x1"
            subprocess.run(cmd, shell=True)
            return True
        return False