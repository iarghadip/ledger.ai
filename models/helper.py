from pathlib import Path

def resolve(type):

    number = 1
    folder = Path(__file__).parent
    childrens = [f for f in folder.iterdir() if f.is_dir() and f.name.startswith("version_")]
    
    if childrens:
        numbers = []
        for f in childrens:
            try:
                numbers.append(int(f.name.split('_')[1]))
            except (IndexError, ValueError):
                continue
        if numbers:
            number = max(numbers)
    
    if type == 'save':
        number = number + 1

    output = dict(
        name=f"version_{number}"
        folder=folder / f"version_{number}"
    )
    
    if type == 'save':
        os.makedirs(output.get('folder'), exist_ok=True)
    
    return output