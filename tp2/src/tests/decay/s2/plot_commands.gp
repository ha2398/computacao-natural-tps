set terminal png size 1200,900
set output 'graph.png'
set title 'SJC2.dat: Iteração x Custo da Melhor Solução'
set xlabel 'Iteração'
set ylabel 'Custo da Melhor Solução'
plot '0.3.dat' u 1:2 title '0.3' smooth bezier, '0.6.dat' u 1:2 title '0.6' smooth bezier, '0.8.dat' u 1:2 title '0.8' smooth bezier, '0.9.dat' u 1:2 title '0.9' smooth bezier