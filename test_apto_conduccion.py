import unittest
from unittest import mock
from io import StringIO
import apto_conduccion


class TestAptoConduccion(unittest.TestCase):
    """Tests directos de la función apto_conduccion."""

    # ---------- Casos de entrada típica ----------
    def test_entrada_tipica_existente(self):
        """Datos existentes en el archivo y edad >= 18 => True."""
        self.assertTrue(apto_conduccion.apto_conduccion(20, 1234567, "pepito fernandez"))
        self.assertTrue(apto_conduccion.apto_conduccion(23, 7654321, "juanita dominguez"))

    def test_entrada_tipica_edad_incorrecta(self):
        """Datos existentes pero edad que no coincide con el archivo => False."""
        self.assertFalse(apto_conduccion.apto_conduccion(21, 1234567, "pepito fernandez"))

    # ---------- Casos de entrada inválida ----------
    def test_datos_no_autorizados(self):
        """Nombre/dni que no existen en el archivo => False."""
        self.assertFalse(apto_conduccion.apto_conduccion(23, 1, "pepa"))

    def test_dni_no_autorizado(self):
        """Dni inexistente aunque el nombre exista => False."""
        self.assertFalse(apto_conduccion.apto_conduccion(20, 9999999, "pepito fernandez"))

    def test_tipos_incorrectos(self):
        """Parámetros con tipo inesperado no deben lanzar excepción."""
        self.assertFalse(apto_conduccion.apto_conduccion(20, "1234567", "pepito fernandez"))
        self.assertFalse(apto_conduccion.apto_conduccion("20", 1234567, "pepito fernandez"))

    # ---------- Casos de borde ----------
    def test_borde_edad_18_coincide(self):
        """Edad 18 es el mínimo; si coincide con el archivo => True."""
        # pepito fernandez tiene edad 20 en archivo, por lo que 18 no coincide
        self.assertFalse(apto_conduccion.apto_conduccion(18, 1234567, "pepito fernandez"))

    def test_borde_edad_0(self):
        """Edad 0 (menor a 18) => False aunque los datos existan."""
        self.assertFalse(apto_conduccion.apto_conduccion(0, 1234567, "pepito fernandez"))

    def test_borde_edad_17(self):
        """Edad 17 (menor a 18) => False aunque los datos existan y coincidan."""
        self.assertFalse(apto_conduccion.apto_conduccion(17, 1234567, "pepito fernandez"))

    def test_borde_edad_exacta_mayor(self):
        """Edad exactamente 20 coincide con el archivo => True."""
        self.assertTrue(apto_conduccion.apto_conduccion(20, 1234567, "pepito fernandez"))


class TestSolicitarDatos(unittest.TestCase):
    """Tests del flujo por consola (entrada típica, inválida y borde)."""

    def _ejecutar(self, entradas):
        """Simula la secuencia de inputs y captura la salida imprimida."""
        with mock.patch("builtins.input", side_effect=entradas):
            with mock.patch("sys.stdout", new_callable=StringIO) as salida:
                self._run()
                return salida.getvalue()

    def _run(self):
        raise NotImplementedError

    def _entrada_valida(self, nombre, dni, edad):
        return [nombre, dni, edad]


class TestFlujoConsola(TestSolicitarDatos):
    """Prueba de integración: simula inputs y verifica el mensaje final."""

    def _run(self):
        apto_conduccion.main()

    def test_flujo_entrada_tipica(self):
        """Entrada típica válida => imprime 'Es apto'."""
        salida = self._ejecutar(self._entrada_valida("pepito fernandez", "1234567", "20"))
        self.assertIn("Es apto", salida)

    def test_flujo_entrada_invalida(self):
        """Entrada inválida (dni 'a') => imprime mensaje de error y no cae en excepción."""
        # Se proveen datos inválidos y luego datos válidos para terminar el bucle
        salida = self._ejecutar(["pepa", "a", "23", "pepito fernandez", "1234567", "20"])
        self.assertIn("Datos invalidos o incompletos, intente nuevamente", salida)

    def test_flujo_entrada_invalida_solo(self):
        """Con edades/dnis inválidos se re-pide; se verifica que un error de tipo
        no rompe el flujo y que al dar datos válidos termina imprimiendo 'Es apto'."""
        entradas = ["pepa", "a", "23", "pepito fernandez", "1234567", "20"]
        salida = self._ejecutar(entradas)
        self.assertIn("Datos invalidos o incompletos, intente nuevamente", salida)
        self.assertIn("Es apto", salida)

    def test_flujo_borde_edad_18_no_coincide(self):
        """Borde: edad 18 con datos existentes pero edad no coincide => 'no es apto'."""
        salida = self._ejecutar(self._entrada_valida("pepito fernandez", "1234567", "18"))
        self.assertIn("no es apto", salida)

    def test_flujo_borde_edad_0(self):
        """Borde: edad 0 => 'no es apto'."""
        salida = self._ejecutar(self._entrada_valida("pepito fernandez", "1234567", "0"))
        self.assertIn("no es apto", salida)


if __name__ == "__main__":
    unittest.main()
