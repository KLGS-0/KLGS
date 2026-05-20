import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from joblib import dump
from sklearn.preprocessing import LabelEncoder

class Classification(object):
    def __init__(self):
        self.df = pd.read_csv(r'C:\Users\HP\Desktop\test\date_1.csv')

    def get_conditions(self):
        df = self.df
        df['max_ratio'] = df['max_close'] / df['the_close']
        df['min_ratio'] = df['min_close'] / df['the_close']

        high_return_threshold = df['max_ratio'].quantile(0.4)
        high_risk_threshold = df['min_ratio'].quantile(0.4)

        conditions = [
            (df['max_ratio'] >= high_return_threshold) & (df['min_ratio'] <= high_risk_threshold),
            (df['max_ratio'] >= high_return_threshold) & (df['min_ratio'] > high_risk_threshold),
            (df['max_ratio'] < high_return_threshold) & (df['min_ratio'] > high_risk_threshold),
            (df['max_ratio'] < high_return_threshold) & (df['min_ratio'] <= high_risk_threshold)
        ]
        labels = ['高收益高风险', '高收益低风险', '低收益低风险', '低收益高风险']
        df['label'] = np.select(conditions, labels, default='未知')

        features = df[['eps','total_revenue_ps','undist_profit_ps','gross_margin','fcff','fcfe','tangible_asset','bps','netprofit_margin','npta']]
        
        le = LabelEncoder()
        df['category_encoded'] = le.fit_transform(df['label'])

        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)

        # ✅ 保存 scaler 和 le，预测时必须用
        dump(scaler, 'scaler.joblib')
        dump(le, 'le.joblib')

        y = df['category_encoded']
        X_train, X_test, y_train, y_test = train_test_split(features_scaled, y, test_size=0.3, random_state=42)
        return X_train, X_test, y_train, y_test, le

    def knn_utils(self, X_train, X_test, y_train, y_test, le):
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        print("="*50)
        print("KNN 模型结果")
        print(classification_report(y_test, y_pred, target_names=le.classes_))
        dump(knn, 'knn_model.joblib')

    def svm_utils(self, X_train, X_test, y_train, y_test, le):
        svm = SVC(kernel='rbf', random_state=42)
        svm.fit(X_train, y_train)
        y_pred = svm.predict(X_test)
        print("="*50)
        print("SVM 模型结果")
        print(classification_report(y_test, y_pred, target_names=le.classes_))
        dump(svm, 'svm_model.joblib')

    def rf_utils(self, X_train, X_test, y_train, y_test, le):
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)
        print("="*50)
        print("随机森林 模型结果")
        print(classification_report(y_test, y_pred, target_names=le.classes_))
        dump(rf, 'rf_model.joblib')

if __name__ == '__main__':
    ci = Classification()
    X_train, X_test, y_train, y_test, le = ci.get_conditions()
    ci.knn_utils(X_train, X_test, y_train, y_test, le)
    ci.svm_utils(X_train, X_test, y_train, y_test, le)
    ci.rf_utils(X_train, X_test, y_train, y_test, le)