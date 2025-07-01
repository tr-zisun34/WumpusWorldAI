def infer_from_percepts(kb, x, y, percepts):
    # If no percepts, all adjacent are safe
    neighbors = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    if 'Breeze' not in percepts and 'Stench' not in percepts:
        for (nx, ny) in neighbors:
            if 0 <= nx < 10 and 0 <= ny < 10:
                kb.mark_safe(nx, ny)
    else:
        for (nx, ny) in neighbors:
            if 0 <= nx < 10 and 0 <= ny < 10:
                # Possible risk (conservatively unsafe)
                if (nx, ny) not in kb.safe_cells:
                    kb.mark_unsafe(nx, ny)
