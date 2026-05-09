from flask import Flask, render_template, request

app = Flask(__name__)

def calcula_imc(peso, altura_cm):
    altura_m = altura_cm / 100
    return round(peso / (altura_m ** 2), 2)

def categoria_imc(imc):
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 25:
        return "Normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        imc = calcula_imc(peso, altura)
        categoria = categoria_imc(imc)
        return render_template("salida.html", imc=imc, categoria=categoria)
    return render_template("formulario.html")

if __name__ == "__main__":
    app.run(debug=True)

