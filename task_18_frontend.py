import os

file_path = "frontend/src/pages/BusinessPage.tsx"
with open(file_path, "r") as f:
    content = f.read()

# Add provider to SearchFormState
if "provider: string;" not in content:
    content = content.replace(
        "excludeKeywords: string;\n}",
        "excludeKeywords: string;\n  provider: string;\n}"
    )

if 'provider: "google_maps"' not in content:
    content = content.replace(
        'excludeKeywords: ""\n};',
        'excludeKeywords: "",\n  provider: "google_maps"\n};'
    )

# Add provider dropdown to UI
# Find "Max Results" input and insert Provider dropdown next to it
provider_dropdown = """<Dropdown 
                  label="Provider"
                  value={form.provider}
                  onChange={(e) => setForm({ ...form, provider: e.target.value })}
                  options={[
                    { label: "Google Maps (Real Data)", value: "google_maps" },
                    { label: "Mock Data (Demo)", value: "mock" }
                  ]}
                />"""

if "Provider" not in content and "google_maps" not in content:
    content = content.replace(
        '<Input \n                  label="Max Results"',
        provider_dropdown + '\n                <Input \n                  label="Max Results"'
    )

# Also update handleSearch to pass provider
if 'provider: form.provider,' not in content:
    content = content.replace(
        'max_results: parseInt(form.maxResults) || 500,',
        'max_results: parseInt(form.maxResults) || 500,\n      provider: form.provider,'
    )

with open(file_path, "w") as f:
    f.write(content)

print("BusinessPage.tsx updated for provider selection.")
