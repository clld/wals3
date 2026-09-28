# Releasing WALS Online

```shell
git clone https://github.com/clld/wals3
cd wals3
pip install -e .[test]
```

The data served by [WALS Online](https://wals.info) is curated in the GitHub
repository [cldf-datasets/wals](https://github.com/cldf-datasets/wals).
Thus, a release of WALS Online is always bound to a release of this repository.

- update the release info at `wals3/appconf.ini`
- recreate the web application's database running
  ```shell
  clld initdb development.ini --cldf ../wals/cldf/StructureDataset-metadata.json
  ```
- make sure tests pass.
  ```shell
  pytest
  ```
- commit and push.
- deploy the app.

- Store the tested requirements:
  ```shell
  pip freeze > requirements.txt
  ```

- Store a db dump:
  ```shell
  pg_dump -xO wals3 > wals3.sql
  ```

