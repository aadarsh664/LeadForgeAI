from app.schemas.search import SearchRequest
from app.services.search.exceptions import SearchValidationError

class SearchValidator:
    def validate(self, request: SearchRequest) -> None:
        if not request.category or not request.category.strip():
            raise SearchValidationError("Category is required.")
        if not request.location or not request.location.strip():
            raise SearchValidationError("Location is required.")
        if request.max_results and request.max_results <= 0:
            raise SearchValidationError("Maximum results must be greater than 0.")
        if request.radius and request.radius <= 0:
            raise SearchValidationError("Radius must be greater than 0.")
