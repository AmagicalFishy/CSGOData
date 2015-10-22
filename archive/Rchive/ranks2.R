library(RMySQL)
library(MASS)
library(ggplot2)
library(hexbin)
library(mgcv)
library(Cairo)
library(shiny)
library(plot3D)
library(devtools)

# Connect to SQL Database
con = dbConnect(MySQL(), user='root', password='password',
                dbname='csgo', host='localhost')

# Get data from table
dbListTables(con)
dbListFields(con, 'csgo_matches')
query = dbSendQuery(con, "select * from csgo_matches")
dat = fetch(query, n = -1)

# Put data into convenient variables
cs_score1 = dat[4]
cs_rank1 = dat[5]
cs_score2 = dat[7]
cs_rank2 = dat[8]

wl <- ifelse(cs_score1 > cs_score2, 1, 0)

# Dataframe of above differences
dat <- data.frame(x = unlist(cs_rank1), y = unlist(cs_rank2), z = wl)

#image2D(z=test4, border="black", bins = 15)
#help(image2D)
# Plot density map
hexplot <- ggplot(dat, aes(x, y, z = t1score)) +
    stat_binhex(color="black", bins=15) +
    stat_binhex(geom="text", bins=15, label=function(z){sum(wl)}) + 
    xlab("Team 1 Rank") + 
    ylab("Team 2 Rank") + 
    guides(fill = guide_colorbar(barheight = 10,
        label.theme = element_text(size=15, angle=0),
        title.theme = element_text(size=20, angle=0),
        title = "Match\nCount")) + 
    scale_fill_gradient(low = "blue", high = "white") +
    ggtitle("CS:GO\nRank Outcome Visualization") + # Title
    scale_y_continuous(breaks=seq(0,2,.25)) + # y-ticks
    scale_x_continuous(breaks=seq(0,2,.25)) + # x-ticks
    theme(panel.background = element_rect(fill = 'grey'), # Gray BG
        plot.title = element_text(color="#666666", face="bold", 
                                    size=40, hjust=0), 
        axis.title = element_text(color="#666666", face="bold", 
                                    size=25),
        axis.text = element_text(size=20))

## Save file as .png
Cairo(file="scorerankvis.png", type="png", 
    width=1000, height=1000, dpi=72, 
    pointsize=30)
hexplot
dev.off() 
