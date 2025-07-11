from flask import (
    Flask, render_template, request, make_response,
    session, redirect, url_for, flash
)
from weasyprint import HTML
import os
import secrets

app = Flask(__name__)
app.secret_key = 'substitua_por_uma_chave_real_gerada_com_secrets' 

@app.route('/')
def index():
    data = session.get('form_data', {})  # Carrega dados da sessão, se existirem
    return render_template('form.html', data=data)

@app.route('/visualizar', methods=['POST'])
def visualizar():
    dados = request.form.to_dict()
    return render_template('preview.html', **dados)

@app.route('/salvar', methods=['POST'])
def salvar():
    form_data = request.form.to_dict()
    session['form_data'] = form_data  # Salva os dados na sessão (por usuário)
    flash('Dados salvos com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/gerar', methods=['POST'])
def gerar():
    html = render_template('curriculo.html', **request.form.to_dict())
    pdf = HTML(string=html).write_pdf()
    response = make_response(pdf)
    response.headers.update({
        'Content-Type': 'application/pdf',
        'Content-Disposition': f'attachment; filename=curriculo_{request.form.get("nome", "usuario")}.pdf'
    })
    return response

if __name__ == '__main__':
    app.run(debug=True)