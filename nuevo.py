"""Calculadora infinita interactiva.

Escribe expresiones matemáticas y pulsa Enter para ver el resultado.
Escribe "salir" o "q" para terminar.
"""

import ast
import operator
import math

ALLOWED_OPERATIONS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

ALLOWED_FUNCTIONS = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'log10': math.log10,
    'exp': math.exp,
    'abs': abs,
    'round': round,
    'ceil': math.ceil,
    'floor': math.floor,
    'factorial': math.factorial,
    'pi': math.pi,
    'e': math.e,
}


def evaluar_expresion(expr: str) -> float:
    nodo = ast.parse(expr, mode='eval')
    return _evaluar_nodo(nodo.body)


def _evaluar_nodo(nodo):
    if isinstance(nodo, ast.BinOp):
        izquierda = _evaluar_nodo(nodo.left)
        derecha = _evaluar_nodo(nodo.right)
        operador_func = ALLOWED_OPERATIONS.get(type(nodo.op))
        if operador_func is None:
            raise ValueError(f"Operador no permitido: {type(nodo.op).__name__}")
        return operador_func(izquierda, derecha)

    if isinstance(nodo, ast.UnaryOp):
        operador_func = ALLOWED_OPERATIONS.get(type(nodo.op))
        if operador_func is None:
            raise ValueError(f"Operador unario no permitido: {type(nodo.op).__name__}")
        return operador_func(_evaluar_nodo(nodo.operand))

    if isinstance(nodo, ast.Num):
        return nodo.n

    if isinstance(nodo, ast.Constant):
        if isinstance(nodo.value, (int, float)):
            return nodo.value
        raise ValueError(f"Constante no permitida: {nodo.value}")

    if isinstance(nodo, ast.Call):
        if not isinstance(nodo.func, ast.Name):
            raise ValueError("Llamada de función no permitida")
        nombre = nodo.func.id
        función = ALLOWED_FUNCTIONS.get(nombre)
        if función is None:
            raise ValueError(f"Función no permitida: {nombre}")
        argumentos = [_evaluar_nodo(arg) for arg in nodo.args]
        return función(*argumentos)

    if isinstance(nodo, ast.Name):
        valor = ALLOWED_FUNCTIONS.get(nodo.id)
        if valor is None:
            raise ValueError(f"Nombre no permitido: {nodo.id}")
        return valor

    raise ValueError(f"Expresión no permitida: {type(nodo).__name__}")


def main() -> None:
    nombre = input('¿Cuál es tu nombre? ').strip() or 'Usuario'
    print(f"Hola, {nombre}! Bienvenido a la calculadora infinita.")
    print("Escribe expresiones como 2+2, 5*3, sqrt(16), log(10) y pulsa Enter.")
    print("Escribe 'salir' o 'q' para terminar.")

    while True:
        try:
            linea = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print(f'\nSaliendo... ¡Hasta luego, {nombre}!')
            break

        if not linea:
            continue
        if linea.lower() in {'salir', 'q', 'quit', 'exit'}:
            print('Hasta luego!')
            break
        if linea.lower() in {'ayuda', 'help', 'h'}:
            print('Puedes usar: + - * / ** % y funciones: sqrt, sin, cos, tan, log, log10, exp, abs, round, ceil, floor, factorial')
            continue

        try:
            resultado = evaluar_expresion(linea)
            print(resultado)
        except Exception as error:
            print(f"Error: {error}")


if __name__ == '__main__':
    main()
