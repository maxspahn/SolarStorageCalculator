# Importing required functions 
from solarcalc.helpers import DataParser
from flask import Flask, render_template, request

# Flask constructor 
app = Flask(__name__)

# Root endpoint 
@app.route('/', methods=['GET', 'POST'])
def homepage():

    data_parser = DataParser()
    selected_day = '20231229'
    selected_field = 'internal_supply'

    if request.method == 'POST':
        # Get the value entered in the form field
        selected_field = request.form['selected_field']
        selected_day = request.form['selected_day']

    # Get data based on the selected field
    data_parser.parse(f'data/{selected_day}.csv')
    data = data_parser.data_by_field(selected_field).tolist()
    labels = data_parser.get_times()



    return render_template(
        template_name_or_list='index.html',
        data=data,
        labels=labels,
        selected_field=selected_field,
        selected_day=selected_day,
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
