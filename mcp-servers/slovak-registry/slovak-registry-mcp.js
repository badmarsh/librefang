#!/usr/bin/env node
/**
 * Slovak Registry MCP Server v1.0
 *
 * Queries two public Slovak government registries:
 *   - ORSR (Obchodný register SR) — orsr.sk — company ownership
 *   - RPO (Register partnerov verejného sektora) — rpo.sk — beneficial ownership
 *
 * Used by source-rater agent to populate the `ownership_flag` component of:
 *   credibility_score = weighted_avg(accuracy_history=0.5, bias_score=0.3, ownership_flag=0.2)
 *
 * Tools exposed:
 *   - lookup_company(company_name)      → ORSR company record + owners
 *   - lookup_beneficial_owner(name)     → RPO beneficial ownership chain
 *   - get_media_ownership(domain)       → Combined lookup for a news outlet domain
 *   - assess_ownership_flag(domain)     → Returns 0.0–1.0 flag for credibility formula
 *
 * Install: npm install -g @modelcontextprotocol/sdk node-fetch cheerio
 * Run:     node slovak-registry-mcp.js
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

// ─── HTTP fetch helper (Node 18+ has native fetch) ───────────────────────────
async function fetchHtml(url, timeoutMs = 8000) {
  const controller = new AbortController();
  const tid = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'MedialnyDezolator/1.0 OwnershipVerification (+https://github.com/badmarsh/librefang)',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'sk,en;q=0.8',
      },
    });
    clearTimeout(tid);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.text();
  } catch (e) {
    clearTimeout(tid);
    throw e;
  }
}

// ─── ORSR parser ─────────────────────────────────────────────────────────────
async function queryOrsr(companyName) {
  /**
   * Queries orsr.sk search endpoint.
   * Returns: { ico, company_name, address, registered, partners, statutory, found }
   */
  const encoded = encodeURIComponent(companyName);
  const searchUrl = `https://www.orsr.sk/hladaj_subjekt.asp?OBMENO=${encoded}&SID=0&T=&ICO=&ROK=0&SEKCIA=0&akcia=vyhladaj`;

  let html;
  try {
    html = await fetchHtml(searchUrl);
  } catch (e) {
    return { found: false, error: `ORSR fetch failed: ${e.message}`, source: 'orsr.sk' };
  }

  // Extract first result link
  const linkMatch = html.match(/href="(vypis\.asp\?[^"]+)"/);
  if (!linkMatch) {
    return { found: false, note: 'No results on orsr.sk', query: companyName, source: 'orsr.sk' };
  }

  const detailUrl = `https://www.orsr.sk/${linkMatch[1]}`;
  let detailHtml;
  try {
    detailHtml = await fetchHtml(detailUrl);
  } catch (e) {
    return { found: false, error: `ORSR detail fetch failed: ${e.message}`, source: 'orsr.sk' };
  }

  // Parse key fields from the ORSR detail page (table-based layout)
  const extract = (label) => {
    const rx = new RegExp(`${label}[^<]*</td>\\s*<td[^>]*>([^<]{3,200})`, 'i');
    const m = detailHtml.match(rx);
    return m ? m[1].replace(/&amp;/g, '&').replace(/&nbsp;/g, ' ').trim() : null;
  };

  // Extract ICO
  const icoMatch = detailHtml.match(/IČO\s*:?\s*<\/td>\s*<td[^>]*>(\d{8})/);
  const ico = icoMatch ? icoMatch[1] : null;

  // Extract shareholders/partners section
  const partnersMatch = detailHtml.match(/Spoloníci[\s\S]{0,3000}?([\s\S]*?)(?:Štatutárny|Dozorná)/i);
  const partnersRaw = partnersMatch ? partnersMatch[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim() : null;

  // Extract statutory reps
  const statutoryMatch = detailHtml.match(/Štatutárny orgán[\s\S]*?<td[^>]*>([\s\S]{0,500})/i);
  const statutoryRaw = statutoryMatch
    ? statutoryMatch[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 300)
    : null;

  // Extract company name from page
  const nameMatch = detailHtml.match(/<h2[^>]*>([^<]{5,150})<\/h2>/i);
  const resolvedName = nameMatch ? nameMatch[1].trim() : companyName;

  return {
    found: true,
    source: 'orsr.sk',
    url: detailUrl,
    ico,
    company_name: resolvedName,
    partners_raw: partnersRaw ? partnersRaw.slice(0, 500) : null,
    statutory_raw: statutoryRaw,
    note: 'Raw text extracted — structured parsing requires court-specific HTML variants',
  };
}

// ─── RPO parser ──────────────────────────────────────────────────────────────
async function queryRpo(companyName) {
  /**
   * Queries rpo.gov.sk (Register partnerov verejného sektora).
   * Returns beneficial ownership chain for public sector partners.
   */
  const encoded = encodeURIComponent(companyName);
  const url = `https://rpvs.gov.sk/rpvs/Partner/PartnerPublicProfile/SearchPartner?searchString=${encoded}`;

  let html;
  try {
    html = await fetchHtml(url);
  } catch (e) {
    return { found: false, error: `RPO fetch failed: ${e.message}`, source: 'rpvs.gov.sk' };
  }

  if (html.includes('Nenašli sa žiadne') || html.includes('no results')) {
    return { found: false, note: 'Not registered in RPO (not a public sector partner)', source: 'rpvs.gov.sk' };
  }

  // RPO is React-rendered — extract JSON state if embedded
  const jsonMatch = html.match(/window\.__INITIAL_STATE__\s*=\s*({[\s\S]+?});/);
  if (jsonMatch) {
    try {
      const state = JSON.parse(jsonMatch[1]);
      return { found: true, source: 'rpvs.gov.sk', data: state };
    } catch (_) {}
  }

  // Fallback: text extraction
  const nameMatches = [...html.matchAll(/<td[^>]*>([A-ZÁČĎÉÍĽŇÓŠŤÚÝŽ][^<]{5,80})<\/td>/gi)];
  const names = nameMatches.map(m => m[1].trim()).filter(n => n.length > 5).slice(0, 10);

  return {
    found: names.length > 0,
    source: 'rpvs.gov.sk',
    beneficial_owners_raw: names,
    note: 'Partial extraction — RPO uses server-side rendering',
  };
}

// ─── Domain → company name mapping ──────────────────────────────────────────
const KNOWN_DOMAIN_COMPANIES = {
  'hlavnespravy.sk': 'Hlavné správy',
  'dennikn.sk': 'N Press s.r.o.',
  'sme.sk': 'Petit Press a.s.',
  'pravda.sk': 'PEREX a.s.',
  'aktuality.sk': 'Ringier Slovakia Media s.r.o.',
  'cas.sk': 'Ringier Slovakia Media s.r.o.',
  'tvnoviny.sk': 'MARKÍZA - SLOVAKIA, spol. s r.o.',
  'ta3.com': 'C.E.N. s.r.o.',
  'rtvs.sk': 'Rozhlas a televízia Slovenska',
  'postoj.sk': 'Postoj Media s.r.o.',
  'refresher.sk': 'Refresher Media s.r.o.',
  'infovojna.sk': 'Infovojna',
  'zem-a-vek.sk': 'Zem a Vek',
  'slobodnyvysielac.sk': 'Slobodný vysielač',
};

// Known ownership flags (0.0 = state/public, 0.5 = neutral/unknown, 1.0 = opaque/foreign adversarial)
const KNOWN_OWNERSHIP_FLAGS = {
  'hlavnespravy.sk': 0.8,    // Opaque ownership, links to far-right networks
  'dennikn.sk': 0.1,         // N Press — independent, transparent ownership (Hoss family)
  'sme.sk': 0.2,             // Petit Press — Slovak private, transparent
  'pravda.sk': 0.3,          // PEREX — Slovak private
  'aktuality.sk': 0.3,       // Ringier Switzerland — transparent foreign ownership
  'cas.sk': 0.3,             // Ringier Switzerland
  'tvnoviny.sk': 0.3,        // Central European Media Enterprises
  'ta3.com': 0.4,            // Slovak private, less transparent
  'rtvs.sk': 0.0,            // Public broadcaster
  'postoj.sk': 0.2,          // Catholic media, transparent
  'infovojna.sk': 0.9,       // Opaque, known Kremlin-adjacent
  'zem-a-vek.sk': 0.9,       // Opaque, conspiracy/disinfo outlet
  'slobodnyvysielac.sk': 0.85, // Opaque, pro-Russia fringe
};

// ─── Tool implementations ────────────────────────────────────────────────────
async function toolLookupCompany(args) {
  const { company_name } = args;
  if (!company_name) throw new Error('company_name is required');
  const [orsr, rpo] = await Promise.all([queryOrsr(company_name), queryRpo(company_name)]);
  return { orsr, rpo, queried_name: company_name };
}

async function toolGetMediaOwnership(args) {
  const { domain } = args;
  if (!domain) throw new Error('domain is required');
  const companyName = KNOWN_DOMAIN_COMPANIES[domain.toLowerCase()];
  if (!companyName) {
    return {
      domain,
      note: 'Domain not in known mapping — performing text search on domain name',
      orsr: await queryOrsr(domain.replace('.sk', '').replace('.', ' ')),
      rpo: { found: false, note: 'RPO requires exact company name' },
      known_ownership_flag: null,
    };
  }
  const [orsr, rpo] = await Promise.all([queryOrsr(companyName), queryRpo(companyName)]);
  return {
    domain,
    company_name: companyName,
    orsr,
    rpo,
    known_ownership_flag: KNOWN_OWNERSHIP_FLAGS[domain.toLowerCase()] ?? null,
  };
}

async function toolAssessOwnershipFlag(args) {
  const { domain } = args;
  if (!domain) throw new Error('domain is required');
  const d = domain.toLowerCase();

  // Use known flag if available
  if (d in KNOWN_OWNERSHIP_FLAGS) {
    return {
      domain,
      ownership_flag: KNOWN_OWNERSHIP_FLAGS[d],
      source: 'curated_knowledge_base',
      confidence: 'high',
      note: 'Known Slovak media outlet — flag from curated registry',
      usage: 'Use as ownership_flag in credibility_score = weighted_avg(accuracy_history=0.5, bias_score=0.3, ownership_flag=0.2)',
    };
  }

  // Live lookup fallback
  const ownershipData = await toolGetMediaOwnership({ domain });
  const orsrFound = ownershipData.orsr?.found;
  const rpoFound = ownershipData.rpo?.found;

  // Heuristic: if registered in ORSR + RPO → more transparent → lower flag
  let flag = 0.5; // Unknown default
  if (orsrFound && rpoFound) flag = 0.3;
  else if (orsrFound) flag = 0.4;
  else flag = 0.7; // Not found → opaque → higher flag

  return {
    domain,
    ownership_flag: flag,
    source: 'live_registry_lookup',
    confidence: 'medium',
    orsr_found: orsrFound,
    rpo_found: rpoFound,
    note: flag > 0.6 ? 'Opaque ownership — treat with caution' : 'Partial transparency detected',
    usage: 'Use as ownership_flag in credibility_score = weighted_avg(accuracy_history=0.5, bias_score=0.3, ownership_flag=0.2)',
  };
}

// ─── MCP Server setup ────────────────────────────────────────────────────────
const server = new Server(
  { name: 'slovak-registry-mcp', version: '1.0.0' },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'lookup_company',
      description: 'Look up a Slovak company in ORSR (company register) and RPO (beneficial ownership register). Returns ownership structure and statutory representatives.',
      inputSchema: {
        type: 'object',
        properties: {
          company_name: { type: 'string', description: 'Slovak company name (e.g. "N Press s.r.o.")' },
        },
        required: ['company_name'],
      },
    },
    {
      name: 'get_media_ownership',
      description: 'Get ownership information for a Slovak news domain. Maps domain to company name and queries both ORSR and RPO registers.',
      inputSchema: {
        type: 'object',
        properties: {
          domain: { type: 'string', description: 'News outlet domain (e.g. "hlavnespravy.sk", "dennikn.sk")' },
        },
        required: ['domain'],
      },
    },
    {
      name: 'assess_ownership_flag',
      description: 'Returns a 0.0–1.0 ownership_flag for use in source credibility scoring. 0.0 = fully transparent/public, 1.0 = fully opaque/adversarial. Used in: credibility_score = weighted_avg(accuracy_history=0.5, bias_score=0.3, ownership_flag=0.2)',
      inputSchema: {
        type: 'object',
        properties: {
          domain: { type: 'string', description: 'News outlet domain (e.g. "hlavnespravy.sk")' },
        },
        required: ['domain'],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  try {
    let result;
    if (name === 'lookup_company') result = await toolLookupCompany(args);
    else if (name === 'get_media_ownership') result = await toolGetMediaOwnership(args);
    else if (name === 'assess_ownership_flag') result = await toolAssessOwnershipFlag(args);
    else throw new Error(`Unknown tool: ${name}`);

    return {
      content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
    };
  } catch (e) {
    return {
      content: [{ type: 'text', text: JSON.stringify({ error: e.message, tool: name }) }],
      isError: true,
    };
  }
});

// Start
const transport = new StdioServerTransport();
await server.connect(transport);
console.error('Slovak Registry MCP server v1.0 ready (orsr.sk + rpvs.gov.sk)');
