import random
import constants as c

def new_game(n):
    matrix = []
    for i in range(n):
        matrix.append([0] * n)

    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix

# μέθοδος για την προσθήκη ενός 2 στο
# στο πλέγμα σε κάποιο τυχαίο κενό κελί
def add_two(mat):
    row = random.randint(0, len(mat)-1)
    column = random.randint(0, len(mat)-1)
    while mat[row][column] != 0:
        row = random.randint(0, len(mat)-1)
        column = random.randint(0, len(mat)-1)
    mat[row][column] = 2
    return mat

winNum=2048
#μέθοδος για την τρέχουσα κατάσταση του παιχνιδιού
def game_state(mat):
    # έλεγχος αν το παιχίδι κερδήθηκε
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == winNum:
                return 'win'
    # έλεγχος για κενά κελιά
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'
    # έλεγχος αν κάποια κελιά που αγγίζονται μεταξύ τους
    for i in range(len(mat)-1):
        # μείωση εκ προθέσεως για να ελεγχθεί η γραμμή στα δεξιά και κάτω
        for j in range(len(mat[0])-1):
            if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                return 'not over'
    for k in range(len(mat)-1):  # για τον έλεγχο των θέσεων δεξιά/αριστερά της τελευταίας γραμμής
        if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1):  # έλεγχος των πάνω/κάτω θέσεων στην τελευταία στήλη
        if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'

def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

def cover_up(mat):
    new = []
    for j in range(c.GRID_LEN):
        partial_new = []
        for i in range(c.GRID_LEN):
            partial_new.append(0)
        new.append(partial_new)
    done = False
    for i in range(c.GRID_LEN):
        count = 0
        for j in range(c.GRID_LEN):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done


def merge(mat, done):
    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN-1):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                c.SCORE=c.SCORE+ mat[i][j]
                mat[i][j+1] = 0
                done = True
    return mat, done


def up(game):
    #print("up")
    # return matrix after shifting up
    game = transpose(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(game)
    return game, done


def down(game):
    #print("down")
    game = reverse(transpose(game))
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(reverse(game))
    return game, done


def left(game):
    #print("left")
    # return matrix after shifting left
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    return game, done


def right(game):
    #print("right")
    # return matrix after shifting right
    game = reverse(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = reverse(game)
    return game, done
