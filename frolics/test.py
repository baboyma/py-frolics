# * Empty squares are indicated by 0.
# * All number tiles slide all the way to the left.
# * When two identical numbers collide they combine to create the sum of the two numbers.

# The function should take a list of integers representing one row of the grid and return that row after swiping left once. For example:

import sys
import random

# URL: https://play2048.co/

# [0, 2, 4, 2] -> [2, 4, 2, 0]
# [4, 0, 0, 4] -> [8, 0, 0, 0]
# [2, 0, 2, 4] -> [4, 4, 0, 0]
# [2, 4, 4, 2] -> [2, 8, 2, 0]
# [4, 4, 4, 0] -> [8, 4, 0, 0]

def swipe_left_row(row):
    result = []

    new_row = [i for i in row if i != 0]  # Remove zeros
    new_row += [0] * (4 - len(new_row))  # Ensure the row has 4 elements

    print("\n<<== Swiping left row ===")
    print("Original row:", row)
    print("Updated row:", new_row)

    for i,n in enumerate(new_row):
        if i < len(new_row) - 1 and n == new_row[i +1]:
            result.append(n + new_row[i +1])
            new_row[i + 1] = 0
        else:
            result.append(n)

    result = [i for i in result if i != 0]  # Remove zeros again
    result += [0] * (4 - len(result))  # Ensure the result has 4 elements

    print("Result row:", result)

    return result


def swipe_left(rows):
    outrows = []
    for row in rows:
        outrow = swipe_left_row(row)
        outrows.append(outrow)
    return outrows

def main():
    # Example input to stdin
    # 0,2,4,2
    # 4,0,0,4
    # 2,0,2,4
    # 2,4,4,2

    # Example inputs for testing (outside of stdin)
    inputs = [
        [0, 2, 4, 2],
        [4, 0, 0, 4],
        [2, 0, 2, 4],
        [2, 4, 4, 2],
        [4, 4, 4, 0]
    ]

    # if len(sys.argv)==1:
    #     rows = []
    #     for line in sys.stdin:
    #         rows.append([int(r) for r in line.split(",")])
    # else:
    #     rows = [ [int(r) for r in row.split(",")] for row in sys.argv[1:] ]

    rows = random.choice(inputs)

    print("swipe_left")
    print(inputs)

    outrows = swipe_left(inputs)

    for i,outrow in enumerate(outrows):
        print(inputs[i],outrow,sep=" -> ")

    # print("swipe_right")
    # outrows = swipe_right(rows)
    # for i,outrow in enumerate(outrows):
    #     print(rows[i],outrow,sep=" -> ")

if __name__=="__main__":
    main()