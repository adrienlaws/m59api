# m59api Release Process (Internal)

**DO NOT PUBLISH TO PYPI OR GITHUB RELEASES**

This is an internal checklist for releasing new versions of m59api. Only for maintainer use.

---

## Pre-Release Testing

### 1. Test locally in development mode
```bash
cd c:\m59api
pip install -e .
m59api --log-level debug
```

### 2. Test with config file
```bash
m59api --config ./m59api.example.json
```

### 3. Docker multi-server test
```bash
cd c:\m59-blakserv-docker

# Copy resource files if needed
# You need: kodbase.txt, rsc/, memmap/, rooms/

# Create .env file
cp .env.example .env
# Edit with real webhook URLs

# Build and run
docker build -t m59-webhooks .
docker-compose up -d

# Verify each server
docker logs -f m59-server-101
docker logs -f m59-server-102

# Check pipes
docker exec m59-server-101 ls -la /tmp/*webhook*
docker exec m59-server-102 ls -la /tmp/*webhook*

# Test webhook routing
docker exec m59-server-101 bash -c "echo '{\"message\":\"Test from 101\"}' > /tmp/101_m59apiwebhook1"
docker exec m59-server-102 bash -c "echo '{\"message\":\"Test from 102\"}' > /tmp/102_m59apiwebhook1"
```

---

## Publishing to PyPI

**ONLY AFTER SUCCESSFUL TESTING**

### 1. Clean old builds
```bash
cd c:\m59api
rm -rf dist/ build/ *.egg-info
```

### 2. Build distribution
```bash
python setup.py sdist bdist_wheel
```

### 3. Test with TestPyPI (optional)
```bash
pip install twine
twine upload --repository testpypi dist/*

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ m59api==X.Y.Z
```

### 4. Upload to PyPI
```bash
twine upload dist/*
```

### 5. Verify PyPI version
```bash
pip install --upgrade m59api
pip show m59api  # Check version number
```

---

## Post-Release Docker Test

Rebuild Docker to pull from PyPI:
```bash
cd c:\m59-blakserv-docker
docker build --no-cache -t m59-webhooks:X.Y.Z .

# Verify it pulled correct version
docker run -d --name m59-pypi-test m59-webhooks:X.Y.Z
docker exec m59-pypi-test pip show m59api
```

---

## Version Checklist

Before publishing:
- [ ] `setup.py` version updated
- [ ] Local testing complete
- [ ] Docker multi-server testing complete
- [ ] All tests passed
- [ ] No hardcoded credentials in code

After publishing:
- [ ] Docker rebuild with PyPI version successful
- [ ] Version number verified on PyPI
- [ ] Git tag created (optional): `git tag vX.Y.Z && git push origin vX.Y.Z`

---

## Config File Search Order (for reference)

1. `--config /path/to/config.json` (CLI argument)
2. `$M59API_CONFIG` environment variable
3. `./m59api.json` (current directory)
4. `~/.m59api.json` (home directory)
5. `/etc/m59api.json` (system config, Linux/macOS only)
6. Fallback: `DISCORD_WEBHOOK_URL` env var (backwards compatibility)

---

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step production setup instructions.
