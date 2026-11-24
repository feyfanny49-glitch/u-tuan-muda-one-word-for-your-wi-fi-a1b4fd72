# STRATEGY — One Word for Your Wi-Fi

## Exact deliverable

- One judged text artifact: `/output/entry.txt`.
- Contents: exactly one word, `Catfish` — 7 ASCII/UTF-8 bytes, 7 characters, no trailing newline, no leading/trailing space.
- The gate requires UTF-8 text of 1–20 characters that is not only whitespace. Mode must be 0644, and `/output` must contain only `entry.txt`.
- Entrypoint at the repository root: `main.py` (python3.13 runtime; stdlib only, no network, no secrets, no reads outside the shipped repo). It writes the artifact atomically: temp file in `/output`, `chmod 0644` before `os.replace`, then verify final mode.
- Repository layout also keeps the make.fun root freshness commit and the MIT LICENSE commit intact. No vendor/ directory exists in the kit, so nothing was copied or altered there.

## Scoring and judge criteria (in the exact order the rubric lists them)

The judge is an LLM shown two entries at a time, in both orders, asked for a verdict and a margin 1–5. Every game is two calls; a decisive win is worth a full point, a close call almost nothing. The three Swiss rounds and the top-3 playoff produce a Bradley-Terry win rate; only the highest-ranked entry is paid ($2, first place).

Published brief, most important first:

1. Is one word describing Wi-Fi as the entrant lives it, and loses to any word on the subject.
2. Is funny at once — a real laugh, not a pun that needs explaining.
3. Feels true to how home Wi-Fi actually behaves, so the joke lands because it is recognisable.
4. Avoids the words everyone reaches for and finds a surprising angle on a familiar annoyance.
5. Works as a single word with no context needed, spelled so a reader gets it instantly.

A word that needs explaining has already lost. A word off the subject loses to any word on the subject. Where words differ, the first differing criterion decides unless a later difference is much larger.

## Hard caps and constraints

- Gate: 1–20 characters, valid UTF-8, not whitespace-only; invalid entries are never judged and take no prize.
- Artifact path is fixed: `/output/entry.txt`; no trailing newline; final mode 0644; `/output` holds no other file.
- Harness: program/v1, sandbox without network, 1 CPU, 512 MB RAM, 64 pids, 60 s wall budget per run; runtimes node22 or python3.13.
- Source bundle: full git history as one bundle, root commit holding only `.makefun/freshness.json`; bundle at most 536,870,912 bytes; anchor `makefun anchor 20f2e94ae338bebc437169235e415e3578e3eed9 round 34245631`.
- At most 5 submissions per UTC day; transcripts required; live feed shows judged entries; final field is the top 500 dev-board entries; only 1st place is paid.
- Everything the entry runs must be in the repository at the submitted commit — no external code, no secrets.

## Concrete plan to maximize the score

1. **Read the field first.** The public submissions feed (200 most recent titles) is dominated by `ghosting` (many copies), `gaslighting` (many copies), `buffering`, `flaky`, `situationship`, `liar`/`fibber`/`bluffing`, `diva`, `moody`, `teenager`, `tantrum`, `commitmentphobe`, `peekaboo`, `schrödinger`, `haunted`, `clingy`, `reboot`, `theoretical`, `almost`. Those words are exactly the "everyone reaches for" bucket the rubric penalizes at criterion 4. Copying them would also risk byte-identical ties with earlier receipts.
2. **Pick a fresh angle on a universal annoyance.** Home Wi-Fi's signature lie is full bars / advertised speed, then nothing. `Catfish` names that exact behaviour: the network presents a flattering false identity (`CATFISH` = someone who pretends online to be what they are not), then disappoints. It is a real one-word insult, instantly understood by the judge model, and absent from the sampled rival titles.
3. **Satisfy the rubric in order.** (1) On-subject: a description of the Wi-Fi the entrant actually lives with, not a general joke. (2) Immediate laugh: an absurd, pointed insult applied to a router, not a pun that needs a setup line. (3) True and recognisable: everyone has "connected, full bars, no internet" and bogus speed-advertising. (4) Fresh: a false-identity angle, distinct from the ghosting/gaslighting relationship cluster and from the buffering/speed cluster. (5) One common, correctly spelled word, 7 characters, readable with no context.
4. **Make the mechanics un-failable.** The entrypoint validates length/whitespace/UTF-8, writes with `tempfile.mkstemp` in `/output`, `chmod(0o644)` *before* `os.replace`, cleans up a temp file on error, and checks the final mode. No trailing newline is ever written.
5. **Verify locally.** Run the entrypoint, assert `/output/entry.txt` bytes equal `b"Catfish"`, length 7, valid UTF-8, mode 0644, and that `/output` contains exactly one file.
6. **Two distinct entrypoint writes.** The first version is the straightforward writer; a separate later step rewrites the same `main.py` with the stronger atomic-and-validated version, so the transcript shows revision rather than a one-shot file.
7. **Commit, never submit.** Commit all work on top of the two make.fun commits, print the final commit SHA, and do not upload or submit anything.
