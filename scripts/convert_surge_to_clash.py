# 文件路径: scripts/convert_surge_to_clash.py
import os
import yaml

# 定义需要扫描的根目录，'.' 表示当前仓库根目录
ROOT_DIR = '.'

def parse_surge_line(line):
    line = line.strip()
    # ... (前面的去注释逻辑保持不变) ...
    if '//' in line:
        line = line.split('//')[0].strip()
        
    parts = line.split(',')
    if len(parts) < 2:
        return None
    
    rule_type = parts[0].strip().upper()
    value = parts[1].strip()
    
    # --- 修改重点开始 ---
    # 我们不再生成 '+.domain.com' 这种缩写
    # 而是生成完整的 Clash 规则格式
    
    if rule_type == 'DOMAIN-SUFFIX':
        return f"DOMAIN-SUFFIX,{value}"
        
    elif rule_type == 'DOMAIN':
        return f"DOMAIN,{value}"
        
    elif rule_type == 'DOMAIN-KEYWORD':
        # 这下 KEYWORD 就复活了！
        return f"DOMAIN-KEYWORD,{value}"
        
    elif rule_type in ['IP-CIDR', 'IP-CIDR6']:
        # 顺便把 no-resolve 带上（如果有的话）
        return f"{rule_type},{value},no-resolve"
        
    # --- 修改重点结束 ---
    
    return None

def convert_file(file_path):
    """读取 list 文件并生成 yaml 文件"""
    yaml_path = os.path.splitext(file_path)[0] + '.yaml'
    
    print(f"🔄 正在转换: {file_path}")
    
    payload = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            res = parse_surge_line(line)
            if res:
                payload.append(res)
    
    if not payload:
        print(f"⚠️  跳过（无有效规则）: {file_path}")
        return

    # 写入 YAML 文件
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write("payload:\n")
        for item in payload:
            f.write(f"  - {item}\n")
    
    print(f"✅ 已生成: {yaml_path}")

def main():
    # 遍历所有目录
    for root, dirs, files in os.walk(ROOT_DIR):
        # 排除 .git 和 .github 目录
        if '.git' in root or '.github' in root:
            continue
            
        for file in files:
            if file.endswith('.list'):
                full_path = os.path.join(root, file)
                convert_file(full_path)

if __name__ == "__main__":
    main()