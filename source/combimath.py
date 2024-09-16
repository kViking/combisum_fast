import torch

def combisum(target, numbers) -> list[list[float], dict]:
    # Create a dictionary to store flags and error messages
    flag = {
        "cuda": None,  # Flag indicating if CUDA is available
        "max_length": None,  # Maximum combination length for CUDA
        "combo_length": None,  # Current combination length being processed
        "target": target,  # Target sum
        "numbers": numbers,  # List of numbers
        "error": None  # Error message
    }

    if target == 0:
        flag["error"] = "Target must be nonzero"  # Check if target is zero
        return [[], flag]
    
    # Convert numbers to integers if they have two decimal places
    int_numbers = [int(100*x) if round(100*x) == 100*x else None for x in numbers]
    int_numbers = [x for x in int_numbers if x is not None]
    numbers = numbers if len(int_numbers) != len(numbers) else int_numbers
    target = int(100*target) if type(numbers[0]) == int else target

    if torch.cuda.is_available():
        device = torch.device("cuda")  # Use CUDA if available
        flag['cuda'] = True
    else:
        device = torch.device("cpu")  # Use CPU if CUDA is not available
        flag['max_length'] = 5  # Set maximum combination length for CPU
        flag['cuda'] = False

    tensor = torch.tensor(numbers).to(device)  # Convert numbers to tensor and move to device
    target = torch.tensor(target).to(device)  # Convert target to tensor and move to device

    combinations = []
    for i in range(2, len(numbers) + 1):
        if flag['max_length'] and i > flag['max_length']:
            flag["error"] = f"CUDA not accessible. CPU run with restricted combination length {flag['max_length']}" if flag["cuda"] else "Reached device's computational limit"
            break
        try:
            combs = torch.combinations(tensor, r=i, with_replacement=False)  # Generate combinations of length i
            combinations.append(combs)  # Add combinations to the list
            flag['combo_length'] = i  # Update the current combination length
        except Exception as e:
            flag["error"] = "Reached device's computational limit"  # Handle exception when reaching computational limit
            break

    valid_combinations = []
    for combo in combinations:
        indices = torch.where(torch.sum(combo, dim=1) == target)[0]  # Find indices where sum of each combination equals target
        valid_combinations.extend(combo[indices].tolist())  # Add valid combinations to the list

    valid_combinations = [[x/100 for x in y] for y in valid_combinations] if type(numbers[0]) == int else [[round(x, 2) for x in y] for y in valid_combinations]  # Convert back to original format

    return [valid_combinations, flag]  # Return valid combinations and flag dictionary
