# Debugging Log — Azure Deployment & Meraki Integration (2026-09-22)

## Reference values

- Live app URL: `https://netopsgateway-g3gre6a2anaphpdk.westus3-01.azurewebsites.net`
- Resource group: `netopsgatewaycomphealth-rg`, App Service name: `netopsgateway`
- Working `ORG_ID`: `1795064` (Meraki org name: `Student`)
- Broken `ORG_ID` (do not use): `669910444571370036` (`DevNet-Jg8aSYcjHWSU` — 404s on every network/device call, likely an inaccessible placeholder org)
- Startup command: `gunicorn --bind=0.0.0.0 --timeout 600 --capture-output --enable-stdio-inheritance --log-level info application:app`
- Test network created for demo: "West Branch" (`N_3661426497052257047`), wireless type, no physical/virtual device claimed

## Issue 1 — App restart command produced no output

**Symptom:** `az webapp restart` returned nothing, looked like it failed.
**Cause:** Not a bug — that command is silent on success in Azure CLI.
**Fix:** Verified via `az webapp show --query state` instead.

## Issue 2 — Confirmed no API key ever leaks in responses/logs

Reviewed `application.py`: the Meraki key is read once via `os.environ.get`, used only server-side to construct the API client, and never appears in any route's JSON response. Flask `debug=True` only applies when running `python application.py` directly — never under gunicorn — so debug tracebacks can't leak it in production either.

## Issue 3 — All endpoints always returned hardcoded mock data (the big one)

**Symptom:** `/networks` and `/devices` always returned the same 3 hardcoded mock entries, never real Meraki data, even with `MERAKI_API_KEY`/`ORG_ID` set.

**Dead ends tried (each a real lesson):**
1. Enabled Azure App Service filesystem application logging — didn't surface the app's `print()` output at all.
2. Set `PYTHONUNBUFFERED=1` — still nothing in Log Stream.
3. Added gunicorn's `--capture-output --enable-stdio-inheritance` flags — still nothing for runtime request logs (only startup-sequence logs ever appeared reliably).

**What actually worked:** Added a temporary `/debug/meraki` endpoint that put the real Meraki API error/success info directly in the JSON response body — bypassing the unreliable logging pipeline entirely. Got the real error on the first try:
```
"organizations, getOrganizationNetworks - 404 Not Found, please wait a minute if the key or org was just newly created."
```

**Root cause, in two parts:**
1. `ORG_ID` was pointed at the wrong Meraki org (`DevNet-Jg8aSYcjHWSU`) — one the API key could *see* in an `/organizations` listing, but couldn't actually query resources from.
2. The correct org (`Student`, `1795064`) was itself empty — fixed by creating a network ("West Branch") via the Meraki dashboard UI. Claiming a physical/virtual device isn't required for a network to exist and be queryable.

**Cleanup:** Removed the `/debug/meraki` endpoint once diagnosed — Claude Code's own safety check flagged leaving a public, unauthenticated debug endpoint live as a real info-leak risk, which was the right call. Lesson for next time: gate any future debug endpoint behind a shared-secret query parameter before it's ever pushed live.

## Issue 4 — Health/compliance checks were silently broken even with real data

**Symptom:** `/networks/<id>/health` and `/alerts/scan` "worked" (200 OK) once real data started flowing, but always reported everything healthy with zero alerts — even though that wasn't being genuinely verified.

**Root cause:** `check_network_health()` and `check_device_compliance()` checked a `status` field on the network/device object that only ever existed in the *hardcoded mock data*. Real Meraki objects from `getOrganizationNetworks()`/`getOrganizationDevices()` don't carry live status at all — that requires a separate endpoint.

**Fix:** Added `fetch_device_statuses()` (calls `getOrganizationDevicesStatuses`), and rewrote both health/compliance checks to look up real device status by network ID / serial instead of a nonexistent field. Updated `tests/test_application.py` to match the new function signatures — all 14 tests pass.

## Key takeaway for the presentation

The deployment "working" (HTTP 200, app reachable) and the deployment being *correct* (returning real, meaningfully-checked data) turned out to be two very different bars. Both the ORG_ID mismatch and the mock-data-shaped logic bug would have been invisible in a demo that only checked "does the endpoint respond" — they only surfaced by checking the actual data against real Meraki state.
