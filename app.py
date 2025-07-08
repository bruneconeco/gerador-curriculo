from flask import (
    Flask, render_template, request, make_response,
    session, redirect, url_for, flash
)
from weasyprint import HTML
import json
import os
def carregar_dados():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_dados_em_arquivo(dados):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'dados.json')

app = Flask(__name__)
app.secret_key = 'troque_esse_valor_por_algo_secreto'

@app.route('/')
def index():
    return render_template('form.html', data={})

@app.route('/visualizar', methods=['POST'])
def visualizar():
    dados = { key: request.form[key] for key in request.form }
    return render_template('preview.html', **dados)

@app.route('/salvar', methods=['POST'])
def salvar():
    form_data = request.form.to_dict()
    salvar_dados_em_arquivo(form_data)
    flash('Dados salvos com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/gerar', methods=['POST'])
def gerar():
    # pega os campos (nome, email, etc) de request.form
    html = render_template('curriculo.html', **request.form.to_dict())
    pdf = HTML(string=html).write_pdf()
    response = make_response(pdf)
    response.headers.update({
        'Content-Type': 'application/pdf',
        'Content-Disposition': f'attachment; filename=curriculo_{request.form["nome"]}.pdf'
    })
    return response

if __name__ == '__main__':
    app.run(debug=True)