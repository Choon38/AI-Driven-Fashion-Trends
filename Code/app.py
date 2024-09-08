from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Dummy clothing class names
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Generate mock data for future trends
future_years = range(2022, 2028)
mock_trend_data = pd.DataFrame({
    'year': np.repeat(future_years, len(class_names)),
    'clothing_type': np.tile(class_names, len(future_years)),
    'popularity_score': np.random.rand(len(class_names) * len(future_years))
})

# Normalize popularity scores across years
mock_trend_data['popularity_score'] = mock_trend_data.groupby('clothing_type')['popularity_score'].transform(lambda x: (x - x.min()) / (x.max() - x.min()))

# Aggregate data by year and clothing type
yearly_trends = mock_trend_data.groupby(['year', 'clothing_type']).mean().reset_index()

# Identify top trends for each year
top_trends_per_year = yearly_trends.loc[yearly_trends.groupby('year')['popularity_score'].idxmax()]

# Generate the projection plot
def plot_trend_projection():
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
    plt.xticks(future_years)
    plt.tight_layout()
    plt.savefig('static/fashion_trends_projection.png')
    plt.close()

# Generate top 5 trends plot
def plot_top_5_trends():
    top_trends = yearly_trends.groupby('clothing_type')['popularity_score'].mean().nlargest(5).reset_index()
    plt.figure(figsize=(10, 5))
    plt.barh(top_trends['clothing_type'], top_trends['popularity_score'], color='skyblue')
    plt.xlabel('Popularity Score')
    plt.title('Top 5 Future Fashion Trends')
    plt.gca().invert_yaxis()
    plt.savefig('static/top_5_trends.png')
    plt.close()

# Generate yearly trend plot for selected clothing type
def plot_yearly_trend(clothing_type):
    years = np.arange(2018, 2028)
    trend_data = {item: np.random.rand(len(years)) * 100 for item in class_names}
    yearly_scores = trend_data[clothing_type]
    
    plt.figure(figsize=(8, 5))
    plt.plot(years, yearly_scores, marker='o', color='b', linestyle='-', linewidth=2, markersize=6)
    plt.ylim(0, 100)
    plt.xlabel('Year')
    plt.ylabel('Popularity Score')
    plt.title(f'Yearly Trend for {clothing_type}')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'static/yearly_trend_{clothing_type}.png')
    plt.close()

# Flask routes
@app.route('/')
def index():
    # Generate the plots
    plot_trend_projection()
    plot_top_5_trends()

    # Convert data to HTML tables for display
    yearly_trends_html = yearly_trends.to_html(classes='table table-striped', index=False)
    top_trends_per_year_html = top_trends_per_year.to_html(classes='table table-striped', index=False)

    return render_template('index.html', 
                           yearly_trends_html=yearly_trends_html, 
                           top_trends_per_year_html=top_trends_per_year_html,
                           class_names=class_names)

@app.route('/update_plot', methods=['POST'])
def update_plot():
    clothing_type = request.form['clothing_type']
    plot_yearly_trend(clothing_type)
    return f'static/yearly_trend_{clothing_type}.png'

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
