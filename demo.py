# -*- coding: utf-8 -*-
"""
Demo nhanh để test map_loader
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Đảm bảo encoding UTF-8 cho console output trên Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from map_loader import read_map_file, draw_map, get_walkable_cells

def main():
    print("=" * 70)
    print("DEMO MAP LOADER")
    print("=" * 70)
    
    # Đọc map
    map_path = "Map/w_woundedcoast_map1.map"
    
    if not os.path.exists(map_path):
        print(f"ERROR: Không tìm thấy file {map_path}")
        return
    
    print(f"\n1. Đọc file map: {map_path}")
    grid = read_map_file(map_path)
    
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    
    print(f"   ✓ Kích thước: {width} x {height}")
    
    # Đếm các loại ô
    cell_counts = {}
    for row in grid:
        for cell in row:
            cell_counts[cell] = cell_counts.get(cell, 0) + 1
    
    print(f"\n2. Phân tích map:")
    for cell_type, count in sorted(cell_counts.items()):
        percentage = (count / (width * height)) * 100
        cell_names = {'@': 'Obstacle', 'T': 'Tree', '.': 'Walkable', 'S': 'Swamp', 'W': 'Water'}
        cell_name = cell_names.get(cell_type, 'Unknown')
        print(f"   '{cell_type}' ({cell_name:8s}): {count:7,} ô ({percentage:5.2f}%)")
    
    # Lấy walkable cells
    walkable = get_walkable_cells(grid)
    print(f"\n3. Số ô có thể đi: {len(walkable):,} ô")
    
    print(f"\n4. Hiển thị map với pygame...")
    print("   (Nhấn ESC hoặc đóng cửa sổ để thoát)")
    print("=" * 70)
    
    # Hiển thị map (auto scale)
    draw_map(grid)
    
    print("\n✓ Hoàn tất!")

if __name__ == "__main__":
    main()

