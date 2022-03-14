# Releasing WALS Online

The data served by [WALS Online](https://wals.info) is curated in the GitHub
repository [cldf-datasets/wals](https://github.com/cldf-datasets/wals).
Thus, a release of WALS Online is always bound to a release of this repository.

The DOIs of different versions of the cldf dataset are hard-coded in
the html of the app.  So you have to update these manually when you
publish a new release of the data.  Check the output of `grep -Rin "doi" ./wals3/`
to find files that contain DOIs.

To create the database With the cldf-datasets/wals repository located
in `./wals-data`, run

```shell script
clld initdb --cldf ./wals-data/cldf/StructureDataset-metadata.json development.ini
```

- run tests with `pytest .`

- deploy the app running `fab deploy:production` via `appconfig`.
