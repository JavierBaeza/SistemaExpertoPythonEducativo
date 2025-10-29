from motor_inferencia import MotorDeInferencia

def main():
    """
    Función principal para ejecutar el sistema experto en un ciclo.
    """
    # Inicializamos el motor con la base de conocimiento
    motor = MotorDeInferencia("base_conocimiento.json")

    print("--- Sistema Experto para Detección de Errores en Python ---")
    print("Comandos:")
    print("  - Escribe tu código línea por línea.")
    print("  - Escribe 'analizar' en una línea nueva para evaluar el código.")
    print("  - Escribe 'salir' en una línea nueva para terminar el programa.")
    print("-" * 60)

    # Bucle principal del programa
    while True:
        print("\n(Modo de entrada: escribe 'analizar' para procesar, 'salir' para terminar)")
        codigo_usuario = []
        
        # Bucle de entrada de código
        while True:
            try:
                linea = input("> ")
            except EOFError:
                # Manejar Ctrl+D como 'salir'
                linea = "salir"

            if linea.lower().strip() == "salir":
                print("\n¡Hasta pronto!")
                return  # Termina la función main y el programa
            
            if linea.lower().strip() == "analizar":
                break  # Rompe el bule de entrada para ir al análisis
            
            codigo_usuario.append(linea)

        codigo_completo = "\n".join(codigo_usuario)

        if not codigo_completo.strip():
            print("\nNo se ha introducido código. Escribe de nuevo o 'salir'.")
            continue  # Vuelve al inicio del bule principal

        # --- 1. ANÁLISIS DE ERRORES ---
        print("\n--- Analizando tu código... ---")
        diagnosticos = motor.diagnosticar(codigo_completo)

        # --- 2. EJECUCIÓN (SI ES SEGURO) ---
        
        # Revisamos si hay errores que impiden la ejecución (Sintaxis/Indentación)
        # Estos son los 'error_id' de tu JSON
        errores_bloqueantes = {"E001", "E002"} 
        hay_error_critico = False
        
        for diag in diagnosticos:
            if diag.get("error_id") in errores_bloqueantes:
                hay_error_critico = True
                break

        if not hay_error_critico:
            print("\n--- Resultado de la Ejecución ---")
            try:
                # Usamos un entorno global para que las variables (como 'x' e 'y')
                # se compartan entre las líneas del código ejecutado.
                entorno_global = {} 
                exec(codigo_completo, entorno_global)
            except Exception as e:
                # Captura cualquier error de runtime (NameError, TypeError, etc.)
                # que ocurrió durante la ejecución real.
                print(f"Error durante la ejecución: {type(e).__name__}: {e}")
            print("--- Fin de la Ejecución ---")
        else:
            print("\nEl código no se ejecutará debido a errores de sintaxis o indentación.")


        # --- 3. REPORTE DE DIAGNÓSTICO ---
        if not diagnosticos:
            print("\n¡Felicitaciones! No se encontraron errores comunes en tu código.")
        else:
            print("\nSe encontraron los siguientes problemas:")
            for i, diag in enumerate(diagnosticos, 1):
                print(f"\n--- Problema #{i}: {diag['nombre']} (ID: {diag.get('error_id', 'N/A')}) ---")
                print(f"  Mensaje: {diag['mensaje']}")
                print(f"  Explicación: {diag['explicacion']}")
                print("-" * (len(diag['nombre']) + 24))
        
        print("\n" + "=" * 60)
        print("Listo para un nuevo análisis.")

if __name__ == "__main__":
    main()