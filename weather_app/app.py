from flask import Flask, render_template, request, send_file
import os
from weather import get_weather_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        zip_code = request.form['zip_code']
        df, plot_filename, csv_filename = get_weather_data(zip_code)
        
        if df is not None:
            return render_template('result.html', 
                                   data=df.to_html(classes='table table-striped', index=False),
                                   plot=plot_filename,
                                   csv=csv_filename,
                                   zip_code=zip_code)
        else:
            return render_template('index.html', error="An error occurred while fetching the weather data.")
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    if filename.endswith('.csv'):
        return send_file(os.path.join('output', 'csv', filename), as_attachment=True)
    elif filename.endswith('.png'):
        return send_file(os.path.join('output', 'plots', filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
