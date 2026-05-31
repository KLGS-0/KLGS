import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from sklearn.preprocessing import StandardScaler
warnings.filterwarnings('ignore')

class ClassName(object):
       
    def __init__(self):
        self.df = pd.read_csv('tourist_agency_ratio.csv')
        self.features = self.df[['non_weekend_ratio', 'out_province_ratio', 'elderly_ratio']]
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False  
    def get_k_means_clusters(self):
        """
        获取KMeans聚类结果
        """
        scaler = StandardScaler()
        self.features = scaler.fit_transform(self.features)
        kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
        self.df['cluster'] = kmeans.fit_predict(self.features)
        # 查看聚类结果
        print(self.df[['tourist_agency_name', 'cluster']])
        # 查看聚类中心（反标准化）
        centers = scaler.inverse_transform(kmeans.cluster_centers_)
        print(pd.DataFrame(centers, columns=['non_weekend_ratio', 'out_province_ratio', 'elderly_ratio']))
        # 保存结果
        self.df.to_csv('tourist_agency_ratio_cluster.csv', index=False)
        # 将聚类中心转化为DataFrame
        centers_df = pd.DataFrame(centers, columns=['non_weekend_ratio', 'out_province_ratio', 'elderly_ratio'])
        centers_df['cluster'] = [f'Cluster {i}' for i in range(centers.shape[0])]
        # 将宽边转换为长边（适合seaborn）
        centers_long = centers_df.melt(id_vars=['cluster'], var_name='feature', value_name='value')
        # 绘制分组柱状图
        colos = ['#FFD700', '#FFA500', '#FF8C00', '#FF69B4', '#FF4500', '#FF0000']  # 颜色列表
        plt.figure(figsize=(12, 8))
        sns.barplot(x='feature', y='value', hue='cluster', data=centers_long, palette=colos)
        plt.title('聚类中心')
        plt.xlabel('特征')
        plt.ylabel('值')
        plt.legend(title='簇', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.0)
        # 添加数值标签
        for p in plt.gca().patches:
            height = p.get_height()
            plt.gca().text(p.get_x() + p.get_width() / 2, height + 0.02, f'{height:.2f}', ha='center'
            )
        plt.tight_layout()
        plt.show()
    
    
if __name__ == '__main__':
    cu = ClassName()
    cu.get_k_means_clusters()