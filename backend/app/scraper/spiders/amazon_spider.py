# backend/app/scraper/spiders/amazon_spider.py
from bs4 import BeautifulSoup
import re
import json
from typing import List, Dict, Optional
from .base import BaseSpider
from ...utils.logger import get_logger
from ...utils.price_parser import parse_price

logger = get_logger(__name__)

class AmazonSpider(BaseSpider):
    """"""Spider for scraping jewelry data from Amazon""""""
    
    BASE_URL = ""https://www.amazon.com/s""
    
    def __init__(self):
        super().__init__()
        self.platform = ""amazon""
        self.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    async def search_products(self, query: str, max_items: int = 100) -> List[Dict]:
        """"""Search for jewelry products on Amazon""""""
        products = []
        page = 1
        
        while len(products) < max_items:
            params = {
                'k': f""{query} jewelry"",
                'i': 'fashion-womens-jewelry',
                'page': page,
                'ref': 'sr_pg_' + str(page)
            }
            
            html = await self.get_page(self.BASE_URL, params=params)
            if not html:
                break
                
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.select('div[data-asin]:not([data-asin=""""])')
            
            if not items:
                break
                
            for item in items:
                if len(products) >= max_items:
                    break
                    
                try:
                    product_data = await self._parse_product_card(item)
                    if product_data:
                        products.append(product_data)
                except Exception as e:
                    logger.error(f""Error parsing Amazon product: {str(e)}"")
                    continue
            
            page += 1
            
        return products

    async def _parse_product_card(self, item: BeautifulSoup) -> Optional[Dict]:
        """"""Parse individual product card from search results""""""
        try:
            title_elem = item.select_one('span.a-text-normal')
            price_elem = item.select_one('span.a-price > span.a-offscreen')
            image_elem = item.select_one('img.s-image')
            url_elem = item.select_one('a.a-link-normal[href]')
            rating_elem = item.select_one('span.a-icon-alt')
            reviews_elem = item.select_one('span.a-size-base.s-underline-text')
            
            if not (title_elem and price_elem and url_elem):
                return None
                
            product_url = url_elem['href']
            if not product_url.startswith('http'):
                product_url = f""https://www.amazon.com{product_url}""
            
            return {
                'title': title_elem.text.strip(),
                'price': parse_price(price_elem.text),
                'image_url': image_elem['src'] if image_elem else None,
                'product_url': product_url,
                'platform': self.platform,
                'rating': rating_elem.text.split(' ')[0] if rating_elem else None,
                'reviews_count': reviews_elem.text.replace(',', '') if reviews_elem else None,
                'asin': item.get('data-asin')
            }
        except Exception as e:
            logger.error(f""Error parsing Amazon product card: {str(e)}"")
            return None

    async def get_product_details(self, url: str) -> Optional[Dict]:
        """"""Get detailed product information from Amazon product page""""""
        html = await self.get_page(url)
        if not html:
            return None
            
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # Extract structured data
            structured_data = None
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and data.get('@type') == 'Product':
                        structured_data = data
                        break
                except json.JSONDecodeError:
                    continue
            
            # Extract product details
            details = {
                'title': soup.select_one('#productTitle').text.strip() if soup.select_one('#productTitle') else None,
                'price': parse_price(soup.select_one('#priceblock_ourprice').text) if soup.select_one('#priceblock_ourprice') else None,
                'description': soup.select_one('#productDescription').text.strip() if soup.select_one('#productDescription') else None,
                'features': [li.text.strip() for li in soup.select('#feature-bullets li') if li.text.strip()],
                'images': self._extract_images(soup),
                'specifications': self._extract_specifications(soup),
                'platform': self.platform
            }
            
            # Merge with structured data if available
            if structured_data:
                details.update({
                    'brand': structured_data.get('brand', {}).get('name'),
                    'rating': structured_data.get('aggregateRating', {}).get('ratingValue'),
                    'reviews_count': structured_data.get('aggregateRating', {}).get('reviewCount'),
                })
            
            return details
            
        except Exception as e:
            logger.error(f""Error parsing Amazon product details: {str(e)}"")
            return None

    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """"""Extract all product images""""""
        images = []
        
        # Try to get images from image gallery
        try:
            script = soup.find('script', text=re.compile('colorImages'))
            if script:
                data = re.search(r'colorImages\s*:\s*({.*})', script.string)
                if data:
                    image_data = json.loads(data.group(1))
                    images = [img['large'] for img in image_data.get('initial', [])]
        except Exception:
            pass
        
        # Fallback to main product image
        if not images:
            main_image = soup.select_one('#landingImage')
            if main_image and 'src' in main_image.attrs:
                images = [main_image['src']]
        
        return images

    def _extract_specifications(self, soup: BeautifulSoup) -> Dict:
        """"""Extract product specifications""""""
        specs = {}
        
        # Try product details section
        details_section = soup.select('#productDetails_detailBullets_sections1 tr')
        for row in details_section:
            label = row.select_one('th')
            value = row.select_one('td')
            if label and value:
                specs[label.text.strip()] = value.text.strip()
        
        # Try technical details section
        tech_details = soup.select('#productDetails_techSpec_section_1 tr')
        for row in tech_details:
            label = row.select_one('.label')
            value = row.select_one('.value')
            if label and value:
                specs[label.text.strip()] = value.text.strip()
        
        return specs