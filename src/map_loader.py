# -*- coding: utf-8 -*-
"""
Module đọc và hiển thị bản đồ với các hàm tiện ích
"""

import pygame
import matplotlib.pyplot as plt
import numpy as np

# Cấu hình màu sắc cho các loại ô
COLORS_PYGAME = {
    '@': (50, 50, 50),       # Obstacle - màu xám đậm
    'T': (34, 139, 34),      # Tree - màu xanh lá
    '.': (240, 240, 240),    # Walkable - màu trắng xám
    'S': (100, 100, 200),    # Swamp - màu xanh tím
    'W': (70, 130, 180),     # Water - màu xanh nước biển
}

COLORS_MATPLOTLIB = {
    '@': [50/255, 50/255, 50/255],
    'T': [34/255, 139/255, 34/255],
    '.': [240/255, 240/255, 240/255],
    'S': [100/255, 100/255, 200/255],
    'W': [70/255, 130/255, 180/255],
}

def read_map_file(filepath):
    """
    Đọc file map định dạng octile (.map)
    
    Args:
        filepath (str): Đường dẫn đến file .map
        
    Returns:
        list: Grid 2D chứa dữ liệu bản đồ
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if len(lines) < 4:
        raise ValueError(f"File map không hợp lệ: {filepath}")
    
    # Parse header
    map_type = lines[0].strip().split()[1] if len(lines[0].strip().split()) > 1 else "unknown"
    height = int(lines[1].strip().split()[1])
    width = int(lines[2].strip().split()[1])
    
    # Kiểm tra dòng "map"
    if not lines[3].strip().startswith("map"):
        raise ValueError("Định dạng map không đúng, dòng thứ 4 phải là 'map'")
    
    # Đọc grid data từ dòng thứ 5 (index 4)
    grid = []
    for i in range(4, min(4 + height, len(lines))):
        line = lines[i].rstrip('\n\r')
        row = list(line)
        
        # Đảm bảo mỗi dòng có đúng width ký tự
        if len(row) < width:
            row.extend(['@'] * (width - len(row)))
        elif len(row) > width:
            row = row[:width]
        
        grid.append(row)
    
    # Nếu thiếu dòng, thêm dòng '@' vào
    while len(grid) < height:
        grid.append(['@'] * width)
    
    return grid


def get_walkable_cells(grid):
    """
    Lấy danh sách tất cả các ô có thể đi được
    
    Args:
        grid (list): Grid 2D của bản đồ
        
    Returns:
        list: Danh sách các tuple (x, y) của các ô có thể đi
    """
    walkable = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != '@':  # '@' là obstacle
                walkable.append((x, y))
    return walkable


def visualize_map(grid, save_path=None):
    """
    Hiển thị bản đồ bằng matplotlib (để phân tích, xuất ảnh)
    
    Args:
        grid (list): Grid 2D của bản đồ
        save_path (str, optional): Đường dẫn để lưu ảnh, nếu None thì chỉ hiển thị
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    
    # Tạo mảng màu RGB
    img = np.zeros((height, width, 3))
    
    for y in range(height):
        for x in range(len(grid[y])):
            cell = grid[y][x]
            color = COLORS_MATPLOTLIB.get(cell, [1.0, 1.0, 1.0])
            img[y, x] = color
    
    # Tạo figure với kích thước phù hợp
    dpi = 100
    fig_width = width / dpi if width > height else 12
    fig_height = height / dpi if height > width else 12
    
    plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
    plt.imshow(img, interpolation='nearest')
    plt.axis('off')
    plt.title(f'Map Visualization ({width}x{height})')
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0, dpi=dpi)
        print(f"Đã lưu ảnh vào: {save_path}")
    else:
        plt.show()
    
    plt.close()


def _calculate_optimal_cell_size(map_width, map_height, max_window_width=1600, max_window_height=900):
    """
    Tính toán kích thước ô tối ưu để map vừa với màn hình
    
    Args:
        map_width (int): Chiều rộng map (số ô)
        map_height (int): Chiều cao map (số ô)
        max_window_width (int): Chiều rộng cửa sổ tối đa (px)
        max_window_height (int): Chiều cao cửa sổ tối đa (px)
        
    Returns:
        int: Kích thước ô tối ưu (px)
    """
    # Tính cell_size dựa trên tỷ lệ để fit vào cửa sổ
    cell_size_by_width = max_window_width // map_width
    cell_size_by_height = max_window_height // map_height
    
    # Chọn giá trị nhỏ hơn để đảm bảo vừa cả 2 chiều
    cell_size = min(cell_size_by_width, cell_size_by_height)
    
    # Đảm bảo cell_size ít nhất là 1
    cell_size = max(1, cell_size)
    
    return cell_size


def draw_map(grid, cell_size=None, max_window_size=(1600, 900)):
    """
    Hiển thị bản đồ bằng pygame (interactive)
    
    Args:
        grid (list): Grid 2D của bản đồ
        cell_size (int, optional): Kích thước mỗi ô (px). Nếu None, tự động tính toán
        max_window_size (tuple): Kích thước cửa sổ tối đa (width, height)
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    
    # Tự động tính cell_size nếu không được cung cấp
    if cell_size is None:
        cell_size = _calculate_optimal_cell_size(width, height, max_window_size[0], max_window_size[1])
        print(f"Cell size tự động: {cell_size}px")
    
    # Khởi tạo pygame
    pygame.init()
    window_width = width * cell_size
    window_height = height * cell_size
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(f"Map Viewer - {width}x{height} (cell={cell_size}px)")
    clock = pygame.time.Clock()
    
    # Vẽ map một lần
    def render_map():
        for y in range(height):
            for x in range(len(grid[y])):
                cell_type = grid[y][x]
                color = COLORS_PYGAME.get(cell_type, (255, 255, 255))
                
                rect = pygame.Rect(
                    x * cell_size,
                    y * cell_size,
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(screen, color, rect)
        pygame.display.flip()
    
    # Vẽ map ban đầu
    render_map()
    
    # Vòng lặp chính
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        clock.tick(30)
    
    pygame.quit()


# ============= SCRIPT CHÍNH ============= 

def main():
    """Hàm chính để test các chức năng"""
    import sys
    import os
    
    # Đảm bảo encoding UTF-8 cho console output trên Windows
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    
    # Đường dẫn đến file map
    map_path = os.path.join(os.path.dirname(__file__), "..", "Map", "den312d_map3.map")
    
    if not os.path.exists(map_path):
        print(f"Không tìm thấy file: {map_path}")
        return
    
    print("=" * 60)
    print("ĐANG ĐỌC FILE MAP...")
    print("=" * 60)
    
    # Đọc map
    grid = read_map_file(map_path)
    
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    
    print(f"\nThông tin map:")
    print(f"  - Kích thước: {width} x {height}")
    print(f"  - Tổng số ô: {width * height}")
    
    # Đếm các loại ô
    cell_counts = {}
    for row in grid:
        for cell in row:
            cell_counts[cell] = cell_counts.get(cell, 0) + 1
    
    print(f"\nPhân bố các loại ô:")
    for cell_type, count in sorted(cell_counts.items()):
        percentage = (count / (width * height)) * 100
        cell_name = {
            '@': 'Obstacle',
            'T': 'Tree',
            '.': 'Walkable',
            'S': 'Swamp',
            'W': 'Water'
        }.get(cell_type, 'Unknown')
        print(f"  - '{cell_type}' ({cell_name}): {count:,} ô ({percentage:.2f}%)")
    
    # Lấy các ô có thể đi
    walkable = get_walkable_cells(grid)
    print(f"\nSố ô có thể đi: {len(walkable):,} ô")
    
    print("\n" + "=" * 60)
    print("ĐANG HIỂN THỊ MAP BẰNG PYGAME...")
    print("(Nhấn ESC hoặc đóng cửa sổ để thoát)")
    print("=" * 60)
    
    # Hiển thị map với pygame (tự động scale)
    draw_map(grid)
    
    print("\nĐã đóng map viewer.")


if __name__ == "__main__":
    main()
