def flood_fill(surface, x, y, new_color):
    width = surface.get_width()
    height = surface.get_height()

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    old_color = surface.get_at((x, y))
    new_color = (new_color[0], new_color[1], new_color[2], 255)

    if old_color == new_color:
        return

    points = [(x, y)]

    while points:
        px, py = points.pop()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != old_color:
            continue

        surface.set_at((px, py), new_color)
        points.append((px + 1, py))
        points.append((px - 1, py))
        points.append((px, py + 1))
        points.append((px, py - 1))
