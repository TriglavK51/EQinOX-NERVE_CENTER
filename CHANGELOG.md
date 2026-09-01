# Changelog

## 1.3.0

- Added `supply_chain_sbom`, a local adapter for free OWASP cdxgen CycloneDX
	SBOM generation in pre-build mode without dependency installation.
- Added `cra_evidence_pack`, a local adapter for generating and verifying
	hash-chained EU CRA technical evidence packs from SBOMs and product manifests.
- Added Apache-2.0 attribution and license retention for the cdxgen-informed
	adapter and MIT attribution and license retention for the CRA evidence
	adapter; no third-party source code is included.

## 1.2.0

- Added categorized local-skill discovery and parallel category dispatch.
- Classified bundled adapters into SEO, GEO, crawling, security, writing,
  token optimization, code quality, DevOps, and taste categories.
- Replaced the SEO audit stub with a deterministic static HTML audit that runs
	fully offline.
- Added MIT license retention and attribution for the SEOmator-informed audit
	scope and Taste Skill-informed frontend review scope; no third-party source
	code is included.
- Added the `openserp` adapter for a free, self-hosted local SERP API, limited
	to loopback connections and documented with its MIT license.

## 1.1.0

- Added the local MCP service, dispatcher, vault, CLI, VS Code shim, and offline test suite.
- Added 15 discoverable, local-only skill adapters with deterministic fallbacks.
- Added a validated tool registry and a complete skill-authoring guide.

## 0.1.0

- Initial production scaffold.