from combimath import combisum

def test_simple_case():
    target = 5.0
    numbers = [1.0, 2.0, 3.0, 4.0]
    result = combisum(target, numbers)[0]
    print(result)

    for combination in result:
        assert sum(combination) == target
test_simple_case()

# def test_negative_numbers():
#     target = -10
#     numbers = [-1, -2, -3, -4]
#     result = combisum(target, numbers)[0]
#     print(result)

#     for combination in result:
#         assert sum(combination) == target
# def test_large_array():
#     target = 100
#     numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
#     result = combisum(target, numbers)[0]
#     print(result)

#     for combination in result:
#         assert sum(combination) == target

# # def test_commas_in_numbers():
# #     target = 3556.21
# #     numbers = ["1,210.54", "2,345.67", "3,456.78"]
# #     result = combisum(target, numbers)[0]
# #     print(result)a

# #     for combination in result:
# #         assert sum(combination) == target

# def test_floats_and_integers():
#     target = 7.5
#     numbers = [1, 2.5, 3, 4.5, 5]
#     result = combisum(target, numbers)[0]
#     print(result)

#     for combination in result:
#         assert sum(combination) == target

# def test_other_cases():
#     target = 0
#     numbers = [-1, 0, 1]
#     result = combisum(target, numbers)[1]
#     print(result)

#     assert result['error'] == "Target must be nonzero"
