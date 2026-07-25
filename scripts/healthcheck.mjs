#!/usr/bin/env node
/**
 * Health Check — verifica MCP, LSP, agents, skills no start da sessão
 * Previne travamento em espera silenciosa por componentes offline.
 *
 * Uso:
 *   node /mnt/dados/opencode/scripts/healthcheck.mjs
 *
 * Retorna exit code 0 se tudo OK, 1 se algum componente crítico offline.
 */

const CHECKS = {
  mcp: { label: 'MCP Servers', status: 'unknown', critical: false },
  lsp: { label: 'LSP Servers', status: 'unknown', critical: false },
  agents: { label: 'Key Subagents', status: 'unknown', critical: false },
  skills: { label: 'Skills Root', status: 'unknown', critical: false },
};

async function run() {
  console.log(`[HealthCheck] === System Health Check ===`);
  console.log(`[HealthCheck] Time: ${new Date().toISOString()}\n`);

  // 1. MCP — check resource templates (cheap probe)
  try {
    const mcpResources = await list_mcp_resources().catch(() => null);
    const mcpTemplates = await list_mcp_resource_templates().catch(() => null);
    const mcpCount = (mcpResources?.length || 0) + (mcpTemplates?.length || 0);
    CHECKS.mcp.status = mcpCount > 0 ? '✅ active' : '⚠️  no resources';
    console.log(`[HealthCheck] MCP: ${CHECKS.mcp.status} (${mcpCount} resources/templates)`);
  } catch (e) {
    CHECKS.mcp.status = '❌ error';
    console.log(`[HealthCheck] MCP: ${CHECKS.mcp.status} — ${e.message}`);
  }

  // 2. LSP — check configured servers
  try {
    const lspInfo = await lsp_status().catch(() => null);
    if (lspInfo && lspInfo.servers && lspInfo.servers.length > 0) {
      CHECKS.lsp.status = `✅ ${lspInfo.servers.length} server(s)`;
      for (const srv of lspInfo.servers) {
        console.log(`[HealthCheck]   LSP: ${srv.name || srv.id} — ${srv.state || 'active'}`);
      }
    } else if (lspInfo && lspInfo.servers && lspInfo.servers.length === 0) {
      CHECKS.lsp.status = '⚠️  no LSP servers configured';
      console.log(`[HealthCheck] LSP: ${CHECKS.lsp.status}`);
    } else {
      // lsp_status returned but no servers field
      CHECKS.lsp.status = '⚠️  LSP check inconclusive';
      console.log(`[HealthCheck] LSP: ${CHECKS.lsp.status}`);
    }
  } catch (e) {
    CHECKS.lsp.status = '⚠️  unavailable';
    console.log(`[HealthCheck] LSP: ${CHECKS.lsp.status} — ${e.message}`);
  }

  // 3. Agents — check available task subagent types
  try {
    // Probe: try to get agent list from the runtime
    const agentProbe = await task({
      subagent_type: 'explore',
      run_in_background: true,
      description: 'Health check probe',
      prompt: 'PROBE — list available tools. Return "OK" if this agent is reachable.',
    }).catch(() => null);

    if (agentProbe && agentProbe.task_id) {
      CHECKS.agents.status = '✅ reachable';
      console.log(`[HealthCheck] Agent: ${CHECKS.agents.status}`);
    } else {
      CHECKS.agents.status = '⚠️  probe returned no ID';
      console.log(`[HealthCheck] Agent: ${CHECKS.agents.status}`);
    }
  } catch (e) {
    CHECKS.agents.status = '⚠️  check skipped';
    console.log(`[HealthCheck] Agent: ${CHECKS.agents.status} — ${e.message}`);
  }

  // 4. Skills — check skills directory exists
  try {
    const fs = require('fs');
    const path = require('path');
    const skillDirs = [
      path.join(process.env.HOME || '/home/johncoffee', '.opencode', 'skills'),
      path.join(process.env.HOME || '/home/johncoffee', '.config', 'opencode', 'skills'),
    ];
    let found = 0;
    for (const d of skillDirs) {
      if (fs.existsSync(d)) {
        const items = fs.readdirSync(d).filter(x => !x.startsWith('.'));
        found += items.length;
        console.log(`[HealthCheck]   Skills @ ${d}: ${items.length} items`);
      }
    }
    CHECKS.skills.status = found > 0 ? `✅ ${found} skills found` : '⚠️  empty';
    console.log(`[HealthCheck] Skills: ${CHECKS.skills.status}`);
  } catch (e) {
    CHECKS.skills.status = '❌ error';
    console.log(`[HealthCheck] Skills: ${CHECKS.skills.status} — ${e.message}`);
  }

  // Summary
  console.log(`\n[HealthCheck] === Summary ===`);
  let allOk = true;
  for (const [key, check] of Object.entries(CHECKS)) {
    const icon = check.status.startsWith('✅') ? 'OK' : check.status.startsWith('⚠️') ? 'WARN' : 'FAIL';
    if (icon === 'FAIL' && check.critical) allOk = false;
    console.log(`[HealthCheck]   ${icon} ${check.label}: ${check.status}`);
  }

  // Warnings
  const warnings = [];
  if (CHECKS.mcp.status.includes('⚠️') || CHECKS.mcp.status.includes('❌')) {
    warnings.push('MCP: agents that depend on GhidraMCP (ex: reverser) WILL FAIL');
  }
  if (CHECKS.lsp.status.includes('⚠️')) {
    warnings.push('LSP: diagnostics and go-to-definition may be limited');
  }
  if (warnings.length > 0) {
    console.log(`\n[HealthCheck] ⚠️  Warnings:`);
    for (const w of warnings) console.log(`[HealthCheck]   - ${w}`);
  }

  console.log(`\n[HealthCheck] === Done ===`);
  process.exit(allOk ? 0 : 1);
}

run().catch(e => {
  console.error(`[HealthCheck] Fatal: ${e.message}`);
  process.exit(1);
});
