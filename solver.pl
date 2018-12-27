/* Autor original: Markus Triska  (triska@metalevel.at) */

:- use_module(library(clpfd)).

sudoku(Rows) :-
        length(Rows, 9),                        /* Verifica que el numero de filas sea igual a 9 */
	maplist(same_length(Rows), Rows),       /* Verifica que todas las filas sean del mismo tamaño */
        append(Rows, Vs),                       /* Aplana la lista, todo el tablero queda en Vs */
	Vs ins 1..9,                            /* Verifica que todos los elementos de Vs se encuentren en el dominio [0,9] */
        maplist(all_distinct, Rows),            /* Condición de que todos los elementos de cada fila deben ser distintos */
        transpose(Rows, Columns),               /* Traspone filas para obtener lista de columnas */
	maplist(all_distinct, Columns),         /* Condición de que todos los elementos de cada columna deben ser distintos */
        Rows = [As,Bs,Cs,Ds,Es,Fs,Gs,Hs,Is],    /* Unifica Rows con la lista de variables */
        blocks(As, Bs, Cs), blocks(Ds, Es, Fs), blocks(Gs, Hs, Is). /* Verifica que no se repita ningún dígito en cada bloque */

blocks([N1,N2,N3|Ns1], [N4,N5,N6|Ns2], [N7,N8,N9|Ns3]) :- all_distinct([N1,N2,N3,N4,N5,N6,N7,N8,N9]), blocks(Ns1, Ns2, Ns3). /* Verifica bloques uno por uno recursivamente */
blocks([], [], []). /* Termina la recursión si todas las listas son vacías */

solve_sudoku(Board) :- sudoku(Board), maplist(labeling([ff]), Board). /* Resuelve probando diferentes valores para las filas */
