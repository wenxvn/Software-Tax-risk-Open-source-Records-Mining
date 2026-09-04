from pathlib import Path

from taxrisk.integrity import build_manifest, sha256_file, verify_manifest


def test_hash_manifest(tmp_path: Path):
    raw = tmp_path / "raw"
    raw.mkdir()
    file = raw / "a.txt"
    file.write_text("immutable", encoding="utf-8")
    manifest = tmp_path / "manifest.csv"
    build_manifest(raw, manifest)
    assert len(sha256_file(file)) == 64
    assert verify_manifest(raw, manifest).iloc[0]["unchanged"]
    file.write_text("changed", encoding="utf-8")
    assert not verify_manifest(raw, manifest).iloc[0]["unchanged"]

