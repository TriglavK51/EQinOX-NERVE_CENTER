# OpenSERP: Free Local API Setup

The `openserp` adapter needs a self-hosted OpenSERP process. It has no API key,
subscription, or Nerve-Center configuration change. The adapter permits only
HTTP(S) loopback addresses and defaults to `http://127.0.0.1:7000`.

## Install and Start

OpenSERP requires Go as specified by its own project. From its source directory
in the read-only EQinOX resource catalog, run:

```powershell
go build -o openserp.exe .
.\openserp.exe serve -a 127.0.0.1 -p 7000
```

Alternatively, install it with Go:

```powershell
go install github.com/karust/openserp@latest
openserp serve -a 127.0.0.1 -p 7000
```

## Use Through Nerve-Center

```json
{
  "tool": "openserp",
  "input": {
    "query": "local SEO audit",
    "engines": ["duckduckgo"],
    "limit": 10
  }
}
```

The local OpenSERP service may query search engines. Its operation must comply
with the terms and applicable rules of each selected engine. Nerve-Center sends
no request directly to an external API, stores no API key, and has no paid
service dependency.