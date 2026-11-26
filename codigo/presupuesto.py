articulo = "Cuaderno"
cantidad = 3
precio = 5
total = cantidad * precio
print(f"{articulo}: {cantidad} x S/ {precio} = S/ {total}")

with open("resultado.html", "w", encoding="utf-8") as salida:
    salida.write(
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>Prueba Haiku</title></head><body>"
        f"<h1>Presupuesto desde Haiku</h1><p>{articulo}: {cantidad} x S/ {precio} = S/ {total}</p>"
        "</body></html>"
    )
