# -*- coding: utf-8 -*-
"""
Các ví dụ sử dụng map_loader
"""

import sys
import os

# Đảm bảo encoding UTF-8 cho console output trên Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from map_loader import read_map_file, visualize_map, draw_map, get_walkable_cells


def example_1_read_map(grid):
    """Ví dụ 1: Đọc file map"""
    print("=" * 60)
    print("VÍ DỤ 1: THÔNG TIN MAP")
    print("=" * 60)
    
    print(f"Đã đọc map: {len(grid[0])}x{len(grid)}")
    print(f"Vài ô đầu tiên:")
    for y in range(min(5, len(grid))):
        print(f"  Dòng {y}: {''.join(grid[y][:50])}...")
    print()


def example_2_get_walkable(grid):
    """Ví dụ 2: Lấy các ô có thể đi"""
    print("=" * 60)
    print("VÍ DỤ 2: LẤY CÁC Ô CÓ THỂ ĐI")
    print("=" * 60)
    
    walkable = get_walkable_cells(grid)
    print(f"Tổng số ô có thể đi: {len(walkable)}")
    print(f"10 ô đầu tiên: {walkable[:10]}")
    print()


def example_3_visualize_matplotlib(grid):
    """Ví dụ 3: Hiển thị map bằng matplotlib"""
    print("=" * 60)
    print("VÍ DỤ 3: HIỂN THỊ MAP BẰNG MATPLOTLIB")
    print("=" * 60)
    
    print("Đang hiển thị map bằng matplotlib...")
    print("(Đóng cửa sổ matplotlib để tiếp tục)")
    
    # Hiển thị map (không lưu)
    visualize_map(grid)
    
    # Hoặc lưu vào file
    # visualize_map(grid, save_path="../output_map.png")
    print()


def example_4_draw_pygame(grid):
    """Ví dụ 4: Hiển thị map bằng pygame"""
    print("=" * 60)
    print("VÍ DỤ 4: HIỂN THỊ MAP BẰNG PYGAME")
    print("=" * 60)
    
    print("Đang hiển thị map bằng pygame...")
    print("(Nhấn ESC hoặc đóng cửa sổ để thoát)")
    
    # Hiển thị với auto scale (phù hợp với màn hình)
    draw_map(grid)
    
    # Hoặc chỉ định cell_size cố định
    # draw_map(grid, cell_size=2)
    print()


def example_5_draw_custom_size(grid):
    """Ví dụ 5: Hiển thị map với kích thước cửa sổ tùy chỉnh"""
    print("=" * 60)
    print("VÍ DỤ 5: HIỂN THỊ MAP VỚI KÍCH THƯỚC TÙY CHỈNH")
    print("=" * 60)
    
    print("Đang hiển thị map với kích thước cửa sổ tùy chỉnh...")
    
    # Hiển thị với max window size cho màn Full HD
    draw_map(grid, max_window_size=(1920, 1080))
    
    # Hoặc cho màn 2K
    # draw_map(grid, max_window_size=(2560, 1440))
    print()


def main():
    """Menu chính"""
    # Nhập tên file map một lần ở đầu
    print("=" * 60)
    print("CHƯƠNG TRÌNH XEM BẢN ĐỒ")
    print("=" * 60)
    
    while True:
        map_name = input("\nNhập tên file map (ví dụ: w_woundedcoast_map1): ").strip()
        
        # Tự động thêm .map nếu người dùng không nhập
        if map_name and not map_name.endswith('.map'):
            map_name += '.map'
        
        if not map_name:
            print("Tên file không hợp lệ! Vui lòng thử lại.")
            continue
        
        map_path = os.path.join(os.path.dirname(__file__), "..", "Map", map_name)
        
        # Kiểm tra file có tồn tại không
        if not os.path.exists(map_path):
            print(f"Không tìm thấy file: {map_name}")
            retry = input("Thử lại? (y/n): ").strip().lower()
            if retry != 'y':
                print("Tạm biệt!")
                return
            continue
        
        # Đọc map
        print(f"\nĐang đọc map: {map_name}...")
        grid = read_map_file(map_path)
        print(f"Đã tải map: {len(grid[0])}x{len(grid)}")
        
        # Menu chức năng
        while True:
            print("\n" + "=" * 60)
            print(f"MAP ĐANG XEM: {map_name}")
            print("=" * 60)
            print("1. Xem thông tin map")
            print("2. Lấy các ô có thể đi")
            print("3. Hiển thị map bằng matplotlib")
            print("4. Hiển thị map bằng pygame (auto scale)")
            print("5. Hiển thị map với kích thước tùy chỉnh")
            print("0. Thoát (để chọn map khác hoặc kết thúc)")
            print("=" * 60)
            
            choice = input("Nhập lựa chọn (0-5): ").strip()
            
            if choice == '1':
                example_1_read_map(grid)
            elif choice == '2':
                example_2_get_walkable(grid)
            elif choice == '3':
                example_3_visualize_matplotlib(grid)
            elif choice == '4':
                example_4_draw_pygame(grid)
            elif choice == '5':
                example_5_draw_custom_size(grid)
            elif choice == '0':
                again = input("\nChọn map khác? (y/n): ").strip().lower()
                if again == 'y':
                    break  # Quay lại nhập tên map
                else:
                    print("Tạm biệt!")
                    return
            else:
                print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()

