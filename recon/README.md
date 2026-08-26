# Tournament recon

Evidence pulled from the public tournament page, the auditing API, Loki and Hugging Face by
`/project-badut:recon`. Committed because it is cross-tournament intel that gets referenced weeks later:
a task id, a competitor's rank, a failure signature. Loki rolls off at about 30 days, so a log not
captured here is gone.

**No credentials.** The recon script strips the auditing API's signed `training_data` / `test_data`
links and never prints the presigned `diff_report` URL; only `dataset_url_expires_at` survives, which is
a timestamp. Verified before this was committed. If you add files here by hand, check the same thing —
whoever holds one of those links can read the data.

## What is here

`tourn_e758aac2d861c378_20260824/` — the tournament our hotkey `5D2Qee4V…` lost round 1 of, and the
whole basis for commits `a50b7f6` and `ae8423d`. The three `loki_*_full.json` files are the primary
evidence: they carry the `ImportError` that made tokenisation write nothing, the five `[FAST-CRASH]`
attempts at ~6 seconds each, and the `[noise]` fallback line that explains why every one of our scored
losses came back at the validator's own `init_loss`.

`tourn_03a3ba3f5bb25c4a_20260817/` — the previous tournament, audited first by mistake and kept because
it carries an independent instance of the same shape: three miners eliminated by one base model that
would not load, including the winners of both other round-1 tasks.

## Reading it

`--full` matters. A plain `loki` call returns `lines_truncated_for_display` with 200 of 2042 lines and
stops inside the Docker build, which reads exactly like a run that never started training.
