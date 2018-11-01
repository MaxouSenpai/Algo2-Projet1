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
    HyperedgeList = list(hypertree.E.keys())
    #print(HyperedgeList)
    matrix = hypertree.incidenceMatrixTranspose
    check = True
    mat = copy.deepcopy(matrix)
    solution = []
    while check :
        row = 0
        while row < len(mat) :
            column ,min = find_column(mat)
            if not min :
                return solution
            print("Naniiiiiiiiii",row)
            columnslist = []
            rowslist = []
            colonne = 0
            printMatrix(mat)
            print("solution :",solution)

            if mat[row][column] :
                print("Choisir une ligne L telle que ALC = 1")
                print("L :",HyperedgeList[row],"C :",column)
                solution.append(HyperedgeList[row])


                while colonne < len(mat[0]) :
                    line = 0

                    if mat[row][colonne] :
                        print("Pour chaque colonne J telle que ALJ = 1")
                        print("L :",HyperedgeList[row],"J :",colonne)

                        while line < len(mat) :


                            if mat[line][colonne] :
                                print("Pour chaque ligne I telle que AIJ = 1")
                                print("I :",HyperedgeList[line],"J :",colonne)
                                print(rowslist)
                                if line not in rowslist  :
                                    rowslist.append(line)

                            line += 1

                        columnslist.append(colonne)
                    colonne += 1
                if rowslist :
                    if not (set([HyperedgeList[i] for i in rowslist]) == set([ E for E in HyperedgeList])) :
                        print("Cut rows :"," ".join([HyperedgeList[i] for i in rowslist]))
                        mat = cut_row(mat,rowslist)
                        deleteRowsName = [HyperedgeList[i] for i in rowslist]
                        for RowName in deleteRowsName :

                            HyperedgeList.remove(RowName)

                        printMatrix(mat)
                    else :
                        print("Cut All Rows !!!!!!!!!")
                        solution = []
                        check = False
                        break

                if columnslist :
                    print("Cut columns :"," ".join([str(i) for i in columnslist]))
                    mat = cut_column(mat,columnslist)
                    printMatrix(mat)
            row += 1
            if (row == len(matrix) and not mat) or not mat :
                check = False
                break
            else :
                column ,min = find_column(mat)
                if not min :
                    mat = copy.deepcopy(matrix)
                    solution = []
                    HyperedgeList = list(hypertree.E.keys())

    return solution

def find_column(mat) :
    min = len(mat)
    column = 0
    x = 0
    for i in range(len(mat[0])) :
        for row in mat :
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
        if temp :
            newmat.append(temp)
    return newmat

def printMatrix(Matrix) :
    if Matrix :
        n = len(Matrix)
        m = len(Matrix[0])
        print("\n".join([" ".join([str(Matrix[i][j]) for j in range(m)]) for i in range(n)]))
    else :
        print("Matrix vide")
