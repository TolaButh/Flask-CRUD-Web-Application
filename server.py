from enum import unique
import re
from flask import Flask
from flask import render_template,url_for,redirect,request 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(10), nullable=False,unique=True)
    product_name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(100), nullable =False)
    price = db.Column(db.String(10), nullable=False)
    def __repr__(self):
        return f"<Product: {self.product_name}/>"

@app.route("/")
def home():
    title = 'Home Page'

    return render_template('index.html',title=title)
@app.route("/products")
def product():
    title = 'Production Online'
    product = Product.query.all()
    return render_template('product.html', title = title, product = product)
@app.route("/add_product", methods=['GET', 'POST'])
def add_product():
    title = "Add Product"
    if request.method =='POST':
        product_id = request.form['product_id']
        product_name=request.form['product_name']
        category =request.form['category']
        description =request.form['description']
        price = request.form['price']
        product  = Product(product_id=product_id, product_name = product_name, category=category, description=description, price=price)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('product'))
    return render_template('add_product.html',title=title)
@app.route("/delete_product/<int:id>")
def delete(id):
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product'))

@app.route("/update_product/<int:id>", methods=['GET', 'POST'])
def update(id):
    title = "Update Product"
    product = Product.query.filter_by(id=id).first()
    if request.method == "POST":
        product.product_id = request.form['product_id']
        product.product_name=request.form['product_name']
        product.category =request.form['category']
        product.description =request.form['description']
        product.price = request.form['price']
        db.session.commit()
        return redirect(url_for('product'))
    return render_template('update_product.html',title=title, product=product)
if __name__ == "__main__":
    app.run(debug=True)


