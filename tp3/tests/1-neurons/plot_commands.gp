set terminal png size 1200,900
set output 'graph.png'
set title 'Época x Acurácia (por quantidade de neurônios)'
set xlabel 'Época'
set ylabel 'Acurácia'
plot '128.dat' u 1:2 title '128' smooth bezier, '64.dat' u 1:2 title '64' smooth bezier, '32.dat' u 1:2 title '32' smooth bezier, '16.dat' u 1:2 title '16' smooth bezier, '8.dat' u 1:2 title '8' smooth bezier