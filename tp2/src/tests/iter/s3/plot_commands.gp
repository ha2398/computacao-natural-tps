set terminal png size 1200,900
set output 'graph.png'
set title 'SJC3b.dat: Iteração x Custo da Melhor Solução'
set xlabel 'Iteração'
set ylabel 'Custo da Melhor Solução'
plot 'best.dat' u 1:2 title 'Global' smooth bezier, 'local.dat' u 1:2 title 'Local' smooth bezier