import json
import ast 

class MotorDeInferencia:
    def __init__(self, ruta_base_conocimiento):
        """
        Inicializa el motor cargando las reglas desde un archivo JSON.
        """
        self.reglas = self._cargar_reglas(ruta_base_conocimiento)
        self.hechos = []

    def _cargar_reglas(self, ruta_archivo):
        """Carga las reglas desde el archivo JSON."""
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return json.load(f)

    def diagnosticar(self, codigo):
        """
        Evalúa un fragmento de código contra la base de conocimiento.
        """
        diagnosticos = []
        self.hechos = self._extraer_hechos(codigo)

        for regla in self.reglas:
            funcion_condicion = getattr(self, regla["condicion"])
            if funcion_condicion(codigo):
                diagnosticos.append({
                    "nombre": regla["nombre"],
                    "mensaje": regla["mensaje"],
                    "explicacion": regla["explicacion"]
                })
        return diagnosticos

    def _extraer_hechos(self, codigo):
        """
        Función simple para simular la extracción de hechos.
        """
        hechos = []
        if "print" in codigo:
            hechos.append("usa_print")
        if "if" in codigo:
            hechos.append("usa_condicional")
        return hechos

    # --- Funciones de Condición  ---

    def check_syntax(self, codigo):
        """
        Verifica si hay errores de sintaxis en el código.
        """
        try:
            ast.parse(codigo)
        except SyntaxError:
            # Encontró el error que buscaba
            return True
        return False

    def check_indentation(self, codigo):
        """
        Verifica errores de indentación.
        """
        try:
            ast.parse(codigo)
        except IndentationError:
            # Encontró el error que buscaba
            return True
        except SyntaxError:
            #  Ignora otros errores de sintaxis
            return False 
        return False

    def check_name_error(self, codigo):
        """
        Verifica si hay un NameError al intentar ejecutar el código.
        """
        try:
            # Ejecutamos el código en un entorno vacío
            exec(codigo, {})
        except NameError:
            # Encontró el error que buscaba
            return True
        except Exception:
            #  Ignora cualquier otro error (incluido SyntaxError)
            return False
        return False