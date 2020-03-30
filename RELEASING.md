# Releasing WALS Online

The data served by [WALS Online](https://wals.info) is curated in the GitHub
repository [cldf-datasets/wals](https://github.com/cldf-datasets/wals).
Thus, a release of WALS Online is always bound to a release of this repository.

So, assuming `cldf-datasets/wals` has been released on Zenodo, with DOI `<DOI>`
assigned to it, we

- recreate the web application's database running
  ```shell script
  wals-app initdb --doi <DOI> --repos ../../cldf/wals
  ```
- deploy the app running `fab deploy:production` via `appconfig`.
