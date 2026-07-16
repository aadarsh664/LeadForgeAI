import React, { useState } from "react";
import { 
  Card, Button, Badge, Checkbox, Dropdown, H3, Text, Divider,
  SectionHeader, Avatar 
} from "../design-system/components";
import { 
  Search, LayoutGrid, List as ListIcon, MapPin, Star, Phone, Globe, 
  Mail, Map, RefreshCcw, Download, CheckSquare, Square
} from "lucide-react";
import type { NormalizedBusiness } from "../../types/search";

interface BusinessResultsProps {
  results: NormalizedBusiness[];
  onBack: () => void;
}

export default function BusinessResults({ results, onBack }: BusinessResultsProps) {
  const [viewMode, setViewMode] = useState<"card" | "table">("card");
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());

  const handleSelectAll = () => {
    if (selectedIds.size === results.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(results.map(r => r.business_id)));
    }
  };

  const toggleSelect = (id: string) => {
    const newSet = new Set(selectedIds);
    if (newSet.has(id)) newSet.delete(id);
    else newSet.add(id);
    setSelectedIds(newSet);
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
      
      {/* Toolbar */}
      <Card style={{ padding: "16px 24px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "24px" }}>
          <div>
            <H3 style={{ margin: 0 }}>Search Results</H3>
            <Text style={{ margin: "4px 0 0 0", fontSize: "0.85rem" }}>{results.length} businesses found</Text>
          </div>
          <Divider style={{ width: "1px", height: "32px", borderTop: "none", borderLeft: "1px solid var(--color-border-default)", margin: 0 }} />
          <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
            <Button variant="ghost" onClick={handleSelectAll} icon={selectedIds.size === results.length ? <CheckSquare size={16}/> : <Square size={16}/>}>
              {selectedIds.size === results.length ? "Deselect All" : "Select All"}
            </Button>
            <span style={{ fontSize: "0.85rem", color: "var(--color-text-tertiary)" }}>
              {selectedIds.size} selected
            </span>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <Dropdown 
            label=""
            value="relevance"
            onChange={() => {}}
            options={[
              { label: "Sort: Relevance", value: "relevance" },
              { label: "Sort: Rating", value: "rating" },
              { label: "Sort: Reviews", value: "reviews" }
            ]}
          />
          <div style={{ display: "flex", background: "var(--color-bg-subtle)", padding: "4px", borderRadius: "var(--radius-md)", border: "1px solid var(--color-border-subtle)" }}>
            <button 
              onClick={() => setViewMode("card")}
              style={{ background: viewMode === "card" ? "var(--color-bg-base)" : "transparent", border: "none", padding: "6px", borderRadius: "var(--radius-sm)", cursor: "pointer", boxShadow: viewMode === "card" ? "var(--shadow-sm)" : "none" }}
            >
              <LayoutGrid size={16} color={viewMode === "card" ? "var(--color-text-primary)" : "var(--color-text-tertiary)"} />
            </button>
            <button 
              onClick={() => setViewMode("table")}
              style={{ background: viewMode === "table" ? "var(--color-bg-base)" : "transparent", border: "none", padding: "6px", borderRadius: "var(--radius-sm)", cursor: "pointer", boxShadow: viewMode === "table" ? "var(--shadow-sm)" : "none" }}
            >
              <ListIcon size={16} color={viewMode === "table" ? "var(--color-text-primary)" : "var(--color-text-tertiary)"} />
            </button>
          </div>
          <Button variant="ghost" icon={<RefreshCcw size={16}/>} />
          <Button variant="ghost" icon={<Download size={16}/>} disabled>Export</Button>
          <Button variant="secondary" onClick={onBack}>Back to Search</Button>
        </div>
      </Card>

      {/* Content */}
      {viewMode === "card" ? (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(350px, 1fr))", gap: "24px" }}>
          {results.map(business => (
            <Card key={business.business_id} style={{ display: "flex", flexDirection: "column", gap: "16px", cursor: "pointer" }}>
              <div style={{ display: "flex", gap: "12px", alignItems: "flex-start" }}>
                <div onClick={(e) => { e.stopPropagation(); toggleSelect(business.business_id); }}>
                  <Checkbox checked={selectedIds.has(business.business_id)} onChange={() => toggleSelect(business.business_id)} />
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                    <H3 style={{ margin: "0 0 4px 0", fontSize: "1.1rem" }}>{business.name}</H3>
                    {business.raw_data?.demo_data && <Badge variant="warning">Demo Data</Badge>}
                  </div>
                  <Text style={{ margin: 0, fontSize: "0.85rem", color: "var(--color-text-secondary)" }}>{business.category}</Text>
                  
                  <div style={{ display: "flex", gap: "12px", alignItems: "center", marginTop: "12px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "4px", color: "#f59e0b", fontSize: "0.85rem", fontWeight: 600 }}>
                      <Star size={14} fill="currentColor" /> {business.rating}
                    </div>
                    <span style={{ color: "var(--color-text-tertiary)", fontSize: "0.85rem" }}>({business.reviews} reviews)</span>
                  </div>
                </div>
              </div>

              <Divider style={{ margin: 0 }} />

              <div style={{ display: "flex", flexDirection: "column", gap: "12px", fontSize: "0.85rem", color: "var(--color-text-secondary)" }}>
                <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                  <MapPin size={16} /> <span>{business.address}, {business.city}</span>
                </div>
                <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                  <Phone size={16} /> <span>{business.phone}</span>
                </div>
                <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                  <Globe size={16} /> <a href={business.website} target="_blank" rel="noreferrer" style={{ color: "var(--color-primary)", textDecoration: "none" }}>{business.website}</a>
                </div>
                <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                  <Mail size={16} /> <span>{business.email}</span>
                </div>
              </div>
              
              <Button variant="ghost" style={{ marginTop: "auto", alignSelf: "flex-start" }} disabled icon={<Map size={16}/>}>
                Open Maps
              </Button>
            </Card>
          ))}
        </div>
      ) : (
        <Card style={{ padding: 0, overflow: "hidden" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.85rem" }}>
            <thead>
              <tr style={{ background: "var(--color-bg-subtle)", borderBottom: "1px solid var(--color-border-subtle)", textAlign: "left", color: "var(--color-text-secondary)" }}>
                <th style={{ padding: "16px", width: "40px" }}><Checkbox checked={selectedIds.size === results.length && results.length > 0} onChange={handleSelectAll}/></th>
                <th style={{ padding: "16px" }}>Business</th>
                <th style={{ padding: "16px" }}>Rating</th>
                <th style={{ padding: "16px" }}>Contact</th>
                <th style={{ padding: "16px" }}>Location</th>
              </tr>
            </thead>
            <tbody>
              {results.map(business => (
                <tr key={business.business_id} style={{ borderBottom: "1px solid var(--color-border-subtle)" }}>
                  <td style={{ padding: "16px" }}>
                    <Checkbox checked={selectedIds.has(business.business_id)} onChange={() => toggleSelect(business.business_id)} />
                  </td>
                  <td style={{ padding: "16px" }}>
                    <div style={{ fontWeight: 600, color: "var(--color-text-primary)", marginBottom: "4px" }}>
                      {business.name} {business.raw_data?.demo_data && <Badge variant="warning" style={{ zoom: 0.8, marginLeft: "8px" }}>Demo</Badge>}
                    </div>
                    <div style={{ color: "var(--color-text-secondary)" }}>{business.category}</div>
                  </td>
                  <td style={{ padding: "16px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "4px", color: "#f59e0b", fontWeight: 600 }}>
                      <Star size={14} fill="currentColor" /> {business.rating}
                    </div>
                    <div style={{ color: "var(--color-text-tertiary)", marginTop: "4px" }}>{business.reviews} reviews</div>
                  </td>
                  <td style={{ padding: "16px", color: "var(--color-text-secondary)" }}>
                    <div>{business.phone}</div>
                    <div>{business.email}</div>
                  </td>
                  <td style={{ padding: "16px", color: "var(--color-text-secondary)" }}>
                    <div>{business.address}</div>
                    <div>{business.city}, {business.country}</div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      )}

      {/* Pagination Placeholder */}
      <div style={{ display: "flex", justifyContent: "center", marginTop: "16px" }}>
        <div style={{ display: "flex", gap: "8px" }}>
          <Button variant="ghost" disabled>Previous</Button>
          <Button variant="primary">1</Button>
          <Button variant="ghost">2</Button>
          <Button variant="ghost">3</Button>
          <Button variant="ghost">Next</Button>
        </div>
      </div>
    </div>
  );
}
