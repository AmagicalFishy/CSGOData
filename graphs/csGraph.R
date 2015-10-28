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
query_text = "SELECT * FROM csgo_matches"
query = dbSendQuery(con, query_text)
dataset = fetch(query, n = -1)

t1_ranks <- unlist(dataset[5])
t2_ranks <- unlist(dataset[8])
t1_wins <- ifelse(dataset[4] > dataset[7], 1, 0)
t1_wins <- unlist(t1_wins)

rankDat <- data.frame(x = t1_ranks, y = t2_ranks, z = t1_wins)

# Build Hexagonal Histogram
rankHex <- ggplot(rankDat, aes(x, y, z = t1score)) + 
    stat_binhex(bins = 10, color="black") + 
    # Percent labels
    stat_summary_hex(aes(label=..value..),
                     bins = 10, fun = function(z) {
                         (round(sum(z)/length(z),2))*100
                     },
                     geom="text") +
    xlab("Team 1 Rank") + # x-label
    ylab("Team 2 Rank") + # y-label
    guides(fill = guide_colorbar(barheight = 10,
        label.theme = element_text(size=15, angle=0),
        title.theme = element_text(size=20, angle=0),
        title = "Number of\nMatches\nin Bin")) + 
    scale_fill_gradient(low = "blue", high = "white") +
    ggtitle("CS:GO\nRank Outcome Visualization") + # Title
    scale_y_continuous(breaks=seq(0,2,.25)) + # y-ticks
    scale_x_continuous(breaks=seq(0,2,.25)) + # x-ticks
    theme(panel.background = element_rect(fill = 'grey'), # Gray BG
        plot.title = element_text(color="#666666", face="bold", 
                                    size=40, hjust=0), 
        axis.title = element_text(color="#666666", face="bold", 
                                    size=25),
        axis.text = element_text(size=20)) +
    annotate("text", x = .5, y = .25, 
             label = "Numbers are percentage of the
             games in the bin won by Team 1", size=7, face="bold")

## Save file as .png
Cairo(file="rankcompare.png", type="png", 
    width=1000, height=1000, dpi=72, 
    pointsize=30)
rankHex
dev.off() 

## Build bar plot of rank winnings
color <- c(Ties = "yellow", Wins = "dark green", Losses = "dark red")
wl = ifelse(dataset[4] == dataset[7], "Ties",
             ifelse(dataset[4] > dataset[7], "Wins", "Losses"))
team = rep("Team 1", length(wl))
datWin <- data.frame(x = team, y = wl)

teamBar = ggplot(datWin, aes(x = x, fill = t1score)) + 
    geom_bar() +
    scale_x_discrete(expand=1) +
    scale_fill_manual(values = color)

Cairo(file="teamwin.png", type="png", 
    width=1000, height=1000, dpi=72, 
    pointsize=30)
teamBar
dev.off() 

dbDisconnect(con)

#all_cons <- dbListConnections(MySQL())
#for(con in all_cons) { dbDisconnect(con) }
