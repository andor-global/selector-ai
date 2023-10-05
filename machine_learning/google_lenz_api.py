from serpapi import GoogleSearch
import pandas as pd



def query(link):
  params = {
    "engine": "google_lens",
    "url": link,
    "api_key": ""
  }
  search = GoogleSearch(params)
  results = search.get_dict()
  knowledge_graph = results
  data = parse_api_results(results)
  return data


def parse_api_results(results):
  visual_matches = results['visual_matches']
  links = []
  thumbnails = []
  prices = []
  titles = []

  for item in visual_matches[:10]:
    try:
      thumbnails.append(item['thumbnail'])
    except:
      thumbnails.append(None)
    try:
      links.append(item['link'])
    except:
      links.append(None)
    try:
      prices.append(item['price']['value'])
    except:
      prices.append(None)
    try:
      titles.append(item['title'])
    except:
      titles.append(None)

  data = {'pic': thumbnails, 'title': titles, 'price': prices, 'link': links}
  df = pd.DataFrame(data=data)
  return df


# Example
url = 'https://raw.githubusercontent.com/GENLapp/genL/main/1.jpg'
data = query(url)
data.to_csv('data.csv')
print(data)