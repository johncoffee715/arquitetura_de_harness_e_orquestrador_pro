#!/usr/bin/env python3
"""TDD tests for harness/mcp/obsidian_server.py (P4 — Obsidian MCP)."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.mcp.obsidian_server import VaultServer, TOOLS


def _req(method, params=None, rid=1):
    return {"jsonrpc": "2.0", "id": rid, "method": method,
            "params": params or {}}


class VaultServerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self.tmp.name)
        self.server = VaultServer(self.vault)

    def tearDown(self):
        self.tmp.cleanup()

    def test_initialize(self):
        resp = self.server.handle(_req("initialize"))
        self.assertEqual(resp["result"]["serverInfo"]["name"], "obsidian")

    def test_tools_list_has_three_tools(self):
        resp = self.server.handle(_req("tools/list"))
        names = [t["name"] for t in resp["result"]["tools"]]
        self.assertEqual(names, ["list_notes", "read_note", "write_note"])

    def test_list_notes_empty_vault(self):
        resp = self.server.handle(_req("tools/call",
                                       {"name": "list_notes"}))
        text = resp["result"]["content"][0]["text"]
        self.assertEqual(json.loads(text), [])

    def test_write_then_read_note(self):
        w = self.server.handle(_req("tools/call", {"name": "write_note",
                                                   "arguments": {
                                                       "name": "decisao",
                                                       "content": "# Decisão"}}))
        self.assertIn("written", json.loads(w["result"]["content"][0]["text"]))
        r = self.server.handle(_req("tools/call", {"name": "read_note",
                                                   "arguments": {"name": "decisao"}}))
        self.assertEqual(json.loads(r["result"]["content"][0]["text"]),
                         "# Decisão")

    def test_read_missing_note_is_error(self):
        resp = self.server.handle(_req("tools/call", {"name": "read_note",
                                                      "arguments": {"name": "nope"}}))
        self.assertIn("error", resp)

    def test_path_traversal_blocked(self):
        resp = self.server.handle(_req("tools/call", {"name": "read_note",
                                                      "arguments": {"name": "../etc/passwd"}}))
        self.assertIn("error", resp)
        self.assertIn("traversal", resp["error"]["message"])

    def test_unknown_method_is_error(self):
        resp = self.server.handle(_req("bogus"))
        self.assertEqual(resp["error"]["code"], -32601)

    def test_missing_argument_is_error(self):
        resp = self.server.handle(_req("tools/call", {"name": "read_note",
                                                      "arguments": {}}))
        self.assertEqual(resp["error"]["code"], -32602)

    def test_unknown_tool_is_error(self):
        resp = self.server.handle(_req("tools/call", {"name": "nope"}))
        self.assertEqual(resp["error"]["code"], -32601)


if __name__ == "__main__":
    unittest.main()