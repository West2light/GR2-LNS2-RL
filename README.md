# Map Loader - Đọc và Hiển thị Bản đồ Octile

Module đọc và hiển thị file bản đồ định dạng octile (.map) với các chức năng đầy đủ.

## Cấu trúc Module

### `map_loader.py`

Module chính với các hàm tiện ích:

#### 1. `read_map_file(path)` → đọc .map -> grid
Đọc file .map và trả về grid 2D.

```python
from map_loader import read_map_file

grid = read_map_file("Map/w_woundedcoast_map1.map")
print(f"Kích thước: {len(grid[0])}x{len(grid)}")
```

#### 2. `visualize_map(grid)` → hiển thị bằng matplotlib
Hiển thị bản đồ bằng matplotlib (tốt cho phân tích và xuất ảnh).

```python
from map_loader import read_map_file, visualize_map

grid = read_map_file("Map/w_woundedcoast_map1.map")

# Hiển thị trực tiếp
visualize_map(grid)

# Hoặc lưu vào file
visualize_map(grid, save_path="output_map.png")
```

#### 3. `draw_map(grid)` → hiển thị bằng pygame
Hiển thị bản đồ bằng pygame (interactive, real-time).

```python
from map_loader import read_map_file, draw_map

grid = read_map_file("Map/w_woundedcoast_map1.map")

# Tự động scale để fit màn hình
draw_map(grid)

# Hoặc chỉ định cell_size cố định
draw_map(grid, cell_size=2)

# Hoặc tùy chỉnh kích thước cửa sổ tối đa
draw_map(grid, max_window_size=(1920, 1080))  # Full HD
draw_map(grid, max_window_size=(2560, 1440))  # 2K
```

#### 4. `get_walkable_cells(grid)` → list các ô có thể đi
Trả về danh sách tọa độ các ô có thể đi được.

```python
from map_loader import read_map_file, get_walkable_cells

grid = read_map_file("Map/w_woundedcoast_map1.map")
walkable = get_walkable_cells(grid)

print(f"Số ô có thể đi: {len(walkable)}")
print(f"Vài ô đầu: {walkable[:5]}")
```

## Tính năng Auto Scale

Module tự động tính toán kích thước ô (`cell_size`) để map vừa với màn hình:

- **Màn Full HD (1920x1080)**: `max_window_size=(1920, 1080)`
- **Màn 2K (2560x1440)**: `max_window_size=(2560, 1440)`
- **Tự động**: Mặc định sử dụng `(1600, 900)` - phù hợp với hầu hết màn hình

Scale được tính để giữ nguyên tỷ lệ khung hình của map, đảm bảo hiển thị đúng ở mọi độ phân giải.

## Định dạng File Map

File .map sử dụng định dạng octile:

```
type octile
height 578
width 642
map
@@@@@@@@...
.......T@@...
...
```

### Các loại ô:

- `@` - Obstacle (không đi được) - màu xám đậm
- `.` - Walkable (đi được) - màu trắng xám
- `T` - Tree (cây) - màu xanh lá
- `S` - Swamp (đầm lầy) - màu xanh tím
- `W` - Water (nước) - màu xanh nước biển

## Chạy Examples

### Chạy tất cả chức năng:
```bash
python src/map_loader.py
```

### Chọn ví dụ cụ thể:
```bash
python src/example_usage.py
```

### Test nhanh:
```bash
python src/test_map.py
```

## Dependencies

```bash
pip install pygame matplotlib numpy
```

## Module Bổ sung

- `map_reader.py` - Class MapReader để đọc map (OOP style)
- `map_viewer.py` - Class MapViewer để hiển thị map (OOP style)

## Ghi chú

- Map hiển thị với tỷ lệ cố định, không phụ thuộc vào độ phân giải màn hình
- Hỗ trợ cả UTF-8 trên Windows (tự động xử lý encoding)
- Nhấn ESC hoặc đóng cửa sổ để thoát pygame viewer

