from typing import Dict, Any

class GoogleMapsNormalizer:
    @staticmethod
    def normalize(raw: Dict[str, Any]) -> Dict[str, Any]:
        # Converts Google Maps specific raw schema into the common schema
        # For now, it just passes through as we haven't implemented the scraper
        return {
            "name": raw.get("name", "Unknown Business"),
            "category": raw.get("category", "Uncategorized"),
            "phone": raw.get("phone", ""),
            "website": raw.get("website", ""),
            "address": raw.get("address", ""),
            "city": raw.get("city", ""),
            "rating": float(raw.get("rating", 0.0)),
            "reviews": int(raw.get("reviews", 0)),
            "raw_data": raw
        }
