import joblib, os
files = ['Models/online_model.sav', 'Models/online_model.pkl', 'Models/unsw_online_model.sav']
for f in files:
    print(f, os.path.exists(f))
    if os.path.exists(f):
        try:
            m = joblib.load(f)
            print('loaded', type(m), hasattr(m, 'predict'), hasattr(m, 'predict_proba'))
        except Exception as e:
            print('error', type(e).__name__, e)
