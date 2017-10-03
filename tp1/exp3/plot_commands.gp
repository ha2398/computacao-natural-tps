set terminal png size 1200,900
set output 'graph.png'
set title 'Geração x Melhor Fitness'
set xlabel 'Geração'
set ylabel 'Melhor Fitness'
plot 'values.dat' u 12 title 'C=0.6, M=0.3' smooth bezier, \
'values.dat' u 13 title 'C=0.9, M=0.05' smooth bezier