import flet as ft
import re

def main(page: ft.Page):
    page.title = "Calculadora"
    page.bgcolor = "#2d2d2d"
    page.window.width = 350
    page.window.height = 300

    total_values = ""

    resultado_texto = ft.Text(value="0", size=28, color="white", text_align="right")

    def entrar_valor(e):
        nonlocal total_values
        total_values += str(e.control.text)
        resultado_texto.value = total_values
        page.update()

    def limpar_tela(e):
        nonlocal total_values
        total_values = ""
        resultado_texto.value = "0"
        page.update()

    def calculo(e):
        nonlocal total_values
        try:
            resultado_texto.value = str(eval(total_values))
            total_values = resultado_texto.value
        except:
            resultado_texto.value = "Error"
            total_values = ""
        page.update()

    def backspace(e):
        nonlocal total_values
        total_values = total_values[:-1]
        resultado_texto.value = total_values if total_values else "0"
        page.update()

    def calcular_porcentagem(e):
        nonlocal total_values

        try:
            exp = total_values
            m = re.search(r"^(.+?)([+\-*/])(\d+\.?\d*)$", exp)
            if m:
                lhs_str, op, rhs_str = m.groups()
                lhs = eval(lhs_str)
                rhs = float(rhs_str)
                
                if op == "+":
                    result = lhs + (lhs * rhs / 100)
                elif op == "-":
                    result = lhs - (lhs * rhs / 100)
                elif op == "*":
                    result = lhs * (rhs / 100)
                else:
                    result = lhs / (rhs / 100)
            else:
                valor = eval(exp)
                result = valor / 100
                
            total_values = str(result)
            resultado_texto.value = total_values
        except Exception:
            resultado_texto.value = "Erro"
            total_values = ""
        page.update()






    display = ft.Container(
        content=resultado_texto,
        bgcolor="#37474F",
        padding=10,
        border_radius=10,
        height=70,
        alignment=ft.alignment.center_right
    )

    estilo_numeros = {
        "height": 60,
        "bgcolor":"#4d4d4d",
        "color":"white",
        "expand":1,
    }

    estilo_operadores = {
        "height": 60,
        "bgcolor":"#FF9500",
        "color":"white",
        "expand":1,
    }

    estilo_limpar = {
        "height": 60,
        "bgcolor":"#FF3B30",
        "color":"white",
        "expand":1,
    }

    estilo_igual = {
        "height": 60,
        "bgcolor":"#34C759",
        "color":"white",
        "expand":1,
    }


    grid_botoes = [
        [("C", estilo_limpar, limpar_tela),
        ("%", estilo_operadores, calcular_porcentagem),
        ("/", estilo_operadores, entrar_valor),
        ("*", estilo_operadores, entrar_valor)
        ],

        [("7", estilo_numeros, entrar_valor),
        ("8", estilo_numeros, entrar_valor),
        ("9", estilo_numeros, entrar_valor),
        ("-", estilo_operadores, entrar_valor)
        ],

        [("4", estilo_numeros, entrar_valor),
        ("5", estilo_numeros, entrar_valor),
        ("6", estilo_numeros, entrar_valor),
        ("+", estilo_operadores, entrar_valor)
        ],

        [("1", estilo_numeros, entrar_valor),
        ("2", estilo_numeros, entrar_valor),
        ("3", estilo_numeros, entrar_valor),
        ("=", estilo_igual, calculo)
        ],

        [("0", {**estilo_numeros, "expand":2}, entrar_valor),
        (".", estilo_numeros, entrar_valor),
        ("⌫", estilo_operadores, backspace)
        ],
    ]

    botoes = []

    for row in grid_botoes:
        linha_control = []
        for texto, estilo, handler in row:
            btn = ft.ElevatedButton(
                text=texto,
                on_click=handler,
                **estilo,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=5),
                    padding=0
                )
            )
            linha_control.append(btn)
        botoes.append(ft.Row(linha_control, spacing=5))

    page.add(
        ft.Column(
            [
                display,
                ft.Column(botoes, spacing=5)
            ]
        )
    )


ft.app(target=main)
