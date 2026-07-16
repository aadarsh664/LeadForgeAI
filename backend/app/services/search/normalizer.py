from typing import Any, Dict, List
from datetime import datetime, timezone
from app.schemas.search import NormalizedBusiness
import uuid

class SearchNormalizer:
    def normalize(self, raw_data: Dict[str, Any], provider_name: str) -> NormalizedBusiness:
        """
        Base normalization logic. 
        In the future, providers will have specific normalizers or pass their mapping.
        For now, this assumes the provider tries to give somewhat standardized raw data.
        """
        return NormalizedBusiness(
            business_id=raw_data.get("id", str(uuid.uuid4())),
            name=raw_data.get("name", "Unknown Business"),
            category=raw_data.get("category", "Unknown"),
            rating=raw_data.get("rating"),
            reviews=raw_data.get("reviews"),
            address=raw_data.get("address"),
            city=raw_data.get("city"),
            state=raw_data.get("state"),
            country=raw_data.get("country"),
            phone=raw_data.get("phone"),
            email=raw_data.get("email"),
            website=raw_data.get("website"),
            latitude=raw_data.get("latitude"),
            longitude=raw_data.get("longitude"),
            is_open=raw_data.get("is_open"),
            is_verified=raw_data.get("is_verified"),
            is_closed=raw_data.get("is_closed"),
            provider_source=provider_name,
            discovery_date=datetime.now(timezone.utc),
            raw_data=raw_data
        )

    def normalize_batch(self, raw_batch: List[Dict[str, Any]], provider_name: str) -> List[NormalizedBusiness]:
        return [self.normalize(item, provider_name) for item in raw_batch]
