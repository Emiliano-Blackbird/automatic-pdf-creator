from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


def generate_pdf(template_name, context, output_path):
    env = Environment(loader=FileSystemLoader('app/templates'))
    template = env.get_template(template_name)
    html_out = template.render(context)
    HTML(string=html_out, base_url="app/templates").write_pdf(output_path)


def pedir_datos_item():
    descripcion = input("Descripción del ítem: ")
    cantidad = int(input("Cantidad: "))
    precio_unitario = float(input("Precio unitario (€): "))
    return {"descripcion": descripcion, "cantidad": cantidad, "precio_unitario": precio_unitario}


if __name__ == "__main__":
    print("=== Generador de presupuesto PDF ===")

    cliente = input("Nombre del cliente: ")
    proyecto = input("Nombre del proyecto: ")
    fecha = input("Fecha (YYYY-MM-DD): ")
    validez = input("Validez del presupuesto (ej. 30 días): ")
    descripcion_proyecto = input("Descripción del proyecto: ")

    items = []
    while True:
        print("\nIngrese un ítem para el presupuesto:")
        item = pedir_datos_item()
        items.append(item)

        mas = input("¿Agregar otro ítem? (s/n): ").strip().lower()
        if mas != 's':
            break

    impuestos_pct = 0.21  # IVA fijo

    data = {
        "cliente": cliente,
        "proyecto": proyecto,
        "fecha": fecha,
        "validez": validez,
        "descripcion_proyecto": descripcion_proyecto,
        "items": items,
        "impuestos_pct": impuestos_pct
    }

    subtotal = sum(item['cantidad'] * item['precio_unitario'] for item in items)
    impuestos = subtotal * impuestos_pct
    total = subtotal + impuestos

    data.update({
        "subtotal": subtotal,
        "impuestos": impuestos,
        "total": total
    })

    output_pdf = f"presupuesto_{cliente.replace(' ', '_').lower()}.pdf"
    generate_pdf("budget.html", data, output_pdf)
    print(f"\nPDF generado correctamente: {output_pdf}")
