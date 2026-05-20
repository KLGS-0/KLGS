import pandas as pd
import numpy as np
from joblib import load

class Classification(object):
    def __init__(self):
        # 加载所有必须的文件
        self.knn = load('knn_model.joblib')
        self.svm = load('svm_model.joblib')
        self.rf = load('rf_model.joblib')
        self.le = load('le.joblib')
        self.scaler = load('scaler.joblib')

    def get_predict_conditions(self, X):
        feature_order = [
            'eps', 'total_revenue_ps', 'undist_profit_ps', 'gross_margin',
            'fcff', 'fcfe', 'tangible_asset', 'bps',
            'netprofit_margin', 'npta'
        ]
        new_values = np.array([[X[col] for col in feature_order]])
        new_values_scaled = self.scaler.transform(new_values)

        # 预测
        y_pred = self.knn.predict(new_values_scaled)
        label = self.le.inverse_transform(y_pred)[0]
        return label

if __name__ == '__main__':
    ci = Classification()
    new_data = {
        "eps": -1.5132,
        "total_revenue_ps": 18.431,
        "undist_profit_ps": 6.3427,
        "gross_margin": 20894700000,
        "fcff": -25189400000,
        "fcfe": -23392500000,
        "tangible_asset": 17105900000,
        "bps": 19.6233,
        "netprofit_margin": -7.4573,
        "npta": -1.1459
    }

    result = ci.get_predict_conditions(new_data)
    print("预测分类结果：", result)