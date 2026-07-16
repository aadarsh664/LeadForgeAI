import React, { useState, useEffect } from "react";
import {
  Card,
  H2,
  H3,
  Text,
  Button,
  Input,
  SearchInput,
  Divider,
  Switch,
  Checkbox,
  Badge,
  PageHeader,
  SectionHeader,
  Dropdown
} from "../design-system/components";
import { Search, RotateCcw, MapPin, Building2, Tag, ChevronDown, ChevronUp, Clock, Sparkles } from "lucide-react";

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
  excludeKeywords: ""
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
  const [form, setForm] = useState<SearchFormState>(defaultForm);
  const [filters, setFilters] = useState<FilterState>(defaultFilters);
  const [advancedOpen, setAdvancedOpen] = useState(false);

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
  }, []);

  // Save state on change
  useEffect(() => {
    const timeout = setTimeout(() => {
      localStorage.setItem("leadforgeai_search_form", JSON.stringify({ form, filters }));
    }, 500);
    return () => clearTimeout(timeout);
  }, [form, filters]);

  const isValid = form.category.trim() !== "" && form.location.trim() !== "";

  const handleReset = () => {
    setForm(defaultForm);
    setFilters(defaultFilters);
    localStorage.removeItem("leadforgeai_search_form");
  };

  const handleSearch = () => {
    // In future this will trigger backend request
    console.log("Searching with", form, filters);
  };

  return (
    <div className="page-container" style={{ padding: "0 16px 64px 16px" }}>
      <PageHeader 
        title="Business Search" 
        description="Discover local businesses and generate high-quality leads."
        action={
          <div style={{ display: 'flex', gap: '12px' }}>
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
          
          <Card style={{ backgroundColor: "var(--color-primary)", color: "var(--color-text-inverse)", borderColor: "transparent" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "16px" }}>
              <Sparkles size={16} />
              <H3 style={{ margin: 0, color: "var(--color-text-inverse)", fontSize: "1rem" }}>Search Preview</H3>
            </div>
            
            <div style={{ display: "flex", flexDirection: "column", gap: "8px", fontFamily: "var(--font-family-mono)", fontSize: "0.85rem", color: "rgba(255,255,255,0.8)" }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span>Category</span>
                <span style={{ color: "white", fontWeight: 600 }}>{form.category || "Any"}</span>
              </div>
              <Divider style={{ borderColor: "rgba(255,255,255,0.1)", margin: "4px 0" }} />
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span>Location</span>
                <span style={{ color: "white", fontWeight: 600 }}>{form.location || "Anywhere"}</span>
              </div>
              {form.country && (
                <>
                  <Divider style={{ borderColor: "rgba(255,255,255,0.1)", margin: "4px 0" }} />
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span>Country</span>
                    <span style={{ color: "white", fontWeight: 600 }}>{form.country}</span>
                  </div>
                </>
              )}
              <Divider style={{ borderColor: "rgba(255,255,255,0.1)", margin: "4px 0" }} />
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span>Max Results</span>
                <span style={{ color: "white", fontWeight: 600 }}>{form.maxResults || "500"}</span>
              </div>
            </div>
            
            <Button 
              variant="secondary" 
              style={{ width: "100%", marginTop: "24px", color: "var(--color-primary)", background: "white" }}
              disabled={!isValid}
              onClick={handleSearch}
            >
              {isValid ? "Run Search" : "Fill required fields"}
            </Button>
          </Card>

          <Card>
            <SectionHeader title="Saved Templates" />
            <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
              {["Local Businesses", "Restaurants", "Hospitals", "Schools", "Gyms", "Real Estate", "Lawyers", "Hotels", "Clinics"].map(t => (
                <Badge key={t} variant="default" style={{ cursor: "pointer", padding: "6px 12px", border: "1px solid var(--color-border-subtle)" }}>
                  {t}
                </Badge>
              ))}
            </div>
          </Card>

          <Card>
            <SectionHeader title="Recent Searches" />
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "24px 0", color: "var(--color-text-tertiary)" }}>
              <Clock size={24} style={{ marginBottom: "8px", opacity: 0.5 }} />
              <Text style={{ fontSize: "0.85rem" }}>No searches yet</Text>
            </div>
          </Card>

          <Card>
            <SectionHeader title="Search Tips" />
            <ul style={{ margin: 0, padding: "0 0 0 16px", fontSize: "0.85rem", color: "var(--color-text-secondary)", display: "flex", flexDirection: "column", gap: "8px" }}>
              <li>Be specific with your location (City + State works best).</li>
              <li>Use keywords to narrow down niche businesses.</li>
              <li>Exclude words like "chain" to find independent shops.</li>
              <li>Set a radius to restrict wide area searches.</li>
              <li>Filter by "Has Website" for higher quality leads.</li>
            </ul>
          </Card>

        </div>
      </div>
    </div>
  );
}
