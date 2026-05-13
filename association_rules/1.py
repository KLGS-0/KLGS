# 导入库
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import networkx as nx

# 读取数据
df = pd.read_excel('./association_rules/餐厅数据.xlsx')
print(df.head())
trsations = df['菜品'].str.split(',').to_list()
print(trsations)

# 标准化
te = TransactionEncoder()
te_ary = te.fit(trsations).transform(trsations)
df_enecoded = pd.DataFrame(te_ary, columns=te.columns_)
print(df_enecoded)

# 使用apriori进行分析
frequent_itemsets = apriori(df_enecoded, min_support=0.1, use_colnames=True)
frequent_itemsets.sort_values(by='support', ascending=False, inplace=True)

# 查看2项集
print(frequent_itemsets[frequent_itemsets['itemsets'].str.len() == 2])

# 生成关联规则
rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.1)

# 筛选有效规则
effective = rules[
    (rules['confidence'] > 0.1) & (rules['lift'] > 1)
].sort_values(by=['lift', 'confidence'], ascending=False)
print(effective[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# 可视化关联规则
# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 关联关系可视化
G = nx.DiGraph()
for _, row in effective.iterrows():
    G.add_edge(','.join(list(row['antecedents'])),
               ','.join(list(row['consequents'])),
               weight=row['lift'])
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True,
        edge_color=[G[u][v]['weight'] for u, v in G.edges()],
        width=2,
        edge_cmap=plt.cm.Blues
        )
plt.show()