# 导入库
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.frequent_patterns import fpgrowth

# 读取数据
df = pd.read_excel('./association_rules/餐厅数据.xlsx')
print(df.head())

# 标准化
trsations = df['菜品'].str.split(',').to_list()

te = TransactionEncoder()
te_ary = te.fit(trsations).transform(trsations)
df_enecoded = pd.DataFrame(te_ary, columns=te.columns_)
print(df_enecoded)
# 使用apriori进行分析
frequent_itemsets = apriori(df_enecoded, min_support=0.1, use_colnames=True)

# 生成关联规则
rules = association_rules(frequent_itemsets, metric='lift', min_threshold=0.1)
rules = rules.sort_values(by=['lift'], ascending=False)

# 保存模型
frequent_itemsets.to_pickle('./association_rules/frequent_itemsets.pkl')
rules.to_pickle('./association_rules/rules.pkl')


print("\n" + "="*30)
print("正在运行 FP-Growth 算法...")

# 2. 使用 fpgrowth 进行分析
# 参数说明：
# df_enecoded: 之前已经处理好的独热编码数据
# min_support: 最小支持度，保持和上面 Apriori 一致 (0.1)
# use_colnames: 使用列名而不是整数索引
frequent_itemsets_fp = fpgrowth(df_enecoded, min_support=0.1, use_colnames=True)

# 3. 生成关联规则
# 同样使用 lift 作为指标，阈值 0.1
rules_fp = association_rules(frequent_itemsets_fp, metric='lift', min_threshold=0.1)
rules_fp = rules_fp.sort_values(by=['lift'], ascending=False)

# 4. 打印结果预览
print("FP-Growth 频繁项集:")
print(frequent_itemsets_fp.head())
print("\nFP-Growth 关联规则:")
print(rules_fp.head())

# 5. 保存 FP-Growth 的模型结果
# 为了防止覆盖 Apriori 的结果，文件名加上 '_fp' 后缀
frequent_itemsets_fp.to_pickle('./association_rules/frequent_itemsets_fp.pkl')
rules_fp.to_pickle('./association_rules/rules_fp.pkl')

print("\nFP-Growth 模型已保存至 ./association_rules/ 目录")
