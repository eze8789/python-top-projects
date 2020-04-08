# The program will request the most starred python project in GitHub.
import requests
from plotly import offline


def make_request(url, headers):
    """Make the get request to the  API"""
    r = requests.get(url, headers=headers)
    return r


def store_content(req):
    """Store request content in a dictionary"""
    repositories_dict = req.json()
    return repositories_dict['items']


def process_data(repositories_dict):
    """Process top projects information"""
    stars, repo_links = [], []
    for repo in repositories_dict:
        stars.append(repo['stargazers_count'])
        repo_link = f"<a href='{repo['html_url']}'>{repo['name']}</a>"
        repo_links.append(repo_link)
    return repo_links, stars


def graph_data(repo_links, stars):
    """Visualizing data based on stars"""
    data = [{
        'type': 'bar',
        'x': repo_links,
        'y': stars,
        'marker': {
            'color': 'rgb(60, 100, 150)',
            'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
        },
        'opacity': 0.6,
    }]

    layout = {
        'title': 'Most starred Python projects',
        'titlefont': {'size': 32},
        'xaxis': {
            'title': 'Repository',
            'titlefont': {'size': 28},
            'tickfont': {'size': 14},
            'autorange': "reversed"
        },
        'yaxis': {
            'title': 'Stars',
            'titlefont': {'size': 28},
            'tickfont': {'size': 14},
        }
    }

    fig = {'data': data, 'layout': layout}
    offline.plot(fig, filename='python-top-repos.html')


url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'}

r = make_request(url, headers)
repositories_keys = store_content(r)
process_repos = process_data(repositories_keys)

graph_data(process_repos[0], process_repos[1])
