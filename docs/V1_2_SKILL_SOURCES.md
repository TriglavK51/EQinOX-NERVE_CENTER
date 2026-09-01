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

The included adapters are independent implementations. Neither includes source
code or prose copied from the referenced project; the retained license and
attribution documents preserve provenance required by this release policy.

## Excluded Sources

| Source | Reason for exclusion |
| --- | --- |
| LibreCrawl | Crawling remote URLs requires network access. |
| GEORank | Core diagnostics depend on an AI service/API. |
| SkillOpt | Declares an external OpenAI dependency. |
| worldmonitor | AGPL license is outside the allowed license set. |
| gego | GPL-3.0 license is outside the allowed license set. |

Other source directories were retained only as read-only research material and
are not shipped in Nerve-Center v1.2.