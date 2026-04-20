# Encrypted secrets

This directory holds `sops`-encrypted secret files — one per deployment env.
Layout:

```
secrets/
  dev.env.sops.yaml       # encrypted, commit this
  staging.env.sops.yaml   # encrypted, commit this
  prod.env.sops.yaml      # encrypted, commit this
```

Never commit plaintext `.env` files. The decrypted runtime output goes to
`/run/secrets/<env>.env` (tmpfs, mode 0600) and is read by docker-compose via
`env_file`.

## One-time bootstrap

Install sops + age (v3+):

```bash
# Debian/Ubuntu (or download binaries from GitHub releases)
sudo apt install age
curl -L https://github.com/getsops/sops/releases/latest/download/sops-v3.9.1.linux.amd64 \
    -o /usr/local/bin/sops && sudo chmod +x /usr/local/bin/sops
```

Generate keys:

```bash
mkdir -p ~/.config/sops/age
age-keygen -o ~/.config/sops/age/personal.txt
# Print the public key (age1...) and add it to .sops.yaml under the env(s)
# you want to be able to decrypt.
age-keygen -y ~/.config/sops/age/personal.txt
```

Bootstrap a secret file from `.env.example`:

```bash
cp .env.example /tmp/dev.env     # edit with real dev values
sops --encrypt --input-type dotenv --output-type yaml /tmp/dev.env \
    > secrets/dev.env.sops.yaml
shred -u /tmp/dev.env
```

## Daily usage

```bash
make secrets-edit ENV=dev          # edit encrypted in-place ($EDITOR)
make secrets-decrypt ENV=dev       # write /run/secrets/dev.env
make up ENV=dev                    # compose picks it up via env_file
```

Rotating recipients:

```bash
# After editing .sops.yaml (add/remove age keys)
sops updatekeys secrets/prod.env.sops.yaml
```

## VPS / CI

- **VPS**: `/etc/sops/age-key.txt` (0600, owned by the service user). Ansible
  role `app` provisions it from `ansible-vault`.
- **GitLab CI**: variable `SOPS_AGE_KEY` (masked, protected) containing the
  raw key material. Used by the deploy job to decrypt prod secrets before
  `scp`-ing them to the VPS.

Recovery keys stay offline (Bitwarden / paper). Rotate them quarterly.
