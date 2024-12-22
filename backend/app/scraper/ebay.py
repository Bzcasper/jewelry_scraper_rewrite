# backend/app/scrapers/ebay.py
from .base import BaseScraper
from bs4 import BeautifulSoup
from typing import List, Dict
import asyncio

class EbayScraper(BaseScraper):
    async def search_products(self, query: str, max_items: int) -> List[Dict]:
        await self.init_session()
        products = []
        page = 1
        
        while len(products) < max_items:
            url = f""https://www.ebay.com/sch/i.html?_nkw={query}&_pgn={page}""
            try:
                html = await self.get_page(url)
                soup = BeautifulSoup(html, 'html.parser')
                
                items = soup.find_all('div', {'class': 's-item__wrapper'})
                if not items:
                    break
                
                for item in items:
                    if len(products) >= max_items:
                        break
                    
                    product = self._parse_item(item)
                    if product:
                        products.append(product)
                
                page += 1
                
            except Exception as e:
                print(f""Error scraping page {page}: {str(e)}"")
                break
        
        await self.close_session()
        return products
    
    def _parse_item(self, item_soup) -> Dict:
        try:
            return {
                'title': item_soup.find('h3', {'class': 's-item__title'}).text.strip(),
                'price': float(item_soup.find('span', {'class': 's-item__price'})
                             .text.replace('$', '').replace(',', '')),
                'url': item_soup.find('a', {'class': 's-item__link'})['href'],
                'image_url': item_soup.find('img', {'class': 's-item__image-img'})['src'],
                'platform': 'ebay'
            }
        except Exception:
            return None