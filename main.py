from pathlib import Path
import hashlib
import json
# 当前脚本所在的文件夹
base_dir = Path(__file__).resolve().parent
# 拼接出测试文件夹的路径
test_dir = base_dir / "test_files"
def calculate_hash(file_path):
    # 读取文件内容
    with file_path.open('rb') as f:
        content = f.read()
    fingerprint = hashlib.sha256(content).hexdigest()
    # 计算指纹
    # 返回指纹
    return fingerprint
files_hashes ={}
for i in test_dir.iterdir():
    if (i.is_file()):
        # print(i.name)
        files_hashes[i.name]=calculate_hash(i)
            

snapshot_path = base_dir / "snapshot_backup.json"
            
if not snapshot_path.exists():
    with snapshot_path.open("w", encoding="utf-8") as f:
        json.dump(files_hashes, f, ensure_ascii=False, indent=4)
    print('首次运行，已建立快照')
else:
    has_change=False
    with snapshot_path.open('r',encoding='utf-8') as f:
        old_hashes=json.load(f)
    for name in files_hashes:
        if name not in old_hashes:
            print(f'新增文件:{name}')
            has_change = True
    for name in old_hashes:
        if name not in files_hashes:
            print(f'删除文件:{name}')
            has_change = True
    for name in files_hashes:
        if (name in old_hashes):
            if(files_hashes[name]!=old_hashes[name]):
                print(f'修改文件:{name}')
                has_change = True
    if not has_change:
        print('未发现变化')
    if has_change:
        answer = input('是否将当前状态保存为新快照？(y/n): ').strip().lower()
        if answer=='y':
            with snapshot_path.open('w',encoding='utf-8') as f:
                json.dump(files_hashes,f,ensure_ascii=False,indent=4)
            print('快照已更新')
        else:
            print('保留旧快照')