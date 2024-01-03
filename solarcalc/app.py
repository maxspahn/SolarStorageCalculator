# Importing required functions 
from solarcalc.helpers import DataParser, Storage
from flask import Flask, render_template, request

# Flask constructor 
app = Flask(__name__)

# Root endpoint 
@app.route('/', methods=['GET', 'POST'])
def homepage():

    data_parser = DataParser()
    selected_day = '20231229'
    selected_field = 'internal_supply'
    initial_charge = 10000
    capacity = 15000

    if request.method == 'POST':
        if 'selected_field' in request.form:
            # Get the value entered in the form field
            selected_field = request.form['selected_field']
            selected_day = request.form['selected_day']
            initial_charge = float(request.form['initial_charge'])
            capacity = float(request.form['capacity'])


    # Get data based on the selected field
    data_parser.parse(f'data/{selected_day}.csv')
    storage = Storage(initial_charge, data_parser.interval, capacity)
    data = data_parser.data_by_field(selected_field).tolist()
    labels = data_parser.get_times()
    
    data_internal = data_parser.data_by_field('generation').tolist()
    data_external = data_parser.data_by_field('consumption').tolist()
    feed_in = data_parser.data_by_field('feed-in').tolist()
    external_supply = data_parser.data_by_field('external_supply').tolist()
    sum_feed_in = sum(feed_in) * data_parser.interval
    sum_external = sum(external_supply) * data_parser.interval
    storage.set_production_consumption(data_internal, data_external)



    return render_template(
        template_name_or_list='index.html',
        data=data,
        labels=labels,
        data_internal=data_internal,
        data_external=data_external,
        data_internal_battery=storage.feed_in,
        data_external_battery=storage.external,
        data_charge=storage.charge,
        initial_charge=initial_charge,
        capacity=capacity,
        selected_field=selected_field,
        selected_day=selected_day,
        sum_feed_in_battery=storage.sum_feed_in,
        sum_external_battery=storage.sum_external,
        sum_feed_in=sum_feed_in,
        sum_external=sum_external,
    )



	# Return the components to the HTML template 
    return render_template(
		template_name_or_list='index.html',
		data=data,
		labels=labels,
	)


# Main Driver Function 
if __name__ == '__main__':
	# Run the application on the local development server ##
	app.run(debug=True)
