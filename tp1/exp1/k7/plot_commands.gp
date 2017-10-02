set terminal png size 1200,900
set output 'graph.png'
set title 'Geração x Melhor Fitness'
set xlabel 'Geração'
set ylabel 'Melhor Fitness'
set xrange [0:10]
plot 'values.dat' u 1:2 notitle smooth bezier