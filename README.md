# GDAL Wheels

Pre-built GDAL Python wheels for macOS (arm64 / x86_64), Windows (x86_64) and Linux (manylinux_2_28 x86_64).

## 下載

前往 [Releases](../../releases) 頁面下載對應平台和 Python 版本的 `.whl` 文件。

```bash
pip install gdal-3.9.3-cp311-cp311-manylinux_2_28_x86_64.whl
```

## 支持矩陣

| 平台 | 架構 | Python |
|------|------|--------|
| Linux (manylinux_2_28) | x86_64 | 3.9, 3.10, 3.11, 3.12 |
| macOS | arm64 (Apple Silicon) | 3.11, 3.12 |
| macOS | x86_64 (Intel) | 3.11, 3.12 |
| Windows | x86_64 | 3.9, 3.10, 3.11, 3.12 |

## 構建新版本

```bash
git tag v3.9.3
git push origin v3.9.3
```

GitHub Actions 將自動構建所有平台的 wheel 並發佈到 Releases。
