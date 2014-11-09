set terminal png size 1024, 768
set output "rxtx.png"

set grid ytics lt 0 lw 1 lc rgb "#bbbbbb"
set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"

set xtics 16
#set ytics 0.1

plot [*:*][*:*] 'rxtx.txt' using 1:2 with lines title "tx", \
                'rxtx.txt' using 1:3 with lines title "rx", \
                'rxtx_1.txt' using 1:2 with lines title "tx lastyear", \
                'rxtx_1.txt' using 1:3 with lines title "rx lastyear"