# Public timestamping and proof of existence

This repository includes an automated workflow that creates OpenTimestamps proofs for commits and releases. Below are recommended steps and background to create stronger, verifiable timestamps for your work.

## Why GitHub timestamps alone are not always sufficient
- Git commit metadata includes author and committer dates, which can be changed locally before pushing.
- GitHub release publish times are recorded by GitHub servers and are more trustworthy than local commit dates.
- For cryptographic, tamper-evident proof, combine signed commits/tags with an external timestamping system such as OpenTimestamps or a commercial TSA (RFC3161).

## Recommended practice
1. Create GPG-signed commits or tags
   - Configure GPG and git (example):
     - `git config user.signingkey <your-key-id>`
     - `git config commit.gpgsign true`
     - `git commit -S -m "Your signed commit message"`
   - For signed tags:
     - `git tag -s v1.0.0 -m "Release version 1.0.0"`

2. Use GitHub Releases for major milestones
   - Tag and sign a release version:
     - `git tag -s v1.0.0 -m "Release 1.0.0"`
     - `git push origin v1.0.0`
   - Create a GitHub Release from the tag with release notes.
   - The workflow will automatically stamp the release commit.

3. Manual OTS stamping (optional, for extra verification)
   - Export a commit SHA to a file:
     - `git rev-parse HEAD > sha.txt`
     - `ots stamp sha.txt`
     - Keep `sha.txt` and `sha.txt.ots` together as your proof.

4. Verifying an OTS proof
   - Install the OpenTimestamps client and run:
     - `ots verify sha.txt`
   - The proof will show that the SHA existed at or before the anchored blockchain time.

## Automation in this repo
- The workflow `.github/workflows/ots-stamp.yml` stamps the commit SHA on push and publishes the proof as an artifact named `ots-proof-<commit-sha>`.
- To download the proof:
  1. Go to the GitHub Actions tab
  2. Click on the workflow run for your commit
  3. Download the artifact from the artifacts section
  4. Extract and verify with `ots verify commit-sha.txt`

## More information
- OpenTimestamps documentation: https://opentimestamps.org
- GPG signing guide: https://docs.github.com/en/authentication/managing-commit-signature-verification
- RFC3161 timestamping: https://www.ietf.org/rfc/rfc3161.txt
