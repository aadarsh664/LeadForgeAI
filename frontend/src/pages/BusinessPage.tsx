import React, { useState, useEffect } from "react";
import {
  Card,
  H3,
  Text,
  Button,
  Input,
  Divider,
  Switch,
  Checkbox,
  Badge,
  PageHeader,
  SectionHeader,
  Dropdown,
  Loader
} from "../design-system/components";
import { Search, RotateCcw, ChevronDown, ChevronUp, Clock, Sparkles, Bookmark, History } from "lucide-react";
import BusinessResults from "./BusinessResults";
import BusinessProfile from "./BusinessProfile";
import SearchHistory from "./SearchHistory";
import JobProgressCard from "../components/search/JobProgressCard";
import type { NormalizedBusiness } from "../types/search";

interface SearchFormState {
  category: string;
  location: string;
  radius: string;
  language: string;
  maxResults: string;
  country: string;
  state: string;
  city: string;
  keywords: string;
  excludeKeywords: string;
  provider: string;
}

interface FilterState {
  hasWebsite: boolean;
  hasEmail: boolean;
  hasPhone: boolean;
  minRating: string;
  minReviews: string;
  openNow: boolean;
  verified: boolean;
  hideClosed: boolean;
}

const defaultForm: SearchFormState = {
  category: "",
  location: "",
  radius: "10",
  language: "en",
  maxResults: "500",
  country: "",
  state: "",
  city: "",
  keywords: "",
  excludeKeywords: "",
  provider: "google_maps"
};

const defaultFilters: FilterState = {
  hasWebsite: false,
  hasEmail: false,
  hasPhone: false,
  minRating: "",
  minReviews: "",
  openNow: false,
  verified: false,
  hideClosed: false
};

export default function BusinessPage() {
  const [viewState, setViewState] = useState<"form" | "progress" | "results" | "error" | "profile" | "history">("form");
  const [form, setForm] = useState<SearchFormState>(defaultForm);
  const [filters, setFilters] = useState<FilterState>(defaultFilters);
  const [advancedOpen, setAdvancedOpen] = useState(false);
  
  const [results, setResults] = useState<NormalizedBusiness[]>([]);
  const [errorMsg, setErrorMsg] = useState("");
  const [selectedBusiness, setSelectedBusiness] = useState<NormalizedBusiness | null>(null);

  // Job Execution State
  const [currentJob, setCurrentJob] = useState<any>(null);

  // Recent History snippet for the right column
  const [recentSnippet, setRecentSnippet] = useState<any[]>([]);

  const loadSnippet = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/v1/history/history");
      const data = await res.json();
      setRecentSnippet(data.slice(0, 3));
    } catch(e) {
      // ignore
    }
  };

  // Load persisted state
  useEffect(() => {
    const saved = localStorage.getItem("leadforgeai_search_form");
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (parsed.form) setForm(parsed.form);
        if (parsed.filters) setFilters(parsed.filters);
      } catch (e) {
        console.error("Failed to parse saved search form", e);
      }
    }
    loadSnippet();
  }, []);

  const activeResults = React.useMemo(() => {
    return results.filter((b) => {
      if (filters.hasWebsite && !b.website) return false;
      if (filters.hasPhone && !b.phone) return false;
      if (filters.hasEmail && !b.email) return false;
      if (filters.minRating && (b.rating || 0) < parseFloat(filters.minRating)) return false;
      if (filters.minReviews && (b.reviews || 0) < parseInt(filters.minReviews)) return false;
      if (filters.openNow && !b.is_open) return false;
      if (filters.verified && !b.is_verified) return false;
      if (filters.hideClosed && b.is_closed) return false;
      return true;
    });
  }, [results, filters]);

  // Save state on change
  useEffect(() => {
    const timeout = setTimeout(() => {
      localStorage.setItem("leadforgeai_search_form", JSON.stringify({ form, filters }));
    }, 500);
    return () => clearTimeout(timeout);
  }, [form, filters]);

  // Polling Effect
  useEffect(() => {
    let interval: any;
    if (viewState === "progress" && currentJob && !["Completed", "Failed", "Cancelled"].includes(currentJob.status)) {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`http://localhost:8000/api/v1/search/jobs/${currentJob.id}`);
          if (res.ok) {
            const jobData = await res.json();
            setCurrentJob(jobData);
            if (jobData.status === "Completed") {
              setResults(jobData.results || []);
              setViewState("results");
              loadSnippet();
            } else if (jobData.status === "Failed") {
              setErrorMsg(jobData.error || "Job failed");
            }
          }
        } catch (e) {
          console.error("Polling error", e);
        }
      }, 500);
    }
    return () => clearInterval(interval);
  }, [viewState, currentJob]);

  const isValid = form.category.trim() !== "" && form.location.trim() !== "";

  const handleReset = () => {
    setForm(defaultForm);
    setFilters(defaultFilters);
    localStorage.removeItem("leadforgeai_search_form");
  };

  const executeSearchRequest = async (requestBody: any) => {
    setViewState("progress");
    setCurrentJob(null);
    try {
      const response = await fetch("http://localhost:8000/api/v1/search/jobs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody)
      });
      
      const jobData = await response.json();
      if (!response.ok) throw new Error(jobData.detail || "Failed to start job");
      
      setCurrentJob(jobData);
    } catch (err: any) {
      setErrorMsg(err.message || "An unknown error occurred");
      setViewState("error");
    }
  }

  const handleSearch = async () => {
    if (!isValid) return;
    const requestBody = {
      category: form.category,
      location: form.location,
      keywords: form.keywords,
      country: form.country,
      state: form.state,
      city: form.city,
      radius: parseInt(form.radius) || 10,
      max_results: parseInt(form.maxResults) || 500,
      provider: form.provider,
      language: form.language,
      filters: {
        has_website: filters.hasWebsite,
        has_email: filters.hasEmail,
        has_phone: filters.hasPhone,
        min_rating: filters.minRating ? parseFloat(filters.minRating) : null,
        min_reviews: filters.minReviews ? parseInt(filters.minReviews) : null,
        open_now: filters.openNow,
        verified: filters.verified,
        hide_closed: filters.hideClosed
      }
    };
    await executeSearchRequest(requestBody);
  };

  const handleCancelJob = async () => {
    if (currentJob?.id) {
      await fetch(`http://localhost:8000/api/v1/search/jobs/${currentJob.id}/cancel`, { method: "POST" });
    }
  };

  const handleRetryJob = async () => {
    if (currentJob?.id) {
      await fetch(`http://localhost:8000/api/v1/search/jobs/${currentJob.id}/retry`, { method: "POST" });
      // Polling will naturally pick it up since status becomes Queued
    }
  };

  const handleSaveSearch = async () => {
    const name = prompt("Enter a name for this saved search:", `${form.category} in ${form.location}`);
    if (name) {
      const requestBody = {
        category: form.category,
        location: form.location,
        keywords: form.keywords,
        country: form.country,
        state: form.state,
        city: form.city,
        radius: parseInt(form.radius) || 10,
        max_results: parseInt(form.maxResults) || 500,
      provider: form.provider,
        language: form.language,
        filters: {
          has_website: filters.hasWebsite,
          has_email: filters.hasEmail,
          has_phone: filters.hasPhone,
          min_rating: filters.minRating ? parseFloat(filters.minRating) : null,
          min_reviews: filters.minReviews ? parseInt(filters.minReviews) : null,
          open_now: filters.openNow,
          verified: filters.verified,
          hide_closed: filters.hideClosed
        }
      };
      const res = await fetch("http://localhost:8000/api/v1/history/saved", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, request: requestBody })
      });
      if (res.ok) {
        alert("Search saved successfully!");
      } else {
        alert("Failed to save search (Name might already exist).");
      }
    }
  };

  const handleRunFromHistory = (req: any) => {
    setForm({
      category: req.category || "",
      location: req.location || "",
      radius: (req.radius || 10).toString(),
      language: req.language || "en",
      maxResults: (req.max_results || 500).toString(),
      country: req.country || "",
      state: req.state || "",
      city: req.city || "",
      keywords: req.keywords || "",
      excludeKeywords: ""
    });
    setFilters({
      hasWebsite: req.filters?.has_website || false,
      hasEmail: req.filters?.has_email || false,
      hasPhone: req.filters?.has_phone || false,
      minRating: req.filters?.min_rating ? req.filters.min_rating.toString() : "",
      minReviews: req.filters?.min_reviews ? req.filters.min_reviews.toString() : "",
      openNow: req.filters?.open_now || false,
      verified: req.filters?.verified || false,
      hideClosed: req.filters?.hide_closed || false
    });
    executeSearchRequest(req);
  };

  if (viewState === "progress") {
    return (
      <div className="page-container" style={{ padding: "0 16px 64px 16px" }}>
        {!currentJob ? (
           <div style={{ display: "flex", justifyContent: "center", padding: "64px" }}><Loader size="lg" /></div>
        ) : (
          <JobProgressCard 
            job={currentJob} 
            onCancel={handleCancelJob} 
            onRetry={handleRetryJob} 
          />
        )}
      </div>
    );
  }

  if (viewState === "error") {
    return (
      <div className="page-container" style={{ padding: "0 16px 64px 16px" }}>
        <Card style={{ textAlign: "center", padding: "64px 24px", maxWidth: "600px", margin: "64px auto", borderColor: "var(--color-danger)", backgroundColor: "var(--color-bg-subtle)" }}>
          <H3 style={{ color: "var(--color-danger)", marginBottom: "16px" }}>Search Error</H3>
          <Text style={{ marginBottom: "32px" }}>{errorMsg}</Text>
          <Button variant="primary" onClick={() => setViewState("form")}>Try Again</Button>
        </Card>
      </div>
    );
  }

  if (viewState === "profile" && selectedBusiness) {
    return (
      <div className="page-container" style={{ padding: "0 16px 64px 16px" }}>
        <BusinessProfile business={selectedBusiness} onBack={() => setViewState("results")} />
      </div>
    );
  }

  if (viewState === "history") {
    return (
      <div className="page-container" style={{ padding: "0 16px 64px 16px" }}>
        <SearchHistory onBack={() => { setViewState("form"); loadSnippet(); }} onRunSearch={handleRunFromHistory} />
      </div>
    );
  }

  if (viewState === "results") {
    if (activeResults.length === 0) {
      return (
        <div className="page-container" style={{ padding: "0 16px 64px 16px" }}>
          <Card style={{ textAlign: "center", padding: "64px 24px", maxWidth: "600px", margin: "64px auto" }}>
            <H3 style={{ marginBottom: "16px" }}>No Businesses Found</H3>
            <Text style={{ marginBottom: "32px", color: "var(--color-text-secondary)" }}>We couldn't find any businesses matching your search criteria.</Text>
            <Button variant="primary" onClick={() => setViewState("form")}>Modify Search</Button>
          </Card>
        </div>
      );
    }
    
    return (
      <div className="page-container" style={{ padding: "0 16px 64px 16px" }}>
        <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "16px" }}>
          <Button variant="secondary" onClick={handleSaveSearch} icon={<Bookmark size={16}/>}>Save this Search</Button>
        </div>
        <BusinessResults 
          results={activeResults} 
          onBack={() => setViewState("form")} 
          onSelect={(b) => { setSelectedBusiness(b); setViewState("profile"); }}
        />
      </div>
    );
  }

  return (
    <div className="page-container" style={{ padding: "0 16px 64px 16px" }}>
      <PageHeader 
        title="Business Search" 
        description="Discover local businesses and generate high-quality leads."
        action={
          <div style={{ display: 'flex', gap: '12px' }}>
            <Button variant="ghost" onClick={() => setViewState("history")} icon={<History size={16}/>}>History</Button>
            <Button variant="ghost" onClick={handleReset} icon={<RotateCcw size={16}/>}>Reset</Button>
            <Button variant="primary" onClick={handleSearch} disabled={!isValid} icon={<Search size={16}/>}>Search</Button>
          </div>
        }
      />

      <div style={{ display: "grid", gridTemplateColumns: "1fr 380px", gap: "32px", alignItems: "start" }}>
        
        {/* Left Column: Search Form & Filters */}
        <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
          <Card>
            <SectionHeader title="Search Criteria" description="Define your target audience." />
            
            <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: "16px", marginBottom: "24px" }}>
              <div style={{ display: "flex", gap: "16px" }}>
                <div style={{ flex: 1 }}>
                  <Input 
                    label="Business Category *" 
                    placeholder="e.g. Dentists, Restaurants, Plumbers"
                    value={form.category}
                    onChange={(e) => setForm({ ...form, category: e.target.value })}
                  />
                </div>
                <div style={{ flex: 1 }}>
                  <Input 
                    label="Location *" 
                    placeholder="e.g. New York, London, Tokyo"
                    value={form.location}
                    onChange={(e) => setForm({ ...form, location: e.target.value })}
                  />
                </div>
              </div>

              <div style={{ display: "flex", gap: "16px" }}>
                <div style={{ flex: 1 }}>
                  <Input 
                    label="Keywords" 
                    placeholder="e.g. specialized, cheap, 24/7"
                    value={form.keywords}
                    onChange={(e) => setForm({ ...form, keywords: e.target.value })}
                  />
                </div>
                <div style={{ flex: 1 }}>
                  <Input 
                    label="Exclude Keywords" 
                    placeholder="e.g. chain, franchise"
                    value={form.excludeKeywords}
                    onChange={(e) => setForm({ ...form, excludeKeywords: e.target.value })}
                  />
                </div>
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px" }}>
                <Input 
                  label="Country" 
                  placeholder="Optional"
                  value={form.country}
                  onChange={(e) => setForm({ ...form, country: e.target.value })}
                />
                <Input 
                  label="State/Province" 
                  placeholder="Optional"
                  value={form.state}
                  onChange={(e) => setForm({ ...form, state: e.target.value })}
                />
                <Input 
                  label="City" 
                  placeholder="Optional"
                  value={form.city}
                  onChange={(e) => setForm({ ...form, city: e.target.value })}
                />
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px" }}>
                <Input 
                  label="Radius (km)" 
                  type="number"
                  value={form.radius}
                  onChange={(e) => setForm({ ...form, radius: e.target.value })}
                />
                <Dropdown 
                  label="Language"
                  value={form.language}
                  onChange={(e) => setForm({ ...form, language: e.target.value })}
                  options={[
                    { label: "English", value: "en" },
                    { label: "Spanish", value: "es" },
                    { label: "French", value: "fr" },
                    { label: "German", value: "de" },
                  ]}
                />
                <Input 
                  label="Max Results" 
                  type="number"
                  value={form.maxResults}
                  onChange={(e) => setForm({ ...form, maxResults: e.target.value })}
                />
              </div>
            </div>
          </Card>

          <Card>
            <div 
              style={{ display: "flex", justifyContent: "space-between", alignItems: "center", cursor: "pointer", userSelect: "none" }}
              onClick={() => setAdvancedOpen(!advancedOpen)}
            >
              <div>
                <H3 style={{ margin: 0 }}>Advanced Filters</H3>
                <Text style={{ margin: "4px 0 0 0", fontSize: "0.85rem" }}>Refine results by contact details, ratings, and status.</Text>
              </div>
              <Button variant="ghost" icon={advancedOpen ? <ChevronUp size={20}/> : <ChevronDown size={20}/>} />
            </div>

            {advancedOpen && (
              <div style={{ marginTop: "24px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", animation: "fadeIn var(--transition-normal)" }}>
                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  <Text style={{ fontWeight: 600, fontSize: "0.85rem", color: "var(--color-text-primary)", marginBottom: "4px" }}>Contact Information</Text>
                  <Switch label="Has Website" checked={filters.hasWebsite} onChange={(e) => setFilters({ ...filters, hasWebsite: e.target.checked })} />
                  <Switch label="Has Phone" checked={filters.hasPhone} onChange={(e) => setFilters({ ...filters, hasPhone: e.target.checked })} />
                  <Switch label="Has Email" checked={filters.hasEmail} onChange={(e) => setFilters({ ...filters, hasEmail: e.target.checked })} />
                </div>
                
                <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                  <Text style={{ fontWeight: 600, fontSize: "0.85rem", color: "var(--color-text-primary)", marginBottom: "4px" }}>Business Status</Text>
                  <Checkbox label="Open Now" checked={filters.openNow} onChange={(e) => setFilters({ ...filters, openNow: e.target.checked })} />
                  <Checkbox label="Verified Business" checked={filters.verified} onChange={(e) => setFilters({ ...filters, verified: e.target.checked })} />
                  <Checkbox label="Hide Permanently Closed" checked={filters.hideClosed} onChange={(e) => setFilters({ ...filters, hideClosed: e.target.checked })} />
                </div>

                <div style={{ display: "flex", gap: "16px", gridColumn: "span 2", marginTop: "8px" }}>
                  <div style={{ flex: 1 }}>
                    <Dropdown 
                      label="Minimum Rating" 
                      value={filters.minRating}
                      onChange={(e) => setFilters({ ...filters, minRating: e.target.value })}
                      options={[
                        { label: "Any Rating", value: "" },
                        { label: "3.0 & Up", value: "3" },
                        { label: "4.0 & Up", value: "4" },
                        { label: "4.5 & Up", value: "4.5" }
                      ]}
                    />
                  </div>
                  <div style={{ flex: 1 }}>
                    <Input 
                      label="Minimum Reviews" 
                      type="number"
                      placeholder="e.g. 50"
                      value={filters.minReviews}
                      onChange={(e) => setFilters({ ...filters, minReviews: e.target.value })}
                    />
                  </div>
                </div>
              </div>
            )}
          </Card>
        </div>

        {/* Right Column: Previews & History */}
        <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
          
          <Card>
            <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "16px" }}>
              <Sparkles size={16} />
              <H3 style={{ margin: 0, fontSize: "1rem" }}>Search Preview</H3>
            </div>
            
            <div style={{ display: "flex", flexDirection: "column", gap: "8px", fontFamily: "var(--font-family-mono)", fontSize: "0.85rem", color: "var(--color-text-secondary)" }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span>Category</span>
                <span style={{ fontWeight: 600, color: "var(--color-text-primary)" }}>{form.category || "Any"}</span>
              </div>
              <Divider style={{ margin: "4px 0" }} />
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span>Location</span>
                <span style={{ fontWeight: 600, color: "var(--color-text-primary)" }}>{form.location || "Anywhere"}</span>
              </div>
              {form.country && (
                <>
                  <Divider style={{ margin: "4px 0" }} />
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span>Country</span>
                    <span style={{ fontWeight: 600, color: "var(--color-text-primary)" }}>{form.country}</span>
                  </div>
                </>
              )}
              <Divider style={{ margin: "4px 0" }} />
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span>Max Results</span>
                <span style={{ fontWeight: 600, color: "var(--color-text-primary)" }}>{form.maxResults || "500"}</span>
              </div>
            </div>
            
            <Button 
              variant="primary" 
              style={{ width: "100%", marginTop: "24px" }}
              disabled={!isValid}
              onClick={handleSearch}
            >
              {isValid ? "Run Search" : "Fill required fields"}
            </Button>
          </Card>

          <Card>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <SectionHeader title="Recent Searches" style={{ margin: 0 }} />
              <Button variant="ghost" size="small" onClick={() => setViewState("history")}>View All</Button>
            </div>
            
            <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
              {recentSnippet.length === 0 ? (
                <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "16px 0", color: "var(--color-text-tertiary)" }}>
                  <Clock size={24} style={{ marginBottom: "8px", opacity: 0.5 }} />
                  <Text style={{ fontSize: "0.85rem" }}>No searches yet</Text>
                </div>
              ) : (
                recentSnippet.map((s, i) => (
                  <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px", background: "var(--color-bg-subtle)", borderRadius: "var(--radius-sm)", cursor: "pointer" }} onClick={() => handleRunFromHistory(s.request)}>
                    <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                      <Text style={{ margin: 0, fontWeight: 500, fontSize: "0.85rem" }}>{s.request.category}</Text>
                      <Text style={{ margin: 0, fontSize: "0.75rem", color: "var(--color-text-secondary)" }}>{s.request.location}</Text>
                    </div>
                    <Badge variant="default" style={{ zoom: 0.8 }}>{s.result_count}</Badge>
                  </div>
                ))
              )}
            </div>
          </Card>

        </div>
      </div>
    </div>
  );
}
