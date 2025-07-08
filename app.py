from flask import (
    Flask, render_template, request, make_response,
    session, redirect, url_for, flash
)
from weasyprint import HTML
from flask import session
import os
import secrets
print(secrets.token_hex(16))

    return {}



DATA_FILE = os.path.join(os.path.dirname(__file__), 'dados.json')

app = Flask(__name__)
app.secret_key = 'um_valor_secreto_aleatorio'

@app.route('/')
def index():
    data = session.get('form_data', {})
    return render_template('form.html', data=data)

@app.route('/visualizar', methods=['POST'])
def visualizar():
    dados = { key: request.form[key] for key in request.form }
    return render_template('preview.html', **dados)

@app.route('/salvar', methods=['POST'])
def salvar():
    form_data = request.form.to_dict()
    session['form_data'] = form_data
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