# Login system examples and analysis

This workspace contains two example login implementations and an analysis script.

- `insecure_login.py` — intentionally insecure AI-style example with hardcoded credentials.
- `secure_login.py` — minimal secure implementation using PBKDF2-HMAC-SHA256 and a JSON store.
- `analyze_login.py` — static + dynamic checks that look for hardcoded credentials and insecure patterns; also runs a smoke test against `secure_login.py`.

How to run

1. Run the analyzer to see findings and run the secure smoke test:

```powershell
python analyze_login.py
```

2. Try the secure CLI:

```powershell
python secure_login.py
```

Notes

- The secure example uses only Python standard library; no external deps.
- The insecure example is intentionally bad — do not copy it to production.
