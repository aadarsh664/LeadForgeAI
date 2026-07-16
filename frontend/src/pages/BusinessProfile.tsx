import React from "react";
import { 
  Card, Button, Badge, H2, H3, Text, Divider,
  SectionHeader, Avatar 
} from "../design-system/components";
import { 
  ArrowLeft, Star, Phone, Globe, Mail, MapPin, CheckCircle2,
  Clock, FileText,
  Map, Calendar, Database, Sparkles, Megaphone, CheckCircle
} from "lucide-react";
import type { NormalizedBusiness } from "../../types/search";

interface BusinessProfileProps {
  business: NormalizedBusiness;
  onBack: () => void;
}

export default function BusinessProfile({ business, onBack }: BusinessProfileProps) {
  const isDemo = business.raw_data?.demo_data === True || business.raw_data?.demo_data === true;
  
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
      
      {/* Header Navigation */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <Button variant="ghost" onClick={onBack} icon={<ArrowLeft size={16}/>}>
          Back to Results
        </Button>
        <div style={{ display: "flex", gap: "12px" }}>
          <Button variant="secondary" icon={<FileText size={16}/>}>Export PDF</Button>
          <Button variant="primary" icon={<CheckCircle size={16}/>}>Save to CRM</Button>
        </div>
      </div>

      {/* Main Grid */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 380px", gap: "24px", alignItems: "start" }}>
        
        {/* Left Column */}
        <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
          
          {/* Business Header */}
          <Card>
            <div style={{ display: "flex", gap: "24px", alignItems: "flex-start" }}>
              <Avatar fallback={business.name.substring(0, 2).toUpperCase()} size={80} style={{ borderRadius: "var(--radius-lg)" }} />
              <div style={{ flex: 1 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                  <H2 style={{ margin: "0 0 8px 0", fontSize: "1.75rem" }}>{business.name}</H2>
                  {isDemo && <Badge variant="warning">Demo Data</Badge>}
                </div>
                
                <div style={{ display: "flex", gap: "16px", alignItems: "center", marginBottom: "16px" }}>
                  <Badge variant="default">{business.category}</Badge>
                  <div style={{ display: "flex", alignItems: "center", gap: "4px", color: "#f59e0b", fontWeight: 600 }}>
                    <Star size={16} fill="currentColor" /> {business.rating || "N/A"}
                  </div>
                  <Text style={{ margin: 0, fontSize: "0.9rem", color: "var(--color-text-tertiary)" }}>
                    ({business.reviews || 0} reviews)
                  </Text>
                  {business.is_open ? (
                    <Badge variant="success">Open Now</Badge>
                  ) : (
                    <Badge variant="danger">Closed</Badge>
                  )}
                </div>

                <Text style={{ margin: 0, color: "var(--color-text-secondary)" }}>
                  {business.raw_data?.description || "No description available for this business."}
                </Text>
              </div>
            </div>
          </Card>

          {/* Business Details */}
          <Card>
            <SectionHeader title="Business Details" />
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px" }}>
              <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                <div>
                  <Text style={{ fontSize: "0.75rem", fontWeight: 600, color: "var(--color-text-tertiary)", marginBottom: "4px", textTransform: "uppercase", letterSpacing: "0.05em" }}>Category</Text>
                  <Text style={{ margin: 0 }}>{business.category}</Text>
                </div>
                <div>
                  <Text style={{ fontSize: "0.75rem", fontWeight: 600, color: "var(--color-text-tertiary)", marginBottom: "4px", textTransform: "uppercase", letterSpacing: "0.05em" }}>Verification Status</Text>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    {business.is_verified ? <CheckCircle2 size={16} color="var(--color-success)"/> : <Clock size={16} color="var(--color-text-tertiary)"/>}
                    <Text style={{ margin: 0 }}>{business.is_verified ? "Verified Claim" : "Unverified"}</Text>
                  </div>
                </div>
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
                <div>
                  <Text style={{ fontSize: "0.75rem", fontWeight: 600, color: "var(--color-text-tertiary)", marginBottom: "4px", textTransform: "uppercase", letterSpacing: "0.05em" }}>Source Provider</Text>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <Database size={16} color="var(--color-text-secondary)"/>
                    <Text style={{ margin: 0, textTransform: "capitalize" }}>{business.provider_source}</Text>
                  </div>
                </div>
                <div>
                  <Text style={{ fontSize: "0.75rem", fontWeight: 600, color: "var(--color-text-tertiary)", marginBottom: "4px", textTransform: "uppercase", letterSpacing: "0.05em" }}>Discovery Date</Text>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <Calendar size={16} color="var(--color-text-secondary)"/>
                    <Text style={{ margin: 0 }}>{new Date(business.discovery_date).toLocaleDateString()}</Text>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {/* AI Analysis Placeholder */}
          <Card style={{ backgroundColor: "var(--color-bg-subtle)", border: "1px dashed var(--color-border-strong)" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "16px", color: "var(--color-primary)" }}>
              <Sparkles size={20} />
              <H3 style={{ margin: 0, fontSize: "1rem" }}>AI Lead Analysis</H3>
            </div>
            <Text style={{ margin: 0, color: "var(--color-text-tertiary)" }}>
              AI Analysis will appear here. Future updates will automatically scrape their website, score the lead quality, and identify decision makers.
            </Text>
          </Card>

        </div>

        {/* Right Column */}
        <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
          
          {/* Contact Card */}
          <Card>
            <SectionHeader title="Contact Information" />
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              
              <div style={{ display: "flex", gap: "12px", alignItems: "flex-start" }}>
                <div style={{ background: "var(--color-bg-subtle)", padding: "8px", borderRadius: "50%", color: "var(--color-text-secondary)" }}>
                  <Phone size={16} />
                </div>
                <div style={{ flex: 1 }}>
                  <Text style={{ margin: "0 0 4px 0", fontSize: "0.75rem", color: "var(--color-text-tertiary)" }}>Phone Number</Text>
                  <Text style={{ margin: 0, fontWeight: 500 }}>{business.phone || "Not Available"}</Text>
                </div>
                <Button variant="ghost" size="small">Copy</Button>
              </div>

              <Divider style={{ margin: 0 }} />

              <div style={{ display: "flex", gap: "12px", alignItems: "flex-start" }}>
                <div style={{ background: "var(--color-bg-subtle)", padding: "8px", borderRadius: "50%", color: "var(--color-text-secondary)" }}>
                  <Mail size={16} />
                </div>
                <div style={{ flex: 1 }}>
                  <Text style={{ margin: "0 0 4px 0", fontSize: "0.75rem", color: "var(--color-text-tertiary)" }}>Email Address</Text>
                  <Text style={{ margin: 0, fontWeight: 500 }}>{business.email || "Not Available"}</Text>
                </div>
                <Button variant="ghost" size="small">Copy</Button>
              </div>

              <Divider style={{ margin: 0 }} />

              <div style={{ display: "flex", gap: "12px", alignItems: "flex-start" }}>
                <div style={{ background: "var(--color-bg-subtle)", padding: "8px", borderRadius: "50%", color: "var(--color-text-secondary)" }}>
                  <Globe size={16} />
                </div>
                <div style={{ flex: 1 }}>
                  <Text style={{ margin: "0 0 4px 0", fontSize: "0.75rem", color: "var(--color-text-tertiary)" }}>Website</Text>
                  {business.website ? (
                    <a href={business.website} target="_blank" rel="noreferrer" style={{ color: "var(--color-primary)", textDecoration: "none", fontWeight: 500 }}>{business.website}</a>
                  ) : (
                    <Text style={{ margin: 0, fontWeight: 500 }}>Not Available</Text>
                  )}
                </div>
              </div>

            </div>
          </Card>

          {/* Location Card */}
          <Card>
            <SectionHeader title="Location" />
            <div style={{ display: "flex", gap: "12px", alignItems: "flex-start", marginBottom: "16px" }}>
              <MapPin size={16} color="var(--color-text-secondary)" style={{ marginTop: "2px" }} />
              <div>
                <Text style={{ margin: 0, fontWeight: 500 }}>{business.address || "No Street Address"}</Text>
                <Text style={{ margin: "4px 0 0 0", color: "var(--color-text-secondary)", fontSize: "0.85rem" }}>
                  {[business.city, business.state, business.country].filter(Boolean).join(", ")}
                </Text>
              </div>
            </div>

            <div style={{ height: "120px", background: "var(--color-bg-subtle)", borderRadius: "var(--radius-md)", display: "flex", justifyContent: "center", alignItems: "center", border: "1px solid var(--color-border-subtle)" }}>
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "8px", color: "var(--color-text-tertiary)" }}>
                <Map size={24} />
                <span style={{ fontSize: "0.8rem" }}>Interactive Map (Coming Soon)</span>
              </div>
            </div>
          </Card>

          {/* Online Presence */}
          <Card>
            <SectionHeader title="Online Presence" />
            <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "var(--color-text-secondary)" }}><Globe size={16}/> <span>Facebook</span></div>
                <Text style={{ margin: 0, fontSize: "0.85rem" }}>Not Available</Text>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "var(--color-text-secondary)" }}><Globe size={16}/> <span>Instagram</span></div>
                <Text style={{ margin: 0, fontSize: "0.85rem" }}>Not Available</Text>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "var(--color-text-secondary)" }}><Globe size={16}/> <span>Twitter/X</span></div>
                <Text style={{ margin: 0, fontSize: "0.85rem" }}>Not Available</Text>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "var(--color-text-secondary)" }}><Globe size={16}/> <span>LinkedIn</span></div>
                <Text style={{ margin: 0, fontSize: "0.85rem" }}>Not Available</Text>
              </div>
            </div>
          </Card>

          {/* Notes */}
          <Card>
            <SectionHeader title="Notes" />
            <Text style={{ margin: 0, color: "var(--color-text-tertiary)", fontSize: "0.9rem", fontStyle: "italic" }}>
              No notes yet.
            </Text>
          </Card>

          {/* Campaigns */}
          <Card>
            <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "16px" }}>
              <Megaphone size={16} color="var(--color-text-secondary)" />
              <H3 style={{ margin: 0, fontSize: "1rem" }}>Active Campaigns</H3>
            </div>
            <Text style={{ margin: 0, color: "var(--color-text-tertiary)", fontSize: "0.9rem" }}>
              No Campaigns Yet.
            </Text>
          </Card>

        </div>
      </div>
    </div>
  );
}
