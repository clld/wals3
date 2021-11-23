# Releasing WALS Online

The data served by [WALS Online](https://wals.info) is curated in the GitHub
repository [cldf-datasets/wals](https://github.com/cldf-datasets/wals).
Thus, a release of WALS Online is always bound to a release of this repository.

To create the database With the cldf-datasets/wals repository located
in `./wals-data`, run

```shell script
clld initdb --cldf ./wals-data/cldf/StructureDataset-metadata.json development.ini
```

- run tests with `pytest .`

- deploy the app running `fab deploy:production` via `appconfig`.
