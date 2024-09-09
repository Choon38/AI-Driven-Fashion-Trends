import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend

from flask import Flask, send_from_directory, request
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import pandas as pd

app = Flask(__name__, static_folder='docs', static_url_path='')

# Simulated data for the trends of each clothing type over the years
class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

# Generate mock trend data
years = np.arange(2022, 2028)
mock_trend_data = pd.DataFrame({
    'clothing_type': np.random.choice(class_names, size=100),
    'year': np.random.choice(years, size=100),
    'popularity_score': np.random.rand(100)
})

def create_fashion_trends_projection_image():
    plt.figure(figsize=(12, 8))

    for clothing_type in class_names:
        data = mock_trend_data[mock_trend_data['clothing_type'] == clothing_type]
        plt.plot(data['year'], data['popularity_score'], marker='o', label=clothing_type)

    plt.xlabel('Year')
    plt.ylabel('Popularity Score')
    plt.title('Fashion Trends Projection (2022-2027)')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.ylim(0, 1)
    plt.xticks(years)
    plt.tight_layout()

    # Save plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')

    plt.close()
    return graph_url

@app.route('/')
def index():
    # Generate the image for the Fashion Trends Projection
    trends_image_url = create_fashion_trends_projection_image()

    # Serve the static index.html file from the 'docs' folder
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fashion Trends</title>
    </head>
    <body>
        <h1>Fashion Trends</h1>
        <h2>Fashion Trends Projection (2022-2027)</h2>
        <img src="data:image/png;base64,{trends_image_url}" alt="Fashion Trends Projection">
        <form action="/show_trends" method="post">
            <label for="clothing_type">Select Clothing Type:</label>
            <select name="clothing_type" id="clothing_type">
                {''.join(f'<option value="{ct}">{ct}</option>' for ct in class_names)}
            </select>
            <button type="submit">Show Trends</button>
        </form>
        <a href="/show_all_trends">View All Trends</a>
    </body>
    </html>
    """

@app.route('/show_trends', methods=['POST'])
def show_trends():
    selected_clothing_type = request.form.get('clothing_type')

    if not selected_clothing_type or selected_clothing_type not in class_names:
        return "Invalid clothing type selected.", 400

    # Generate the trend graph for the selected clothing type
    years = np.arange(2015, 2025)
    trends = np.random.rand(len(years))  # Simulated data

    plt.figure(figsize=(10, 6))
    plt.plot(years, trends, marker='o', linestyle='-', color='b')
    plt.title(f'Trends for {selected_clothing_type} (2015-2024)')
    plt.xlabel('Year')
    plt.ylabel('Popularity')
    plt.grid(True)

    # Save plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')

    plt.close()

    # Serve the HTML with the graph URL
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fashion Trends</title>
    </head>
    <body>
        <h1>Fashion Trends</h1>
        <img src="data:image/png;base64,{graph_url}" alt="Trends Graph">
        <form action="/show_trends" method="post">
            <label for="clothing_type">Select Clothing Type:</label>
            <select name="clothing_type" id="clothing_type">
                {''.join(f'<option value="{ct}">{ct}</option>' for ct in class_names)}
            </select>
            <button type="submit">Show Trends</button>
        </form>
        <a href="/show_all_trends">View All Trends</a>
    </body>
    </html>
    """

@app.route('/show_all_trends')
def show_all_trends():
    plt.figure(figsize=(12, 8))

    for clothing_type in class_names:
        data = mock_trend_data[mock_trend_data['clothing_type'] == clothing_type]
        plt.plot(data['year'], data['popularity_score'], marker='o', label=clothing_type)

    plt.xlabel('Year')
    plt.ylabel('Popularity Score')
    plt.title('Fashion Trends Projection (2022-2027)')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.ylim(0, 1)
    plt.xticks(years)
    plt.tight_layout()

    # Save plot to a bytes buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')

    plt.close()

    # Serve the HTML with the graph URL
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fashion Trends Projection</title>
    </head>
    <body>
        <h1>Fashion Trends Projection (2022-2027)</h1>
        <img src="data:image/png;base64,{graph_url}" alt="All Trends Graph">
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
