#!/bin/bash
# Scope: Bootstrap pinned uv and Python locally before invoking AIkea setup.
set -euo pipefail
stage=bootstrap
trap 'code=$?; printf "BLOCKED stage=%s exit=%s; inspect the error above and retry this command after resolving it.\n" "$stage" "$code" >&2; exit "$code"' ERR
package=$(cd -- "$(dirname -- "$0")" && pwd)
runtime=${1:-"$package/.aikea-runtime"}
mkdir -p -- "$runtime"
runtime=$(cd -- "$runtime" && pwd)
case "$(uname -s)-$(uname -m)" in
  Darwin-arm64)
    target=aarch64-apple-darwin
    digest=162b328fc63e0075d4267688201de91356e1c1b81db50419fa4466cfe2dfdebc ;;
  Linux-x86_64)
    target=x86_64-unknown-linux-gnu
    digest=17fc118ba4d7e9303f84fcabdc0a593fc3480ba76eb6980668fdbbb96fe88562 ;;
  *) printf 'BLOCKED: this candidate requires macOS ARM64 or Linux x86_64.\n' >&2; exit 1 ;;
esac
mkdir -p "$runtime/tools"
archive="$runtime/tools/uv.tar.gz"
stage=download_uv
if [[ ! -f "$archive" ]]; then
  curl --fail --location --proto '=https' --tlsv1.2 --retry 2 \
    --connect-timeout 20 --max-time 300 \
    "https://github.com/astral-sh/uv/releases/download/0.7.3/uv-$target.tar.gz" \
    --output "$archive.part"
  mv "$archive.part" "$archive"
fi
stage=verify_uv
if command -v sha256sum >/dev/null; then
  actual=$(sha256sum "$archive")
else
  actual=$(shasum -a 256 "$archive")
fi
[[ "${actual%% *}" == "$digest" ]]
tar -xzf "$archive" -C "$runtime/tools" --strip-components=1
uv="$runtime/tools/uv"
stage=provision_python
export UV_PYTHON_INSTALL_DIR="$runtime/python"
export UV_CACHE_DIR="$runtime/cache"
export UV_NO_CONFIG=1
export UV_LINK_MODE=copy
unset PYTHONPATH PYTHONHOME VIRTUAL_ENV AIKEA_CADQUERY_PYTHON
if [[ ! -x "$runtime/cad/bin/python" ]]; then
  "$uv" --no-config venv --managed-python --python 3.10.16 "$runtime/cad"
fi
stage=setup
"$runtime/cad/bin/python" "$package/setup_aikea.py" --runtime-directory "$runtime" --uv "$uv"
