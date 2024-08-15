# Choco

## 进度：
model:  
1. 实现 GB 统一接口。
2. 支持任意次 Expression （GB最高支持二次）
2. 不等式约束自动转等式约束（线性约束二元优化情况）
3. 可转换为 GB Model（to_gurobi_model），使用optimize_with_gurobi 可通过 GB 求解
4. 自动转换 Choco-Q 所需内部数据结构  

[测试见 testbed.ipynb](./testbed.ipynb)
