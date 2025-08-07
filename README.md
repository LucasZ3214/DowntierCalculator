# War Thunder 班长率可视化工具

从 Statshark.net 获取 War Thunder 匹配数据，计算并可视化各权重的班长率和壮丁率

## Python依赖
```bash
pip install pandas matplotlib seaborn
```

## 使用方法

从Statshark获取当月数据json（getGlobalUserStats）保存在目录中（data.txt）并运行主脚本

三种历史模式的csv计算结果与四张热力图将保存在 output/ 目录

<img src="output/ARB/arb_total_downtier_rates_heatmap.png " alt="热力图示例" width="600" title="七月空历班长">

如需其他模式（街机、全真），请自行修改extract_xxx_data()函数


## 计算逻辑
具体原理详见b站DaiSongSong大松松的图文
https://www.bilibili.com/opus/1084271069501587462
