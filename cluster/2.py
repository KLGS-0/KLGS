# 导入库
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import matplotlib.pyplot as plt

class KMeansOptimization(object):
    """
    K-Means最优K值确定
    """
    def __init__(self):
        self.df = pd.read_csv('tourist_agency_ratio.csv')
        self.features = self.df[['non_weekend_ratio', 'out_province_ratio', 'elderly_ratio']]

        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

    def elbow_method(self):
        """
        肘部法则
        通过sse（误差平方和）拐点判断最佳K值
        """
        sse = []
        k_range = range(2, 10)
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(self.features)
            sse.append(kmeans.inertia_)

        plt.figure(figsize=(10, 5))
        plt.plot(k_range, sse, 'bo-', linewidth=2, markersize=8)
        plt.xlabel('K值')
        plt.ylabel('SSE')
        plt.title('肘部法则')
        plt.grid(True, linestyle='--', alpha=0.5)
        # 标注每个点的SSE值
        for i, sse_val in enumerate(sse):
            plt.annotate(f'{sse_val:.2f}', (i, sse_val), textcoords="offset points", xytext=(0, 10), fontsize=10, ha='center')
        plt.tight_layout()
        plt.savefig('elbow_method.png', dpi=300)
        plt.show()
        
    def silhouette_analysis(self):
        """
        轮廓系数分析
        评估聚类结果的轮廓系数，选择轮廓系数最高的K值
        """

        k_range = range(2, 10)
        silhouette_scores = []
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(self.features)
            silhouette_scores.append(silhouette_score(self.features, kmeans.labels_))
            print(f'K={k}, 轮廓系数: {silhouette_scores[-1]:.4f}')

        # 轮廓系数图
        plt.figure(figsize=(10, 5))
        plt.plot(k_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
        plt.xlabel('K值')
        plt.ylabel('轮廓系数')
        plt.title('轮廓系数分析')
        plt.xticks(list(k_range))
        plt.grid(True, linestyle='--', alpha=0.5)
        best_k_sil = list(k_range)[silhouette_scores.index(max(silhouette_scores))]
        plt.axvline(best_k_sil, color='red', linestyle='--', label=f'最佳K={best_k_sil}')
        plt.legend()

        plt.tight_layout()
        plt.savefig('silhouette_analysis.png', dpi=300)
        plt.show()
        print(f'最佳K值: {best_k_sil}')

if __name__ == '__main__':
    kmeans_opt = KMeansOptimization()
    kmeans_opt.elbow_method()
    kmeans_opt.silhouette_analysis()
