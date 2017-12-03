set terminal png size 1200,900
set output 'graph.png'
set title 'Época x Acurácia (por quantidade de camadas escondidas)'
set xlabel 'Época'
set ylabel 'Acurácia'
plot '8.dat' u 1:2 title '8' smooth bezier, '6.dat' u 1:2 title '6' smooth bezier, '4.dat' u 1:2 title '4' smooth bezier, '2.dat' u 1:2 title '2' smooth bezier, '1.dat' u 1:2 title '1' smooth bezier