import copy

def cover_hypertree(hypertree) :
    """
    1  Tant que la matrice A n'est pas vide faire
    2  | Choisir la première colonne C contenant un minimum de 1 (déterministe);
    3  | Choisir une ligne L telle que ALC = 1;
    4  | On ajoute la ligne L à la solution partielle;
    5  | Pour chaque colonne J telle que ALJ = 1 faire
    6  | | Pour chaque ligne I telle que AIJ = 1 faire
    7  | | | Supprimer la ligne I de la matrice A;
    8  | | Fin
    9  | | Supprimer la colonne J de la matrice A;
    10 | Fin
    11 Fin
    """

    check = findAVertex(hypertree.incidenceMatrix)
    mat = modifyMat(copy.deepcopy(hypertree.incidenceMatrixTranspose))
    lineIteration ,Rows = howMuch(mat)
    allSolution = []
    solution = []
    while check and lineIteration > 0 :
        row = 1
        while row < len(mat) :
            column = find_column(mat)[0]
            columnslist = []
            rowslist = []
            colonne = 1
            #print("Choisir une ligne :",row)
            if mat[row][column] :
                solution.append(mat[row][0])
                #print("Choisir une ligne L telle que ALC = 1")
                #print("L :",mat[row][0],"C :",column)
                print("solution :",solution)


                while colonne < len(mat[0]) :
                    line = 1

                    if mat[row][colonne] :
                        #print("Pour chaque colonne J telle que ALJ = 1")
                        #print("L :",mat[row][0],"J :",colonne)

                        while line < len(mat) :


                            if mat[line][colonne] :
                                #print("Pour chaque ligne I telle que AIJ = 1")
                                #print("I :",mat[line][0],"J :",colonne)
                                if line not in rowslist  :
                                    rowslist.append(line)

                            line += 1

                        columnslist.append(colonne)
                    colonne += 1
                if rowslist :
                    print("Cut rows :"," ".join([mat[i][0] for i in rowslist]))
                    mat = cut_row(mat,rowslist)
                    printMatrix(mat)

                if columnslist :
                    mat = cut_column(mat,columnslist)
                    print("Cut columns :"," ".join([str(i) for i in columnslist]))
                    printMatrix(mat)
            row += 1

            if mat :
                column ,min = find_column(mat)
                if not min :
                    lineIteration -= 1
                    if lineIteration :
                        row = Rows[len(Rows)-lineIteration]
                        solution = []
                        mat = modifyMat(copy.deepcopy(hypertree.incidenceMatrixTranspose))
            elif not mat :
                allSolution.append(solution)
                lineIteration -= 1
                if lineIteration :
                    row = Rows[len(Rows)-lineIteration]
                    solution = []
                    mat = modifyMat(copy.deepcopy(hypertree.incidenceMatrixTranspose))

    return allSolution

def findAVertex(mat) :
    for row in mat :
        somme = sum(row)
        if somme == 0 or (somme == len(mat[0]) and somme != 1) :
            return False
    return True

def howMuch(mat) :
    column = find_column(mat)[0]
    lst = []
    line = 0
    row = 1
    while row < len(mat) :
        if mat[row][column] == 1 :
            lst.append(row)
            line += 1
        row += 1
    return line,lst

def find_column(mat) :
    min = len(mat)-1
    column = 1
    x = 0
    for i in range(1,len(mat[0])) :
        for row in mat[1:] :
            x += row[i]
        if x <  min :
            min = x
            column = i
        x = 0
    return column, min

def cut_row(mat,rowslist) :

    return [ mat[i] for i in range(len(mat)) if i not in rowslist]

def cut_column(mat,columnslist) :
    newmat = []
    for row in mat :
        temp = [ row[i] for i in range(len(mat[0])) if i not in columnslist ]
        if len(temp) > 1 :
            newmat.append(temp)
    return newmat

def modifyMat(matrix) :
    newmat = [[i for i in range(len(matrix[0])+1)]]
    for i in range(len(matrix)) :
        matrix[i].insert(0,"E"+str(i+1))
        newmat.append(matrix[i])
    newmat[0][0] = "X "

    return newmat

def printMatrix(Matrix) :
    if Matrix :
        n = len(Matrix)
        m = len(Matrix[0])
        print("\n".join(["   ".join([str(Matrix[i][j]) for j in range(m)]) for i in range(n)]))
    else :
        print("Matrix vide")
