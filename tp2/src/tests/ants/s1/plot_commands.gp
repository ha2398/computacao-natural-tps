set terminal png size 1200,900
set output 'graph.png'
set title 'SJC1.dat: Iteração x Ótimo Global'
set xlabel 'Iteração'
set ylabel 'Ótimo Global'
plot '10.txt' u 1:2 title '10' smooth bezier, '30.txt' u 1:2 title '30' smooth bezier, '60.txt' u 1:2 title '60' smooth bezier, '90.txt' u 1:2 title '90' smooth bezier