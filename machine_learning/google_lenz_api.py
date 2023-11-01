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
      prices.append(None)
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
  df_with_prices = df[~df['price'].isna()]
  df_with_no_prices = df[df['price'].isna()]
  if len(df_with_prices) != 0:
     df_with_prices["price"] = df_with_prices["price"].str.replace(r'[^\d.]*', '', regex=True)
  df = pd.concat(df_with_prices, df_with_no_prices)
  return df