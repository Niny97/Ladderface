import csv
import shutil
import pygame


def convert_csv_to_map(filename):
    ground_number = 5
    ladder_number = 3

    with open(filename, newline='') as csvfile:
        map_reader = csv.reader(csvfile)
        game_map = []
        walkable = []

        for row_idx, row in enumerate(map_reader):
            map_row = []

            for col_idx, number_str in enumerate(row):
                try:
                    number = int(number_str)

                    if number == ground_number:
                        map_row.append('G')
                        walkable.append((col_idx, row_idx))

                    elif number == ladder_number:
                        map_row.append('L')
                        walkable.append((col_idx, row_idx))

                    else:
                        # Handle other numbers
                        map_row.append('X')

                except ValueError:
                    map_row.append('X')

            game_map.append(map_row)

    return game_map, walkable


def modify_csv(file_path, row_index, col_index, new_value):
    # Read the CSV file
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    # Modify value
    data[row_index][col_index] = new_value

    # Write data back to the file
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def copy_csv(original, new):
    shutil.copyfile(original, new)
    return new


def render_map(screen, tileset, tile_rects, map_filename, target_size):
    with open(map_filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        tile_size = target_size

        for row_idx, row in enumerate(csvreader):

            for col_idx, tile_id in enumerate(row):
                tile_id = int(str(tile_id.strip()))

                if tile_id in tile_rects:
                    source_rect = pygame.Rect(tile_rects[tile_id])
                    target_rect = pygame.Rect(col_idx * tile_size, row_idx * tile_size, tile_size, tile_size)

                    # Scale the tile to the target size
                    scaled_tile = pygame.transform.scale(tileset.subsurface(source_rect),
                                                         (tile_size, tile_size))

                    # Blit the scaled tile onto the screen
                    screen.blit(scaled_tile, target_rect)
