set terminal png size 1200,900
set output 'graph.png'
set title 'Época x Acurácia (por taxa de aprendizado)'
set xlabel 'Época'
set ylabel 'Acurácia'
plot '0.05.dat' u 1:2 title '0.05' smooth bezier, '0.1.dat' u 1:2 title '0.1' smooth bezier, '0.2.dat' u 1:2 title '0.2' smooth bezier, '0.4.dat' u 1:2 title '0.4' smooth bezier, '0.6.dat' u 1:2 title '0.6' smooth bezier, '0.9.dat' u 1:2 title '0.9' smooth bezier