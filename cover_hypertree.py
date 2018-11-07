from copy import deepcopy

def cover_hypertree(hypertree) :
    """
    Une fonction qui prend en paramètre un hypertree et affichera
    si oui ou nous il existe une couverture exacte pour cet hypertree 
    (si la réponse est oui, la fonction affichera également la couverture).
    """
    matrix = modifyMat(hypertree.incidenceMatrixTranspose)

    solution = cover(matrix,[],[])

    if solution :
        print("\nThere is "+str(len(solution))+" exact cover for this hypertree : ")
        print("\n".join( str(solution[i]) for i in range(len(solution))))
    else :
        print("\nThere is not an exact cover for this hypertree.")

def cover(matrix,solution=[],allSolution = []) :
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

    mat = deepcopy(matrix)
    column = find_column(mat)[0]
    lineIteration , Rows = howMuch(mat,column)

    while lineIteration > 0 :

        row = Rows[len(Rows)-lineIteration]
        columnslist = []
        rowslist = []

        print("lineIteration :",lineIteration)
        print("Row :",mat[row][0])
        print("solution :",solution)

        solution.append(mat[row][0])

        #print("Une ligne L :",mat[row][0]," et C :",mat[0][column],"telle que ALC = 1\n")
        print("solution :",solution)

        for colonne in range(1,len(mat[0])) :

            if mat[row][colonne] :
                #print("L :",mat[row][0]," et Colonne J :",mat[0][colonne]," telle que ALJ = 1\n")
                for line in range(1,len(mat)) :

                    if mat[line][colonne] :
                        #print("Ligne I :",mat[line][0]," et J :",mat[0][colonne]," telle que AIJ = 1\n")
                        if line not in rowslist  :
                            rowslist.append(line)

                columnslist.append(colonne)

        mat = cutMatrix(mat,rowslist,columnslist)

        if mat :
            if not find_column(mat)[1] :
                lineIteration -= 1
                mat = deepcopy(matrix)
            else :
                cover(mat,solution,allSolution)
                lineIteration -= 1
                mat = deepcopy(matrix)

        elif not mat :
            lineIteration -= 1
            print("Solution found : ",solution)
            if solution not in allSolution :
                allSolution.append(solution[:])
            mat = deepcopy(matrix)

        solution.pop()

    return allSolution

def howMuch(mat,column) :
    """
    Renvoie une liste des lignes L telle que matrice[L][C] = 1
    et la longueur de cette liste.
    """
    rows = [ row for row in range(1,len(mat)) if mat[row][column]]
    iteration = len(rows)

    return iteration,rows

def find_column(mat) :
    """
    Renvoie l'indice de la première colonne C de la matrice
    contenant un minimum de 1 et la valeur de ce minimum.
    """
    columnsSumList = [sum( row[i] for row in mat[1:]) for  i in range(1,len(mat[0]))]
    minimumSum = min(columnsSumList)
    columnIndex = columnsSumList.index(minimumSum) + 1

    return columnIndex, minimumSum

def cutMatrix(matrix,rowslist,columnslist) :
    mat = deepcopy(matrix)
    printMatrix(mat)

    if rowslist :
        print("Cut rows :"," ".join([mat[i][0] for i in rowslist]))
        mat = [ mat[i] for i in range(len(mat)) if i not in rowslist]
        printMatrix(mat)

    if columnslist :
        print("Cut columns :"," ".join([str(i) for i in columnslist]))
        newmat = []
        for row in mat :
            temp = [ row[i] for i in range(len(mat[0])) if i not in columnslist ]
            if len(temp) > 1 :
                newmat.append(temp)
        mat = newmat
        printMatrix(mat)
    return mat

def printMatrix(Matrix) :
    if Matrix :
        n = len(Matrix)
        m = len(Matrix[0])
        print("\n".join([" ".join([str(Matrix[i][j]) for j in range(m)]) for i in range(n)]))
    else :
        print("Matrix vide")

def modifyMat(mat) :
    """
    Transformer une matrice

                    X  1 2 3
        0 1 0       E1 0 1 0
    du  1 0 1 vers  E2 1 0 1
        1 1 0       E3 1 1 0


    """
    matrix = deepcopy(mat)
    newmat = [[i for i in range(len(matrix[0])+1)]]
    newmat[0][0] = "X "

    for i in range(len(matrix)) :
        matrix[i].insert(0,"E"+str(i+1))
        newmat.append(matrix[i])

    return newmat
