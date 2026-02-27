from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345abcde'

# MySQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Item({self.name}, {self.price})'
with app.app_context():
    db.create_all()
# Routes
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/market')
def market():
    # Fetch all items from database
    items = Item.query.all()
    return render_template('market.html', title='Market', items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        quantity = int(request.form['quantity'])
        
        new_item = Item(
            name=name,
            price=price,
            description=description,
            quantity=quantity
        )
        
        try:
            db.session.add(new_item)
            db.session.commit()
            flash('Item added successfully!', 'success')
        except:
            flash('Error adding item!', 'error')
        
        return redirect(url_for('market'))

@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    try:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!', 'success')
    except:
        
        flash('Error deleting item!', 'error')
    
    return redirect(url_for('market'))
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Item': Item}
if __name__ == '__main__':
    app.run(debug=True)