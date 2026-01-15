import requests
import pandas as pd
import panel as pn
import hvplot.pandas  # For interactive plotting

# Enable Panel extension
pn.extension()

# Define the community ID and API endpoint
community_id = "uct-prague"  # Replace with the actual community ID
#endpoint = f"https://zenodo.org/api/records/?communities={community_id}&size=1000"  # Fetch up to 1000 records

# The modern way to filter by community is using the 'q' parameter
endpoint = f"https://zenodo.org/api/records?q=communities:{community_id}&size=1000"

# Fetch data
response = requests.get(endpoint)
if response.status_code == 200:
    data = response.json()
else:
    print(f"Failed to fetch data: {response.status_code}")
    exit()

# Extract relevant information
records = []
for item in data['hits']['hits']:
    metadata = item.get('metadata', {})
    stats = item.get('stats', {})
    records.append({
        "Title": metadata.get('title', 'N/A'),
        "Creators": ", ".join(creator['name'] for creator in metadata.get('creators', [])),
        "Publication Date": metadata.get('publication_date', 'N/A'),
        "Type": metadata.get('resource_type', {}).get('type', 'N/A'),  # Dataset type
        "DOI": metadata.get('doi', 'N/A'),
        "Keywords": ", ".join(metadata.get('keywords', [])),
        "Views": stats.get('views', 0),
        "Downloads": stats.get('downloads', 0),
    })

# Convert to DataFrame
df = pd.DataFrame(records)

# Convert 'Publication Date' to datetime and extract the year
df['Publication Date'] = pd.to_datetime(df['Publication Date'], errors='coerce')
df['Year'] = df['Publication Date'].dt.year

# Calculate per-year statistics
yearly_stats = df.groupby('Year').agg(
    Repositories=('Title', 'count'),
    Avg_Views=('Views', 'mean'),
    Avg_Downloads=('Downloads', 'mean'),
    Total_Views=('Views', 'sum'),
    Total_Downloads=('Downloads', 'sum')
).reset_index()

# Calculate cumulative statistics
yearly_stats['Cumulative_Repositories'] = yearly_stats['Repositories'].cumsum()
yearly_stats['Cumulative_Views'] = yearly_stats['Total_Views'].cumsum()
yearly_stats['Cumulative_Downloads'] = yearly_stats['Total_Downloads'].cumsum()

# Yearly Bar Plots with a Simple Color Scheme
repositories_plot = yearly_stats.hvplot.bar(
    x='Year', y='Repositories', title="Repositories Per Year", width=400, color="lightblue"
)
avg_views_plot = yearly_stats.hvplot.bar(
    x='Year', y='Avg_Views', title="Average Views Per Year", width=400, color="lightgreen"
)
avg_downloads_plot = yearly_stats.hvplot.bar(
    x='Year', y='Avg_Downloads', title="Average Downloads Per Year", width=400, color="lightcoral"
)
total_views_plot = yearly_stats.hvplot.bar(
    x='Year', y='Total_Views', title="Total Views Per Year", width=400, color="lightgray"
)
total_downloads_plot = yearly_stats.hvplot.bar(
    x='Year', y='Total_Downloads', title="Total Downloads Per Year", width=400, color="peachpuff"
)

# Cumulative Line Plots
cumulative_repos_plot = yearly_stats.hvplot.line(
    x='Year', y='Cumulative_Repositories', title="Cumulative Repositories", width=400, line_color="blue"
)
cumulative_views_plot = yearly_stats.hvplot.line(
    x='Year', y='Cumulative_Views', title="Cumulative Views", width=400, line_color="green"
)
cumulative_downloads_plot = yearly_stats.hvplot.line(
    x='Year', y='Cumulative_Downloads', title="Cumulative Downloads", width=400, line_color="red"
)

# Panel Widgets for Tables
data_table = pn.widgets.DataFrame(df, name="Zenodo Records Table", width=800, height=400)
yearly_stats_table = pn.widgets.DataFrame(yearly_stats, name="Yearly Statistics", width=800, height=400)

# Define Intro Text with Explicit Styling using HTML
intro_text = pn.pane.HTML(
    """
    <div style="color: black; font-family: Arial; font-size: 16px;">
        <h1>UCT Zenodo Community Dashboard</h1>
        <p>This dashboard provides <b>yearly</b> and <b>cumulative insights</b> for the UCT Community on Zenodo.</p>
        <p>Explore the bar charts, line trends, and detailed tables below.</p>
        <p>Return to <a href="https://uct-datastewardship.github.io/">UCT Data Stewardship</a> blog</p>
    </div>
    """
)

# Create a Panel Layout
dashboard = pn.Column(
    intro_text,
    pn.Row(repositories_plot),
    pn.Row(total_views_plot, avg_views_plot),
    pn.Row(total_downloads_plot, avg_downloads_plot),
    pn.Row(cumulative_repos_plot, cumulative_views_plot, cumulative_downloads_plot),
    "### Detailed Tables",
    pn.Tabs(
        ("Records Table", data_table),
        ("Yearly Statistics", yearly_stats_table)
    ),
    #background="white"  # Ensure the background remains white
)

# Save the dashboard as an HTML file
dashboard.save("assets/uct_community_dashboard.html", embed=True)

# Show the dashboard (Optional)
#dashboard.show()
