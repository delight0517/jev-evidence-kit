# Jev Evidence Kit 0.1.0

Small offline tool for checking a paired task result before you claim token savings.

## What it does

- Compares a ChatGPT baseline and a Jev result against your expected answer.
- Credits avoided ChatGPT tokens only when both answers match the expected answer exactly.
- Keeps local/model token counts separate from ChatGPT token counts.
- Prints a compact JSON report. It makes no network requests and stores no data.

This is an evidence checker and worksheet, **not** an Aside installer or automatic Jev router. It does not intercept ChatGPT, call TypeSafe, connect to Aside, or verify provider usage for you. Enter token counts from the provider's usage records. Incorrect or incomplete inputs produce incorrect evidence.

## Requirements

- macOS 12 or later
- Python 3.10 or later; no third-party Python packages
- No Aside installation, Jev account, or API key required

Aside/TypeSafe integration and buyer-machine compatibility have not been validated. This package does not install or modify system settings.

## Try the sample

Open Terminal in the extracted folder and run:

```sh
python3 jev_measure.py examples/passing_pair.json
```

The sample is synthetic; its numbers are not a product benchmark. The exit code is `0` for valid input and `2` for invalid input.

## Measure your own task

1. Copy `examples/pair_template.json` and fill in one task's expected answer, both outputs, and token counts from provider usage records.
2. Use exact answer text. The checker ignores leading/trailing whitespace and normalizes CRLF to LF; it does not judge semantic equivalence.
3. Enter zero ChatGPT usage for the Jev arm only when provider records confirm it made no ChatGPT calls.
4. Run `python3 jev_measure.py path/to/your_pair.json` and retain the input and report together. Review before sharing; do not publish private prompts or outputs without permission.

A failed answer gets zero avoided-token credit even if it uses fewer tokens. The checker does not validate provider billing or general task quality.

## Self-check

```sh
python3 jev_measure.py --self-test
```

This checks the comparison and conservative-credit rules locally. It does not test TypeSafe, Aside, provider billing, or compatibility with a buyer's machine.

## License

MIT. See `LICENSE`.
