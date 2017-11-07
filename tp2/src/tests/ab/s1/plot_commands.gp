set terminal png size 1200,900
set output 'graph.png'
set title 'SJC1.dat: Iteração x Custo da Melhor Solução'
set xlabel 'Iteração'
set ylabel 'Custo da Melhor Solução'
plot '1-3.dat' u 1:2 title '(alpha, beta) = 1, 3' smooth bezier, '2-2.dat' u 1:2 title '(alpha, beta) = 2, 2' smooth bezier, '3-1.dat' u 1:2 title '(alpha, beta) = 3, 1' smooth bezier