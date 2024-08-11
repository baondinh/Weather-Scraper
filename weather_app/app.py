from flask import Flask, render_template, request
from weather import get_weather_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        zip_code = request.form['zip_code']
        # df, plot_url = get_weather_data(zip_code)
        df = get_weather_data(zip_code)

        if df is not None:
            return render_template('result.html', 
                                   data=df.to_html(classes='table table-striped', index=False),
                                #    plot_url=plot_url,
                                   zip_code=zip_code)
        else:
            return render_template('index.html', error="An error occurred while fetching the weather data.")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
