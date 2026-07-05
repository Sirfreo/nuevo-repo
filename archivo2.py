"""Calculadora simple mejorada."""

import ast
import math
import operator

OPERACIONES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

FUNCIONES = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'exp': math.exp,
    'abs': abs,
}

NOMBRES = {
    'pi': math.pi,
    'e': math.e,
}


def evaluar_expresion(expr: str) -> float:
    nodo = ast.parse(expr, mode='eval')
    return _evaluar(nodo.body)


def _evaluar(nodo):
    if isinstance(nodo, ast.BinOp):
        izquierda = _evaluar(nodo.left)
        derecha = _evaluar(nodo.right)
        op = OPERACIONES.get(type(nodo.op))
        if op is None:
            raise ValueError('Operador no permitido')
        return op(izquierda, derecha)

    if isinstance(nodo, ast.UnaryOp):
        op = OPERACIONES.get(type(nodo.op))
        if op is None:
            raise ValueError('Operador unario no permitido')
        return op(_evaluar(nodo.operand))

    if isinstance(nodo, ast.Constant):
        if isinstance(nodo.value, (int, float)):
            return nodo.value
        raise ValueError('Solo números permitidos')

    if isinstance(nodo, ast.Name):
        valor = NOMBRES.get(nodo.id)
        if valor is None:
            raise ValueError(f'Nombre no permitido: {nodo.id}')
        return valor

    if isinstance(nodo, ast.Call):
        if not isinstance(nodo.func, ast.Name):
            raise ValueError('Llamada de función inválida')
        func = FUNCIONES.get(nodo.func.id)
        if func is None:
            raise ValueError(f'Función no permitida: {nodo.func.id}')
        args = [_evaluar(arg) for arg in nodo.args]
        return func(*args)

    raise ValueError('Expresión no permitida')


def main() -> None:
    nombre = input('ramon').strip() or 'Usuario'
    print(f'Hola {nombre}, esta es tu calculadora simple.')
    print('Usa operadores: + - * / ** % y funciones: sqrt, sin, cos, tan, log, exp, abs')
    print('Escribe "salir" o "q" para terminar.')

    while True:
        expr = input('> ').strip()
        if not expr:
            continue
        if expr.lower() in {'salir', 'q', 'exit', 'quit'}:
            print(f'Adiós, {nombre}!')
            break
        try:
            print(evaluar_expresion(expr))
        except Exception as exc:
            print('Error:', exc)


if __name__ == '__main__':
    main()
