set terminal png size 1200,900
set output 'graph.png'
set title 'Época x Acurácia (por taxa de aprendizado)'
set xlabel 'Época'
set ylabel 'Acurácia'
plot '0.01.dat' u 1:2 title '0.01' smooth bezier, '0.02.dat' u 1:2 title '0.02' smooth bezier, '0.04.dat' u 1:2 title '0.04' smooth bezier, '0.08.dat' u 1:2 title '0.08' smooth bezier, '0.1.dat' u 1:2 title '0.1' smooth bezier