# Hướng dẫn sử dụng Map Loader

## Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

## Cấu trúc Project

```
Project/
├── Map/
│   ├── den312d_map3.map
│   ├── lak303d_map2.map
│   └── w_woundedcoast_map1.map
├── src/
│   ├── map_loader.py       # Module chính ⭐
│   ├── map_reader.py       # Class MapReader (OOP)
│   ├── map_viewer.py       # Class MapViewer (OOP)
│   ├── example_usage.py    # Ví dụ chi tiết
│   └── test_map.py         # Script test
├── demo.py                 # Demo nhanh ⭐
├── requirements.txt
└── README.md
```

## Chạy nhanh

### 1. Demo đơn giản nhất:
```bash
python demo.py
```

### 2. Chạy với đầy đủ chức năng:
```bash
python src/map_loader.py
```

### 3. Chạy menu ví dụ:
```bash
python src/example_usage.py
```

## Sử dụng trong Code

### Import các hàm cần thiết:
```python
from src.map_loader import (
    read_map_file,      # Đọc file .map
    visualize_map,      # Hiển thị bằng matplotlib
    draw_map,           # Hiển thị bằng pygame
    get_walkable_cells  # Lấy danh sách ô đi được
)
```

### Ví dụ 1: Đọc và hiển thị map
```python
# Đọc map
grid = read_map_file("Map/w_woundedcoast_map1.map")

# Hiển thị với pygame (tự động scale)
draw_map(grid)
```

### Ví dụ 2: Hiển thị cho màn hình cụ thể
```python
grid = read_map_file("Map/w_woundedcoast_map1.map")

# Cho màn Full HD (1920x1080)
draw_map(grid, max_window_size=(1920, 1080))

# Cho màn 2K (2560x1440)
draw_map(grid, max_window_size=(2560, 1440))

# Cho màn 4K (3840x2160)
draw_map(grid, max_window_size=(3840, 2160))
```

### Ví dụ 3: Cell size cố định
```python
grid = read_map_file("Map/w_woundedcoast_map1.map")

# Cell size = 2px (nhỏ, cho map lớn)
draw_map(grid, cell_size=2)

# Cell size = 4px (trung bình)
draw_map(grid, cell_size=4)

# Cell size = 8px (lớn, dễ nhìn)
draw_map(grid, cell_size=8)
```

### Ví dụ 4: Lấy các ô có thể đi
```python
grid = read_map_file("Map/w_woundedcoast_map1.map")

# Lấy tất cả ô có thể đi
walkable = get_walkable_cells(grid)

print(f"Có {len(walkable)} ô có thể đi")
print(f"Ô đầu tiên: {walkable[0]}")

# Sử dụng cho pathfinding
start = walkable[0]
goal = walkable[-1]
```

### Ví dụ 5: Xuất ảnh bằng matplotlib
```python
grid = read_map_file("Map/w_woundedcoast_map1.map")

# Lưu vào file
visualize_map(grid, save_path="output_map.png")

# Hoặc hiển thị trực tiếp
visualize_map(grid)
```

## Giải quyết vấn đề Scale

### Vấn đề:
Map hiển thị với kích thước khác nhau ở các độ phân giải màn hình khác nhau.

### Giải pháp:
Module tự động tính toán `cell_size` tối ưu:

1. **Auto Scale** (mặc định):
   ```python
   draw_map(grid)  # Tự động fit vào (1600, 900)
   ```

2. **Chỉ định độ phân giải**:
   ```python
   # Full HD
   draw_map(grid, max_window_size=(1920, 1080))
   
   # 2K
   draw_map(grid, max_window_size=(2560, 1440))
   ```

3. **Cell size cố định**:
   ```python
   draw_map(grid, cell_size=2)  # Luôn 2px/cell
   ```

### Công thức tính:
```python
cell_size = min(
    max_window_width // map_width,
    max_window_height // map_height
)
```

Điều này đảm bảo:
- Map luôn vừa với cửa sổ
- Tỷ lệ khung hình được giữ nguyên
- Không bị méo hay cắt xén

## Troubleshooting

### 1. Lỗi encoding trên Windows:
Đã được xử lý tự động trong code. Nếu vẫn gặp lỗi:
```python
import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
```

### 2. Map hiển thị không đúng:
Kiểm tra:
- File .map có đúng format không?
- Dòng thứ 4 phải là "map"
- Số dòng data = height trong header

### 3. Pygame không hiển thị:
```bash
pip install --upgrade pygame
```

### 4. Matplotlib không hoạt động:
```bash
pip install --upgrade matplotlib
```

## Performance

| Map Size | Cell Size | Window Size | FPS |
|----------|-----------|-------------|-----|
| 642x578  | 2px       | 1284x1156   | 60  |
| 642x578  | 4px       | 2568x2312   | 60  |
| 642x578  | Auto      | ~1600x900   | 60  |

Map được render một lần, không re-render mỗi frame → hiệu suất cao.

## Tính năng nâng cao

### 1. Custom màu sắc:
Chỉnh sửa `COLORS_PYGAME` trong `map_loader.py`:
```python
COLORS_PYGAME = {
    '@': (50, 50, 50),       # Obstacle
    'T': (34, 139, 34),      # Tree
    '.': (240, 240, 240),    # Walkable
    'S': (100, 100, 200),    # Swamp
    'W': (70, 130, 180),     # Water
}
```

### 2. Kiểm tra ô có thể đi:
```python
grid = read_map_file("Map/w_woundedcoast_map1.map")

def is_walkable(x, y):
    if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
        return grid[y][x] != '@'
    return False
```

### 3. Đọc nhiều map:
```python
maps = {}
for map_file in ["map1.map", "map2.map", "map3.map"]:
    maps[map_file] = read_map_file(f"Map/{map_file}")
```

## Next Steps

Module này có thể mở rộng cho:
- Pathfinding (A*, Dijkstra)
- Game development
- Map generation
- Terrain analysis
- AI training

Enjoy coding! 🚀

