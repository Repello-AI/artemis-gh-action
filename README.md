# Artemis Security Scanner GitHub Action

This GitHub Action allows you to run Repello Artemis security scans on your assets directly from your GitHub workflows.

## Usage

```yaml
name: Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  # Allow manual triggering
  workflow_dispatch:
    inputs:
      asset_id:
        description: 'Asset ID to scan (defaults to secret DEFAULT_ASSET_ID if not provided)'
        required: false
      scan_type:
        description: 'Type of scan'
        required: true
        default: 'quick_scan'
        type: choice
        options:
          - quick_scan
          - safety_scan
          - owasp
          - mitre
          - nist
          - whistleblower
          - fingerprint

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Run Artemis Security Scan
        uses: repello-ai/artemis-gh-action@v1
        with:
          asset_id: ${{ github.event.inputs.asset_id || secrets.DEFAULT_ASSET_ID }}
          scan_type: ${{ github.event.inputs.scan_type || 'quick_scan' }}
        env:
          ARTEMIS_CLIENT_ID: ${{ secrets.ARTEMIS_CLIENT_ID }}
          ARTEMIS_CLIENT_SECRET: ${{ secrets.ARTEMIS_CLIENT_SECRET }}
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `asset_id` | The ID of the asset to scan | No* | Uses `DEFAULT_ASSET_ID` secret |
| `scan_type` | Type of scan to run | Yes | `quick_scan` |

\* While the `asset_id` parameter is optional in the workflow, you must either provide it as an input or set up the `DEFAULT_ASSET_ID` secret.

### Supported Scan Types

- `quick_scan`: Basic scan for common issues
- `safety_scan`: Focused on safety concerns
- `owasp`: Scan based on OWASP guidelines
- `mitre`: Scan based on MITRE ATT&CK framework
- `nist`: Scan based on NIST standards
- `whistleblower`: Dedicated whistleblower vulnerability scan
- `fingerprint`: Digital fingerprinting scan

## Environment Variables and Secrets

The action requires the following to be set:

- `ARTEMIS_CLIENT_ID`: Your Repello Artemis client ID (repository secret)
- `ARTEMIS_CLIENT_SECRET`: Your Repello Artemis client secret (repository secret)
- `DEFAULT_ASSET_ID`: Default asset ID to use when none is specified (repository secret)

## Output

The action will output the scan results to the GitHub Actions console, including the scan ID that can be used to retrieve results later from the Artemis platform.

## Development

To contribute to this action:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Make your changes to `main.py`
4. Test locally by running: `python main.py <asset_id> <scan_type>`
5. Test in GitHub Actions by using the workflow_dispatch trigger

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
