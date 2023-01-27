import json

def edges_to_center(points):
    """
    takes in a list of 4 values representing 2 edges(x,y,x2,y2) and returns the center and size(x,y,w,h)
    """
    x1 = points[0]
    y1 = points[1]
    x2 = points[2]
    y2 = points[3]
    center_x = x1 + (x2 - x1) / 2
    center_y = y1 + (y2 - y1) / 2
    w = x2 - x1
    h = y2 - y1
    return (center_x, center_y, w, h)

def edge_with_size_to_center(points):
    """
    takes in a list of 4 values representing an edge(from bottom left) and size(x,y,w,h) and returns the center and size(x,y,w,h)
    """
    x = points[0]
    y = points[1]
    w = points[2]
    h = points[3]
    center_x = x + w / 2
    center_y = y + h / 2
    return (center_x, center_y, w, h)

def normalize(points, img_x, img_y):
    """
    takes in a list of 4 values representing the center and size(x,y,w,h) or edges(x,y,x2,y2) and returns the normalized values based on img size
    """
    x = points[0]
    y = points[1]
    w = points[2]
    h = points[3]
    x = x / img_x
    y = y / img_y
    w = w / img_x
    h = h / img_y
    return (x, y, w, h)

def denormilize(points, img_x, img_y):
    """
    takes in a list of 4 normalized values representing the center and size(x,y,w,h) or edges(x,y,x2,y2) and returns the denormalized values based on img size
    """
    x = points[0]
    y = points[1]
    w = points[2]
    h = points[3]
    x = x * img_x
    y = y * img_y
    w = w * img_x
    h = h * img_y
    return (x, y, w, h)

def center_to_edges(points):
    """
    takes in a list of 4 values representing the center and size(x,y,w,h) and returns the bottom left and top right corners(x,y,x2,y2)
    """
    x = points[0]
    y = points[1]
    w = points[2]
    h = points[3]
    x1 = x - w/2
    y1 = y - h/2
    x2 = x + w/2
    y2 = y + h/2
    return (x1, y1, x2, y2)



def read_app_data(path) -> dict:
    """
    this will read the app data from the file and return it as a dictionary
    """
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}

def write_app_data(path, data: dict) -> None:
    """
    this will clear all previous data and replace it with the new data so be careful
    """
    with open(path, "w") as f:
      json.dump(data, f)

def update_app_data(path, new_data: dict):
    """
    this will update the app data with the new data
    """
    data = read_app_data(path)
    data.update(new_data)
    write_app_data(path, data)