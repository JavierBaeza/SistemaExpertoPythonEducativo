import json
import ast 
import io  # <--- AÑADIR ESTE IMPORT
from contextlib import redirect_stdout # <--- AÑADIR ESTE IMPORT

class MotorDeInferencia:
    def __init__(self, ruta_base_conocimiento):
        """
        Inicializa el motor cargando las reglas desde un archivo JSON.
        """
        self.reglas = self._cargar_reglas(ruta_base_conocimiento)
        self.hechos = []

    def _cargar_reglas(self, ruta_archivo):
        """Carga las reglas desde el archivo JSON."""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de reglas en {ruta_archivo}")
            return []
        except json.JSONDecodeError:
            print(f"Error: El archivo de reglas en {ruta_archivo} no es un JSON válido.")
            return []

    def diagnosticar(self, codigo):
        """
        Evalúa un fragmento de código contra la base de conocimiento.
        """
        diagnosticos = []
        self.hechos = self._extraer_hechos(codigo)

        for regla in self.reglas:
            funcion_condicion = getattr(self, regla["condicion"], None)
            
            if funcion_condicion is None:
                print(f"Advertencia: La condición '{regla['condicion']}' definida en JSON no existe en la clase MotorDeInferencia.")
                continue

            if funcion_condicion(codigo):
                diagnosticos.append({
                    "error_id": regla.get("error_id", "N/A"),
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

    # --- Funciones de Condición (Checks) ---

    # --- Checks de Sintaxis (AST Parse) --- (Sin cambios)

    def check_syntax(self, codigo):
        """
        Verifica si hay errores de sintaxis GENERALES,
        excluyendo errores de indentación.
        """
        try:
            ast.parse(codigo)
        except IndentationError:
            return False 
        except SyntaxError:
            return True 
        return False

    def check_indentation(self, codigo):
        """
        Verifica si hay errores de indentación (incluyendo TabError).
        """
        try:
            ast.parse(codigo)
        except IndentationError:
            return True 
        except SyntaxError:
            #  Ignora otros errores de sintaxis
            return False 
        return False

    # --- Checks de Runtime (exec) --- (MODIFICADOS)

    def check_name_error(self, codigo):
        """Verifica si hay un NameError al intentar ejecutar."""
        f = io.StringIO()
        with redirect_stdout(f): # Silencia la salida
            try:
                exec(codigo, {}, {})
            except NameError:
                return True
            except Exception:
                return False
        return False
        
    def check_type_error(self, codigo):
        """Verifica si ocurre un TypeError al ejecutar."""
        f = io.StringIO()
        with redirect_stdout(f): # Silencia la salida
            try:
                exec(codigo, {}, {})
            except TypeError:
                return True
            except Exception:
                return False
        return False

    def check_index_error(self, codigo):
        """Verifica si ocurre un IndexError (índice fuera de rango)."""
        f = io.StringIO()
        with redirect_stdout(f): # Silencia la salida
            try:
                exec(codigo, {}, {})
            except IndexError:
                return True
            except Exception:
                return False
        return False

    def check_key_error(self, codigo):
        """Verifica si ocurre un KeyError (llave de diccionario no encontrada)."""
        f = io.StringIO()
        with redirect_stdout(f): # Silencia la salida
            try:
                exec(codigo, {}, {})
            except KeyError:
                return True
            except Exception:
                return False
        return False

    def check_attribute_error(self, codigo):
        """Verifica si ocurre un AttributeError (atributo o método incorrecto)."""
        f = io.StringIO()
        with redirect_stdout(f): # Silencia la salida
            try:
                exec(codigo, {}, {})
            except AttributeError:
                return True
            except Exception:
                return False
        return False

    def check_zero_division_error(self, codigo):
        """Verifica si ocurre una división por cero."""
        f = io.StringIO()
        with redirect_stdout(f): # Silencia la salida
            try:
                exec(codigo, {}, {})
            except ZeroDivisionError:
                return True
            except Exception:
                return False
        return False
        
    # --- Checks Estáticos (AST Walk) --- (Sin cambios)
    
    def check_uso_de_eval(self, codigo):
        """Verifica estáticamente si el código usa la función 'eval()'."""
        try:
            tree = ast.parse(codigo)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == 'eval':
                        return True
        except SyntaxError:
            return False
        return False

    def check_mutable_default_args(self, codigo):
        """
        Verifica estáticamente el uso de listas/dicts como argumentos por defecto.
        """
        try:
            tree = ast.parse(codigo)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for default in node.args.defaults:
                        if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                            return True
                    for default in node.args.kw_defaults:
                        if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                            return True
        except SyntaxError:
            return False
        return False