set terminal png size 1200,900
set output 'graph.png'
set title 'Partição x Acurácia'
set xlabel 'Partição'
set ylabel 'Acurácia'
red = "#FF0000"; green = "#00FF00"; blue = "#0000FF"; skyblue = "#87CEEB";
set yrange [0:1]
set style data histogram
set style histogram cluster gap 1
set style fill solid
set boxwidth 0.9
set xtics format ""
set grid ytics
plot 'data.dat' using 2:xtic(1) title "Treino" linecolor rgb red, \
'' using 3 title "Teste" linecolor rgb blue