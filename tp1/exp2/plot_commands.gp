clear
reset
unset key
set terminal png size 1200,900
set output 'graph.png'
set title 'População Inicial x Melhor Fitness'
set xlabel 'População Inicial'
set ylabel 'Melhor Fitness'
set key below center horizontal noreverse enhanced autotitle box dashtype solid
set tics out nomirror
set border 3 front linetype black linewidth 1.0 dashtype solid
set xtics 1
#set mxtics 1
# set ytics 5
set style line 1 linecolor rgb '#0060ad' linetype 1 linewidth 2
set style histogram clustered gap 1 title offset character 0, 0, 0
set style data histograms
set boxwidth 1.0 absolute
set style fill solid 5.0 border -1
plot 'values.dat' using 2:xtic(1) title '10', \
	'' using 3 title '20', \
	'' using 4 title '30', \
	'' using 5 title '40', \
	'' using 6 title '50'