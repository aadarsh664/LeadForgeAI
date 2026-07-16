export interface SearchFilters {
  hasWebsite?: boolean;
  hasEmail?: boolean;
  hasPhone?: boolean;
  minRating?: number;
  minReviews?: number;
  openNow?: boolean;
  verified?: boolean;
  hideClosed?: boolean;
}

export interface SearchRequest {
  category: string;
  location: string;
  keywords?: string;
  country?: string;
  state?: string;
  city?: string;
  radius?: number;
  max_results?: number;
  language?: string;
  filters?: SearchFilters;
}

export interface NormalizedBusiness {
  business_id: string;
  name: string;
  category: string;
  rating?: number;
  reviews?: number;
  address?: string;
  city?: string;
  state?: string;
  country?: string;
  phone?: string;
  email?: string;
  website?: string;
  latitude?: number;
  longitude?: number;
  is_open?: boolean;
  is_verified?: boolean;
  is_closed?: boolean;
  provider_source: string;
  discovery_date: string;
  raw_data: any;
}

export interface SearchResponse {
  search_id: string;
  status: string;
  progress: number;
  provider: string;
  started_at: string;
  finished_at?: string;
  result_count: number;
  duration?: number;
  results: NormalizedBusiness[];
  error?: string;
}
