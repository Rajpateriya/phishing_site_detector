import pickle
predict=['https://www.uitrgpv.ac.in/index.aspx']
loaded_model = pickle.load(open('model.pkl', 'rb'))
result=loaded_model.predict(predict)
print(result)