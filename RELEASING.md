# Releasing WALS Online

The data served by [WALS Online](https://wals.info) is curated in the GitHub
repository [cldf-datasets/wals](https://github.com/cldf-datasets/wals).
Thus, a release of WALS Online is always bound to a release of this repository.

- update the release info at `wals3/appconf.ini`
- recreate the web application's database running
  ```shell script
  clld initdb development.ini --cldf ../wals/cldf/StructureDataset-metadata.json
  ```
- make sure tests pass.
- commit and push.
- deploy the app running `fab deploy:production` via `appconfig`.
