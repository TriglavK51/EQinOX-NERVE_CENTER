# v1.2 Skill Source and License Review

## Inclusion Rules

v1.2 accepts only sources with an MIT or Apache-2.0 license and keeps runtime
execution local. An adapter may not require an API key, external service, or
network egress. The Nerve-Center default configuration continues to set
`allowExternalEgress` to `false`.

## Included Scope

| Source | License | v1.2 outcome | License record |
| --- | --- | --- | --- |
| SEOmator SEO Audit Tool & Skill | MIT | Added independent static HTML audit scope to `seo_audit` | `tools/seo_audit/THIRD_PARTY_LICENSES/SEOmator-MIT.txt` |
| Taste Skill | MIT | Added independent static frontend review scope as `taste_review` | `tools/taste_review/THIRD_PARTY_LICENSES/Taste-Skill-MIT.txt` |
| OpenSERP | MIT | Added loopback-only client for a free self-hosted API | `tools/openserp/THIRD_PARTY_LICENSES/OpenSERP-MIT.txt` |
| Geo Skills | MIT | Added four independent offline GEO adapters: citability, `llms.txt`, AI crawler policy and measurement | `tools/geo_citability/THIRD_PARTY_LICENSES/Geo-Skills-MIT.txt` |

The included adapters are independent implementations. Neither includes source
code or prose copied from the referenced project; the retained license and
attribution documents preserve provenance required by this release policy.

## Self-Hosted Integrations

The following MIT sources are eligible only as separately deployed, local
services. Nerve-Center does not vendor their application code or dependencies;
an adapter may be added only after its loopback API contract is verified.

| Source | Free connection | Reason not embedded |
| --- | --- | --- |
| CrawlSEO | Self-hosted Docker + Google OAuth / Google Autocomplete fallback | Full Next.js/PostgreSQL application. |
| Elmo | Self-hosted Docker Compose | Full application; live engine providers may need credentials. |
| Getcito | Self-hosted Docker Compose | Full application; live providers require configured keys. |
| GEORank | Self-hosted Docker Compose | Full application; model features use an operator-provided API. |

## Excluded Sources

| Source | Reason for exclusion |
| --- | --- |
| LibreCrawl | Crawling remote URLs requires network access. |
| Goose AEO | Real measurements require paid AI provider API calls. |
| Potato | Its free mock is a demonstration, not a measurement of a live answer engine. |
| SkillOpt | Training requires a model backend; it is not an audit runtime. |
| worldmonitor | AGPL license is outside the allowed license set. |
| gego | GPL-3.0 license is outside the allowed license set. |

Other source directories were retained only as read-only research material and
are not shipped in Nerve-Center v1.2.