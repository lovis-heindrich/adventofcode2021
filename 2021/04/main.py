import numpy as np

def check_win(board, numbers):
    mask = np.isin(board, numbers)
    if any(mask.all(axis=1)) or any(mask.all(axis=0)):
        numbers_in_board = [n for n in numbers if n in board.flatten()]
        return (np.sum(board.flatten()) - np.sum(numbers_in_board)) * numbers[-1]
    else:
        return False

def get_winning_score(boards, numbers):
    for index in range(1, len(draw_numbers)):
        drawn_numbers = numbers[0:index]
        for board in boards:
            score = check_win(board, drawn_numbers)
            if score:
                return score

def get_last_winning_score(boards, numbers):
    winning_boards = []
    for index in range(1, len(draw_numbers)):
        drawn_numbers = numbers[0:index]
        for board_index, board in enumerate(boards):
            if board_index not in winning_boards:
                score = check_win(board, drawn_numbers)
                if score:
                    winning_boards.append(board_index)
    return score


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = f.read().splitlines()
    
    draw_numbers = [int(x) for x in lines[0].split(",")]
    
    boards = []
    index = 1
    while index < len(lines):
        if lines[index]:
            board = []
            while index < len(lines) and lines[index]:
                board.append([int(x) for x in lines[index].strip().split(" ") if x])
                index += 1
            boards.append(np.array(board))
        else:
            index += 1

    print(get_winning_score(boards, draw_numbers))

    print(get_last_winning_score(boards, draw_numbers))