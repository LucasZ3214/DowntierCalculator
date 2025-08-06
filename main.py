import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

def ensure_output_dir(mode):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_dir = Path("output",mode)
    output_dir.mkdir(exist_ok=True)
    return output_dir

def read_json_from_file(file_path):
    """从文件读取JSON数据"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_ship_data(data):
    if "Ship Realistic" not in data:
        raise ValueError("数据中缺少'Ship Realistic'部分")
    return data["Ship Realistic"]

def extract_ground_data(data):
    if "Tank Realistic" not in data:
        raise ValueError("数据中缺少'Tank Realistic'部分")
    return data["Tank Realistic"]

def extract_air_data(data):
    if "Air Realistic" not in data:
        raise ValueError("数据中缺少'Air Realistic'部分")
    return data["Air Realistic"]

def prepare_table_data(data):
    """准备表格数据"""
    countries = sorted(data.keys())
    weights = sorted({float(br) for data in data.values() for br in data.keys()})

    table_data = []
    headers = ["Country"] + [str(br) for br in weights]

    for country in countries:
        country_name = country.split('_')[-1].title()  # 格式化国家名
        row = [country_name]
        for br in weights:
            row.append(data[country].get(str(br), {}).get("playCount", 0))
        table_data.append(row)

    return headers, table_data, weights


def save_to_csv(headers, table_data, filename,mode):
    output_dir = ensure_output_dir(mode)
    with open(os.path.join(output_dir,filename), 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(table_data)
    print(f"CSV文件已保存: {filename}")


def calculate_rates(br_data, current_br):
    """
    计算指定权重作为当前权重时的班长率和壮丁率
    """
    current_br = float(current_br)
    if str(current_br)[-1] == '0':
        bd_matches = br_data.get(current_br, 0)
        sd_matches = br_data.get(round(current_br + 0.3, 1), 0)
        su_matches = br_data.get(round(current_br + 0.7, 1), 0)
        bu_matches = br_data.get(round(current_br + 1.0, 1), 0)
    if str(current_br)[-1] == '3':
        bd_matches = br_data.get(current_br, 0)
        sd_matches = br_data.get(round(current_br + 0.4, 1), 0)
        su_matches = br_data.get(round(current_br + 0.7, 1), 0)
        bu_matches = br_data.get(round(current_br + 1.0, 1), 0)
    if str(current_br)[-1] == '7':
        bd_matches = br_data.get(current_br, 0)
        sd_matches = br_data.get(round(current_br + 0.3, 1), 0)
        su_matches = br_data.get(round(current_br + 0.6, 1), 0)
        bu_matches = br_data.get(round(current_br + 1.0, 1), 0)

    total_matches = bd_matches + sd_matches + su_matches + bu_matches

    if total_matches == 0:
        return 0.0, 0.0, 0.0, 0.0

    return (
        bd_matches / total_matches,
        sd_matches / total_matches,
        su_matches / total_matches,
        bu_matches / total_matches
    )


def process_data_to_dataframe(headers, table_data, weights):
    """处理数据到DataFrame"""
    df = pd.DataFrame(table_data, columns=headers)

    # 准备结果DataFrame
    results = []
    for _, row in df.iterrows():
        country = row['Country']
        br_data = {float(br): row[br] for br in row.index[1:]}

        for br in weights:

            big_rate, small_rate, uptier_rate, buptier_rate = calculate_rates(br_data, br)
            if str(br)[-1] == '0':
                total = (br_data.get(br, 0) +
                         br_data.get(round(br + 0.3, 1), 0) +
                         br_data.get(round(br + 0.7, 1), 0) +
                         br_data.get(round(br + 1.0, 1), 0))
            if str(br)[-1] == '3':
                total = (br_data.get(br, 0) +
                         br_data.get(round(br + 0.4, 1), 0) +
                         br_data.get(round(br + 0.7, 1), 0) +
                         br_data.get(round(br + 1.0, 1), 0))
            if str(br)[-1] == '7':
                total = (br_data.get(br, 0) +
                         br_data.get(round(br + 0.3, 1), 0) +
                         br_data.get(round(br + 0.6, 1), 0) +
                         br_data.get(round(br + 1.0, 1), 0))

            results.append({
                'Country': country,
                'BR': br,
                'Full Downtier': big_rate,
                'Downtier': small_rate,
                'Uptier': uptier_rate,
                'Full Uptier': buptier_rate,
                'Count': total
            })

    return pd.DataFrame(results)


def plot_heatmap(df,mode,rate_type='Full Downtier', title='Full Downtier Rates'):
    """绘制热力图"""
    plt.figure(figsize=(15, 8))

    # 创建透视表
    pivot_table = df.pivot(index='BR', columns='Country', values=rate_type)

    # 绘制热力图
    sns.heatmap(
        pivot_table,
        annot=True,
        fmt=".0%",
        cmap="YlGnBu",
        linewidths=.5,
        cbar_kws={'label': 'Rate'}
    )

    plt.title(title, fontsize=16)
    plt.ylabel('Battle Rating', fontsize=12)
    plt.xlabel('Country', fontsize=12)
    plt.yticks(rotation=0)
    plt.tight_layout()

    # 保存图像
    filename = f"{title.lower().replace(' ', '_')}_heatmap.png"
    plt.savefig(os.path.join(ensure_output_dir(mode),filename), dpi=300)
    print(f"热力图已保存: {filename}")

def get_downtier(mode):
    try:
        input_file = "data.txt"
        output_csv = mode+"playcount.csv"
        rates_csv = mode+"rates.csv"

        data = read_json_from_file(input_file)
        if mode == "NRB":
            pdata = extract_ship_data(data)
        elif mode == "GRB":
            pdata = extract_ground_data(data)
        elif mode == "ARB":
            pdata = extract_air_data(data)
        else:
            raise ValueError("无效的模式，请选择 'NRB', 'GRB' 或 'ARB'")
        headers, table_data, weights = prepare_table_data(pdata)
        save_to_csv(headers, table_data, output_csv,mode)

        df = process_data_to_dataframe(headers, table_data, weights)
        df.to_csv(os.path.join(ensure_output_dir(mode),rates_csv), index=False)
        print(f"班长率数据已保存: {rates_csv}")

        #df = df[df['Count'] > 100]  # 只保留对局数大于100的数据

        plot_heatmap(df,mode,'Full Downtier', mode+' Full Downtier Rates')
        plot_heatmap(df,mode,'Downtier', mode+' Downtier Rates')
        plot_heatmap(df,mode,'Uptier', mode+' Uptier Rates')
        plot_heatmap(df, mode, 'Full Uptier', mode+' Full Uptier Rates')

    except Exception as e:
        print(f"发生错误: {str(e)}")
        raise

def main():
    '''
    mode = input("请输入模式 (NRB, GRB, ARB): ").strip().upper()
    if mode not in ["NRB", "GRB", "ARB"]:
        print("无效的模式，请输入 'NRB', 'GRB' 或 'ARB'")
        return

    try:
        get_downtier(mode)
    except Exception as e:
        print(f"处理数据时发生错误: {str(e)}")
    '''
    for mode in ["NRB", "GRB", "ARB"]:
        ensure_output_dir(mode)
        get_downtier(mode)

if __name__ == "__main__":
    main()