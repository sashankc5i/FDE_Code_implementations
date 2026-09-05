from src.data import make_data, split_scale

def test_data():
    df = make_data(1000)
    assert df.shape == (1000, 9)
    assert df["churn"].isin([0,1]).all()

def test_split():
    x1,x2,x3,y1,y2,y3 = split_scale(make_data(1000))
    assert x1.shape[1] == 8
    assert len(x1)==len(y1) and len(x2)==len(y2) and len(x3)==len(y3)
