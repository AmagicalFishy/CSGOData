library(ggplot2)
dat <- data.frame(x = rnorm(100, 0, 0), y = rnorm(1000, 0, 0), z = rnorm(1000, 4, 4))

.hexHist = ggplot(dat, aes(x, y, z = z)) + 
    stat_binhex(bins = 10) +
    stat_summary_hex(aes(label=..value..), bins = 10,
                     fun = function(z) {
                         (round(sum(z)/length(z), 0))
                     },
                     geom = "text")

hexDat = ggplot_build(.hexHist)$data[[1]]
hexHist2 = .hexHist + annotate("text", hexDat$x, hexDat$y, label = "o")

Cairo(file="histexampletest.png", type="png", 
    width=750, height=750, dpi=72, 
    pointsize=30)
hexHist2
dev.off() 



