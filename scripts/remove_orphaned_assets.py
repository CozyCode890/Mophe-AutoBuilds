import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone

# One-off request builds are not catalog apps, but the requester still needs
# time to download the APK, so they stay in the release for this many days
# after the build. Adding the "keep" label makes the app permanent by putting
# it into patch-config.json.
REQUEST_BUILD_GRACE_DAYS = 7


def parse_created(value):
    """Parse a GitHub release asset createdAt value into an aware datetime."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None


def main():
    try:
        with open('patch-config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)

        app_names = [item['app_name'] for item in config.get('patch_list', [])]
    except Exception as e:
        print(f"Error loading patch-config.json: {e}")
        sys.exit(1)

    print("Checking for orphaned assets on GitHub release 'latest'...")
    result = subprocess.run(
        ['gh', 'release', 'view', 'latest', '--json', 'assets',
         '--jq', '.assets[] | [.name, .createdAt] | @tsv'],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"Could not fetch release assets or release doesn't exist: {result.stderr}")
        sys.exit(0)

    cutoff = datetime.now(timezone.utc) - timedelta(days=REQUEST_BUILD_GRACE_DAYS)

    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        asset, _, created_raw = line.partition('\t')
        asset = asset.strip()

        if asset == 'manifest.json':
            continue

        # Check if asset belongs to an active app from our patch config
        # Asset names are typically formatted as {app_name}-{arch}-patch-v{version}.apk
        is_active = any(asset.startswith(f"{app_name}-") for app_name in app_names)

        if is_active:
            continue

        # Keep recent request builds around so the requester can download them.
        created_at = parse_created(created_raw.strip())
        if created_at is not None and created_at >= cutoff:
            print(f"Keeping recent request build: {asset}")
            continue

        print(f"Deleting orphaned asset: {asset}")
        delete_res = subprocess.run(
            ['gh', 'release', 'delete-asset', 'latest', asset, '-y'],
            capture_output=True, text=True
        )
        if delete_res.returncode == 0:
            print(f"[OK] Successfully deleted {asset}")
        else:
            print(f"[ERROR] Failed to delete {asset}: {delete_res.stderr}")

if __name__ == "__main__":
    main()
