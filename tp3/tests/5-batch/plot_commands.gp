set terminal png size 1200,900
set output 'graph2.png'
set title 'Tamanho de Batch x Tempo de treinamento (s)'
set xlabel 'Tamanho de Batch'
set ylabel 'Tempo de treinamento (s)'
set boxwidth 8.0
set style fill solid
set xrange [-5:110]
plot '1.dat' u 1:2:xtic(1) notitle with boxes, '10.dat' u 1:2:xtic(1) notitle with boxes, '25.dat' u 1:2:xtic(1) notitle with boxes, '50.dat' u 1:2:xtic(1) notitle with boxes, '100.dat' u 1:2:xtic(1) notitle with boxes