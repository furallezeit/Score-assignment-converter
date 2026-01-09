import pandas as pd
import warnings
import os
import io
warnings.filterwarnings('ignore')

def load_tables(original_file, score_table_file):
    """
    加载上传的表格文件
    :param original_file: 原始分数表文件对象
    :param score_table_file: 赋分表文件对象
    :return: df_original, df_score
    """
    # 读取原始分数表
    try:
        if original_file.filename.endswith('.xlsx'):
            df_original = pd.read_excel(original_file, dtype=str).fillna('')
        else:
            df_original = pd.read_csv(original_file, dtype=str).fillna('')
    except Exception as e:
        raise ValueError(f"原始分数表读取失败：{str(e)}")
    
    # 读取赋分表
    try:
        if score_table_file.filename.endswith('.xlsx'):
            df_score = pd.read_excel(score_table_file, dtype=str)
        else:
            df_score = pd.read_csv(score_table_file, dtype=str)
    except Exception as e:
        raise ValueError(f"赋分表读取失败：{str(e)}")
    
    # 数据类型转换
    df_score.iloc[:, 0] = pd.to_numeric(df_score.iloc[:, 0], errors='coerce')
    for col in df_score.columns[1:]:
        df_score[col] = pd.to_numeric(df_score[col], errors='coerce')
    
    return df_original, df_score

def calculate_single_score(original_score, subject_score_df):
    """
    计算单个科目的赋分
    :param original_score: 原始分数（数值/空）
    :param subject_score_df: 该科目赋分规则表
    :return: 赋分值（空/数值）
    """
    if pd.isna(original_score) or original_score == '':
        return ''
    
    # 按最低原始分降序排序，匹配最高符合条件的赋分
    subject_score_df = subject_score_df.sort_values(by=subject_score_df.columns[1], ascending=False)
    for _, row in subject_score_df.iterrows():
        min_original = row[subject_score_df.columns[1]]
        assigned_score = row[subject_score_df.columns[0]]
        if pd.notna(min_original) and original_score >= min_original:
            return assigned_score
    return ''

def process_assignment(df_original, df_score, insert_position='after_subject'):
    """
    核心赋分处理逻辑
    :param df_original: 原始分数表DataFrame
    :param df_score: 赋分规则表DataFrame
    :param insert_position: 赋分列位置（after_subject:科目后 | end:表格末尾）
    :return: 处理后的DataFrame
    """
    # 提取科目列表
    subjects = [col.strip() for col in df_score.columns[1:] if col.strip() != '']
    original_cols = df_original.columns.tolist()
    df_result = df_original.copy()
    
    # 第一步：计算所有科目的赋分（临时列）
    total_assigned_dict = {}  # 存储每行总分
    for idx, row in df_result.iterrows():
        total_assigned = 0
        assigned_count = 0
        
        for subject in subjects:
            if subject not in original_cols:
                continue
            
            # 原始分转换
            original_score = row[subject]
            try:
                original_score = float(original_score)
            except (ValueError, TypeError):
                df_result.loc[idx, f'{subject}_赋分'] = ''
                continue
            
            # 筛选该科目赋分规则
            subject_score_df = df_score[['赋分值', subject]].dropna()
            if subject_score_df.empty:
                df_result.loc[idx, f'{subject}_赋分'] = ''
                continue
            
            # 计算赋分
            assigned_score = calculate_single_score(original_score, subject_score_df)
            df_result.loc[idx, f'{subject}_赋分'] = assigned_score
            
            # 累加总分
            if pd.notna(assigned_score) and assigned_score != '':
                total_assigned += float(assigned_score)
                assigned_count += 1
        
        total_assigned_dict[idx] = total_assigned if assigned_count > 0 else ''
    
    # 第二步：添加总分列
    df_result['赋分总分'] = df_result.index.map(total_assigned_dict)
    
    # 第三步：调整赋分列位置
    if insert_position == 'after_subject':
        # 赋分列插入到对应科目后
        new_col_order = []
        for col in original_cols:
            new_col_order.append(col)
            if col in subjects and f'{col}_赋分' in df_result.columns:
                new_col_order.append(f'{col}_赋分')
        new_col_order.append('赋分总分')
        df_result = df_result[new_col_order]
    else:
        # 赋分列全部放在表格末尾（原始列 + 所有赋分列 + 总分）
        assigned_cols = [f'{s}_赋分' for s in subjects if f'{s}_赋分' in df_result.columns]
        new_col_order = original_cols + assigned_cols + ['赋分总分']
        df_result = df_result[new_col_order]
    
    return df_result

def save_to_local(df_result, file_path):
    """
    兼容原有本地保存逻辑（可选保留）
    :param df_result: 处理后的DataFrame
    :param file_path: 保存的完整路径
    :return: 无
    """
    try:
        # 保存为Excel文件（覆盖已存在的文件）
        df_result.to_excel(file_path, index=False, engine='openpyxl')
        if os.path.exists(file_path):
            return True, file_path
        else:
            return False, "文件保存失败：路径不存在"
    except Exception as e:
        return False, f"文件保存失败：{str(e)}"

def save_to_bytes(df_result):
    """
    将结果保存到内存字节流（用于下载）
    :param df_result: 处理后的DataFrame
    :return: 字节流数据
    """
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_result.to_excel(writer, index=False)
        output.seek(0)  # 重置文件指针到开头
        return output.getvalue()
    except Exception as e:
        raise ValueError(f"文件生成失败：{str(e)}")
