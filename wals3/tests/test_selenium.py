import time

def test_ui(selenium):
    dt = selenium.get_datatable('/feature')
    dt.sort('Name')
    time.sleep(2)

