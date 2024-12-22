# config/image_processing.py

IMAGE_CONFIG = {
    'max_dimension': 1200,        # Maximum width or height in pixels
    'quality': 85,                 # Image quality (1-100)
    'format': 'JPEG',              # Image format (JPEG, PNG, etc.)
    'thumbnails': {
        'small': (150, 150),
        'medium': (300, 300),
        'large': (600, 600)
    }
}
