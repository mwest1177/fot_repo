

choices = [
    'Trillium Farm',
    'Trillium Living-Learning Center',
    'Trillium Wilderness Education Retreat Center',
    'Trillium Wilderness Retreat Center',
    'Other',
]

ballots = {
    'John': {
        'Trillium Farm': 3,
        'Trillium Living-Learning Center': 2,
        'Trillium Wilderness Education Retreat Center': 1,
        'Trillium Wilderness Retreat Center': 4,
        'Other': 5,
    },
    
    'Dougie': {
        'Trillium Farm': 5,
        'Trillium Living-Learning Center': 4,
        'Trillium Wilderness Education Retreat Center': 2,
        'Trillium Wilderness Retreat Center': 3,
        'Other': 1,
    },
    
    'Alison': {
        'Trillium Living-Learning Center': 3,
        'Trillium Wilderness Education Retreat Center': 4,
        'Trillium Wilderness Retreat Center': 5,
    },
    
    'Jonah': {
        'Trillium Farm': 5,
        'Trillium Living-Learning Center': 1,
        'Trillium Wilderness Education Retreat Center': 2,
        'Trillium Wilderness Retreat Center': 3,
        'Other': 4,
    },
    
    'Miranda': {
        'Trillium Farm': 2,
        'Trillium Living-Learning Center': 4,
        'Trillium Wilderness Education Retreat Center': 3,
        'Trillium Wilderness Retreat Center': 1,
    },
    
    'Tessa': {
        'Trillium Farm': 5,
        'Trillium Living-Learning Center': 2,
        'Trillium Wilderness Education Retreat Center': 4,
        'Trillium Wilderness Retreat Center': 3,
        'Other': 1,
    },
    
    'Michael': {
        'Trillium Farm': 1,
        'Trillium Living-Learning Center': 4,
        'Trillium Wilderness Education Retreat Center': 3,
        'Trillium Wilderness Retreat Center': 2,
        'Other': 5,
    },
    
    'Shandy': {
        'Trillium Farm': 4,
        'Trillium Living-Learning Center': 1,
        'Trillium Wilderness Education Retreat Center': 5,
        'Trillium Wilderness Retreat Center': 2,
        'Other': 3,
    },
    
    'Thrifty': {
        'Trillium Farm': 5,
        'Trillium Living-Learning Center': 4,
        'Trillium Wilderness Education Retreat Center': 2,
        'Trillium Wilderness Retreat Center': 1,
    },
    
    'Meg': {
        'Trillium Farm': 4,
        'Trillium Living-Learning Center': 1,
        'Trillium Wilderness Education Retreat Center': 3,
        'Trillium Wilderness Retreat Center': 2,
    }
}


matrix = [[0 for x in choices] for y in choices]

def tally(ballot):
    for candidate, score in ballot.items():
        for opponent in choices:
            if candidate == opponent:
                continue

            win = False
            if opponent not in ballot:
                win = True
            else:
                win = score < ballot[opponent]

            if win:
                c_index = choices.index(candidate)
                o_index = choices.index(opponent)
                matrix[c_index][o_index] += 1



for voter, ballot in ballots.items():
    tally(ballot)

def print_matrix():
    for row in matrix:
        print row

    for a in choices:
        print '---'
        for b in choices:
            if a == b:
                continue
            a_index = choices.index(a)
            b_index = choices.index(b)

            if matrix[a_index][b_index] > matrix[b_index][a_index]:
                print a, '--beats-->', b
            elif matrix[a_index][b_index] < matrix[b_index][a_index]:
                pass
            else:
                print a, '==========', b

print_matrix()
