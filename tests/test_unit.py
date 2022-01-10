from clld.db.models.common import Language


def test_Matrix(env, tmp_path):
    from wals3.adapters import Matrix

    class TestMatrix(Matrix):
        def abspath(self, req):
            return tmp_path / 'test'

        def query(self, req):
            return Matrix.query(self, req).filter(Language.pk < 100)

    m = TestMatrix(Language, 'wals3', description="Feature values CSV")
    m.create(env['request'], verbose=False)
    assert tmp_path.joinpath('test').exists()

