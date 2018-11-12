from copy import deepcopy

def cover_hypertree(hypertree) :
    """
    Une fonction qui prend en paramètre un hypertree et affichera
    si oui ou nous il existe une couverture exacte pour cet hypertree
    (si la réponse est oui, la fonction affichera également la couverture).
    """
    matrix = modifyMat(hypertree.incidenceMatrixTranspose)
    # Utiliser la transposée de la matrice d'incidence
    # Lignes de la matrice == les hyper-arêtes
    # Colonnes de la matrice == Les sommets
    solution = Algorithm_X(matrix,[],[])
    # Trouver des solutions au problème de la couverture exacte s'il y en a .

    if solution :
        print("\nThere is "+str(len(solution))+" exact cover for this hypertree : ")
        print("\n".join( str(solution[i]) for i in range(len(solution))))
    else :
        print("\nThere is not an exact cover for this hypertree.")

def Algorithm_X(matrix,solution=[],allSolution = []) :
    """
    L'algorithme de Knuth X est un algorithme récursif,non déterministe,
    depth-first,backtracking algorithme .Il permet de trouver des solutions
    au problème de la couverture exacte.
    """

    mat = deepcopy(matrix)
    column = findMinColumn(mat)[0]
    # La première colonne C (column) contenant un minimum de 1
    Rows = findRows(mat,column)
    # une liste des lignes (L) trouvées telle que matrice[L][C] = 1

    for row in Rows :
        # Une ligne L (row) telle que matrice[L][C] = 1
        columnslist = []
        # Liste contenant les colonnes à supprimer
        rowslist = []
        # Liste contenant les lignes à supprimer

        print("Row :",mat[row][0])

        solution.append(mat[row][0])
        # On ajoute la ligne L à la solution partielle

        print("Partial solution :",solution)

        for colonne in range(1,len(mat[0])) :

            if mat[row][colonne] :
                # Pour chaque colonne J (colonne) telle que matrice[L][J] = 1
                for line in range(1,len(mat)) :

                    if mat[line][colonne] :
                        # Pour chaque ligne I (line) telle que matrice[I][J] = 1
                        if line not in rowslist  :
                            rowslist.append(line)
                            # Ajoute la ligne I de la matrice au rowslist
                columnslist.append(colonne)
                # Ajoute la colonne J de la matrice au columnslist

        mat = cutMatrix(mat,rowslist,columnslist)
        # Supprime les colonnes et les lignes de la matrice

        if mat :
            # La matrice n'est pas vide, on n'est donc pas arrivé à une solution.
            if findMinColumn(mat)[1] :
                # La première colonne avec un minimum de 1 est la colonne qui contient au moins un 1
                Algorithm_X(mat,solution,allSolution)
                # L'algorithme reprend depuis l'étape 1 sur cette nouvelle matrice

            # Else
            # La première colonne avec un minimum de 1 est la colonne qui n'en contient aucun .
            # Comme il n'y a pas de 1, on ne peut donc plus réduire la matrice et
            # cette branche de l'algorithme échoue.

        elif not mat :
            # Il ne reste qu'une matrice vide
            print("Solution found : ",solution)
            if solution not in allSolution :
                # On a trouvé une solution au problème de couverture exacte
                allSolution.append(solution[:])

        solution.pop()
        # On supprime la ligne L de la solution partielle
        mat = deepcopy(matrix)
        # Reprendre sur la matrice d'avant pour la ligne suivante

    return allSolution

def findRows(mat,column) :
    """
    Renvoie une liste des lignes L telle que matrice[L][C] = 1
    C (column) et la longueur de cette liste.
    """
    return [ row for row in range(1,len(mat)) if mat[row][column]]

def findMinColumn(mat) :
    """
    Renvoie l'indice de la première colonne C de la matrice
    contenant un minimum de 1 et la valeur de ce minimum.
    """
    columnsSumList = [sum( row[i] for row in mat[1:]) for  i in range(1,len(mat[0]))]
    # Liste contenant la somme de chaque colonne
    minimumSum = min(columnsSumList)
    # La somme minimum de cette liste
    columnIndex = columnsSumList.index(minimumSum) + 1
    # La première colonne contenant un minimum de 1

    return columnIndex, minimumSum

def cutMatrix(matrix,rowslist,columnslist) :
    """
    Renvoie une nouvelle matrice en enlevant les lignes et les colonnes
    contenu dans rowlist et columnslist
    """
    mat = deepcopy(matrix)
    printMatrix(mat)

    if rowslist :
        # Supprime les lignes de la matrice
        print("Cut rows :"," ".join([mat[i][0] for i in rowslist]))
        mat = [ mat[i] for i in range(len(mat)) if i not in rowslist]
        printMatrix(mat)

    if columnslist :
        # Supprime les colonnes de la matrice
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
    """
    Affiche la matrice .
    """
    if Matrix :
        n = len(Matrix)
        m = len(Matrix[0])
        print("\n".join([" ".join([str(Matrix[i][j]) for j in range(m)]) for i in range(n)]))
    else :
        print("Matrice vide")

def modifyMat(mat) :
    """
    Transforme une matrice

                  X  1 2 3
    0 1 0         E1 0 1 0
    1 0 1   vers  E2 1 0 1
    1 1 0         E3 1 1 0

    """
    matrix = deepcopy(mat)
    newmat = [[i for i in range(len(matrix[0])+1)]]
    newmat[0][0] = "X "

    for i in range(len(matrix)) :
        matrix[i].insert(0,"E"+str(i+1))
        newmat.append(matrix[i])

    return newmat
