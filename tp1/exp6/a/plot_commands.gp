set terminal png size 1200,900
set output 'graph.png'
set title 'Geração x Indivíduos Repetidos'
set xlabel 'Geração'
set ylabel 'Indivíduos Repetidos'
plot 'values.dat' u 1:2 notitle smooth bezier