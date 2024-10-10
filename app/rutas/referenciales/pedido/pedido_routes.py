from flask import Blueprint, render_template

pedmod = Blueprint('pedido', __name__, template_folder='templates')

@pedmod.route('/pedido-index')
def pedidoIndex():
    return render_template('pedido-index.html')