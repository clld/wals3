# coding=utf-8
"""cc-by

Revision ID: 1df16a574334
Revises: 11c8290c0318
Create Date: 2014-10-23 13:09:13.473947

"""

# revision identifiers, used by Alembic.
revision = '1df16a574334'
down_revision = '11c8290c0318'

import datetime

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("""update dataset set jsondata = '{"license_name": "Creative Commons Attribution 4.0 International License", "license_icon": "cc-by.png"}'""")
    op.execute("update dataset set license = 'http://creativecommons.org/licenses/by/4.0/'")


def downgrade():
    op.execute("""update dataset set jsondata = '{"license_name": "Creative Commons Attribution-NonCommercial-NoDerivs 2.0 Germany", "license_icon": "http://wals.info/static/images/cc_by_nc_nd.png"}'""")
    op.execute("update dataset set license = 'http://creativecommons.org/licenses/by-nc-nd/2.0/de/deed.en'")

