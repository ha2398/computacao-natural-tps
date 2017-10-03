set terminal png size 1200,900
set output 'graph.png'
set title 'Geração x Melhor Fitness'
set xlabel 'Geração'
set ylabel 'Melhor Fitness'
plot 'values.dat' u 1:2 title 'E=0' w linespoints, \
'values.dat' u 1:3 title 'E=2' w linespoints