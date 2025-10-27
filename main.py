from motor_inferencia import MotorDeInferencia

def main():
    """
    Función principal para ejecutar el sistema experto.
    """
    # Inicializamos el motor con la base de conocimiento
    motor = MotorDeInferencia("base_conocimiento.json")

    print("--- Sistema Experto para Detección de Errores en Python ---")
    print("Por favor, introduce tu código. Escribe 'salir' para terminar.")
    print("-" * 60)

    codigo_usuario = []
    while True:
        linea = input("> ")
        if linea.lower() == "salir":
            break
        codigo_usuario.append(linea)

    codigo_completo = "\n".join(codigo_usuario)

    if not codigo_completo.strip():
        print("\nNo se ha introducido código.")
        return

    print("\n--- Analizando tu código... ---")
    diagnosticos = motor.diagnosticar(codigo_completo)

    if not diagnosticos:
        print("\n¡Felicitaciones! No se encontraron errores comunes en tu código.")
    else:
        print("\nSe encontraron los siguientes problemas:")
        for i, diag in enumerate(diagnosticos, 1):
            print(f"\n--- Problema #{i}: {diag['nombre']} ---")
            print(f"  Mensaje: {diag['mensaje']}")
            print(f"  Explicación: {diag['explicacion']}")
            print("-" * (len(diag['nombre']) + 18))

if __name__ == "__main__":
    main()