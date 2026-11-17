from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

gears = [
    {
        'id': 1,
        'title': 'Sony a6700',
        'category': 'Camera',
        'brand': 'Sony',
        'price': 100.000,
        'description': 'Описание Sony a6700'
    },
    {
        'id': 2,
        'title': 'Canon EOS R5',
        'category': 'Camera',
        'brand': 'Canon',
        'price': 200.000,
        'description': 'Описание Canon EOS R5'
    }
]

@app.route('/')
def index():
    return render_template('index.html', gears=gears)


@app.route('/gear/<int:gear_id>')
def gear_details(gear_id):
    gear = find_gear(gear_id)
    if gear:
        return render_template('gear_details.html', gear=gear)
    else:
        return "Gear not found", 404


@app.route('/gear/add', methods=['GET', 'POST'])
def add_gear():
    if request.method == 'POST':
        title = request.form.get('title', '')
        category = request.form.get('category', '')
        brand = request.form.get('brand', '')
        price = request.form.get('price', '')
        description = request.form.get('description', '').strip()

        errors = []

        if not title:
            errors.append("Title is required")

        if not category:
            errors.append("Category is required")

        if not brand:
            errors.append("Brand is required")

        if not price:
            errors.append("Price is required")

        if errors:
            return render_template('add_gear.html', errors=errors, title=title, category=category, brand=brand, price=price, description=description)

        new_gear = {
            'id': len(gears) + 1,
            'title': title,
            'category': category,
            'brand': brand,
            'price': price,
            'description': description
        }

        gears.append(new_gear)
        return redirect(url_for('index'))

    return render_template('add_gear.html')

@app.route('/gear/<int:gear_id>/edit', methods=['GET', 'POST'])
def edit_gear(gear_id):
    gear = find_gear(gear_id)
    if not gear:
        return "Gear not found", 404

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        brand = request.form.get('brand', '').strip()
        price = request.form.get('price', '').strip()
        description = request.form.get('description', '').strip()

        errors = []

        if not title:
            errors.append("Title is required")

        if not category:
            errors.append("Category is required")

        if not brand:
            errors.append("Brand is required")

        if not price:
            errors.append("Price is required")

        if errors:
            return render_template('edit_gear.html', errors=errors, title=title, category=category, brand=brand, price=price, description=description, gear=gear)

        gear.update({
            'title': title,
            'category': category,
            'brand': brand,
            'price': price,
            'description': description
        })

        return redirect(url_for('gear_details', gear_id=gear['id']))

    return render_template('edit_gear.html', gear=gear)


def find_gear(gear_id):
    return next((g for g in gears if g['id'] == gear_id), None)


if __name__ == '__main__':
    app.run(debug=True)
