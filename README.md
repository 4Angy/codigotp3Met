# README

## La función `_solicitarDatos`

Esta función se encarga de pedir los datos de una persona en la consola. Su único trabajo es preguntar el **nombre**, el **dni** y la **edad** del usuario.

Si los datos no son válidos (por ejemplo, si el usuario escribe "abc" donde se espera un número, o deja un campo vacío), la función vuelve a preguntar. Repite este proceso hasta que los tres datos estén bien, y entonces los entrega listos para que el resto del programa los use.

Al final devuelve los tres valores como un conjunto ordenado: primero el nombre, luego el dni y por último la edad.

> Nota: el guion bajo al inicio (`_solicitarDatos`) es una convención que indica que es una función interna de apoyo, no pensada para que se use desde fuera del programa.

## Ejemplo mínimo de uso

Como la función lee directamente de la consola, no se le pasan argumentos. Un uso típico sería:

```python
from apto_conduccion import _solicitarDatos

nombre, dni, edad = _solicitarDatos()
print(f"{nombre} tiene {edad} años y su dni es {dni}")
```

Si al ejecutarlo el usuario escribe esto:

```
Ingrese nombre: Ana
Ingrese dni: 38452110
Ingrese edad: 25
```

La variable `nombre` valdrá `"Ana"`, `dni` valdrá `38452110` y `edad` valdrá `25`.
