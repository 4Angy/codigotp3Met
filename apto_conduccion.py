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
    if not isinstance(nombre, str) or not isinstance(dni, int) or not isinstance(edad, int):
        return False

    def coincide(linea: str) -> bool:
        try:
            nombreArchivo, dniArchivo, edadArchivo = linea.strip().split(";")
        except ValueError:
            return False
        try:
            return (nombreArchivo.strip().lower() == nombre.strip().lower()
                    and int(dniArchivo.strip()) == dni
                    and int(edadArchivo.strip()) == edad)
        except ValueError:
            return False

    try:
        with open("autorizadosAconducir.txt", "r", encoding="utf-8") as archivo:
            return any(coincide(linea) for linea in archivo if linea.strip())
    except (FileNotFoundError, OSError):
        return False


def _solicitarDatos() -> tuple:
    """Solicita y valida los datos de entrada por consola.

    Establece un ciclo de entrada/salida bloqueante (input) en el que el
    usuario digita nombre, dni y edad hasta conseguir una terna válida.
    Devuelve siempre una terna normalizada y validada; nunca retorna
    valores vacíos ni no numéricos para dni/edad.

    Args:
        Sin parámetros. Lee directamente de la entrada estándar (input).

    Returns:
        tuple[str, int, int]: (nombre, dni, edad), donde:
            - nombre: str sin espacios al inicio/fin, no vacío, sin
              normalización de mayúsculas.
            - dni: int positivo, resultado de int() sobre la entrada.
            - edad: int, resultado de int() sobre la entrada.

    Raises:
        No lanza excepciones hacia fuera: ante cualquier fallo de
        lectura o conversión, repite la solicitud pidiendo reintentar.
        Excepciones internas capturadas y absorbidas:
            - EOFError: si se cierra la entrada sin datos (heredado de
              input, aquí atrapado por el except Exception del read).
            - KeyboardInterrupt: NO se captura (hereda de Exception en
              Python 3 solo si así está definido); en la práctica
              interrumpe el ciclo. No documentar como manejo.
            - ValueError: conversión de dni/edad no numérica.
            - UnboundLocalError / NameError: no aplican.

    Invariantes:
        - El bucle while True solo termina por la sentencia return de la
          terna válida; toda iteración fallida descarga a via continue.
        - Post-condición: las dos posiciones numéricas del tuple son
          int poseedores de todos los dígitos de la entrada (no se
          renormalizan, se toma el valor tal cual lo interpreta int()).
        - Pre-condición de main: el tuple devuelto siempre tiene tamaño 3
          (desempaquetado seguro en main).

    Casos de borde:
        - Entrada en blanco o solo espacios: rechazada en el primer
          filtro (not nombre/dni/edad con el .strip() previo).
        - dni/edad no numéricos (ej.: "abc", "12a"): rechazada por
          int() y solicita reintentar.
        - Números con signo o espacio interno (ej.: " 12 " o "-3"): el
          strip elimina espacios externos; "-3" es aceptado como int
          negativo por int() (invariante NO excluye negativos).
        - DNI o edad negativos: no validados; int() los acepta y se
          devuelven tal cual (quien invoque debe interpretarlos).
        - stdout piped más allá de la consola (input con flujo no tty):
          depende del entorno de ejecución; el ciclo puede no devolver
          nunca si el stream se cierra limpiamente sin EOFError.
        - Reintento infinito: si el usuario nunca ingresa una terna
          válida, el ciclo no tiene límite de intentos ni opción de
          abortar (salvo KeyboardInterrupt/EOF).
    """
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