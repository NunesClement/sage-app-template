# my-amazing-app-name

`my-amazing-app-name` is a Sage edge application that captures one image from a node's logical `left` camera, computes the channel-wise mean color, publishes the three results, and uploads the source snapshot. Release `0.2.0` follows the current Sage cookiecutter layout and is packaged for the Edge Code Repository (ECR).

## Science and data products

Mean image color is a small but useful example of edge image analysis. It demonstrates the complete Sage data path without requiring a large model: acquire sensor data on the node, calculate a compact result near the sensor, publish timestamped measurements, and optionally retain the source observation for validation.

Each run publishes these measurements using the camera timestamp:

- `color.mean.r`
- `color.mean.g`
- `color.mean.b`

It also uploads `snapshot.jpg`, producing an `upload` record. Uploading every image is useful for this tutorial but can consume substantial bandwidth in a continuously scheduled application. A production application should normally upload only when an event or sampling rule requires it.

## Repository layout

The Docker build context and all Sage packaging files intentionally live at the repository root:

```text
.
├── Dockerfile
├── main.py
├── requirements.txt
├── sage.yaml
├── ecr-meta/
│   ├── ecr-icon.jpg
│   ├── ecr-science-description.md
│   └── ecr-science-image.jpg
├── tests/
│   └── test_main.py
├── example.jpg
└── get-back.py
```

`requirements.txt` is the container dependency source. `pyproject.toml` and `uv.lock` provide a reproducible Python 3.12 environment for local tests and the data-query helper.

## Local checks

Create the local environment and run the hardware-independent unit test:

```bash
uv sync
uv run python -m unittest discover -s tests -v
```

The test verifies the mean-color calculation using an in-memory image. Running `main.py` additionally requires a camera understood by PyWaggle. To write local publish and upload output to disk, set `PYWAGGLE_LOG_DIR` before running the app:

```bash
export PYWAGGLE_LOG_DIR=test-run
uv run python main.py
```

The deployed configuration uses `Camera("left")`, as recommended for Sage nodes with multiple cameras. Change that logical camera name only when the target node exposes a different camera mapping.

## Build and test on a Sage development node

Clone this repository on an authorized development node, then build from the repository root:

```bash
sudo pluginctl build .
```

Run the image reference printed by the build command:

```bash
sudo pluginctl run --name my-amazing-app-name IMAGE_FROM_BUILD
```

For fast iterations, Sage also documents a combined build-and-run command:

```bash
sudo pluginctl run --name my-amazing-app-name $(sudo pluginctl build .)
```

A successful run exits cleanly after publishing three values and one upload record. This workstation does not need `pluginctl`; the authoritative hardware test must run on a Sage development node because camera mappings and the node services are provided there.

## Query recent results

After the app has run on Sage, query its recent color values and upload records with:

```bash
uv run python get-back.py
```

The helper queries the previous 30 minutes. You can also use the Sage Portal Data Query Browser and filter by the app/plugin name.

## Publish release 0.2.0 to ECR

Before registering the release, commit and push `sage.yaml`, the root-level Docker build files, and all three non-empty files in `ecr-meta/`. In the Sage Portal, sign in, open **My Apps**, choose **Create App**, provide this repository URL, and select **Register and Build App**. When the build succeeds, make the app public if it will be scheduled by other Sage users.

The release metadata declares both `linux/amd64` and `linux/arm64`, matching the current official Sage template. The Docker base and PyWaggle version are pinned so that ECR builds are reproducible.

## References

- [Creating an edge app](https://sagecontinuum.org/docs/tutorials/edge-apps/creating-an-edge-app)
- [Testing an edge app](https://sagecontinuum.org/docs/tutorials/edge-apps/testing-an-edge-app)
- [Publishing to ECR](https://sagecontinuum.org/docs/tutorials/edge-apps/publishing-to-ecr)
- [Developer quick reference](https://sagecontinuum.org/docs/reference-guides/dev-quick-reference)
