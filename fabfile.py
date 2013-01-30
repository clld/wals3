from fabric.api import task, hosts
from fabric.contrib.console import confirm

from clld.deploy import config, util


APP = config.APPS['wals3']


@hosts('forkel@cldbstest.eva.mpg.de')
@task
def deploy_test():
    with_db = confirm('Recreate database?', default=False)
    util.deploy(APP, 'test', db=with_db)


@task
def deploy():
    util.deploy(APP, 'production')
