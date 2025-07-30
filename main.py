import json
import os
from multiprocessing import Pool
from pathlib import Path
from typing import Dict, List, Any

from Learn_Cbit_v2 import Learn_Cbit


def learn_cbit_task(user_info: Dict[str, str]) -> None:
    lc = Learn_Cbit(phone=user_info['phone'], name=user_info['name'],
                    password=user_info['passwd'], lessonLibrary_id=user_info['tcid'])
    lc.learn()


def __main() -> None:
    # Use relative path from project root
    file_path = Path('token.json')
    
    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        users: List[Dict[str, str]] = json.load(file)
    
    if not users:
        print("No users found in configuration file")
        return
    
    # Use optimal process count (limited to available CPU cores)
    process_count = min(len(users), os.cpu_count() or 1)
    
    with Pool(processes=process_count) as pool:
        pool.map(learn_cbit_task, users)




if __name__ == "__main__":
    raise SystemExit(__main())
