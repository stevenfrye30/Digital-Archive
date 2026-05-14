# Permanence Audit

Run at: `2026-05-14T15:47:31Z`
Fixture: `01_library/library/permanence/test_fixtures/test_citations.json`
Result: **15/15 passed**

Each test exercises one operational permanence commitment. A failed test is the more useful kind of result: it names exactly where a constitutional promise has not yet survived contact with the resolver.

## Results

| Id  | URN | Expected | Actual | Pass |
|-----|-----|----------|--------|------|
| T01 | `archive:text:jataka` | `resolved` | `resolved` | OK |
| T02 | `archive:tale:jataka::1` | `resolved` | `resolved` | OK |
| T03 | `archive:passage:jataka::chalmers-vol1::1.1` | `resolved` | `resolved` | OK |
| T04 | `archive:passage:jataka::chalmers-vol1::1.1:phrase=Truth:nth=1` | `resolved` | `resolved` | OK |
| T05 | `archive:commentary:editorial-2026-05-14-apannaka-page-bracket` | `resolved` | `resolved` | OK |
| T06 | `archive:commentary:ai-2026-05-14-apannaka-hercules-crossroads-parallel` | `resolved` | `resolved` | OK |
| T07 | `archive:passage:jataka::chalmers-vol1::1.999` | `alias_redirected` | `alias_redirected` | OK |
| T08 | `archive:passage:jataka::chalmers-vol1::1.998` | `retired` | `retired` | OK |
| T09 | `archive:commentary:editorial-test-withdrawn` | `resolved` | `resolved` | OK |
| T10 | `archive:commentary:editorial-test-deprecated` | `resolved` | `resolved` | OK |
| T11 | `archive:commentary:editorial-test-frozen` | `resolved` | `resolved` | OK |
| T12 | `archive:commentary:editorial-test-orphaned` | `resolved` | `resolved` | OK |
| T13 | `archive:passage:jataka::chalmers-vol1::1.5000` | `missing` | `missing` | OK |
| T14 | `archive:commentary:does-not-exist-anywhere` | `missing` | `missing` | OK |
| T15 | `not-a-valid-urn-at-all` | `malformed` | `malformed` | OK |

## Citations

### T01 — `archive:text:jataka`

Bare text-level URN resolves to the registry entry for jataka.

- Expected status: `resolved`
- Actual status: `resolved`
- Pass: **yes**

### T02 — `archive:tale:jataka::1`

Tale-level URN resolves to the Apannaka-jataka virtual object (across translations).

- Expected status: `resolved`
- Actual status: `resolved`
- Pass: **yes**

### T03 — `archive:passage:jataka::chalmers-vol1::1.1`

Bare-canon passage URN resolves to the canonical passage 1.1 (the Apannaka opening) byte-equal to canonical.

- Expected status: `resolved`
- Actual status: `resolved`
- Pass: **yes**

### T04 — `archive:passage:jataka::chalmers-vol1::1.1:phrase=Truth:nth=1`

Passage URN with phrase sub-locator resolves to the passage with the sub-locator phrase confirmed present.

- Expected status: `resolved`
- Actual status: `resolved`
- Pass: **yes**

### T05 — `archive:commentary:editorial-2026-05-14-apannaka-page-bracket`

Real (non-test) editorial commentary record from the May 2026 commentary prototype resolves cleanly.

- Expected status: `resolved`
- Actual status: `resolved`
- Pass: **yes**

### T06 — `archive:commentary:ai-2026-05-14-apannaka-hercules-crossroads-parallel`

Real Layer-6 AI commentary record resolves with quarantine flag preserved.

- Expected status: `resolved`
- Actual status: `resolved`
- Pass: **yes**

### T07 — `archive:passage:jataka::chalmers-vol1::1.999`

Aliased passage URN redirects through the test alias table to the actual passage 1.62; the alias chain is preserved in the response.

- Expected status: `alias_redirected`
- Actual status: `alias_redirected`
- Pass: **yes**

### T08 — `archive:passage:jataka::chalmers-vol1::1.998`

Retired passage URN fails honestly with a 'retired' marker and the retirement reason.

- Expected status: `retired`
- Actual status: `retired`
- Pass: **yes**

### T09 — `archive:commentary:editorial-test-withdrawn`

Withdrawn commentary record resolves but surfaces its withdrawn lifecycle state; the body is preserved.

- Expected status: `resolved`
- Actual status: `resolved`
- Pass: **yes**

### T10 — `archive:commentary:editorial-test-deprecated`

Superseded commentary record resolves with the successor chain visible; both records remain readable.

- Expected status: `resolved`
- Actual status: `resolved`
- Pass: **yes**

### T11 — `archive:commentary:editorial-test-frozen`

Frozen-policy commentary record resolves and the frozen flag is surfaced; the resolver does not attempt to migrate.

- Expected status: `resolved`
- Actual status: `resolved`
- Pass: **yes**

### T12 — `archive:commentary:editorial-test-orphaned`

Orphaned commentary record resolves but surfaces the orphan condition (its anchor target does not exist).

- Expected status: `resolved`
- Actual status: `resolved`
- Pass: **yes**

### T13 — `archive:passage:jataka::chalmers-vol1::1.5000`

Broken anchor — no such passage and no alias — fails honestly with 'missing'.

- Expected status: `missing`
- Actual status: `missing`
- Pass: **yes**

### T14 — `archive:commentary:does-not-exist-anywhere`

Non-existent commentary URN fails honestly with 'missing'.

- Expected status: `missing`
- Actual status: `missing`
- Pass: **yes**

### T15 — `not-a-valid-urn-at-all`

Malformed URN string fails honestly with 'malformed'; no silent best-guess.

- Expected status: `malformed`
- Actual status: `malformed`
- Pass: **yes**

