def apto_conduccion(edad: int, dni: int, nombre: str) -> bool:
    """Determina si una persona es apta para conducir.

    Condiciones:
    - edad >= 18
    - los datos (nombre, dni) deben coincidir con una entrada de
      "autorizadosAconducir.txt"

    Args:
        edad (int): edad de la persona.
        dni (int): documento de la persona.
        nombre (str): nombre de la persona.

    Returns:
        bool: True si es apto, False si no cumple alguna condición.
    """
    try:
        esApto: bool = edad >= 18 and _existeAutorizado(nombre, dni, edad)
    except Exception:
        esApto = False
    return esApto


def _existeAutorizado(nombre: str, dni: int, edad: int) -> bool:
    """Verifica si nombre, dni y edad coinciden con alguna línea del archivo autorizado."""
    try:
        if not isinstance(nombre, str) or not isinstance(dni, int) or not isinstance(edad, int):
            return False
        with open("autorizadosAconducir.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                try:
                    linea = linea.strip()
                    if not linea:
                        continue
                    partes = linea.split(";")
                    if len(partes) == 3:
                        nombreArchivo, dniArchivo, edadArchivo = partes
                        if (nombreArchivo.strip().lower() == nombre.strip().lower()
                                and int(dniArchivo.strip()) == dni
                                and int(edadArchivo.strip()) == edad):
                            return True
                except (IndexError, ValueError):
                    continue
    except (FileNotFoundError, OSError):
        return False
    return False


def _solicitarDatos() -> tuple:
    """Solicita y valida los datos de entrada por consola."""
    while True:
        try:
            nombre = input("Ingrese nombre: ").strip()
            dni = input("Ingrese dni: ").strip()
            edad = input("Ingrese edad: ").strip()
        except Exception:
            print("Datos invalidos o incompletos, intente nuevamente")
            continue

        # Datos incompletos o error de tipo
        if not nombre or not dni or not edad:
            print("Datos invalidos o incompletos, intente nuevamente")
            continue
        try:
            dniValido = int(dni)
            edadValida = int(edad)
        except Exception:
            print("Datos invalidos o incompletos, intente nuevamente")
            continue
        return nombre, dniValido, edadValida


def main() -> None:
    """Función principal: solicita datos, evalúa aptitud e imprime el resultado."""
    nombre, dni, edad = _solicitarDatos()
    esApto: bool = apto_conduccion(edad, dni, nombre)
    print("Es apto" if esApto else "no es apto")


if __name__ == "__main__":
    main()
