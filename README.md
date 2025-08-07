# War Thunder 班长率可视化工具

从 Statshark.net 获取 War Thunder 匹配数据，计算并可视化各权重的班长率和壮丁率

## Python依赖
```bash
pip install pandas matplotlib seaborn
```

## 使用方法

### 班长、壮丁率图

从Statshark获取当月数据json（getGlobalUserStats）保存在目录中（data.txt）并运行主脚本

三种历史模式的csv计算结果与四张热力图将保存在 output/ 目录

<img src="output/ARB/arb_total_downtier_rates_heatmap.png " alt="热力图示例" width="600" title="七月空历大班长">

如需其他模式（街机、全真），请自行修改extract_xxx_data()函数

### 胜率加权图

从Statshark获取当月数据json（getVehicleInfo， GlobalUserStats）保存在目录中（VehicleInfo.json， GlobalUserStats.json）并运行weighted_heatmap脚本

三种历史模式的csv计算结果与热力图将保存在 cal_output/ 目录
<img src="cal_output/ARB/arb_weighted_heatmap.png " alt="热力图示例" width="600" title="七月空历">

如需其他模式（街机、全真），请自行修改函数

## 计算逻辑

班长、壮丁率图具体原理详见b站DaiSongSong大松松的图文

https://www.bilibili.com/opus/1084271069501587462

### 加权图逻辑

（大班长1+班长0.5+壮丁0.5+大壮丁-1）*（胜率-0.5）*10
