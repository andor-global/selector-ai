from serpapi import GoogleSearch
import pandas as pd
import streamlit as st
import re

def query(link):
  params = {
    "engine": "google_lens",
    "url": link,
    "api_key": st.secrets["google_lenz_api_key"]
  }
  search = GoogleSearch(params)
  results = search.get_dict()
  data = parse_api_results(results)
  return data


def parse_api_results(results):
  visual_matches = results['visual_matches']
  links = []
  thumbnails = []
  prices = []
  titles = []

  for item in visual_matches[:20]:
    try:
      prices.append(item['price']['value'])
    except:
      continue
    try:
      thumbnails.append(item['thumbnail'])
    except:
      thumbnails.append(None)
    try:
      links.append(item['link'])
    except:
      links.append(None)
    try:
      titles.append(item['title'])
    except:
      titles.append(None)

  currency = [re.search(r'([^\d.]*)', price).group(0) for price in prices]
  data = {'pic': thumbnails, 'title': titles, 'price': prices, 'currency': currency, 'link': links}
  df = pd.DataFrame(data=data)
  df["price"] = df["price"].str.replace(r'[^\d.]*', '', regex=True)
  return df
