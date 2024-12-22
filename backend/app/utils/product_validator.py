class ProductValidator:
    def validate(self, product: dict) -> bool:
        checks = [
            self._validate_images(product.get('image_url')),
            self._validate_price(product.get('price')),
            self._validate_description(product.get('description', '')),
            self._validate_measurements(product.get('specifications', {}))
        ]
        return all(checks)

    def _validate_images(self, image_url: str) -> bool:
        return image_url is not None and image_url.startswith('http')

    def _validate_price(self, price: float) -> bool:
        return price > 0

    def _validate_description(self, description: str) -> bool:
        return len(description) > 20  # Example check

    def _validate_measurements(self, specifications: dict) -> bool:
        return 'weight' in specifications and specifications['weight'] > 0
