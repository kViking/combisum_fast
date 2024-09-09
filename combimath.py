import torch
import logging

logging.basicConfig(filename='math.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(console_handler) 
logger = logging.getLogger(__name__)

def combisum(target, numbers):
    logger.info(f'Received target: {target}\nlist: {numbers}')

    flag = {
        "cuda": None,
        "max_length": None,
        "combo_length": None,
        "target": target,
        "numbers": numbers,
        "error": None
    }

    if target == 0:
        flag["error"] = "Target must be nonzero"
        return [[],flag]
    
    int_numbers = [int(100*x) if int(100*x)/100 == x else None for x in numbers]
    numbers = numbers if len(int_numbers) != len(numbers) else int_numbers
    target = int(100*target) if type(numbers[0]) == int else target

    if torch.cuda.is_available():
        device = torch.device("cuda")
        logging.info("CUDA is available. Using GPU.")
        flag['cuda'] = True
    else:
        device = torch.device("cpu")
        logging.info("CUDA is not available. Using CPU.")
        flag['max_length'] = 5
        logging.info("Maximum combination length restricted to 5")
        flag['cuda'] = False

    tensor = torch.tensor(numbers).to(device)
    target = torch.tensor(target).to(device)

    combinations = []
    for i in range(2, len(numbers) + 1):
        if flag['max_length'] and i > flag['max_length']:
            flag["error"] = "Reached device's computational limit"
            break
        try:
            logger.info(f"attempting combinations of {i} length")
            combs = torch.combinations(tensor, r=i, with_replacement=False)
            combinations.append(combs)
            flag['combo_length'] = i
        except Exception as e:
            logging.error(f"Error generating combinations: {e}")
            flag["error"] = "Reached device's computational limit"
            break

    valid_combinations = []
    for combo in combinations:
        indices = torch.where(torch.sum(combo, dim=1) == target)[0]
        valid_combinations.extend(combo[indices].tolist())

    valid_combinations = [[x/100 for x in y] for y in valid_combinations]

    return [valid_combinations, flag]

# Example usage
if __name__ == "__main__":
    target = 12.3
    numbers = [1.3, 11, 12, 0.3, 5]
    combinations = combisum(target, numbers)
    print(combinations)